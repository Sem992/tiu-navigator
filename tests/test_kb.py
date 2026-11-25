"""Тесты базы знаний (не требуют Streamlit): python -m unittest discover -s tests"""
import ast
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import kb  # noqa: E402
from data import foreign_students as FS  # noqa: E402


def old_questions():
    src = (ROOT / "app.py").read_text(encoding="utf-8")
    start = src.index("QUESTIONS_DATA = ") + len("QUESTIONS_DATA = ")
    end = src.index("CAMPUS_LOCATIONS")
    return ast.literal_eval(src[start:end].strip())


OLD = old_questions()
NEW1 = kb.load_new_questions(kb.NEW_KB_FILE)      # первая партия, 200 карточек
NEW2 = kb.load_new_questions(kb.NEW_KB_FILE_2)    # вторая партия, 257 карточек
NEW = kb.load_new_questions()                     # обе партии
ALL = kb.merge_questions(OLD, NEW)
REQUIRED = ("id", "question", "category", "answer", "department", "address", "office",
            "phone", "email", "documents", "deadline", "officialSource", "lastChecked")


class DataTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(OLD), 43)
        self.assertEqual(len(NEW1), 200)
        self.assertEqual(len(NEW2), 257)
        self.assertEqual(len(NEW), 457)
        self.assertEqual(len(ALL), 500)

    def test_old_preserved_in_order(self):
        self.assertEqual([x["id"] for x in ALL[:43]], [x["id"] for x in OLD])

    def test_no_duplicates(self):
        ids = [x["id"] for x in ALL]
        qs = [x["question"].casefold().strip() for x in ALL]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(qs), len(set(qs)))

    def test_fields(self):
        for x in NEW:
            for f in REQUIRED:
                self.assertIn(f, x)
            self.assertTrue(x["question"] and x["answer"])
        for x in NEW1:
            self.assertTrue(x["officialSource"].startswith("http"))
        for x in NEW2:  # у общих советов источника может не быть
            self.assertTrue(not x["officialSource"] or x["officialSource"].startswith("http"), x["id"])

    def test_unconfirmed_marks_preserved(self):
        self.assertEqual(sum(1 for x in NEW1 if x["lastChecked"] == "Требует уточнения"), 198)
        self.assertEqual(sum(1 for x in NEW1 if kb.status_of(x)[0] == "warn"), 198)

    def test_merge_skips_duplicates(self):
        again = kb.merge_questions(ALL, NEW + [dict(OLD[0], id="zzz")])
        self.assertEqual(len(again), 500)

    def test_related_ids_exist(self):
        ids = {x["id"] for x in ALL}
        for t in FS.TOPICS:
            for i in t["related"]["ids"]:
                self.assertIn(i, ids)


class SearchTests(unittest.TestCase):
    def test_russian_case_insensitive(self):
        self.assertTrue(kb.search(ALL, "СПРАВКУ"))
        self.assertEqual(len(kb.search(ALL, "справку")), len(kb.search(ALL, "СпРаВкУ")))

    def test_yo(self):
        self.assertTrue(kb.search(ALL, "учёба") == kb.search(ALL, "учеба"))

    def test_english_queries(self):
        for q, expected in [("dormitory", "общежит"), ("certificate", "справк"), ("library", "библиотек"),
                            ("migration", "миграц"), ("scholarship", "стипенд"), ("schedule", "расписан")]:
            hits = kb.search(ALL, q)
            self.assertTrue(hits, q)
            self.assertTrue(any(expected in (h["question"] + h["answer"]).casefold() for h in hits), q)

    def test_empty_query_returns_all(self):
        self.assertEqual(len(kb.search(ALL, "  ")), 500)

    def test_no_match(self):
        self.assertEqual(kb.search(ALL, "qwertyzzz"), [])

    def test_every_new_card_findable_by_own_question(self):
        for x in NEW:
            self.assertIn(x, kb.search(ALL, x["question"]), x["id"])


class FilterTests(unittest.TestCase):
    def test_categories_cover_everything(self):
        cats = {x["category"] for x in ALL}
        self.assertEqual(cats, {"docs", "study", "clubs", "dorm", "scholarship", "events", "sos", "navigation"})
        self.assertEqual(sum(len([x for x in ALL if x["category"] == c]) for c in cats), 500)

    def test_topics_have_labels(self):
        for x in NEW:
            self.assertIn(x["topic"], kb.TOPIC_LABELS)


class Batch2Tests(unittest.TestCase):
    """Вторая партия (257 карточек)."""

    def test_numbers_and_ids(self):
        self.assertEqual([x["id"] for x in NEW2], [f"q_{n:03d}" for n in range(1, 258)])

    def test_first_hundred_are_in_sos(self):
        sos = [x for x in ALL if x["category"] == "sos"]
        self.assertEqual({x["id"] for x in NEW2[:100]} - {x["id"] for x in sos}, set())
        self.assertTrue(all(x["category"] != "sos" for x in NEW2[100:]))
        self.assertEqual(len(sos), 103)  # 3 старых + 100 новых

    def test_no_placeholders_in_visible_fields(self):
        for x in NEW2:
            for f in ("department", "address", "office", "documents", "deadline"):
                self.assertEqual(kb.clean_field(x[f]), x[f], (x["id"], f))
            self.assertEqual(kb.clean_answer(x["answer"]), x["answer"], x["id"])

    def test_answers_are_numbered_sequentially(self):
        import re
        for x in NEW2:
            nums = [int(m.group(1)) for m in re.finditer(r"^(\d+)[.)]\s", x["answer"], re.M)]
            self.assertEqual(nums, list(range(1, len(nums) + 1)), x["id"])

    def test_every_new_card_has_known_topic_and_category(self):
        for x in NEW2:
            self.assertIn(x["topic"], kb.TOPIC_LABELS)
            self.assertIn(x["category"], {"docs", "study", "clubs", "dorm", "scholarship", "events", "sos", "navigation"})

    def test_every_batch2_card_findable(self):
        for x in NEW2:
            self.assertIn(x, kb.search(ALL, x["question"]), x["id"])


class CleaningTests(unittest.TestCase):
    def test_field_placeholders_hidden(self):
        for v in ("", None, "уточняется", "Информация уточняется", "Адрес зависит от корпуса; уточняется",
                  "Не опубликован/не подтверждён для данного сценария — уточнить у ответственного подразделения.",
                  "Требует уточнения", "Не указано", "Нет данных"):
            self.assertEqual(kb.clean_field(v), "", v)

    def test_field_keeps_real_values(self):
        self.assertEqual(kb.clean_field("1–3 рабочих дня"), "1–3 рабочих дня")
        self.assertEqual(kb.clean_field("Паспорт (для подтверждения личности при личном визите)"),
                         "Паспорт (для подтверждения личности при личном визите)")
        self.assertEqual(kb.clean_field("каб. 42 (дирекция; профильный вопрос уточнить)"), "каб. 42")
        self.assertEqual(kb.clean_field("Территориальный отдел; точное подразделение уточнить на странице института"),
                         "Территориальный отдел")

    def test_field_drops_only_the_unconfirmed_part(self):
        out = kb.clean_field("Специальные документы заранее не подтверждены. Подготовьте студенческий билет; "
                             "точный перечень уточните у службы.")
        self.assertEqual(out, "Подготовьте студенческий билет")

    def test_answer_drops_not_found_statements(self):
        out = kb.clean_answer("1. Сервис не найден.\n2. Спросите в дирекции.\n3. Если не нашли — позвоните.")
        self.assertEqual(out, "1. Спросите в дирекции.\n2. Если не нашли — позвоните.")
        self.assertEqual(kb.clean_answer("1. Размер не найден: уточняйте в поддержке.\n2. Удалите письма."),
                         "1. Удалите письма.")  # от строки остался пустой обрывок «Уточняйте…» — убирается

    def test_answer_keeps_normal_text(self):
        text = "1. Откройте личный кабинет.\n2. Выберите справку и подтвердите заказ."
        self.assertEqual(kb.clean_answer(text), text)

    def test_sources(self):
        self.assertEqual(kb.split_sources("https://a.ru/x\nhttps://b.ru/ https://a.ru/x"), ["https://a.ru/x", "https://b.ru/"])
        self.assertEqual(kb.split_sources("javascript:alert(1)"), [])
        self.assertEqual(kb.short_url("https://www.tyuiu.ru/a/b/"), "tyuiu.ru/a/b")


class HelpersTests(unittest.TestCase):
    def test_status(self):
        self.assertEqual(kb.status_of({"lastChecked": "25.09.2026"})[0], "ok")
        self.assertEqual(kb.status_of({"lastChecked": "Готово"})[0], "ok")
        self.assertEqual(kb.status_of({"lastChecked": "Требует проверки перед публикацией"})[0], "warn")
        self.assertEqual(kb.status_of({})[0], "warn")

    def test_placeholder_and_unconfirmed(self):
        self.assertTrue(kb.is_placeholder("уточняется"))
        self.assertTrue(kb.is_placeholder("Информация уточняется"))
        self.assertFalse(kb.is_placeholder("8 (3452) 28-36-60"))
        self.assertTrue(kb.is_unconfirmed("Не опубликован/не подтверждён"))
        self.assertFalse(kb.is_unconfirmed("1–3 рабочих дня"))

    def test_phone(self):
        self.assertEqual(kb.phone_href("8 (3452) 28-36-60"), "tel:+73452283660")
        self.assertEqual(kb.phone_href("уточняется"), "")

    def test_split_answer(self):
        blocks = kb.split_answer("1. Первый шаг\n2. Второй\nОбычный абзац")
        self.assertEqual([b[0] for b in blocks], ["step", "step", "p"])


class ForeignContentTests(unittest.TestCase):
    def _walk(self, node, path=""):
        if isinstance(node, dict) and set(node) == {"ru", "en"}:
            yield path, node
        elif isinstance(node, dict):
            for k, v in node.items():
                yield from self._walk(v, f"{path}/{k}")
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                yield from self._walk(v, f"{path}[{i}]")

    def test_every_text_has_both_languages(self):
        count = 0
        for path, node in self._walk([FS.UI, FS.TOPICS, FS.FAQ, FS.CONTACTS, FS.EMERGENCY]):
            count += 1
            for code in ("ru", "en"):
                self.assertTrue(node[code], path)
            if isinstance(node["ru"], list):
                self.assertEqual(len(node["ru"]), len(node["en"]), path)
                self.assertTrue(all(s.strip() for s in node["ru"] + node["en"]), path)
        self.assertGreater(count, 50)

    def test_seven_topics_and_old_faq_kept(self):
        self.assertEqual(len(FS.TOPICS), 7)
        self.assertEqual(len(FS.FAQ), 8)
        self.assertEqual(len({t["id"] for t in FS.TOPICS}), 7)

    def test_links_valid(self):
        for t in FS.TOPICS:
            for k in t["links"]:
                self.assertTrue(FS.LINKS[k][1].startswith("https://"))

    def test_russian_text_is_cyrillic(self):
        for path, node in self._walk([FS.TOPICS]):
            texts = node["ru"] if isinstance(node["ru"], list) else [node["ru"]]
            for s in texts:
                self.assertTrue(any("а" <= c.lower() <= "я" for c in s), path)


if __name__ == "__main__":
    unittest.main()

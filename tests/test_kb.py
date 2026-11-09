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
NEW = kb.load_new_questions()
ALL = kb.merge_questions(OLD, NEW)
REQUIRED = ("id", "question", "category", "answer", "department", "address", "office",
            "phone", "email", "documents", "deadline", "officialSource", "lastChecked")


class DataTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(OLD), 43)
        self.assertEqual(len(NEW), 200)
        self.assertEqual(len(ALL), 243)

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
            self.assertTrue(x["question"] and x["answer"] and x["officialSource"].startswith("http"))

    def test_unconfirmed_marks_preserved(self):
        self.assertEqual(sum(1 for x in NEW if x["lastChecked"] == "Требует уточнения"), 198)
        self.assertEqual(sum(1 for x in NEW if kb.status_of(x)[0] == "warn"), 198)

    def test_merge_skips_duplicates(self):
        again = kb.merge_questions(ALL, NEW + [dict(OLD[0], id="zzz")])
        self.assertEqual(len(again), 243)

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
        self.assertEqual(len(kb.search(ALL, "  ")), 243)

    def test_no_match(self):
        self.assertEqual(kb.search(ALL, "qwertyzzz"), [])

    def test_every_new_card_findable_by_own_question(self):
        for x in NEW:
            self.assertIn(x, kb.search(ALL, x["question"]), x["id"])


class FilterTests(unittest.TestCase):
    def test_categories_cover_everything(self):
        cats = {x["category"] for x in ALL}
        self.assertEqual(cats, {"docs", "study", "clubs", "dorm", "scholarship", "events", "sos", "navigation"})
        self.assertEqual(sum(len([x for x in ALL if x["category"] == c]) for c in cats), 243)

    def test_topics_have_labels(self):
        for x in NEW:
            self.assertIn(x["topic"], kb.TOPIC_LABELS)


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

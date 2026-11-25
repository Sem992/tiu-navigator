"""Импорт базы вопросов из Excel.

Запуск (из корня проекта):
    python tools/import_excel.py путь/к/файлу.xlsx

Формат определяется по названию листа:
  * лист «200 карточек» -> data/knowledge_base_new.json (первая партия, 13 колонок);
  * лист «Карточки»     -> data/knowledge_base_257.json (вторая партия, 14 колонок:
    №, Вопрос, Категория, Ответ, Куда идти, Адрес, Кабинет, Телефон, Email, Документы,
    Срок, Официальный источник, Статус, Раздел).
Скрипт можно запускать повторно: нужный JSON пересобирается целиком из Excel.
Старые вопросы (app.py и первая партия) не меняются; вопросы, совпадающие со старыми
дословно (после нормализации), пропускаются и выводятся в отчёте; похожие — только
перечисляются в отчёте. Заглушки («уточняется», «не подтверждено» и т.п.) в поля
не попадают: их вырезает kb.clean_field / kb.clean_answer.
Требуется: openpyxl (только для импорта, в самом приложении не нужен).
"""
import ast
import json
import re
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kb  # noqa: E402

OUT = ROOT / "data" / "knowledge_base_new.json"
OUT_2 = ROOT / "data" / "knowledge_base_257.json"
SHEET = "200 карточек"
SHEET_2 = "Карточки"

# Категории Excel -> ключи категорий сайта
CATEGORY_MAP = {
    "Учёба": "study",
    "Документы": "docs",
    "Студенческая жизнь": "clubs",
    "Навигация": "navigation",
}

# В Excel вопросы идут тематическими блоками. Тема определяется по номеру карточки.
TOPIC_RANGES = [
    (1, 20, "it"),
    (21, 40, "plan"),
    (41, 60, "transfer"),
    (61, 80, "tuition"),
    (81, 100, "career"),
    (101, 111, "mobility"),
    (112, 120, "foreign"),
    (121, 140, "library"),
    (141, 160, "safety"),
    (161, 180, "rights"),
    (181, 200, "campus"),
]


# Вторая партия (257 карточек). Первые 100 — раздел «Что делать, если…» (категория sos).
SOS_TOPIC_RANGES = [
    (1, 20, "s_study"),
    (21, 35, "s_digital"),
    (36, 50, "s_docs"),
    (51, 60, "s_finance"),
    (61, 75, "s_dorm"),
    (76, 90, "s_campus"),
    (91, 100, "s_opps"),
]
CATEGORY_MAP_2 = {
    "Учёба": "study",
    "Документы": "docs",
    "Стипендии": "scholarship",
    "Общежитие": "dorm",
    "Навигация": "navigation",
    "Студенческая жизнь": "clubs",
}
# Раздел из Excel -> (тема, категория сайта или None = взять категорию из Excel)
RAZDEL_MAP = {
    "Учёба и организация времени": ("skills", None),
    "Студенческие сервисы и кампус": ("campus", None),
    "Карьера и профессиональное развитие": ("career", "events"),
    "Клубы и общественная жизнь": ("clubs_life", None),
    "Здоровье и психологическое благополучие": ("health", None),
    "Тюмень и жизнь вне университета": ("city", None),
    "Международная среда": ("foreign", None),
    "Техника и цифровые инструменты": ("digital", None),
}


def topic_for(number: int) -> str:
    for lo, hi, key in TOPIC_RANGES:
        if lo <= number <= hi:
            return key
    return ""


def norm(text: str) -> str:
    return re.sub(r"[^\w]+", " ", str(text).casefold().replace("ё", "е")).strip()


def clean(value) -> str:
    return "" if value is None else str(value).strip()


def old_questions() -> set:
    src = (ROOT / "app.py").read_text(encoding="utf-8")
    start = src.index("QUESTIONS_DATA = ") + len("QUESTIONS_DATA = ")
    end = src.index("CAMPUS_LOCATIONS")
    return {norm(x["question"]) for x in ast.literal_eval(src[start:end].strip())}


def sos_topic(number: int) -> str:
    for lo, hi, key in SOS_TOPIC_RANGES:
        if lo <= number <= hi:
            return key
    return ""


def _tokens(text: str) -> set:
    return {w[:5] for w in norm(text).split() if len(w) > 3}


def existing_questions() -> list:
    """Вопросы, уже лежащие в базе: app.py (старые) + первая партия."""
    src = (ROOT / "app.py").read_text(encoding="utf-8")
    start = src.index("QUESTIONS_DATA = ") + len("QUESTIONS_DATA = ")
    end = src.index("CAMPUS_LOCATIONS")
    items = list(ast.literal_eval(src[start:end].strip()))
    items += json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else []
    return items


def main_257(wb) -> None:
    rows = list(wb[SHEET_2].iter_rows(min_row=2, values_only=True))
    existing = existing_questions()
    known = {norm(x["question"]) for x in existing}
    seen, cards, skipped, similar = set(), [], [], []
    for r in rows:
        if not r or not r[1]:
            continue
        number = int(r[0])
        question = clean(r[1])
        key = norm(question)
        if key in known or key in seen:
            skipped.append((number, question))
            continue
        seen.add(key)
        if number <= 100:
            category, topic = "sos", sos_topic(number)
        else:
            topic, forced = RAZDEL_MAP[clean(r[13])]
            category = forced or CATEGORY_MAP_2.get(clean(r[2]))
            if category is None:
                raise SystemExit(f"Неизвестная категория в строке {number}: {r[2]!r}")
        a = _tokens(question)
        for x in existing:
            b = _tokens(x["question"])
            if a and b and len(a & b) / len(a | b) >= 0.5:
                similar.append((number, question, x["id"], x["question"]))
        sources = "\n".join(kb.split_sources(r[11]))
        cards.append({
            "id": f"q_{number:03d}",
            "question": question,
            "category": category,
            "topic": topic,
            "answer": kb.clean_answer(clean(r[3])),
            "department": kb.clean_field(clean(r[4])),
            "address": kb.clean_field(clean(r[5])),
            "office": kb.clean_field(clean(r[6])),
            "phone": kb.clean_field(clean(r[7])),
            "email": kb.clean_field(clean(r[8])),
            "documents": kb.clean_field(clean(r[9])),
            "deadline": kb.clean_field(clean(r[10])),
            "officialSource": sources,
            "lastChecked": clean(r[12]),
        })
    OUT_2.parent.mkdir(exist_ok=True)
    OUT_2.write_text(json.dumps(cards, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Записано карточек: {len(cards)} -> {OUT_2}")
    if skipped:
        print("Пропущены дубли:", skipped)
    for row in similar:
        print("Похожий вопрос (добавлен, проверьте): №%s «%s» ~ %s «%s»" % row)


def main(xlsx_path: str) -> None:
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    if SHEET_2 in wb.sheetnames:
        return main_257(wb)
    rows = list(wb[SHEET].iter_rows(min_row=2, values_only=True))
    existing = old_questions()
    seen, cards, skipped = set(), [], []
    for r in rows:
        if not r or not r[1]:
            continue
        number = int(r[0])
        question = clean(r[1])
        key = norm(question)
        if key in existing or key in seen:
            skipped.append((number, question))
            continue
        seen.add(key)
        category = CATEGORY_MAP.get(clean(r[2]))
        if category is None:
            raise SystemExit(f"Неизвестная категория в строке {number}: {r[2]!r}")
        cards.append({
            "id": f"n_{number:03d}",
            "question": question,
            "category": category,
            "topic": topic_for(number),
            "answer": clean(r[3]),
            "department": clean(r[4]),
            "address": clean(r[5]),
            "office": clean(r[6]),
            "phone": clean(r[7]),
            "email": clean(r[8]),
            "documents": clean(r[9]),
            "deadline": clean(r[10]),
            "officialSource": clean(r[11]),
            # Статус из Excel сохраняется как есть: «Готово» / «Требует уточнения»
            "lastChecked": clean(r[12]),
        })
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(cards, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Записано карточек: {len(cards)} -> {OUT}")
    if skipped:
        print("Пропущены дубли:", skipped)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])

"""Импорт базы вопросов из Excel в data/knowledge_base_new.json.

Запуск (из корня проекта):
    python tools/import_excel.py путь/к/файлу.xlsx

Скрипт можно запускать повторно: JSON пересобирается целиком из Excel.
Старые вопросы из app.py не меняются; вопросы, совпадающие со старыми
дословно (после нормализации), пропускаются и выводятся в отчёте.
Требуется: openpyxl (только для импорта, в самом приложении не нужен).
"""
import ast
import json
import re
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "knowledge_base_new.json"
SHEET = "200 карточек"

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


def main(xlsx_path: str) -> None:
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
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

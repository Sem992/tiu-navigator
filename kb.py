"""Логика базы знаний «ТИУ НАВИГАТОР»: загрузка, поиск, фильтры, статусы.

Модуль не зависит от Streamlit, поэтому его можно тестировать отдельно.
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
NEW_KB_FILE = DATA_DIR / "knowledge_base_new.json"

PLACEHOLDER = "Информация уточняется"
FIELD_KEYS = ("department", "address", "office", "phone", "email", "documents", "deadline")

# Темы для карточек из Excel (для старых карточек темой служит их категория).
TOPIC_LABELS = {
    "it": {"ru": "Личный кабинет и IT-сервисы", "en": "Account & IT services"},
    "plan": {"ru": "Учебный план, курсовые, ВКР", "en": "Curriculum, coursework, thesis"},
    "transfer": {"ru": "Переводы, восстановление, отпуск", "en": "Transfers, reinstatement, leave"},
    "tuition": {"ru": "Оплата обучения и договор", "en": "Tuition & contract"},
    "career": {"ru": "Практика и карьера", "en": "Internships & career"},
    "mobility": {"ru": "Мобильность и обмен", "en": "Exchange & mobility"},
    "foreign": {"ru": "Иностранным студентам", "en": "International students"},
    "library": {"ru": "Библиотека и наука", "en": "Library & research"},
    "safety": {"ru": "Безопасность и поддержка", "en": "Safety & support"},
    "rights": {"ru": "Права, студсовет, инициативы", "en": "Rights & student council"},
    "campus": {"ru": "Кампус и инфраструктура", "en": "Campus & facilities"},
}

# Английские слова -> корни русских слов, чтобы поиск работал на английском
# по русскоязычной базе. Корни подбираются по подстроке, без учёта регистра.
EN_ALIASES = {
    "dorm": ["общежит"], "dormitory": ["общежит"], "hostel": ["общежит"],
    "accommodation": ["общежит", "прожив"], "housing": ["общежит", "прожив"],
    "certificate": ["справк"], "certificates": ["справк"], "letter": ["справк"],
    "document": ["документ"], "documents": ["документ"], "paper": ["документ"],
    "passport": ["паспорт"], "visa": ["виз", "пребыван"], "migration": ["миграц", "пребыван"],
    "registration": ["регистрац", "учет", "учёт"], "stay": ["пребыван"],
    "extension": ["продлени", "продлить"], "insurance": ["страхов"],
    "medical": ["медиц"], "health": ["здоровь", "медиц"], "doctor": ["врач", "медиц"],
    "ambulance": ["скор", "медиц"], "emergency": ["экстрен", "эвакуац", "помощ"],
    "psychologist": ["психолог"], "stress": ["стресс", "психолог"],
    "schedule": ["расписан"], "timetable": ["расписан"], "class": ["занят", "пар"],
    "classes": ["занят", "пар"], "exam": ["экзамен", "аттестац", "сесс"], "exams": ["экзамен", "аттестац", "сесс"],
    "debt": ["задолж"], "retake": ["пересдач"], "credit": ["зачет", "зачёт"],
    "student": ["студент", "обучающ"], "id": ["студенческ", "билет"], "card": ["билет"],
    "account": ["кабинет", "аккаунт"], "portal": ["кабинет"], "login": ["войти", "вход"],
    "password": ["пароль"], "email": ["почт"], "mail": ["почт"], "wifi": ["wi-fi", "wifi"],
    "internet": ["wi-fi", "сеть"], "network": ["сеть", "wi-fi"],
    "library": ["библиотек"], "book": ["книг", "учебник"], "books": ["книг", "учебник"],
    "catalog": ["каталог"], "journal": ["журнал"], "article": ["стать"],
    "tuition": ["оплат", "стоимост", "обучени"], "payment": ["оплат", "платеж", "платёж"],
    "pay": ["оплат"], "fee": ["оплат", "стоимост"], "refund": ["возврат"],
    "contract": ["договор"], "tax": ["налог", "вычет"],
    "scholarship": ["стипенд"], "grant": ["грант"], "stipend": ["стипенд"],
    "internship": ["практик", "стажиров"], "practice": ["практик"], "job": ["работ", "вакан"],
    "career": ["карьер"], "resume": ["резюме"], "cv": ["резюме"], "interview": ["собеседован"],
    "work": ["работ"], "vacancy": ["вакан"],
    "exchange": ["обмен", "мобильност"], "abroad": ["рубеж", "междунар"],
    "international": ["иностран", "междунар"], "foreign": ["иностран"],
    "language": ["язык"], "translation": ["перевод"], "translate": ["перевод"],
    "transfer": ["перевод", "перевест"], "reinstatement": ["восстанов"],
    "expulsion": ["отчислен"], "leave": ["отпуск"], "academic": ["академ"],
    "thesis": ["выпускн", "диплом", "вкр"], "diploma": ["диплом"], "coursework": ["курсов"],
    "course": ["курс", "дисциплин"], "elective": ["электив"], "plan": ["план"],
    "building": ["корпус"], "campus": ["корпус", "кампус"], "map": ["карт"],
    "address": ["адрес"], "route": ["маршрут"], "lost": ["утерян", "потерял", "потеря"],
    "found": ["найден", "забыл"], "elevator": ["лифт"], "lift": ["лифт"],
    "parking": ["парковк"], "bike": ["велосипед"], "bicycle": ["велосипед"],
    "water": ["вод"], "atm": ["банкомат"], "bank": ["банк"], "post": ["почт"],
    "fire": ["пожар"], "evacuation": ["эвакуац"], "safety": ["безопасн"],
    "security": ["безопасн", "охран"], "police": ["полиц"], "injury": ["травм"],
    "disability": ["инвалид", "ограниченн"], "accessibility": ["маломобильн", "доступност"],
    "bullying": ["травл"], "discrimination": ["дискриминац"], "complaint": ["обращен", "жалоб"],
    "appeal": ["апелляц"], "rights": ["прав"], "rules": ["правил"],
    "club": ["клуб", "объединен"], "clubs": ["клуб", "объединен"], "event": ["мероприят"],
    "events": ["мероприят"], "volunteer": ["доброволь", "волонт"], "council": ["совет"],
    "research": ["научн", "исследован"], "science": ["научн"], "patent": ["патент"],
    "plagiarism": ["заимствован", "оригинальн"], "sports": ["спорт"], "sport": ["спорт"],
    "transport": ["транспорт"], "bus": ["автобус"], "food": ["питан", "столов"],
    "canteen": ["столов", "питан"], "weekend": ["выходн"], "holiday": ["праздни", "каникул"],
    "holidays": ["праздни", "каникул"], "adaptation": ["адаптац"],
}


def _fold(text) -> str:
    return str(text or "").casefold().replace("ё", "е")


def _stem(token: str) -> str:
    """Грубое усечение окончания, чтобы «справку» находило «справка»."""
    if len(token) >= 6:
        return token[:-2]
    if len(token) == 5:
        return token[:-1]
    return token


def _tokens(query: str):
    return [t for t in re.split(r"[^\w\-]+", _fold(query)) if t]


def category_of(item) -> str:
    return item.get("category", "")


def topic_of(item) -> str:
    """Тема карточки: у новых — из Excel-блока, у старых — их категория."""
    return item.get("topic") or item.get("category", "")


def topic_label(topic: str, lang: str, category_labels: dict) -> str:
    code = "en" if lang == "English" else "ru"
    if topic in TOPIC_LABELS:
        return TOPIC_LABELS[topic][code]
    return category_labels.get(topic, topic)


def load_new_questions(path: Path = NEW_KB_FILE) -> list:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def merge_questions(old: list, new: list) -> list:
    """Старые карточки сохраняются; новые добавляются без дублей по id и тексту вопроса."""
    result = list(old)
    ids = {x["id"] for x in old}
    texts = {_fold(x["question"]).strip() for x in old}
    for item in new:
        key = _fold(item["question"]).strip()
        if item["id"] in ids or key in texts:
            continue
        ids.add(item["id"])
        texts.add(key)
        result.append(item)
    return result


def _haystack(item) -> str:
    parts = [item.get("question", ""), item.get("answer", ""), item.get("department", ""),
             item.get("documents", "")]
    return _fold(" ".join(parts))


def matches(item, query: str) -> bool:
    """Все слова запроса должны найтись в вопросе/ответе (русский или английский)."""
    tokens = _tokens(query)
    if not tokens:
        return True
    hay = _haystack(item)
    for tok in tokens:
        options = [_stem(tok)]
        options += [_fold(a) for a in EN_ALIASES.get(tok, [])]
        if not any(o and o in hay for o in options):
            return False
    return True


def search(items: list, query: str) -> list:
    """Фильтрует и ранжирует: совпадения в тексте вопроса идут выше."""
    tokens = _tokens(query)
    found = [x for x in items if matches(x, query)]
    if not tokens:
        return found

    def score(x):
        q = _fold(x["question"])
        s = 0
        for tok in tokens:
            opts = [_stem(tok)] + [_fold(a) for a in EN_ALIASES.get(tok, [])]
            if any(o in q for o in opts):
                s += 1
        return -s

    return sorted(found, key=score)  # sorted стабилен: порядок базы сохраняется


def is_placeholder(value) -> bool:
    v = _fold(value).strip()
    return (not v) or v in ("информация уточняется", "уточняется")


def is_unconfirmed(value) -> bool:
    """Значение помечено в базе как неподтверждённое («не опубликован/не подтверждён»)."""
    v = _fold(value)
    return "не подтвержд" in v or "не опубликован" in v


def status_of(item):
    """Возвращает (вид, текст): 'ok' — подтверждено, 'warn' — требует проверки."""
    raw = (item.get("lastChecked") or "").strip()
    if not raw:
        return "warn", "Требует уточнения"
    if raw.casefold() == "готово":
        return "ok", "Готово"
    if re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", raw):
        return "ok", f"Проверено {raw}"
    return "warn", raw


def phone_href(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) == 11 and digits[0] in "78":
        return "tel:+7" + digits[1:]
    return ""


def split_answer(answer: str):
    """Разбивает ответ на блоки: ('step', n, text) | ('p', text) | ('h', text)."""
    blocks = []
    for line in (answer or "").splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(\d+)[.)]\s+(.*)$", line)
        if m:
            blocks.append(("step", m.group(1), m.group(2)))
        elif len(line) < 70 and (line.endswith(":") or line.endswith("?")):
            blocks.append(("h", line))
        else:
            blocks.append(("p", line))
    return blocks

"""Логика базы знаний «ТИУ НАВИГАТОР»: загрузка, поиск, фильтры, статусы.

Модуль не зависит от Streamlit, поэтому его можно тестировать отдельно.
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
NEW_KB_FILE = DATA_DIR / "knowledge_base_new.json"
NEW_KB_FILE_2 = DATA_DIR / "knowledge_base_257.json"
NEW_KB_FILES = (NEW_KB_FILE, NEW_KB_FILE_2)

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
    # Блок «Что делать, если…» (раздел sos)
    "s_study": {"ru": "Учёба и оценки", "en": "Studies & grades"},
    "s_digital": {"ru": "Цифровые сервисы", "en": "Digital services"},
    "s_docs": {"ru": "Документы и заявления", "en": "Documents & applications"},
    "s_finance": {"ru": "Оплата и финансы", "en": "Payments & finance"},
    "s_dorm": {"ru": "Общежитие и быт", "en": "Dormitory & daily life"},
    "s_campus": {"ru": "Кампус, здоровье и безопасность", "en": "Campus, health & safety"},
    "s_opps": {"ru": "Студенческие возможности", "en": "Student opportunities"},
    # Остальные новые карточки
    "skills": {"ru": "Учёба и организация времени", "en": "Study skills & time management"},
    "clubs_life": {"ru": "Клубы и творчество", "en": "Clubs & creativity"},
    "health": {"ru": "Здоровье и баланс", "en": "Health & balance"},
    "city": {"ru": "Тюмень и жизнь вне университета", "en": "Tyumen & life off campus"},
    "digital": {"ru": "Техника и цифровые инструменты", "en": "Tech & digital tools"},
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


def _load_json(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_new_questions(path: Path = None) -> list:
    """Без аргумента — все файлы с новыми карточками (NEW_KB_FILES); с path — один файл."""
    if path is not None:
        return _load_json(Path(path))
    items = []
    for file in NEW_KB_FILES:
        items.extend(_load_json(file))
    return items


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


# Заглушки и пояснения «данных нет / не проверено» в полях карточки.
# Они не должны попадать на сайт: такие фрагменты вырезаются, а если ничего не осталось,
# поле скрывается целиком. «Паспорт для подтверждения личности» сюда не попадает.
_GAP = re.compile(
    r"уточн|не\s?подтвержд|не\s?опубликов|не\s?проверен|требует\s+(?:проверк|уточн)|"
    r"нет\s+данных|не\s+указан|неизвестн|не\s+найден|информация\s+(?:не|отсутств)|"
    r"зависит\s+от\s+корпуса|точн\w+\s+(?:перечень|срок|подразделение|адрес)|профильный\s+вопрос",
    re.I)
_SPLIT = re.compile(r"(;\s*|(?<=[.!?])\s+|\s+[—–]\s+)")


def clean_field(value) -> str:
    """Возвращает значение поля без заглушек; пустая строка — поле показывать не нужно."""
    v = re.sub(r"\s+", " ", str(value or "")).strip()
    if not v:
        return ""
    # скобки с пометками вида «(уточнить через ...)» убираем целиком
    v = re.sub(r"\s*\([^()]*(?:%s)[^()]*\)" % _GAP.pattern, "", v, flags=re.I).strip()
    parts = _SPLIT.split(v)
    segs = parts[0::2]
    seps = parts[1::2] + [""]
    kept = [(seg, sep) for seg, sep in zip(segs, seps) if seg.strip() and not _GAP.search(seg)]
    if not kept:
        return ""
    out = "".join(seg + (sep if i < len(kept) - 1 else "") for i, (seg, sep) in enumerate(kept))
    out = out.strip(" ;,—–-")
    return "" if is_placeholder(out) else out


# Фразы-констатации «информации нет / не удалось подтвердить» в тексте ответа.
# Условные подсказки («Если не нашли — позвоните…») и советы «уточните у…» остаются.
_ANSWER_GAP = re.compile(
    r"не\s?(?:найден|найдена|найдено|найдены|нашл[аио]с?ь?|нашё?л|нашли)\b|найти\s+не\s+удалось|"
    r"не\s+удалось\s+(?:найти|открыть|подтвердить)|подтвердить\s+не\s+удалось|"
    r"не\s?подтвержд|не\s?проверял|не\s+указан[аоы]?\b|не\s+опубликован|"
    r"нет\s+данных|неизвестн|нет\s+подтвержд|актуальность\s+не|нет\s+в\s+проверенн|не\s+описан\w*",
    re.I)
# Строка-констатация «Порядок … нужно уточнить в дирекции» — это не шаг, а пометка об отсутствии данных.
_ANSWER_TODO = re.compile(
    r"^(?:порядок|правила|сроки|условия|перечень)[^.!?]*\b(?:нужно|необходимо|следует)\s+уточнить",
    re.I)
_ASPLIT = re.compile(r"(;\s*|(?<=[.!?])\s+|\s*[:—–]\s+)")


def _capitalize(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


def clean_answer(answer) -> str:
    """Убирает из ответа фразы вида «… не найдено / не удалось подтвердить», оставляя действия.
    Строки с «Если …» (условные шаги) не затрагиваются. Нумерация шагов пересобирается."""
    lines = []
    for raw in str(answer or "").splitlines():
        line = raw.rstrip()
        if not line.strip():
            lines.append("")
            continue
        m = re.match(r"^(\s*(?:\d+[.)]|[•\-–])\s+)(.*)$", line)
        prefix, body = (m.group(1), m.group(2)) if m else ("", line.strip())
        if _ANSWER_TODO.match(body):
            continue
        if re.match(r"^(?:если|при\s)", body, re.I) or not _ANSWER_GAP.search(body):
            lines.append(prefix + body)
            continue
        parts = _ASPLIT.split(body)
        segs, seps = parts[0::2], parts[1::2] + [""]
        kept = [(a, b) for a, b in zip(segs, seps) if a.strip() and not _ANSWER_GAP.search(a)]
        if not kept:
            continue
        out = "".join(a + (b if i < len(kept) - 1 else "") for i, (a, b) in enumerate(kept)).strip(" ;,:—–")
        # от строки остался только обрывок вроде «Позвони и уточни» — без смысла, убираем
        if re.match(r"^(?:уточн\w*|позвон\w*)\b", out, re.I) and len(out.split()) <= 5:
            continue
        if out and out[-1] not in ".!?»)":
            out += "."
        lines.append(prefix + _capitalize(out))
    # пересборка нумерации
    result, n = [], 0
    for line in lines:
        m = re.match(r"^(\d+)([.)])\s+(.*)$", line)
        if m:
            n += 1
            line = f"{n}{m.group(2)} {m.group(3)}"
        result.append(line)
    return "\n".join(result).strip()


def split_sources(value) -> list:
    """Список ссылок из поля officialSource (несколько ссылок — через перенос строки/пробел)."""
    urls = []
    for tok in re.split(r"[\s,]+", str(value or "")):
        if tok.startswith(("http://", "https://")) and tok not in urls:
            urls.append(tok)
    return urls


def short_url(url: str, limit: int = 46) -> str:
    """Читаемая подпись ссылки: без схемы, www и завершающего слэша."""
    text = re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
    return text if len(text) <= limit else text[: limit - 1] + "…"


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

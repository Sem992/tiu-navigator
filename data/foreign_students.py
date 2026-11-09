"""Контент раздела для иностранных студентов (RU / EN).

ВАЖНО: здесь нет выдуманных номеров кабинетов, сроков, перечней обязательных
документов и миграционных требований. Всё, что нельзя подтвердить, помечено
как «уточнить в подразделении ТИУ». Общие контакты ТИУ (телефон, e-mail,
библиотека) взяты из таблицы вопросов и ответов и требуют проверки
перед публикацией.

Структура: каждый текст — словарь {"ru": "...", "en": "..."}.
Чтобы добавить подраздел, добавьте элемент в TOPICS.
"""


def L(ru, en):
    return {"ru": ru, "en": en}


def LL(ru_list, en_list):
    return {"ru": ru_list, "en": en_list}


UI = {
    "title": L("Иностранным студентам", "For international students"),
    "subtitle": L(
        "Универсальный раздел для студентов из любых стран: поступление, документы, общежитие, учёба, жизнь в Тюмени.",
        "A single guide for students from any country: admission, documents, dormitory, studies and life in Tyumen.",
    ),
    "language": L("Язык раздела", "Section language"),
    "topics": L("Темы", "Topics"),
    "back_topics": L("← Все темы раздела", "← All topics"),
    "open": L("Открыть", "Open"),
    "important": L("Важно", "Important"),
    "verify": L("Уточните в ТИУ", "Confirm with TIU"),
    "links": L("Официальные ссылки", "Official links"),
    "related": L("Связанные вопросы из базы знаний", "Related questions from the knowledge base"),
    "related_note": L(
        "Ответы в базе знаний написаны на русском языке.",
        "Answers in the knowledge base are written in Russian.",
    ),
    "faq": L("Частые вопросы", "Frequently asked questions"),
    "global_note": L(
        "Миграционные правила, сроки и перечни документов зависят от гражданства, статуса и ситуации и могут меняться. "
        "Информация на этой странице — справочная, а не официальные правила ТИУ. Перед любым действием уточните свой случай "
        "в подразделении ТИУ, которое работает с иностранными студентами, и на официальных государственных ресурсах.",
        "Migration rules, deadlines and document lists depend on your citizenship, status and situation, and can change. "
        "This page is general guidance, not official TIU rules. Before you act, confirm your individual case with the TIU office "
        "that works with international students and on official government websites.",
    ),
    "emergency_title": L("Экстренные номера", "Emergency numbers"),
}

LINKS = {
    "tiu": ("tyuiu.ru", "https://tyuiu.ru/", L("Официальный сайт ТИУ", "TIU official website")),
    "portal": ("my.tyuiu.ru", "https://my.tyuiu.ru/", L("Личный кабинет студента ТИУ", "TIU student portal")),
    "educon": ("educon2.tyuiu.ru", "https://educon2.tyuiu.ru/", L("Электронная образовательная среда (Educon)", "Electronic learning environment (Educon)")),
    "students": ("tyuiu.ru/…/studentam",
                 "https://www.tyuiu.ru/obrazovanie/instituty/institut-servisa-i-otraslevogo-upravleniia/studentam",
                 L("ТИУ: информация для студентов", "TIU: information for students")),
    "library": ("tyuiu.ru/…/biblioteka",
                "https://www.tyuiu.ru/infrastruktura/naucnaia-biblioteka/elektronnye-resursy",
                L("Научная библиотека ТИУ: электронные ресурсы", "TIU Scientific Library: e-resources")),
    "gosuslugi": ("gosuslugi.ru", "https://www.gosuslugi.ru/", L("Госуслуги (государственные услуги)", "Gosuslugi (state services portal)")),
    "mvd": ("мвд.рф", "https://xn--b1aew.xn--p1ai/", L("МВД России (официальный сайт)", "Russian Ministry of Internal Affairs (official site)")),
}

# Общие контакты из таблицы вопросов (требуют проверки перед публикацией)
CONTACTS = [
    {
        "name": L("ТИУ: общий контакт", "TIU: general contact"),
        "address": L("г. Тюмень, ул. Володарского, 38", "38 Volodarskogo St., Tyumen"),
        "phone": "8 (3452) 28-36-60",
        "email": "general@tyuiu.ru",
        "note": L("Общий контакт университета. Подразделение для иностранных студентов уточните здесь.",
                  "General university contact. Ask here which office handles international students."),
    },
    {
        "name": L("Научная библиотека ТИУ", "TIU Scientific Library"),
        "address": L("г. Тюмень, ул. Мельникайте, 72", "72 Melnikaite St., Tyumen"),
        "phone": "8 (3452) 28-30-69",
        "email": "kajukovadh@tyuiu.ru",
        "note": L("Кабинет и режим работы уточните перед визитом.", "Confirm the room and opening hours before you go."),
    },
]

EMERGENCY = [
    ("112", L("Единый номер экстренных служб", "Single emergency number")),
    ("101", L("Пожарная служба", "Fire service")),
    ("102", L("Полиция", "Police")),
    ("103", L("Скорая медицинская помощь", "Ambulance")),
]

TOPICS = [
    # ------------------------------------------------------------------ 1
    {
        "id": "admission",
        "icon": "🎓",
        "title": L("Поступление и оформление", "Admission & enrolment"),
        "summary": L("Этапы поступления, документы, оформление после зачисления, студенческие документы.",
                     "Admission steps, documents, enrolment and student documents."),
        "warning": L("Требования к иностранным абитуриентам (приглашение, виза, признание документов об образовании, квоты) "
                     "зависят от гражданства и программы. Уточняйте их в приёмной комиссии ТИУ и в подразделении для иностранных студентов.",
                     "Requirements for international applicants (invitation, visa, recognition of education documents, quotas) depend on "
                     "citizenship and programme. Confirm them with the TIU admissions office and the international students office."),
        "sections": [
            {"title": L("Основные этапы", "Main stages"), "kind": "steps",
             "items": LL([
                 "Выберите направление и изучите правила приёма на официальном сайте ТИУ.",
                 "Подайте заявление и документы способом и в сроки, которые указывает приёмная комиссия.",
                 "Дождитесь решения о зачислении и выполняйте инструкции университета (в том числе по договору, если он нужен).",
                 "После зачисления подтвердите оформление в университете и уточните, как получить доступ к личному кабинету.",
                 "Получите студенческие документы и узнайте расписание.",
             ], [
                 "Choose your programme and read the admission rules on the official TIU website.",
                 "Submit your application and documents in the way and by the deadlines set by the admissions office.",
                 "Wait for the admission decision and follow the university's instructions (including the contract, if one is required).",
                 "After enrolment, confirm your registration at the university and ask how to access your student portal.",
                 "Collect your student documents and check your timetable.",
             ])},
            {"title": L("Документы: о чём спросить заранее", "Documents: what to ask about in advance"), "kind": "list",
             "note": L("Это не официальный перечень. Точный список для вашей страны и программы выдаёт ТИУ.",
                       "This is not an official list. TIU provides the exact list for your country and programme."),
             "items": LL([
                 "паспорт или иной документ, удостоверяющий личность;",
                 "документ об образовании и требования к его переводу и признанию;",
                 "документы по миграционному статусу (виза, миграционная карта — если применимо);",
                 "медицинские документы и страхование — нужны ли они в вашем случае;",
                 "фотографии и заявление в формате, который требует ТИУ.",
             ], [
                 "passport or other identity document;",
                 "education certificate and the requirements for its translation and recognition;",
                 "migration status documents (visa, migration card — if applicable);",
                 "medical documents and insurance — whether they are required in your case;",
                 "photos and an application in the format TIU requires.",
             ])},
            {"title": L("Оформление после зачисления", "After enrolment"), "kind": "list",
             "items": LL([
                 "Обратитесь в дирекцию своего института или подразделение, которое ведёт студенческие документы.",
                 "Уточните, где и когда получить студенческий билет и нужны ли дополнительные документы.",
                 "Войдите в личный кабинет и проверьте свои данные и расписание.",
                 "Сразу сообщайте об ошибках в ФИО, датах и паспортных данных — их проще исправить в начале обучения.",
             ], [
                 "Contact your institute's dean's office or the office that handles student records.",
                 "Ask where and when to collect your student ID and whether extra documents are needed.",
                 "Sign in to the student portal and check your personal data and timetable.",
                 "Report mistakes in your name, dates or passport details at once — they are easier to fix early.",
             ])},
        ],
        "links": ["tiu", "portal"],
        "related": {"ids": ["n_120", "n_112", "n_113"], "categories": []},
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "migration",
        "icon": "🛂",
        "title": L("Миграционный учёт и документы", "Migration registration & documents"),
        "summary": L("Постановка на учёт, продление пребывания, смена адреса, потеря документов.",
                     "Registration, extending your stay, change of address, lost documents."),
        "warning": L("Ошибки в миграционных вопросах могут привести к штрафам и проблемам с пребыванием. "
                     "Не опирайтесь на этот текст как на закон: сроки и документы зависят от вашего гражданства и статуса. "
                     "Обращайтесь заранее и не откладывайте. Не пользуйтесь неофициальными «посредниками».",
                     "Mistakes in migration matters can lead to fines and problems with your stay. "
                     "Do not treat this text as law: deadlines and documents depend on your citizenship and status. "
                     "Ask early and do not delay. Do not use unofficial “agents”."),
        "verify": L("Точные сроки постановки на учёт, продления пребывания и перечень документов — уточнить в подразделении ТИУ, "
                    "которое работает с иностранными студентами, и в органах миграционного контроля.",
                    "Exact deadlines for registration and extension, and the document list — confirm with the TIU office for international "
                    "students and with the migration authorities."),
        "sections": [
            {"title": L("Постановка на миграционный учёт", "Migration registration"), "kind": "steps",
             "items": LL([
                 "Сразу после приезда обратитесь в подразделение ТИУ, которое сопровождает иностранных студентов.",
                 "Узнайте, кто в вашем случае подаёт уведомление (университет, общежитие или другая принимающая сторона) и что нужно от вас.",
                 "Предоставьте документы, которые у вас попросят (обычно паспорт, миграционная карта, виза — если применимо, данные о месте проживания).",
                 "Сохраните подтверждающий документ и сделайте его копию.",
             ], [
                 "Right after arrival, contact the TIU office that supports international students.",
                 "Ask who submits the notification in your case (university, dormitory or another host party) and what is needed from you.",
                 "Provide the documents they ask for (usually passport, migration card, visa — if applicable, accommodation details).",
                 "Keep the confirmation document and make a copy.",
             ])},
            {"title": L("Продление срока пребывания", "Extending your stay"), "kind": "list",
             "items": LL([
                 "Начинайте заранее: не ждите последних дней срока.",
                 "Уточните в подразделении ТИУ, какие документы нужны и кто их подаёт.",
                 "Следите за сроком действия визы или иного документа и записывайте дату в календарь.",
             ], [
                 "Start in advance: do not wait until the last days.",
                 "Ask the TIU office which documents are needed and who submits them.",
                 "Track the expiry date of your visa or other document and put the date in your calendar.",
             ])},
            {"title": L("Если изменилось место проживания", "If your address changes"), "kind": "list",
             "items": LL([
                 "Сообщите об этом в подразделение ТИУ до или сразу после переезда.",
                 "Уточните, нужно ли заново оформлять учёт по новому адресу и кто это делает.",
                 "Сохраните подтверждение нового места проживания.",
             ], [
                 "Tell the TIU office before or immediately after you move.",
                 "Ask whether registration at the new address is required and who does it.",
                 "Keep proof of your new place of residence.",
             ])},
            {"title": L("Если документы потеряны или украдены", "If documents are lost or stolen"), "kind": "steps",
             "items": LL([
                 "Не откладывайте: сообщите в подразделение ТИУ для иностранных студентов в тот же день.",
                 "Следуйте их указаниям, какие органы нужно уведомить и в каком порядке (в том числе полицию и посольство или консульство вашей страны).",
                 "Заранее храните копии или фото паспорта, визы и миграционной карты отдельно от оригиналов.",
             ], [
                 "Do not wait: tell the TIU office for international students the same day.",
                 "Follow their instructions on which authorities to notify and in what order (including the police and your country's embassy or consulate).",
                 "Keep copies or photos of your passport, visa and migration card separately from the originals.",
             ])},
        ],
        "links": ["gosuslugi", "mvd", "tiu"],
        "related": {"ids": ["n_116", "n_117", "n_118", "n_119", "n_120", "n_113"], "categories": []},
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "dorm",
        "icon": "🏠",
        "title": L("Общежитие и проживание", "Dormitory & housing"),
        "summary": L("Место в общежитии, заселение, документы, правила, бытовые вопросы.",
                     "Getting a room, check-in, documents, rules and everyday issues."),
        "warning": L("Не приезжайте на заселение, пока не подтвердили в ТИУ дату, место и условия. "
                     "Условия оплаты и перечень документов уточняйте в офисе, который отвечает за общежития.",
                     "Do not travel to check in until TIU has confirmed the date, room and terms. "
                     "Confirm payment terms and the document list with the office responsible for dormitories."),
        "sections": [
            {"title": L("Как получить место и заселиться", "Getting a room and checking in"), "kind": "steps",
             "items": LL([
                 "Заранее свяжитесь с подразделением ТИУ, которое занимается общежитиями (кампус-офис).",
                 "Подтвердите общежитие, дату заселения, наличие места и условия оплаты.",
                 "Подготовьте документы, которые попросит университет (обычно паспорт, миграционные документы, подтверждение зачисления).",
                 "При заселении проверьте комнату и мебель, уточните правила и сохраните договор или другие документы.",
             ], [
                 "Contact the TIU office that handles dormitories (campus office) in advance.",
                 "Confirm the dormitory, check-in date, room availability and payment terms.",
                 "Prepare the documents the university asks for (usually passport, migration documents, enrolment confirmation).",
                 "At check-in, inspect the room and furniture, ask about the rules and keep your contract or other papers.",
             ])},
            {"title": L("Правила и быт", "Rules and everyday life"), "kind": "list",
             "items": LL([
                 "Правила проживания выдаёт общежитие: прочитайте их при заселении и спросите, если что-то непонятно.",
                 "Режим, гости, оплата, уборка, техника в комнате — уточните у коменданта или администрации.",
                 "Берегите ключи и документы; не передавайте их посторонним.",
             ], [
                 "The dormitory provides its own rules: read them at check-in and ask if anything is unclear.",
                 "Curfew, guests, payments, cleaning and electrical appliances — ask the dormitory administration.",
                 "Look after your keys and documents; do not hand them to strangers.",
             ])},
            {"title": L("Если возникла проблема", "If something goes wrong"), "kind": "list",
             "items": LL([
                 "Поломка, конфликт, потеря ключа: сначала обратитесь к коменданту или администрации общежития.",
                 "Если вопрос не решается — к подразделению ТИУ, отвечающему за общежития, или в дирекцию института.",
                 "Опасность для жизни, пожар, травма: звоните 112.",
             ], [
                 "Breakage, conflict or lost key: first speak to the dormitory manager or administration.",
                 "If it is not solved, go to the TIU office responsible for dormitories or your institute's dean's office.",
                 "Danger to life, fire or injury: call 112.",
             ])},
        ],
        "links": ["students", "tiu"],
        "related": {"ids": ["n_118"], "categories": ["dorm"]},
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "study",
        "icon": "📚",
        "title": L("Обучение", "Studies"),
        "summary": L("Расписание, личный кабинет, электронная среда, библиотека, экзамены, задолженности.",
                     "Timetable, student portal, e-learning, library, exams and academic debts."),
        "sections": [
            {"title": L("Расписание и личный кабинет", "Timetable and student portal"), "kind": "list",
             "items": LL([
                 "Расписание и справки доступны в личном кабинете студента: my.tyuiu.ru.",
                 "Проверяйте расписание перед каждым учебным днём: время и аудитории могут меняться.",
                 "Если не получается войти в кабинет, обратитесь в дирекцию своего института.",
             ], [
                 "Your timetable and certificate requests are in the student portal: my.tyuiu.ru.",
                 "Check the timetable before each study day: times and rooms may change.",
                 "If you cannot sign in, contact your institute's dean's office.",
             ])},
            {"title": L("Электронная образовательная среда и библиотека", "E-learning and library"), "kind": "list",
             "items": LL([
                 "Учебные материалы и задания размещаются в электронной образовательной среде (Educon).",
                 "Научная библиотека предоставляет электронные ресурсы и каталог; режим работы и порядок получения читательского билета уточните в библиотеке.",
             ], [
                 "Course materials and assignments are placed in the electronic learning environment (Educon).",
                 "The Scientific Library offers e-resources and a catalogue; ask the library about opening hours and how to get a reader's card.",
             ])},
            {"title": L("Экзамены, зачёты и задолженности", "Exams, credits and academic debts"), "kind": "steps",
             "items": LL([
                 "Узнайте у преподавателя и в дирекции формат и даты экзаменов и зачётов.",
                 "Если есть задолженность, не ждите: обратитесь к преподавателю и в дирекцию, чтобы узнать порядок и сроки пересдачи.",
                 "Если вы пропустили занятия или экзамен по уважительной причине (например, болезнь), сохраните подтверждающие документы и сообщите в дирекцию.",
             ], [
                 "Ask your teacher and the dean's office about the format and dates of exams and credits.",
                 "If you have a debt, do not wait: speak to the teacher and the dean's office about the retake procedure and dates.",
                 "If you missed classes or an exam for a valid reason (e.g. illness), keep the documents and inform the dean's office.",
             ])},
        ],
        "links": ["portal", "educon", "library"],
        "related": {"ids": ["n_001", "n_010", "n_121", "n_122", "n_166"], "categories": []},
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "city",
        "icon": "🏙️",
        "title": L("Адаптация в Тюмени", "Settling in Tyumen"),
        "summary": L("Транспорт, магазины, банки, ориентирование в городе, полезные контакты.",
                     "Transport, shops, banks, getting around and useful contacts."),
        "sections": [
            {"title": L("Ориентирование и транспорт", "Getting around"), "kind": "list",
             "items": LL([
                 "Найдите нужный корпус в разделе «Карта корпусов» и откройте маршрут в Яндекс Картах.",
                 "Стоимость проезда и способы оплаты зависят от вида транспорта: уточняйте на остановке, у водителя или у старшекурсников.",
                 "Зимой в Тюмени холодно: заранее подготовьте тёплую одежду и обувь.",
             ], [
                 "Find your building in the “Campus map” section and open the route in Yandex Maps.",
                 "Fares and payment methods depend on the type of transport: ask at the stop, the driver or senior students.",
                 "Winters in Tyumen are cold: prepare warm clothes and shoes in advance.",
             ])},
            {"title": L("Магазины, услуги и банки", "Shops, services and banks"), "kind": "list",
             "items": LL([
                 "Для банковских услуг обычно нужен паспорт; требования к иностранным гражданам зависят от банка — уточняйте в отделении.",
                 "Не передавайте паспорт, пароли и коды из СМС посторонним.",
                 "Банкоматы и сервисы на территории университета — см. вопросы базы знаний.",
             ], [
                 "Banks usually require a passport; requirements for foreign citizens depend on the bank — ask at the branch.",
                 "Never give your passport, passwords or SMS codes to strangers.",
                 "For ATMs and services on campus, see the knowledge base questions.",
             ])},
            {"title": L("Полезные контакты", "Useful contacts"), "kind": "list",
             "items": LL([
                 "Общий контакт ТИУ и библиотека — в разделе «Контакты и помощь».",
                 "Экстренные номера — в разделе «Здоровье и безопасность».",
             ], [
                 "The general TIU contact and the library are listed in “Contacts & help”.",
                 "Emergency numbers are in “Health & safety”.",
             ])},
        ],
        "links": ["tiu"],
        "related": {"ids": ["n_112", "n_110", "n_111", "n_181", "n_182"], "categories": []},
        "link_page": "map",
    },
    # ------------------------------------------------------------------ 6
    {
        "id": "health",
        "icon": "🩺",
        "title": L("Здоровье и безопасность", "Health & safety"),
        "summary": L("Медицинская помощь, экстренные ситуации, полезные номера, личная безопасность.",
                     "Medical help, emergencies, useful numbers and personal safety."),
        "warning": L("В экстренной ситуации сначала звоните 112 (или 103 — скорая помощь), а потом сообщайте в университет.",
                     "In an emergency call 112 first (or 103 for an ambulance), then inform the university."),
        "show_emergency": True,
        "sections": [
            {"title": L("Медицинская помощь", "Medical help"), "kind": "list",
             "items": LL([
                 "Узнайте в подразделении ТИУ для иностранных студентов, какое медицинское страхование нужно в вашем случае и как оно оформляется.",
                 "При плохом самочувствии на занятиях сообщите преподавателю или сотрудникам корпуса и вызовите скорую помощь при необходимости.",
                 "Сохраняйте медицинские справки: они могут понадобиться в университете.",
             ], [
                 "Ask the TIU office for international students which medical insurance applies in your case and how to get it.",
                 "If you feel unwell in class, tell your teacher or building staff and call an ambulance if needed.",
                 "Keep your medical certificates: the university may need them.",
             ])},
            {"title": L("Личная безопасность", "Personal safety"), "kind": "list",
             "items": LL([
                 "Храните копии документов отдельно от оригиналов.",
                 "Проверяйте информацию о миграционных сроках только на официальных ресурсах; не доверяйте сообщениям в соцсетях и «помощникам» за деньги.",
                 "Если вам угрожают или вы стали свидетелем конфликта, сообщите в полицию (102 или 112) и в университет.",
                 "Психологическую поддержку в ТИУ уточняйте в базе знаний или в дирекции института.",
             ], [
                 "Keep copies of your documents separately from the originals.",
                 "Check migration deadlines only on official resources; do not trust social media messages or paid “helpers”.",
                 "If you are threatened or witness a conflict, report it to the police (102 or 112) and to the university.",
                 "For psychological support at TIU, see the knowledge base or ask your dean's office.",
             ])},
        ],
        "links": [],
        "related": {"ids": ["n_114", "n_115", "n_141", "n_142", "n_154", "n_155", "n_148"], "categories": []},
    },
    # ------------------------------------------------------------------ 7
    {
        "id": "contacts",
        "icon": "📞",
        "title": L("Контакты и помощь", "Contacts & help"),
        "summary": L("Подразделения, службы, официальные ссылки и куда идти по типу проблемы.",
                     "Offices, services, official links and where to go for each kind of problem."),
        "verify": L("Контакты взяты из таблицы вопросов и ответов и требуют проверки перед публикацией. "
                    "Название подразделения для иностранных студентов, его кабинет и часы приёма в проекте не подтверждены — уточните по общему контакту ТИУ.",
                    "Contacts come from the Q&A table and must be verified before publication. "
                    "The name, room and opening hours of the international students office are not confirmed in this project — ask via the general TIU contact."),
        "show_contacts": True,
        "sections": [
            {"title": L("Куда обратиться: по типу проблемы", "Where to go: by type of problem"), "kind": "list",
             "items": LL([
                 "**Миграционный учёт, виза, документы** — подразделение ТИУ для иностранных студентов (название и кабинет уточните по общему контакту ТИУ).",
                 "**Учёба, расписание, справки, студенческий билет** — дирекция вашего института и личный кабинет my.tyuiu.ru.",
                 "**Общежитие** — комендант и администрация общежития; затем подразделение ТИУ, отвечающее за общежития.",
                 "**Оплата обучения и договор** — подразделение, указанное в вашем договоре; уточните по общему контакту.",
                 "**Библиотека** — Научная библиотека ТИУ.",
                 "**Здоровье, опасность** — 112 (экстренно); затем сообщите в университет.",
             ], [
                 "**Migration registration, visa, documents** — the TIU office for international students (ask the general TIU contact for its name and room).",
                 "**Studies, timetable, certificates, student ID** — your institute's dean's office and the my.tyuiu.ru portal.",
                 "**Dormitory** — the dormitory manager and administration; then the TIU office responsible for dormitories.",
                 "**Tuition and contract** — the office named in your contract; confirm via the general contact.",
                 "**Library** — TIU Scientific Library.",
                 "**Health, danger** — 112 (emergency); then inform the university.",
             ])},
        ],
        "links": ["tiu", "portal", "educon", "students", "gosuslugi", "mvd"],
        "related": {"ids": ["n_112", "n_164", "n_167"], "categories": []},
    },
]

# Ответы на частые вопросы сохранены из прежней версии сайта (английские) и переведены на русский.
FAQ = [
    (L("Как заселиться в общежитие ТИУ?", "How do I check in to a TIU dormitory?"),
     L("Свяжитесь с офисом ТИУ по размещению (кампус-офис) до приезда. Подтвердите общежитие, дату заселения, наличие места, условия оплаты и необходимые документы. "
       "Возьмите паспорт, миграционные документы, подтверждение зачисления и другие документы, которые запросит университет. Не приезжайте на заселение, не подтвердив время и актуальные требования.",
       "Contact the TIU accommodation / campus office before arrival. Confirm your assigned dormitory, check-in date, room availability, payment terms and required documents. "
       "Bring your passport, migration documents, admission/enrolment confirmation and any documents requested by the university. Do not travel to check in without confirming the appointment and current requirements.")),
    (L("Миграционный учёт: что делать?", "Migration registration: what should I do?"),
     L("Иностранные граждане, находящиеся в России, обязаны соблюдать правила миграционного учёта. Сразу после приезда обратитесь в подразделение ТИУ, отвечающее за иностранных студентов или миграционное сопровождение, "
       "и предоставьте паспорт, миграционную карту, визу (если применимо), данные о приезде и месте проживания. Сроки и принимающая сторона зависят от вашего статуса и места проживания. "
       "Всегда следуйте актуальным указаниям ТИУ и официальных миграционных органов.",
       "Foreign citizens staying in Russia must comply with migration registration rules. Immediately after arrival, contact the TIU office responsible for international students or migration support and provide your passport, "
       "migration card, visa (if applicable), arrival details and accommodation information. Deadlines and the responsible receiving party depend on your status and place of stay. "
       "Always follow the latest instructions from TIU and official migration authorities.")),
    (L("Как получить студенческий билет?", "How can I get my student ID?"),
     L("После подтверждения зачисления обратитесь в дирекцию своего института или в подразделение, которое ведёт студенческие документы. Уточните, готов ли билет, где его получить и нужны ли фотография или дополнительные документы. "
       "Возьмите паспорт и данные о зачислении.",
       "After your enrolment is confirmed, contact your institute's dean's office or the office responsible for student records. Ask whether your student ID is ready, where to collect it and whether a photo or additional documents are required. "
       "Bring your passport and enrolment details.")),
    (L("Где посмотреть расписание занятий?", "Where can I find my class schedule?"),
     L("Войдите в личный кабинет студента ТИУ: https://my.tyuiu.ru/. Откройте раздел расписания и проверяйте его перед каждым учебным днём, так как аудитории и время могут меняться.",
       "Sign in to the TIU student portal: https://my.tyuiu.ru/ . Open the schedule section and check it again before each study day because rooms and times may change.")),
    (L("Как найти корпус ТИУ?", "How do I find a TIU building?"),
     L("Воспользуйтесь разделом «Карта корпусов» на этом сайте. Найдите корпус по номеру или адресу, выберите метку и откройте маршрут в Яндекс Картах. Если вы знаете только номер аудитории, сначала уточните корпус в институте или в расписании.",
       "Use the Campus map section of this website. Search by building number or address, select a marker and open the route in Yandex Maps. If you only know a classroom number, confirm its building with your institute or the timetable first.")),
    (L("Где получить справку об обучении?", "Where can I get a certificate of enrolment?"),
     L("Войдите в личный кабинет студента ТИУ (https://my.tyuiu.ru/) и найдите услугу заказа справок. Если нужной справки онлайн нет, обратитесь в дирекцию своего института. Уточните место получения и срок изготовления.",
       "Sign in to the TIU student portal at https://my.tyuiu.ru/ and look for the certificate / document request service. If the required certificate is not available online, contact your institute's dean's office. Confirm the collection location and processing time.")),
    (L("К кому обратиться за помощью?", "Who should I contact if I need help?"),
     L("Начните с дирекции своего института или подразделения ТИУ, которое сопровождает иностранных студентов. В экстренной ситуации (опасность, медицинская помощь) звоните 112. "
       "Не полагайтесь на неофициальные сообщения в соцсетях в вопросах права и миграционных сроков.",
       "Start with your institute's dean's office or the TIU office supporting international students. For an urgent safety or medical emergency in Russia, call 112. "
       "Do not rely on unofficial social media messages for legal or migration deadlines.")),
    (L("Могут ли иностранные студенты участвовать в клубах и мероприятиях?", "Can international students join clubs and events?"),
     L("Во многие студенческие клубы, спортивные секции, волонтёрские проекты и мероприятия могут вступать и иностранные студенты. Условия участия и требования к языку различаются. "
       "Прочитайте объявление о мероприятии и свяжитесь с организатором до регистрации.",
       "Many student clubs, sports activities, volunteer projects and events may be open to international students. Eligibility and language requirements vary. "
       "Check the event announcement and contact its organiser before registering.")),
]

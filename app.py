import streamlit as st

# 1. Настройка страницы
st.set_page_config(
    page_title="ТИУ Навигатор",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Единая база данных вопросов из файлов команды
QUESTIONS_DATA = [
    # === ДОКУМЕНТЫ ===
    {
        "id": "doc_1",
        "question": "Как получить справку об обучении?",
        "category": "docs",
        "answer": "1. Зайдите в личный кабинет студента ТИУ (my.tyuiu.ru).\n2. Перейдите в раздел «Заказ справок».\n3. Выберите нужный тип справки и укажите количество экземпляров.\n4. Заберите готовую справку в дирекции вашего института.",
        "department": "Учебный отдел / Дирекция института",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Студенческий билет или паспорт",
        "deadline": "1–3 рабочих дня",
        "officialSource": "https://my.tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "doc_2",
        "question": "Как заказать справку?",
        "category": "docs",
        "answer": "Авторизуйтесь в Личном кабинете студента «Мой ТИУ», перейдите во вкладку заказа документов и выберите нужный вид справки.",
        "department": "Дирекция института",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Не требуются (при заказе онлайн)",
        "deadline": "Информация уточняется",
        "officialSource": "https://my.tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "doc_3",
        "question": "Как получить справку для военкомата (Форма №4)?",
        "category": "docs",
        "answer": "Обратитесь во 2-й отдел ТИУ (Военно-учетный стол) с паспортом и приписным свидетельством.",
        "department": "2-й отдел ТИУ (Военно-учетный стол)",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Паспорт, приписное свидетельство",
        "deadline": "В день обращения",
        "officialSource": "https://tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "doc_4",
        "question": "Где можно распечатать документы?",
        "category": "docs",
        "answer": "Распечатать документы можно в Библиотечно-издательском комплексе ТИУ:\n• ул. Мельникайте, 72, каб. 16 — печать А0–А5;\n• ул. Мельникайте, 72, каб. 210 — печать А1–А5;\n• ул. Мельникайте, 70, каб. 106 — печать А1–А5;\n• ул. Луначарского, 2, корп. 1, каб. 158а — печать А3–А5.",
        "department": "Библиотечно-издательский комплекс ТИУ",
        "address": "ул. Мельникайте, 72 / ул. Мельникайте, 70 / ул. Луначарского, 2",
        "office": "каб. 16, 210, 106, 158а",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Файл с документом на флешке или в электронном виде",
        "deadline": "В момент обращения",
        "officialSource": "https://tyuiu.ru/infrastruktura/bibliotecno-izdatelskii-kompleks/kontakty",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "doc_5",
        "question": "Где можно сделать ксерокопию?",
        "category": "docs",
        "answer": "Ксерокопию можно сделать в Библиотечно-издательском комплексе ТИУ:\n• ул. Мельникайте, 72, каб. 16;\n• ул. Мельникайте, 72, каб. 210;\n• ул. Мельникайте, 70, каб. 106;\n• ул. Луначарского, 2, корп. 1, каб. 158а.",
        "department": "Библиотечно-издательский комплекс ТИУ",
        "address": "ул. Мельникайте, 72 / ул. Мельникайте, 70 / ул. Луначарского, 2",
        "office": "каб. 16, 210, 106, 158а",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Оригинал документа",
        "deadline": "В момент обращения",
        "officialSource": "https://tyuiu.ru/infrastruktura/bibliotecno-izdatelskii-kompleks/kontakty",
        "lastChecked": "25.09.2026"
    },

    # === УЧЁБА ===
    {
        "id": "study_1",
        "question": "Где посмотреть свое расписание?",
        "category": "study",
        "answer": "Интернет-ресурс: «Мой ТИУ», в своем профиле, в разделе «Расписание».",
        "department": "Учебный отдел / Диспетчерская",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Информация уточняется",
        "deadline": "Информация уточняется",
        "officialSource": "https://my.tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_2",
        "question": "Где узнать номер своей группы?",
        "category": "study",
        "answer": "Узнать номер своей группы можно через Личный кабинет студента «Мой ТИУ».",
        "department": "Информация уточняется",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Информация уточняется",
        "deadline": "Информация уточняется",
        "officialSource": "https://my.tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_3",
        "question": "Как узнать, в какой подгруппе я учусь?",
        "category": "study",
        "answer": "1. Войдите в свой аккаунт на ресурсе «Эдукон» или в «Мой ТИУ».\n2. Внутри электронных курсов по предметам, где группа делится (например, «Иностранный язык»), преподаватели часто вывешивают списки подгрупп.\n3. Также информацию можно уточнить у старосты группы.",
        "department": "Преподаватель дисциплины / Староста",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Информация уточняется",
        "deadline": "Информация уточняется",
        "officialSource": "https://educon2.tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_4",
        "question": "Где найти расписание на следующую неделю?",
        "category": "study",
        "answer": "Расписание на следующую неделю публикуется на портале «Мой ТИУ» в личном кабинете в разделе «Расписание».",
        "department": "Диспетчерская учебного отдела",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Информация уточняется",
        "deadline": "Обновляется еженедельно",
        "officialSource": "https://my.tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_5",
        "question": "Где посмотреть изменение в расписании?",
        "category": "study",
        "answer": "Всегда проверяйте вкладку расписания в «Мой ТИУ» вечером перед учебным днем, так как диспетчеры институтов могут внести изменения в конце рабочего дня.",
        "department": "Учебная часть",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Информация уточняется",
        "deadline": "Ежедневно вечером",
        "officialSource": "https://my.tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_6",
        "question": "Что делать при академической задолженности (долгах)?",
        "category": "study",
        "answer": "Возьмите бегунок в дирекции института и согласуйте с преподавателем дату пересдачи.",
        "department": "Дирекция института",
        "address": "Информация уточняется",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Зачетная книжка / Студенческий билет",
        "deadline": "В период ликвидации задолженностей",
        "officialSource": "https://tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_7",
        "question": "Где находится нужный корпус?",
        "category": "study",
        "answer": "Учебные корпуса ТИУ находятся по адресам:\n• корпус №1 — ул. Володарского, 38;\n• корпус №1А — ул. Орджоникидзе, 54;\n• корпус №2 — ул. Мельникайте, 72;\n• корпус №3 — ул. 50 лет Октября, 38;\n• корпус №4 — ул. Володарского, 56;\n• корпус №7 — ул. Мельникайте, 70;\n• корпуса №8/1, 8/2, 8/3, 8/4, 8/6 — ул. Луначарского, 2;\n• корпус №9 — ул. Луначарского, 4;\n• корпуса №10, №11 — ул. Энергетиков, 44 и 44, корп. 1;\n• корпус №13, №14 — ул. Холодильная, 85;\n• корпус №16 — ул. 50 лет Октября, 62;\n• корпус №17 — ул. Киевская, 78, корп. 1.",
        "department": "Департамент имущественных отношений ТИУ",
        "address": "Указаны в ответе",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Пропуск ТИУ / Студенческий билет",
        "deadline": "По графику работы корпусов",
        "officialSource": "https://tyuiu.ru/sveden/common/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_8",
        "question": "Где находится библиотека?",
        "category": "study",
        "answer": "Научная библиотека ТИУ находится по адресу г. Тюмень, ул. Мельникайте, 72. Основные помещения библиотеки находятся в кабинетах 12, 13, 15, 31, 32–33, 41, 42, 44, 45. Также библиотечные пункты находятся по адресам ул. Мельникайте, 70 и ул. Луначарского, 2, корп. 1.",
        "department": "Научная библиотека ТИУ",
        "address": "г. Тюмень, ул. Мельникайте, 72",
        "office": "каб. 12, 13, 15, 31, 32, 41",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Студенческий билет / Читательский билет",
        "deadline": "Пн-Сб: 08:00–18:00",
        "officialSource": "https://tyuiu.ru/infrastruktura/bibliotecno-izdatelskii-kompleks/kontakty",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_9",
        "question": "Где находится столовая?",
        "category": "study",
        "answer": "Пункты питания ТИУ находятся по адресам:\n• Столовая корп. №1 — ул. Володарского, 38\n• Пиццерия корп. №2 — ул. Мельникайте, 72\n• Буфет корп. №3 — ул. 50 лет Октября, 38\n• Буфет корп. №7 (5 этаж) — ул. Мельникайте, 70\n• Столовая корп. №10 — ул. Энергетиков, 44/1\n• Столовая корп. №13 — ул. Холодильная, 85\n• Буфет корп. №16 — ул. 50 лет Октября, 62\n• Столовая корп. №17 — ул. Киевская, 78/1.",
        "department": "Комбинат питания ТИУ",
        "address": "Указаны в ответе",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Не требуются",
        "deadline": "Согласно расписанию работы",
        "officialSource": "https://tyuiu.ru/sveden/catering/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_10",
        "question": "Где находится спортзал?",
        "category": "study",
        "answer": "Спортивные залы ТИУ расположены по нескольким адресам: ул. Володарского, 38; ул. Мельникайте, 72; ул. 50 лет Октября, 38; ул. Бабарынка, 20Б; ул. 50 лет Октября, 62.",
        "department": "Спортивный клуб ТИУ",
        "address": "Указаны в ответе",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Спортивная форма, пропуск",
        "deadline": "По расписанию занятий",
        "officialSource": "https://www.tyuiu.ru/infrastruktura/sportivnye-zaly/arenda",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_11",
        "question": "Где находится бассейн?",
        "category": "study",
        "answer": "Плавательный бассейн ТИУ находится по адресу: г. Тюмень, ул. Луначарского, 2, корп. 5.",
        "department": "Спортивный комплекс ТИУ",
        "address": "г. Тюмень, ул. Луначарского, 2, корп. 5",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Медицинская справка, плавательные принадлежности",
        "deadline": "По расписанию сеансов",
        "officialSource": "https://www.tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_12",
        "question": "Где находится медицинский пункт?",
        "category": "study",
        "answer": "Медицинские пункты ТИУ находятся по адресам:\n• ул. Володарского, 38, 3 этаж — медицинское отделение;\n• ул. Нагорная, 6, 1 этаж — доврачебная помощь;\n• ул. Киевская, 80, 1 этаж — доврачебная помощь.",
        "department": "Медицинский пункт ТИУ",
        "address": "ул. Володарского, 38 / ул. Нагорная, 6 / ул. Киевская, 80",
        "office": "3 этаж / 1 этаж",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Паспорт, медицинский полис ОМС",
        "deadline": "Пн-Пт в рабочее время",
        "officialSource": "https://www.tyuiu.ru/obrazovanie/instituty/institut-servisa-i-otraslevogo-upravleniia/kontakty",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_13",
        "question": "Где можно зарядить телефон или ноутбук?",
        "category": "study",
        "answer": "Зарядить телефон или ноутбук можно в библиотечных и учебных пространствах ТИУ. Основные места: ул. Мельникайте, 72; ул. Мельникайте, 70; ул. Луначарского, 2; ул. Луначарского, 2/1; ул. Володарского, 38; ул. 50 лет Октября, 38.",
        "department": "Студенческие пространства ТИУ",
        "address": "Указаны в ответе",
        "office": "Коворкинги, холы, библиотеки",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Не требуются",
        "deadline": "В часы работы корпусов",
        "officialSource": "https://tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_14",
        "question": "Где есть место для самостоятельной работы?",
        "category": "study",
        "answer": "Для самостоятельной работы можно воспользоваться библиотекой ТИУ и студенческими пространствами. Библиотека — ул. Мельникайте, 72 (08:00–18:00). Помещения также есть в корпусах: ул. Мельникайте, 70; ул. Луначарского, 2; ул. Володарского, 38; ул. 50 лет Октября, 38.",
        "department": "Научная библиотека / Коворкинги",
        "address": "Указаны в ответе",
        "office": "Информация уточняется",
        "phone": "Информация уточняется",
        "email": "Информация уточняется",
        "documents": "Студенческий билет",
        "deadline": "08:00–18:00",
        "officialSource": "https://tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "study_15",
        "question": "Как записаться в кружок?",
        "category": "study",
        "answer": "Выберите интересующее объединение на сайте ТИУ и обратитесь к руководителю. Для консультации обратитесь в Центр молодёжных инициатив: ул. Мельникайте, 72/1, каб. 103, тел. +7 (3452) 28-39-76.",
        "department": "Центр молодёжных инициатив ТИУ",
        "address": "ул. Мельникайте, 72/1",
        "office": "каб. 103",
        "phone": "+7 (3452) 28-39-76",
        "email": "Информация уточняется",
        "documents": "Заявление (заполняется на месте)",
        "deadline": "В течение учебного года",
        "officialSource": "https://www.tyuiu.ru/vneucebnaia-deiatelnost/tvorcestvo/studii",
        "lastChecked": "25.09.2026"
    },

    # === ОБЩЕЖИТИЕ ===
    {
        "id": "dorm_1",
        "question": "Где находится моё общежитие?",
        "category": "dorm",
        "answer": "1. Откройте официальный приказ о заселении на сайте ТИУ или в группе Студенческого городка ВКонтакте.\n2. Найдите в списках свои ФИО и узнайте номер общежития.\n3. Перейдите в раздел контактов Студгородка, чтобы посмотреть точный адрес.",
        "department": "Студенческий городок ТИУ (Центр учета проживающих)",
        "address": "г. Тюмень, ул. Нагорная, д. 6",
        "office": "Информация уточняется",
        "phone": "+7 (3452) 28-35-65",
        "email": "burovtsevaaa@tyuiu.ru",
        "documents": "Паспорт (для подтверждения личности при личном визите)",
        "deadline": "Приказы публикуются массово в августе",
        "officialSource": "https://www.tyuiu.ru/infrastruktura/studgorodok/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "dorm_2",
        "question": "Сколько стоит проживание в общежитии?",
        "category": "dorm",
        "answer": "1. Ознакомьтесь с актуальными тарифами в приказе ректора на сайте ТИУ.\n2. Для студентов на бюджете тариф составляет от 532 до 951 руб./мес., на договоре — от 977 до 1773 руб./мес. в зависимости от типа общежития.",
        "department": "Бухгалтерия Студенческого городка ТИУ",
        "address": "г. Тюмень, ул. Нагорная, д. 6",
        "office": "Информация уточняется",
        "phone": "+7 (3452) 28-35-65",
        "email": "burovtsevaaa@tyuiu.ru",
        "documents": "Квитанция об оплате, паспорт, льготные документы (при наличии)",
        "deadline": "Утверждается ежегодно на календарный год",
        "officialSource": "https://www.tyuiu.ru/infrastruktura/studgorodok/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "dorm_3",
        "question": "Как оплатить общежитие?",
        "category": "dorm",
        "answer": "1. Зайдите на официальный сайт ТИУ в раздел онлайн-оплаты.\n2. Выберите пункт «Оплата за проживание в общежитии», введите ФИО, номер договора и сумму.\n3. Введите данные карты и подтвердите платеж.\n4. Сохраните чек об оплате.",
        "department": "Студенческий городок ТИУ (Касса / Бухгалтерия)",
        "address": "г. Тюмень, ул. Нагорная, д. 6",
        "office": "Информация уточняется",
        "phone": "+7 (3452) 28-35-65",
        "email": "burovtsevaaa@tyuiu.ru",
        "documents": "Реквизиты договора найма жилого помещения, банковская карта",
        "deadline": "Зачисление от 1 до 3 рабочих дней",
        "officialSource": "https://www.tyuiu.ru/infrastruktura/studgorodok/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "dorm_4",
        "question": "Какие документы нужны для заселения?",
        "category": "dorm",
        "answer": "Для заселения в общежитие подготовьте следующий комплект документов:\n• Паспорт + копия (первая страница и регистрация);\n• Справка о прохождении флюорографии;\n• Медицинская справка (форма 086/у);\n• 3 фотографии 3х4.",
        "department": "Заведующий общежитием / Студгородок",
        "address": "По адресу вашего общежития",
        "office": "Кабинет заведующего",
        "phone": "+7 (3452) 28-35-65",
        "email": "burovtsevaaa@tyuiu.ru",
        "documents": "Паспорт, флюорография, справка 086/у, 3 фото 3х4",
        "deadline": "В день заселения",
        "officialSource": "https://www.tyuiu.ru/infrastruktura/studgorodok/",
        "lastChecked": "25.09.2026"
    },

    # === СТИПЕНДИИ ===
    {
        "id": "scholarship_1",
        "question": "Какие стипендии есть в ТИУ?",
        "category": "scholarship",
        "answer": "1. Ознакомьтесь со списком выплат (государственная академическая, социальная, повышенная ПГАС, именные стипендии).\n2. Проверьте критерии назначения.\n3. Соберите пакет документов и подайте через Личный кабинет студента или Единый деканат.",
        "department": "Единый деканат (Служба поддержки студентов ТИУ)",
        "address": "г. Тюмень, ул. Володарского, д. 38",
        "office": "Информация уточняется",
        "phone": "+7 (3452) 28-36-60",
        "email": "general@tyuiu.ru",
        "documents": "Паспорт, заявление в ЛК, документы на льготы/достижения",
        "deadline": "По результатам промежуточной аттестации (2 раза в год)",
        "officialSource": "https://www.tyuiu.ru/students/stipendii/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "scholarship_2",
        "question": "Как получить академическую стипендию?",
        "category": "scholarship",
        "answer": "1. Успешно сдайте сессию без оценок «удовлетворительно» (троек) и долгов.\n2. Дождитесь автоматического формирования приказа (заявление не требуется).\n3. Выплата начисляется ежемесячно на карту «МИР».",
        "department": "Единый деканат ТИУ",
        "address": "г. Тюмень, ул. Володарского, д. 38",
        "office": "Информация уточняется",
        "phone": "+7 (3452) 28-36-60",
        "email": "general@tyuiu.ru",
        "documents": "Документы не требуются (назначается автоматически)",
        "deadline": "Назначается на семестр до следующей сессии",
        "officialSource": "https://www.tyuiu.ru/students/stipendii/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "scholarship_3",
        "question": "Как получить повышенную стипендию?",
        "category": "scholarship",
        "answer": "1. Дождитесь старта приема заявок на ПГАС в начале семестра.\n2. Подтвердите отсутствие троек и задолженностей.\n3. Сформируйте портфолио достижений за последний год.\n4. Заполните форму в Личном кабинете и передайте комплект на верификацию в дирекцию.",
        "department": "Дирекция вашего института / филиала",
        "address": "г. Тюмень, ул. Володарского, д. 38 (или корпус института)",
        "office": "Информация уточняется",
        "phone": "+7 (3452) 28-36-60",
        "email": "general@tyuiu.ru",
        "documents": "Заявление-анкета, копия зачетки, грамоты, дипломы, статьи",
        "deadline": "В установленные приказом ТИУ сроки 2 раза в год",
        "officialSource": "https://www.tyuiu.ru/students/stipendii/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "scholarship_4",
        "question": "Как подать на повышенную государственную академическую стипендию (ПГАС)?",
        "category": "scholarship",
        "answer": "ПГАС назначается за особые достижения в учебной, научно-исследовательской, общественной, культурно-творческой и спортивной деятельности. Портфолио подается в начале каждого семестра через ЛК ТИУ.",
        "department": "Дирекция института / Студенческий отдел",
        "address": "г. Тюмень, ул. Володарского, д. 38",
        "office": "Информация уточняется",
        "phone": "+7 (3452) 28-36-60",
        "email": "general@tyuiu.ru",
        "documents": "Портфолио достижений, сертификаты, публикации, копии дипломов",
        "deadline": "В первые 2–3 недели семестра",
        "officialSource": "https://www.tyuiu.ru/students/stipendii/",
        "lastChecked": "25.09.2026"
    },

    # === ЧТО ДЕЛАТЬ, ЕСЛИ... (SOS) ===
    {
        "id": "sos_1",
        "question": "🚨 Потерял студенческий билет",
        "category": "sos",
        "answer": "1. Напишите заявление об утере в дирекции своего института.\n2. Оплатите пошлину за восстановление по реквизитам.\n3. Принесите фото 3х4 и чек в дирекцию для оформления дубликата.",
        "department": "Дирекция института",
        "address": "Адрес учебного корпуса вашего института",
        "office": "Кабинет дирекции",
        "phone": "+7 (3452) 28-36-60",
        "email": "general@tyuiu.ru",
        "documents": "Заявление, фото 3х4, квитанция об оплате пошлины",
        "deadline": "5–10 рабочих дней",
        "officialSource": "https://tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "sos_2",
        "question": "🚨 Потерял пропуск в корпус / общежитие",
        "category": "sos",
        "answer": "1. Напишите заявление на восстановление электронного пропуска.\n2. Обратитесь в Бюро пропусков ТИУ для заблокирования старой карты.\n3. Оплатите стоимость изготовления нового пропуска и получите дубликат.",
        "department": "Бюро пропусков ТИУ / Служба безопасности",
        "address": "ул. Володарского, 38",
        "office": "Бюро пропусков",
        "phone": "+7 (3452) 28-36-60",
        "email": "general@tyuiu.ru",
        "documents": "Паспорт, заявление, документ провизора оплаты",
        "deadline": "В день обращения",
        "officialSource": "https://tyuiu.ru/",
        "lastChecked": "25.09.2026"
    },
    {
        "id": "sos_3",
        "question": "🚨 Заболел и пропустил занятия",
        "category": "sos",
        "answer": "1. Обратитесь к врачу в медучреждение или медпункт ТИУ в первый день заболевания.\n2. Получите медицинскую справку установленной формы.\n3. Сдайте справку в дирекцию института в течение 3 дней после выздоровления для закрытия пропусков по уважительной причине.",
        "department": "Медицинский пункт ТИУ / Дирекция института",
        "address": "ул. Володарского, 38, 3 этаж (Медпункт)",
        "office": "Медпункт / Дирекция",
        "phone": "+7 (3452) 28-36-60",
        "email": "general@tyuiu.ru",
        "documents": "Справка о болезни от врача (Форма 095/у)",
        "deadline": "В течение 3 дней после выздоровления",
        "officialSource": "https://tyuiu.ru/",
        "lastChecked": "25.09.2026"
    }
]

# 3. Кастомный CSS для тёмно-синего дизайна и крупных кнопок
st.markdown("""
    <style>
    /* Главный фон и шрифт */
    .stApp {
        background-color: #0A1128;
        color: #FFFFFF;
    }

    /* Шапка сайта */
    .header-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        color: #00D2FF;
        margin-bottom: 5px;
    }

    .header-subtitle {
        text-align: center;
        font-size: 1.05rem;
        color: #B0C4DE;
        margin-bottom: 25px;
    }

    /* Стилизация крупных кнопок на главной */
    div.stButton > button {
        width: 100%;
        height: 65px;
        background: linear-gradient(135deg, #1C274C 0%, #0052CC 100%);
        color: #FFFFFF;
        border: 1px solid #00D2FF44;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease-in-out;
        margin-bottom: 10px;
    }

    /* Эффект при наведении на кнопку */
    div.stButton > button:hover {
        background: linear-gradient(135deg, #0052CC 0%, #00D2FF 100%);
        border-color: #00D2FF;
        color: #FFFFFF;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 210, 255, 0.3);
    }

    /* Информационная карточка ответа */
    .detail-card {
        background-color: #1C274C;
        border-left: 4px solid #00D2FF;
        padding: 18px;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    
    .field-title {
        color: #00D2FF;
        font-weight: 700;
        font-size: 0.95rem;
        margin-top: 10px;
    }

    .field-value {
        color: #FFFFFF;
        font-size: 1rem;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Инициализация состояний навигации
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_q_id' not in st.session_state:
    st.session_state.selected_q_id = None


def set_page(page_name):
    st.session_state.page = page_name
    st.session_state.selected_q_id = None


def open_question(q_id):
    st.session_state.selected_q_id = q_id


def close_question():
    st.session_state.selected_q_id = None


# 4. Шапка сайта
st.markdown('<div class="header-title">🎓 ТИУ Навигатор</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Всё, что нужно студенту ТИУ — в одном месте.</div>', unsafe_allow_html=True)

# 5. Главная страница с 5 крупными кнопками
if st.session_state.page == 'main':
    st.write("### Выберите раздел:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Документы", use_container_width=True):
            set_page('docs')
            st.rerun()

        if st.button("🏠 Общежитие", use_container_width=True):
            set_page('dorm')
            st.rerun()

    with col2:
        if st.button("📚 Учёба", use_container_width=True):
            set_page('study')
            st.rerun()

        if st.button("💰 Стипендии", use_container_width=True):
            set_page('scholarship')
            st.rerun()

    if st.button("⚡ Что делать, если…", use_container_width=True):
        set_page('sos')
        st.rerun()

# 6. Внутренние страницы с поиском и карточками
else:
    # Конфигурация заголовков и подсказок для поиска
    page_configs = {
        'docs': ("📄 Раздел: Документы и справки", "🔍 Поиск по документам..."),
        'study': ("📚 Раздел: Учёба", "🔍 Что вас интересует в учёбе?"),
        'dorm': ("🏠 Раздел: Общежития", "🔍 Поиск по вопросам общежития..."),
        'scholarship': ("💰 Раздел: Стипендии и поддержка", "🔍 Найти информацию о стипендии..."),
        'sos': ("⚡ Что делать, если…", "🔍 Опишите вашу проблему...")
    }

    current_title, current_placeholder = page_configs.get(
        st.session_state.page, ("Раздел", "🔍 Поиск...")
    )

    # Кнопка «На главную»
    if st.button("⬅ На главную"):
        set_page('main')
        st.rerun()

    st.subheader(current_title)

    # Отображение детальной карточки выбранного вопроса
    if st.session_state.selected_q_id:
        selected_q = next((q for q in QUESTIONS_DATA if q['id'] == st.session_state.selected_q_id), None)
        if selected_q:
            if st.button("⬅ Назад к списку вопросов"):
                close_question()
                st.rerun()

            st.markdown(f"### {selected_q['question']}")

            st.markdown("""
                <div class="detail-card">
            """, unsafe_allow_html=True)

            st.markdown('<div class="field-title">📋 Что делать?</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="field-value">{selected_q["answer"]}</div>', unsafe_allow_html=True)

            if selected_q.get("department") and selected_q["department"] != "Информация уточняется":
                st.markdown('<div class="field-title">🏛 Куда обращаться</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{selected_q["department"]}</div>', unsafe_allow_html=True)

            if selected_q.get("address") and selected_q["address"] != "Информация уточняется":
                st.markdown('<div class="field-title">📍 Адрес</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{selected_q["address"]}</div>', unsafe_allow_html=True)

            if selected_q.get("office") and selected_q["office"] != "Информация уточняется":
                st.markdown('<div class="field-title">🚪 Кабинет</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{selected_q["office"]}</div>', unsafe_allow_html=True)

            if selected_q.get("phone") and selected_q["phone"] != "Информация уточняется":
                st.markdown('<div class="field-title">📞 Телефон</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{selected_q["phone"]}</div>', unsafe_allow_html=True)

            if selected_q.get("email") and selected_q["email"] != "Информация уточняется":
                st.markdown('<div class="field-title">✉️ Email</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{selected_q["email"]}</div>', unsafe_allow_html=True)

            if selected_q.get("documents") and selected_q["documents"] != "Информация уточняется":
                st.markdown('<div class="field-title">📄 Какие документы нужны</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{selected_q["documents"]}</div>', unsafe_allow_html=True)

            if selected_q.get("deadline") and selected_q["deadline"] != "Информация уточняется":
                st.markdown('<div class="field-title">⏱ Срок</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value">{selected_q["deadline"]}</div>', unsafe_allow_html=True)

            if selected_q.get("officialSource"):
                st.markdown('<div class="field-title">🔗 Официальный источник</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="field-value"><a href="{selected_q["officialSource"]}" target="_blank">{selected_q["officialSource"]}</a></div>', unsafe_allow_html=True)

            st.markdown(f'<div class="field-title">🔄 Последняя проверка: <span style="color:#FFFFFF; font-weight:normal;">{selected_q.get("lastChecked", "25.09.2026")}</span></div>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # Отображение списка вопросов с поиском
    else:
        # Поисковая строка для текущего раздела
        search_query = st.text_input("", placeholder=current_placeholder, key=f"search_{st.session_state.page}")

        # Фильтрация вопросов по текущему разделу
        category_questions = [q for q in QUESTIONS_DATA if q['category'] == st.session_state.page]

        # Фильтрация по тексту поискового запроса
        if search_query.strip():
            query_words = search_query.lower().split()
            filtered_questions = [
                q for q in category_questions
                if any(
                    word in q['question'].lower() or word in q['answer'].lower()
                    for word in query_words
                )
            ]
        else:
            filtered_questions = category_questions

        st.write("#### Популярные вопросы:")

        if filtered_questions:
            for q in filtered_questions:
                # Отображение каждой карточки как кликабельной кнопки
                if st.button(f"📌 {q['question']}", key=f"btn_{q['id']}", use_container_width=True):
                    open_question(q['id'])
                    st.rerun()
        else:
            st.info("Ничего не нашли. Попробуйте изменить запрос.")

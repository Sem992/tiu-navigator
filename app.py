import streamlit as st

# 1. Настройка страницы
st.set_page_config(
    page_title="ТИУ Навигатор",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Кастомный CSS для тёмно-синего дизайна и крупных кнопок
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

    /* Стилизация крупных кнопок */
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

    /* Карточка с вопросом/инструкцией */
    .question-card {
        background-color: #1C274C;
        border-left: 4px solid #00D2FF;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Инициализация состояния выбранной категории
if 'page' not in st.session_state:
    st.session_state.page = 'main'


def set_page(page_name):
    st.session_state.page = page_name


# 3. Шапка сайта (Заголовок и слоган)
st.markdown('<div class="header-title">🎓 ТИУ Навигатор</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Всё, что нужно студенту ТИУ — в одном месте.</div>', unsafe_allow_html=True)

# 4. Главная страница с 5 крупными кнопками
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

    # Крупная кнопка во всю ширину для главного раздела
    if st.button("⚡ Что делать, если…", use_container_width=True):
        set_page('sos')
        st.rerun()

# 5. Страницы с вопросами и сценариями

# --- ДОКУМЕНТЫ ---
elif st.session_state.page == 'docs':
    if st.button("⬅ На главную"):
        set_page('main')
        st.rerun()

    st.subheader("📄 Раздел: Документы и справки")

    with st.expander("Как получить справку об обучении?"):
        st.write("""
        1. Зайдите в личный кабинет студента ТИУ.
        2. Перейдите в раздел **Заказ справок**.
        3. Выберите нужный тип справки и укажите количество экземпляров.
        4. Заберите готовую справку в дирекции вашего института.
        """)
        st.caption("Официальный источник: Учебный отдел ТИУ | Обновлено: 25.09.2026")

    with st.expander("Как получить справку для военкомата (Форма №4)?"):
        st.write("Обратитесь во 2-й отдел ТИУ (Военно-учетный стол) с паспортом и приписным свидетельством.")

# --- УЧЁБА ---
elif st.session_state.page == 'study':
    if st.button("⬅ На главную"):
        set_page('main')
        st.rerun()

    st.subheader("📚 Раздел: Учёба")

    with st.expander("Где посмотреть расписание занятий?"):
        st.write("Расписание доступно на официальном портале ТИУ или в сервисе «ТИУ Расписание».")

    with st.expander("Что делать при академической задолженности (долгах)?"):
        st.write("Возьмите бегунок в дирекции института и согласуйте с преподавателем дату пересдачи.")

# --- ОБЩЕЖИТИЕ ---
elif st.session_state.page == 'dorm':
    if st.button("⬅ На главную"):
        set_page('main')
        st.rerun()

    st.subheader("🏠 Раздел: Общежития")

    with st.expander("Какие документы нужны для заселения?"):
        st.write("""
        * Паспорт + копия (первая страница и прописка)
        * Справка о прохождении флюорографии
        * Медицинская справка (форма 086/у)
        * 3 фотографии 3х4
        """)

# --- СТИПЕНДИИ ---
elif st.session_state.page == 'scholarship':
    if st.button("⬅ На главную"):
        set_page('main')
        st.rerun()

    st.subheader("💰 Раздел: Стипендии и поддержка")

    with st.expander("Как подать на повышенную государственную академическую стипендию (ПГАС)?"):
        st.write(
            "ПГАС назначается за достижения в учебной, научно-исследовательской, общественной, культурно-творческой и спортивной деятельности. Портфолио подается в начале семестра.")

# --- ЧТО ДЕЛАТЬ, ЕСЛИ... ---
elif st.session_state.page == 'sos':
    if st.button("⬅ На главную"):
        set_page('main')
        st.rerun()

    st.subheader("⚡ Что делать, если…")

    with st.expander("🚨 Потерял студенческий билет"):
        st.write("""
        1. Напишите заявление об утере в дирекции своего института.
        2. Оплатите пошлину за восстановление.
        3. Принесите фото 3х4 в дирекцию для оформления нового документа.
        """)

    with st.expander("🚨 Потерял пропуск в корпус / общежитие"):
        st.write("Обратитесь в бюро пропусков ТИУ для блокировки старой карты и выпуска дубликата.")

    with st.expander("🚨 Заболел и пропустил занятия"):
        st.write(
            "Обратитесь к врачу в день заболевания. Справку о болезни нужно сдать в дирекцию института течение 3 дней после выздоровления.")
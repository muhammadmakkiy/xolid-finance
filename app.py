import streamlit as st
import pandas as pd
from datetime import datetime

# Саҳифа созламалари
st.set_page_config(
    page_title="Xolid Finance",
    page_icon="💸",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- ПРЕМИУМ ДИЗАЙН ВА СТИЛЛАР ---
st.markdown("""
<style>
/* Умумий фон */
.main { background-color: #f1f5f9; color: #0f172a; }

/* Лого ва Сарлавҳа стили */
.logo-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 15px 0;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
.logo-img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #38bdf8;
    background-color: white;
}
.logo-text {
    color: #ffffff;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-top: 8px;
}

/* Касса қолдиқлари карточкалари */
.kassa-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 20px;
}
@media (max-width: 600px) {
    .kassa-grid { grid-template-columns: repeat(2, 1fr); }
}
.kassa-card {
    background: #ffffff;
    border: 2px solid #cbd5e1;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 2px 4px rgb(0 0 0 / 0.05);
}
.kassa-card .currency {
    font-size: 18px;
    font-weight: 800;
    color: #1e293b;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-bottom: 6px;
}
.kassa-card .value {
    font-size: 16px;
    font-weight: 700;
    color: #0284c7;
}

/* Горизонтал Жорий Курслар панели */
.rates-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    background: #ffffff;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    margin-bottom: 15px;
    justify-content: center;
}
.rate-item {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 6px 12px;
    border-radius: 6px;
    text-align: center;
    font-size: 12px;
}
.rate-item b { color: #0f172a; font-size: 14px; }

/* Excel Жадвал Элементлари Учун Стиллар */
.excel-cell-header {
    background-color: #e2e8f0;
    color: #1e293b;
    font-weight: bold;
    border: 1px solid #cbd5e1;
    padding: 8px;
    text-align: center;
    font-size: 13px;
}
.excel-cell-data {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    padding: 8px;
    text-align: center;
    font-size: 13px;
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# Логотип URL манзили
LOGO_URL = "https://sub-m.com/file/obmen.png" 

# Доимий кўриниб турувчи Логотип ва Сарлавҳа блоки
st.markdown(f"""
<div class="logo-container">
    <img src="{LOGO_URL}" class="logo-img" alt="Xolid Finance Logo">
    <div class="logo-text">XOLID FINANCE</div>
</div>
""", unsafe_allow_html=True)

# Валюталар рўйхати
ALL_CURRENCIES = ["KGS", "USD", "EUR", "RUB", "CNY", "KZT", "UZS", "MBANK"]

# --- СЕССИЯ МАЪЛУМОТЛАРИНИ ИНИЦИАЛИЗАЦИЯ ҚИЛИШ ---
if 'rates' not in st.session_state:
    st.session_state.rates = {
        "KGS": {"buy": 1.0, "sell": 1.0}, "USD": {"buy": 86.00, "sell": 86.80},
        "EUR": {"buy": 92.50, "sell": 93.50}, "RUB": {"buy": 0.94, "sell": 0.98},
        "CNY": {"buy": 11.70, "sell": 12.10}, "KZT": {"buy": 0.175, "sell": 0.185},
        "UZS": {"buy": 0.0064, "sell": 0.0069}, "MBANK": {"buy": 0.99, "sell": 1.01}
    }

if 'shops' not in st.session_state: st.session_state.shops = ["Дўстлик", "Наримон"]

if 'employees' not in st.session_state:
    st.session_state.employees = [
        {"Исм": "Одилжон", "Телефон": "+996558143464", "Пароль": "7777"},
        {"Исм": "Ҳузайфа", "Телефон": "+996553707490", "Пароль": "8888"}
    ]

# Айирбошлаш тарихи
if 'history' not in st.session_state: 
    st.session_state.history = [
        {"ID": 1, "Вақт": "2026-07-08 10:00", "Дўкон": "Дўстлик", "Ходим": "Одилжон", "Берилди": "USD", "Миқдор": 100.0, "Олинди": "KGS", "Берилган Миқдор": 8600.0, "Изоҳ": "Илк савдо"},
        {"ID": 2, "Вақт": "2026-07-09 05:36", "Дўкон": "Дўстлик", "Ходим": "Одилжон", "Берилди": "RUB", "Миқдор": 6000.0, "Олинди": "KGS", "Берилган Миқдор": 5640.0, "Изоҳ": ""},
        {"ID": 3, "Вақт": "2026-07-09 05:47", "Дўкон": "Дўстлик", "Ходим": "Одилжон", "Берилди": "KZT", "Миқдор": 250000.0, "Олинди": "KGS", "Берилган Миқдор": 43750.0, "Изоҳ": ""}
    ]

# Қарзлар базаси
if 'debts' not in st.session_state:
    st.session_state.debts = [
        {"ID": 1, "Кимга": "Алихон", "Валюта": "USD", "Сумма": 500.0, "Вақт": "2026-07-09 08:00", "Ҳолат": "Қарз берилди"}
    ]

# Харажатлар базаси
if 'expenses' not in st.session_state:
    st.session_state.expenses = [
        {"ID": 1, "Сабаб": "Обед учун", "Валюта": "KGS", "Сумма": 450.0, "Вақт": "2026-07-09 08:15"}
    ]

# Касса қолдиқлари
if 'kassa' not in st.session_state:
    st.session_state.kassa = {
        "KGS": 94360.0, "USD": 5000.0, "EUR": 5000.0, "RUB": 106000.0,
        "CNY": 5000.0, "KZT": 5000.0, "UZS": 100000.0, "MBANK": 5000.0
    }

MANAGERS = ["Муҳаммад Али"]
DIRECTORS = ["Муҳаммад Диёр"]

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'current_role' not in st.session_state: st.session_state.current_role = None
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'current_shop' not in st.session_state: st.session_state.current_shop = None
if 'sub_page' not in st.session_state: st.session_state.sub_page = "Меню"
if 'editing_report' not in st.session_state: st.session_state.editing_report = None

# ==================== АВТОРИЗАЦИЯ САҲИФАСИ ====================
if not st.session_state.authenticated:
    st.markdown("<h4 style='text-align:center;'>🔐 Тизимга кириш</h4>", unsafe_allow_html=True)
    auth_shop = st.selectbox("Дўкон:", st.session_state.shops)
    auth_role = st.selectbox("Рол:", ["Ходим", "Менежер", "Директор"])
    
    if auth_role == "Директор":
        auth_user = st.selectbox("Исм:", DIRECTORS)
        password = st.text_input("Парол:", type="password")
        if st.button("Кириш", use_container_width=True, type="primary"):
            if password == "1111":
                st.session_state.authenticated = True; st.session_state.current_role = auth_role
                st.session_state.current_user = auth_user; st.session_state.current_shop = auth_shop; st.rerun()
    elif auth_role == "Менежер":
        auth_user = st.selectbox("Исм:", MANAGERS)
        password = st.text_input("Парол:", type="password")
        if st.button("Кириш", use_container_width=True, type="primary"):
            if password == "2222":
                st.session_state.authenticated = True; st.session_state.current_role = auth_role
                st.session_state.current_user = auth_user; st.session_state.current_shop = auth_shop; st.rerun()
    else:
        emp_names = [e["Исм"] for e in st.session_state.employees]
        auth_user = st.selectbox("Исм:", emp_names)
        password = st.text_input("Парол:", type="password")
        if st.button("Кириш", use_container_width=True, type="primary"):
            emp_data = next(e for e in st.session_state.employees if e["Исм"] == auth_user)
            if password == emp_data["Пароль"]:
                st.session_state.authenticated = True; st.session_state.current_role = auth_role
                st.session_state.current_user = auth_user; st.session_state.current_shop = auth_shop; st.rerun()

# ==================== АСОСИЙ ИЛОВА ТИЗИМИ ====================
else:
    st.markdown(f"<p style='font-size:13px; text-align:center; color:#475569;'>📍 {st.session_state.current_shop} | 👤 {st.session_state.current_user} ({st.session_state.current_role})</p>", unsafe_allow_html=True)
    
    if st.button("🚪 Тизимдан чиқиш", type="secondary", use_container_width=True):
        st.session_state.authenticated = False; st.session_state.sub_page = "Меню"; st.rerun()
        
    st.markdown("---")

    # ---------------- АСОСИЙ МЕНЮ ----------------
    if st.session_state.sub_page == "Меню":
        if st.button("💸 Айирбошлаш (Обмен)", use_container_width=True, type="primary"):
            st.session_state.sub_page = "💸 Айирбошлаш"; st.rerun()
        if st.button("📋 Касса ва Ҳисоботлар", use_container_width=True):
            st.session_state.sub_page = "📋 Касса ва Ҳисоботлар"; st.rerun()
        if st.button("📕 Қарз Дафтари", use_container_width=True):
            st.session_state.sub_page = "📕 Қарз Дафтари"; st.rerun()
        if st.button("📉 Харажатлар", use_container_width=True):
            st.session_state.sub_page = "📉 Харажатлар"; st.rerun()
            
        if st.session_state.current_role in ["Менежер", "Директор"]:
            if st.button("⚙️ Курсларни Созлаш", use_container_width=True):
                st.session_state.sub_page = "⚙️ Курсларни Созлаш"; st.rerun()

    # ==================== БЎЛИМ 1: АЙИРБОШЛАШ ====================
    elif st.session_state.sub_page == "💸 Айирбошлаш":
        st.markdown("##### 📊 Жорий Валюта Курслари (Сотиш / Олиш)")
        
        rates_html = "<div class='rates-panel'>"
        for curr, val in st.session_state.rates.items():
            if curr != "KGS":
                rates_html += f"""
                <div class='rate-item'>
                    <b>{curr}</b><br>
                    <span style='color:green;'>Олиш: {val['buy']}</span><br>
                    <span style='color:red;'>Сотиш: {val['sell']}</span>
                </div>"""
        rates_html += "</div>"
        st.markdown(rates_html, unsafe_allow_html=True)

        st.write("📥 Мижоз берадиган (Кириш валюта):")
        cols_give = st.columns(len(ALL_CURRENCIES))
        if 'active_give' not in st.session_state: st.session_state.active_give = "USD"
        for idx, c in enumerate(ALL_CURRENCIES):
            b_type = "primary" if st.session_state.active_give == c else "secondary"
            if cols_give[idx].button(c, key=f"g_{c}", type=b_type, use_container_width=True):
                st.session_state.active_give = c; st.rerun()

        st.write("📤 Мижоз оладиган (Чиқиш валюта):")
        cols_get = st.columns(len(ALL_CURRENCIES))
        if 'active_get' not in st.session_state: st.session_state.active_get = "KGS"
        for idx, c in enumerate(ALL_CURRENCIES):
            b_type = "primary" if st.session_state.active_get == c else "secondary"
            if cols_get[idx].button(c, key=f"gt_{c}", type=b_type, use_container_width=True):
                st.session_state.active_get = c; st.rerun()

        g_curr = st.session_state.active_give
        get_curr = st.session_state.active_get

        if g_curr == get_curr:
            st.warning("⚠️ Илтимос, ҳар хил валюталарни танланг!")
        else:
            r_give = st.session_state.rates[g_curr]["buy"] if get_curr == "KGS" or g_curr != "KGS" else 1.0
            r_get = st.session_state.rates[get_curr]["sell"] if g_curr == "KGS" or get_curr != "KGS" else 1.0
            cross_rate = r_give / r_get
            
            st.info(f"ℹ️ Крос-Курс: 1 {g_curr} = {cross_rate:.4f} {get_curr}")
            
            comment = st.text_input("💬 Изоҳ / Телефон / Банк номи:")
            amount_give = st.number_input(f"💵 Суммани киритинг ({g_curr}):", min_value=0.0, value=100.0)
            total_get = amount_give * cross_rate
            
            st.success(f"🧮 Бериладиган сумма: {total_get:,.2f} {get_curr}")
            
            if st.button("🚀 Амалиётни Бажариш", type="primary", use_container_width=True):
                if st.session_state.kassa[get_curr] < total_get:
                    st.error("Кассада маблағ етарли эмас!")
                else:
                    st.session_state.kassa[g_curr] += amount_give
                    st.session_state.kassa[get_curr] -= total_get
                    st.session_state.history.append({
                        "ID": len(st.session_state.history) + 1, "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Дўкон": st.session_state.current_shop, "Ходим": st.session_state.current_user,
                        "Берилди": g_curr, "Миқдор": amount_give, "Олинди": get_curr, "Берилган Миқдор": total_get, "Изоҳ": comment
                    })
                    st.success("Амалиёт бажарилди ва базага ёзилди!")

    # ==================== БЎЛИМ 2: КАССА ВА ҲИСОБОТЛАР ====================
    elif st.session_state.sub_page == "📋 Касса ва Ҳисоботлар":
        st.markdown("##### 🪙 Касса Қолдиқлари (Excel Катакчаларида)")
        
        k_html = "<div class='kassa-grid'>"
        for c in ALL_CURRENCIES:
            k_html += f"""
            <div class='kassa-card'>
                <div class='currency'>{c}</div>
                <div class='value'>{st.session_state.kassa[c]:,.2f}</div>
            </div>"""
        k_html += "</div>"
        st.markdown(k_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### 📊 Сиз сўраган соддалаштирилган жадвал кўриниши")

        if st.session_state.history:
            # Устунлар ўлчами ва номланиши
            h_cols = st.columns([0.4, 1.4, 1.4, 1.3, 1.5])
            headers = ["☑️", "📥 Кириш Валюта", "📤 Чиқиш Валюта", "📅 Сана ва Вақт", "💬 Изоҳ"]
            for idx, text in enumerate(headers):
                h_cols[idx].markdown(f"<div class='excel-cell-header'>{text}</div>", unsafe_allow_html=True)

            selected_row = None

            # Тарих элементларини уланиб турган жадвал кўринишида чиқариш
            for rep in reversed(st.session_state.history):
                r_cols = st.columns([0.4, 1.4, 1.4, 1.3, 1.5])
                
                with r_cols[0]:
                    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
                    is_chosen = st.checkbox("", key=f"chk_grid_{rep['ID']}", label_visibility="collapsed")
                    if is_chosen:
                        selected_row = rep
                        
                r_cols[1].markdown(f"<div class='excel-cell-data' style='color:green; font-weight:bold;'>{rep['Миқдор']:,} {rep['Берилди']}</div>", unsafe_allow_html=True)
                r_cols[2].markdown(f"<div class='excel-cell-data' style='color:red; font-weight:bold;'>{rep['Берилган Миқдор']:,.1f} {rep['Олинди']}</div>", unsafe_allow_html=True)
                r_cols[3].markdown(f"<div class='excel-cell-data'>{rep['Вақт']}</div>", unsafe_allow_html=True)
                r_cols[4].markdown(f"<div class='excel-cell-data'>{rep['Изоҳ'] if rep['Изоҳ'] else '-'}</div>", unsafe_allow_html=True)

            # Галичка танланганда ҳаракатлар панели
            if selected_row:
                st.markdown(f"⚙️ **Танланди: Амалиёт ID {selected_row['ID']}**")
                c1, c2 = st.columns(2)
                
                if c1.button("🗑️ Базадан Ўчириш", type="primary", use_container_width=True):
                    st.session_state.kassa[selected_row["Берилди"]] -= selected_row["Миқдор"]
                    st.session_state.kassa[selected_row["Олинди"]] += selected_row["Берилган Миқдор"]
                    st.session_state.history.remove(selected_row)
                    st.success("Амалиёт ўчирилди ва касса қайта тикланди!")
                    st.rerun()
                    
                if c2.button("✏️ Сатрни Тўғрилаш", use_container_width=True):
                    st.session_state.editing_report = selected_row
                    st.rerun()

            # Тўғрилаш ойнаси
            if st.session_state.editing_report:
                st.markdown("---")
                st.markdown("##### 🛠️ Изоҳни ўзгартириш")
                ed_rep = st.session_state.editing_report
                new_comment = st.text_input("Янги маълумот киритинг:", value=ed_rep["Изоҳ"])
                if st.button("💾 Сақлаш", type="primary"):
                    for item in st.session_state.history:
                        if item["ID"] == ed_rep["ID"]:
                            item["Изоҳ"] = new_comment
                    st.session_state.editing_report = None
                    st.success("Ўзгариш сақланди!")
                    st.rerun()
        else:
            st.info("Ҳисоботлар базаси бўш.")

    # ==================== БЎЛИМ 3: ҚАРЗ ДАФТАРИ (ТЎЛИҚ ИШЛАЙДИ) ====================
    elif st.session_state.sub_page == "📕 Қарз Дафтари":
        st.markdown("##### 📕 Янги Қарз Ёзиш")
        d_name = st.text_input("👤 Кимга (Исми):")
        d_curr = st.selectbox("Валюта тури:", ALL_CURRENCIES, key="debt_c")
        d_amount = st.number_input("Сумма:", min_value=0.0, value=0.0)
        
        if st.button("➕ Қарзни Базага Қўшиш", type="primary", use_container_width=True):
            if d_name and d_amount > 0:
                if st.session_state.kassa[d_curr] >= d_amount:
                    st.session_state.kassa[d_curr] -= d_amount  # Кассадан чиқиб кетади
                    st.session_state.debts.append({
                        "ID": len(st.session_state.debts) + 1, "Кимга": d_name, "Валюта": d_curr,
                        "Сумма": d_amount, "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M"), "Ҳолат": "Берилди"
                    })
                    st.success("Қарз муваффақиятли ёзилди ва кассадан айирилди!")
                    st.rerun()
                else:
                    st.error("Кассада бунча маблағ йўқ!")
            else:
                st.warning("Илтимос, исм ва суммани тўғри киритинг!")

        st.markdown("---")
        st.markdown("##### 📜 Жорий Берлиган Қарзлар Рўйхати")
        if st.session_state.debts:
            for d in st.session_state.debts:
                st.markdown(f"👤 **{d['Кимга']}** | 💰 {d['Сумма']:,} {d['Валюта']} | 📅 {d['Вақт']} | Status: `{d['Ҳолат']}`")
                if st.button(f"✅ Қарз қайтди (Узилди) - ID {d['ID']}", key=f"pay_{d['ID']}"):
                    st.session_state.kassa[d['Валюта']] += d['Сумма']  # Кассага қайтади
                    st.session_state.debts.remove(d)
                    st.success("Қарз узилди ва кассага қайта қўшилди!")
                    st.rerun()
        else:
            st.info("Ҳозирча фаол қарзлар йўқ.")

    # ==================== БЎЛИМ 4: ХАРАЖАТЛАР (ТЎЛИҚ ИШЛАЙДИ) ====================
    elif st.session_state.sub_page == "📉 Харажатлар":
        st.markdown("##### 📉 Янги Чиқим / Харажат Қўшиш")
        ex_reason = st.text_input("💬 Харажат мақсади (Масалан: Обед, Аренда, Свет):")
        ex_curr = st.selectbox("Қайси валютадан тўланади:", ALL_CURRENCIES, key="ex_c")
        ex_amount = st.number_input("Харажат суммаси:", min_value=0.0, value=0.0)
        
        if st.button("📉 Харажатни Тасдиқлаш", type="primary", use_container_width=True):
            if ex_reason and ex_amount > 0:
                if st.session_state.kassa[ex_curr] >= ex_amount:
                    st.session_state.kassa[ex_curr] -= ex_amount  # Кассадан чиқиб кетади
                    st.session_state.expenses.append({
                        "ID": len(st.session_state.expenses) + 1, "Сабаб": ex_reason,
                        "Валюта": ex_curr, "Сумма": ex_amount, "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("Харажат базага қўшилди ва кассадан чиқим қилинди!")
                    st.rerun()
                else:
                    st.error("Кассада етарли маблағ мавжуд эмас!")
            else:
                st.warning("Маълумотларни тўлиқ тўлдиринг!")

        st.markdown("---")
        st.markdown("##### 📋 Бугунги Харажатлар Рўйхати")
        if st.session_state.expenses:
            for ex in st.session_state.expenses:
                st.markdown(f"❌ **{ex['Сабаб']}** uchun: -{ex['Сумма']:,} {ex['Валюта']} | 📅 {ex['Вақт']}")
        else:
            st.info("Бугун ҳали харажатлар киритилмади.")

    # ==================== БЎЛИМ 5: КУРСЛАРНИ СОЗЛАШ ====================
    elif st.session_state.sub_page == "⚙️ Курсларни Созлаш":
        st.markdown("##### 🛠️ Курсларни янгилаш")
        for curr in ALL_CURRENCIES:
            if curr != "KGS":
                st.write(f"**{curr}**")
                st.session_state.rates[curr]["buy"] = st.number_input(f"{curr} Олиш:", value=st.session_state.rates[curr]["buy"], key=f"b_{curr}")
                st.session_state.rates[curr]["sell"] = st.number_input(f"{curr} Сотиш:", value=st.session_state.rates[curr]["sell"], key=f"s_{curr}")
        if st.button("Сақлаш", type="primary", use_container_width=True):
            st.success("Курслар тизимда янгиланди!")

    # ---------------- ОРҚАГА ҚАЙТИШ ТУГМАСИ ----------------
    if st.session_state.sub_page != "Меню":
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ Асосий Менюга Қайтиш", type="secondary", use_container_width=True):
            st.session_state.sub_page = "Меню"
            st.session_state.editing_report = None
            st.rerun()
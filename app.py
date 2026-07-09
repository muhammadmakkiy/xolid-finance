import streamlit as st
import pandas as pd
from datetime import datetime

# Саҳифа созламалари
st.set_page_config(
    page_title="Xolid Finance",
    page_icon="👑",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- ЭСКИ СЕССИЯ ХАТОЛИКЛАРИНИ ТОЗАЛАШ ВА ҚАЙТА ЮКЛАШ ---
if 'debts' in st.session_state:
    # Агар эски хатолик билан ёзилган маълумот бўлса, тозалаб юборамиз
    for debt in st.session_state.debts:
        if 'Сумma' in debt:
            debt['Сумма'] = debt.pop('Сумma')

# --- ЕНГИЛ ВА ҲАШАМАТЛИ ДИЗАЙН (ОҚ, ОСМОН ВА ТИЛЛА РАНГ) ---
st.markdown("""
<style>
/* Умумий енгил фон */
.main { background-color: #f4f9fc; color: #1e293b; }

/* Премиум Сарлавҳа блоки */
.logo-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 25px 0;
    background: linear-gradient(135deg, #ffffff, #e0f2fe);
    border-radius: 20px;
    margin-bottom: 25px;
    border: 2px solid #d97706; /* Тилла ранг чегара */
    box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.15);
}
.logo-img {
    width: 95px;
    height: 95px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #d97706; /* Тилла ранг */
    background-color: white;
    box-shadow: 0 4px 12px rgba(217, 119, 6, 0.35);
}
.logo-text {
    color: #0284c7; /* Осмон ранг */
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 2.5px;
    margin-top: 12px;
    text-shadow: 1px 1px 2px rgba(217, 119, 6, 0.1);
}

/* Касса қолдиқлари карточкалари */
.kassa-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 25px;
}
@media (max-width: 600px) {
    .kassa-grid { grid-template-columns: repeat(2, 1fr); }
}
.kassa-card {
    background: #ffffff;
    border: 1px solid #bae6fd;
    border-bottom: 4px solid #d97706; /* Тилла ранг пастки чизиқ */
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.kassa-card .currency {
    font-size: 16px;
    font-weight: 800;
    color: #0369a1;
    padding-bottom: 4px;
    margin-bottom: 6px;
}
.kassa-card .value {
    font-size: 15px;
    font-weight: 700;
    color: #b45309;
}

/* Курслар панели */
.rates-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    background: #ffffff;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #bae6fd;
    margin-bottom: 20px;
    justify-content: center;
}
.rate-item {
    background: #f0f9ff;
    border: 1px solid #e0f2fe;
    padding: 8px 14px;
    border-radius: 8px;
    text-align: center;
    font-size: 12px;
}
.rate-item b { color: #0369a1; font-size: 14px; }

/* Excel уланиб турган катакчалар */
.excel-cell-header {
    background-color: #e0f2fe;
    color: #0369a1;
    font-weight: bold;
    border: 1px solid #bae6fd;
    padding: 10px;
    text-align: center;
    font-size: 13px;
}
.excel-cell-data {
    background-color: #ffffff;
    border: 1px solid #e0f2fe;
    padding: 10px;
    text-align: center;
    font-size: 13px;
    min-height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Тугмалар */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s;
}
</style>
""", unsafe_allow_html=True)

# Янги Танланган Жуда Премиум ва Ҳашаматли Логотип (Олтин Тож ва Молия тимсоли)
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/2984/2984134.png" 

# Сарлавҳа блоки
st.markdown(f"""
<div class="logo-container">
    <img src="{LOGO_URL}" class="logo-img" alt="Premium Gold Logo">
    <div class="logo-text">XOLID FINANCE</div>
</div>
""", unsafe_allow_html=True)

# Валюталар
ALL_CURRENCIES = ["KGS", "USD", "EUR", "RUB", "CNY", "KZT", "UZS", "MBANK"]

# --- БАЗА ВА СЕССИЯЛАР ---
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

if 'history' not in st.session_state: 
    st.session_state.history = [
        {"ID": 1, "Вақт": "2026-07-08 10:00", "Берилди": "USD", "Миқдор": 100.0, "Олинди": "KGS", "Берилган Миқдор": 8600.0, "Изоҳ": "Илк савдо"},
        {"ID": 2, "Вақт": "2026-07-09 05:36", "Берилди": "RUB", "Миқдор": 6000.0, "Олинди": "KGS", "Берилган Миқдор": 5640.0, "Изоҳ": ""},
        {"ID": 3, "Вақт": "2026-07-09 05:47", "Берилди": "KZT", "Миқдор": 250000.0, "Олинди": "KGS", "Берилган Миқдор": 43750.0, "Изоҳ": ""}
    ]

if 'debts' not in st.session_state: st.session_state.debts = []
if 'expenses' not in st.session_state: st.session_state.expenses = []

if 'kassa' not in st.session_state:
    st.session_state.kassa = {
        "KGS": 94360.0, "USD": 5000.0, "EUR": 5000.0, "RUB": 106000.0,
        "CNY": 5000.0, "KZT": 5000.0, "UZS": 100000.0, "MBANK": 5000.0
    }

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'sub_page' not in st.session_state: st.session_state.sub_page = "Меню"
if 'editing_report' not in st.session_state: st.session_state.editing_report = None

# --- АВТОРИЗАЦИЯ ---
if not st.session_state.authenticated:
    st.markdown("<h4 style='text-align:center;'>🔐 Кириш</h4>", unsafe_allow_html=True)
    auth_user = st.selectbox("Ходим:", [e["Исм"] for e in st.session_state.employees])
    password = st.text_input("Парол:", type="password")
    if st.button("Тизимга Кириш", use_container_width=True, type="primary"):
        emp_data = next(e for e in st.session_state.employees if e["Исм"] == auth_user)
        if password == emp_data["Пароль"]:
            st.session_state.authenticated = True; st.session_state.sub_page = "Меню"; st.rerun()
else:
    # --- АСОСИЙ МЕНЮ ---
    if st.session_state.sub_page == "Меню":
        c1, c2 = st.columns(2)
        if c1.button("💸 Айирбошлаш (Обмен)", use_container_width=True, type="primary"):
            st.session_state.sub_page = "💸 Айирбошлаш"; st.rerun()
        if c2.button("📋 Касса ва Ҳисоботлар", use_container_width=True):
            st.session_state.sub_page = "📋 Касса ва Ҳисоботлар"; st.rerun()
        
        c3, c4 = st.columns(2)
        if c3.button("📕 Қарз Дафтари", use_container_width=True):
            st.session_state.sub_page = "📕 Қарз Дафтари"; st.rerun()
        if c4.button("📉 Харажатлар", use_container_width=True):
            st.session_state.sub_page = "📉 Харажатлар"; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Чиқиш", type="secondary", use_container_width=True):
            st.session_state.authenticated = False; st.rerun()

    # ==================== БЎЛИМ 1: АЙИРБОШЛАШ ====================
    elif st.session_state.sub_page == "💸 Айирбошлаш":
        st.markdown("##### 📊 Валюта Курслари")
        rates_html = "<div class='rates-panel'>"
        for curr, val in st.session_state.rates.items():
            if curr != "KGS":
                rates_html += f"<div class='rate-item'><b>{curr}</b><br><span style='color:green;'>Олиш: {val['buy']}</span><br><span style='color:red;'>Сотиш: {val['sell']}</span></div>"
        rates_html += "</div>"
        st.markdown(rates_html, unsafe_allow_html=True)

        st.write("📥 Мижоз берадиган:")
        cols_give = st.columns(len(ALL_CURRENCIES))
        if 'active_give' not in st.session_state: st.session_state.active_give = "USD"
        for idx, c in enumerate(ALL_CURRENCIES):
            if cols_give[idx].button(c, key=f"g_{c}", type="primary" if st.session_state.active_give == c else "secondary", use_container_width=True):
                st.session_state.active_give = c; st.rerun()

        st.write("📤 Мижоз оладиган:")
        cols_get = st.columns(len(ALL_CURRENCIES))
        if 'active_get' not in st.session_state: st.session_state.active_get = "KGS"
        for idx, c in enumerate(ALL_CURRENCIES):
            if cols_get[idx].button(c, key=f"gt_{c}", type="primary" if st.session_state.active_get == c else "secondary", use_container_width=True):
                st.session_state.active_get = c; st.rerun()

        g_curr = st.session_state.active_give
        get_curr = st.session_state.active_get

        if g_curr == get_curr:
            st.warning("⚠️ Илтимос, ҳар хил валюталарни танланг!")
        else:
            r_give = st.session_state.rates[g_curr]["buy"] if get_curr == "KGS" or g_curr != "KGS" else 1.0
            r_get = st.session_state.rates[get_curr]["sell"] if g_curr == "KGS" or get_curr != "KGS" else 1.0
            cross_rate = r_give / r_get
            
            amount_give = st.number_input(f"💵 Суммани киритинг ({g_curr}):", min_value=0.0, value=100.0)
            total_get = amount_give * cross_rate
            st.success(f"🧮 Бериладиган сумма: {total_get:,.2f} {get_curr} (Курс: {cross_rate:.4f})")
            
            comment = st.text_input("💬 Изоҳ киритинг:")
            
            if st.button("🚀 Амалиётни Бажариш", type="primary", use_container_width=True):
                if st.session_state.kassa[get_curr] < total_get:
                    st.error("Кассада маблағ етарли эмас!")
                else:
                    st.session_state.kassa[g_curr] += amount_give
                    st.session_state.kassa[get_curr] -= total_get
                    st.session_state.history.append({
                        "ID": len(st.session_state.history) + 1, "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Берилди": g_curr, "Миқдор": amount_give, "Олинди": get_curr, "Берилган Миқдор": total_get, "Изоҳ": comment
                    })
                    st.success("Муваффақиятли бажарилди!")
                    st.rerun()

    # ==================== БЎЛИМ 2: КАССА ВА ҲИСОБОТЛАР ====================
    elif st.session_state.sub_page == "📋 Касса ва Ҳисоботлар":
        st.markdown("##### 🪙 Касса Қолдиқлари")
        k_html = "<div class='kassa-grid'>"
        for c in ALL_CURRENCIES:
            k_html += f"<div class='kassa-card'><div class='currency'>{c}</div><div class='value'>{st.session_state.kassa[c]:,.2f}</div></div>"
        k_html += "</div>"
        st.markdown(k_html, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### 📊 Ҳисоботлар Жадвали")

        if st.session_state.history:
            h_cols = st.columns([0.4, 1.4, 1.4, 1.3, 1.5])
            headers = ["☑️", "📥 Кириш Валюта", "📤 Чиқиш Валюта", "📅 Сана ва Вақт", "💬 Изоҳ"]
            for idx, text in enumerate(headers):
                h_cols[idx].markdown(f"<div class='excel-cell-header'>{text}</div>", unsafe_allow_html=True)

            selected_row = None
            for rep in reversed(st.session_state.history):
                r_cols = st.columns([0.4, 1.4, 1.4, 1.3, 1.5])
                with r_cols[0]:
                    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
                    is_chosen = st.checkbox("", key=f"chk_grid_{rep['ID']}", label_visibility="collapsed")
                    if is_chosen: selected_row = rep
                        
                r_cols[1].markdown(f"<div class='excel-cell-data' style='color:green; font-weight:bold;'>{rep['Миқдор']:,} {rep['Берилди']}</div>", unsafe_allow_html=True)
                r_cols[2].markdown(f"<div class='excel-cell-data' style='color:red; font-weight:bold;'>{rep['Берилган Миқдор']:,.1f} {rep['Олинди']}</div>", unsafe_allow_html=True)
                r_cols[3].markdown(f"<div class='excel-cell-data'>{rep['Вақт']}</div>", unsafe_allow_html=True)
                r_cols[4].markdown(f"<div class='excel-cell-data'>{rep['Изоҳ'] if rep['Изоҳ'] else '-'}</div>", unsafe_allow_html=True)

            if selected_row:
                st.markdown(f"⚙️ **Танланди: ID {selected_row['ID']}**")
                c1, c2 = st.columns(2)
                if c1.button("🗑️ Ўчириш", type="primary", use_container_width=True):
                    st.session_state.kassa[selected_row["Берилди"]] -= selected_row["Миқдор"]
                    st.session_state.kassa[selected_row["Олинди"]] += selected_row["Берилган Миқдор"]
                    st.session_state.history.remove(selected_row)
                    st.success("Ўчирилди!")
                    st.rerun()
                if c2.button("✏️ Тўғрилаш", use_container_width=True):
                    st.session_state.editing_report = selected_row
                    st.rerun()

            if st.session_state.editing_report:
                ed_rep = st.session_state.editing_report
                new_comment = st.text_input("Янги изоҳ:", value=ed_rep["Изоҳ"])
                if st.button("💾 Сақлаш"):
                    for item in st.session_state.history:
                        if item["ID"] == ed_rep["ID"]: item["Изоҳ"] = new_comment
                    st.session_state.editing_report = None
                    st.success("Сақланди!")
                    st.rerun()
        else:
            st.info("База бўш.")

    # ==================== БЎЛИМ 3: ҚАРЗ ДАФТАРИ (ХАТОЛИК БУТУНЛАЙ ТУЗАТИЛДИ) ====================
    elif st.session_state.sub_page == "📕 Қарз Дафтари":
        st.markdown("##### 📕 Янги Қарз Қўшиш")
        d_name = st.text_input("👤 Мижоз исми:", key="debt_name_input")
        d_phone = st.text_input("📞 Телефон рақами:", key="debt_phone_input")
        d_curr = st.selectbox("Валюта:", ALL_CURRENCIES, key="debt_curr_select")
        d_amount = st.number_input("Сумма:", min_value=0.0, value=0.0, key="debt_amount_input")
        
        if st.button("➕ Қарзни Рўйхатга Олиш", type="primary", use_container_width=True):
            if d_name and d_amount > 0:
                if st.session_state.kassa[d_curr] >= d_amount:
                    st.session_state.kassa[d_curr] -= d_amount  
                    st.session_state.debts.append({
                        "ID": len(st.session_state.debts) + 1, 
                        "Исм": d_name, 
                        "Тел": d_phone,
                        "Валюта": d_curr, 
                        "Сумма": d_amount, # Калит фақат тўғри форматда сақланади
                        "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("Қарз муваффақиятли ёзилди!")
                    st.rerun()
                else:
                    st.error("Кассада маблағ етарли эмас!")
            else:
                st.warning("Маълумотларни тўлиқ киритинг!")

        st.markdown("---")
        st.markdown("##### 📜 Берилган Қарзлар")
        if st.session_state.debts:
            for d in list(st.session_state.debts):
                # Эски хатолик қолдиқларидан ҳимоя қилиш
                debt_sum = d.get('Сумма', d.get('Сумma', 0.0))
                
                st.info(f"👤 {d.get('Исм','-')} ({d.get('Тел','-')}) | 💰 {debt_sum:,} {d.get('Валюта','KGS')} | 📅 {d.get('Вақт','-')}")
                
                if st.button(f"✅ Қарз қайтди - ID {d['ID']}", key=f"pay_{d['ID']}"):
                    st.session_state.kassa[d['Валюта']] += debt_sum 
                    st.session_state.debts.remove(d)
                    st.success("Қарз ёпилди ва маблағ кассага қайтди!")
                    st.rerun()
        else:
            st.info("Фаол қарздорлар йўқ.")

    # ==================== БЎЛИМ 4: ХАРАЖАТЛАР ====================
    elif st.session_state.sub_page == "📉 Харажатлар":
        st.markdown("##### 📉 Янги Харажат Киритиш")
        ex_reason = st.text_input("💬 Харажат мақсади / Сабаби:")
        ex_curr = st.selectbox("Валюта:", ALL_CURRENCIES, key="ex_curr_box")
        ex_amount = st.number_input("Сумма:", min_value=0.0, value=0.0)
        
        if st.button("📉 Харажатни Тасдиқлаш", type="primary", use_container_width=True):
            if ex_reason and ex_amount > 0:
                if st.session_state.kassa[ex_curr] >= ex_amount:
                    st.session_state.kassa[ex_curr] -= ex_amount  
                    st.session_state.expenses.append({
                        "ID": len(st.session_state.expenses) + 1, "Сабаб": ex_reason,
                        "Валюта": ex_curr, "Сумма": ex_amount, "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("Харажат кассадан чиқарилди!")
                    st.rerun()
                else:
                    st.error("Кассада етарли маблағ йўқ!")
            else:
                st.warning("Маълумотларни тўлдиринг!")

        st.markdown("---")
        st.markdown("##### 📋 Харажатлар Тарихи")
        if st.session_state.expenses:
            for ex in st.session_state.expenses:
                st.error(f"❌ {ex['Сабаб']} | -{ex['Сумма']:,} {ex['Валюта']} | 📅 {ex['Вақт']}")
        else:
            st.info("Харажатлар мавжуд эмас.")

    # --- ОРҚАГА ҚАЙТИШ ТУГМАСИ ---
    if st.session_state.sub_page != "Меню":
        st.markdown("<br><hr>", unsafe_allow_html=True)
        if st.button("⬅️ Асосий Менюга Қайтиш", type="secondary", use_container_width=True):
            st.session_state.sub_page = "Меню"
            st.session_state.editing_report = None
            st.rerun()
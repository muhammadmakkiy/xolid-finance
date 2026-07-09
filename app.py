import streamlit as st
import pandas as pd
from datetime import datetime

# Саҳифа созламалари
st.set_page_config(
    page_title="Холид Финанс Обмен валюта",
    page_icon="💸",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Замонавий Премиум Дизайн ва СТИЛЛАР
st.markdown("""
<style>
.main { background-color: #f8fafc; color: #0f172a; }

/* Экран кенглиги бўйича тугмалар учун контейнер */
.stButton > button {
    border-radius: 6px;
}

/* Excel типидаги ихчам жадвал стиллари */
.excel-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 13px;
    background: #ffffff;
}
.excel-table th {
    background-color: #f1f5f9;
    color: #334155;
    font-weight: bold;
    border: 1px solid #cbd5e1;
    padding: 6px;
    text-align: center;
}
.excel-table td {
    border: 1px solid #e2e8f0;
    padding: 6px;
    text-align: center;
}
.excel-table tr:hover {
    background-color: #f8fafc;
}

.app-title {
    text-align: center; margin-bottom: 15px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;
}
.app-title h2 {
    margin: 0; font-size: 22px; color: #0f172a; font-weight: 900; letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# Инглизча пул бирликлари
ALL_CURRENCIES = ["KGS", "USD", "EUR", "RUB", "CNY", "KZT", "UZS", "MBANK"]

# --- СЕССИЯ МАЪЛУМОТЛАРИНИ ИНИЦИАЛИЗАЦИЯ ҚИЛИШ ---
if 'rates' not in st.session_state:
    st.session_state.rates = {
        "KGS": {"buy": 1.0, "sell": 1.0}, "USD": {"buy": 86.00, "sell": 86.80},
        "EUR": {"buy": 92.50, "sell": 93.50}, "RUB": {"buy": 0.94, "sell": 0.98},
        "CNY": {"buy": 11.70, "sell": 12.10}, "KZT": {"buy": 0.175, "sell": 0.185},
        "UZS": {"buy": 0.0064, "sell": 0.0069}, "MBANK": {"buy": 0.99, "sell": 1.01}
    }

if 'shops' not in st.session_state:
    st.session_state.shops = ["Дўстлик", "Наримон"]

if 'employees' not in st.session_state:
    st.session_state.employees = [
        {"Исм": "Одилжон", "Телефон": "+996558143464", "Gmail": "odiljon@gmail.com", "Паспорт": "АН1234567", "Пароль": "7777"},
        {"Исм": "Ҳузайфа", "Телефон": "+996553707490", "Gmail": "huzaifa@gmail.com", "Паспорт": "АН7654321", "Пароль": "8888"}
    ]

if 'history' not in st.session_state: 
    st.session_state.history = [
        {"ID": 1, "Вақт": "2026-07-08 10:00:00", "Дўкон": "Дўстлик", "Ходим": "Одилжон", "Берилди": "USD", "Миқдор": 100.0, "Олинди": "KGS", "Берилган Миқдор": 8600.0, "Изоҳ": "Илк савдо"}
    ]
if 'expenses' not in st.session_state: st.session_state.expenses = []
if 'kassa' not in st.session_state:
    st.session_state.kassa = {c: 100000.0 if c in ["KGS", "RUB", "UZS"] else 5000.0 for c in ALL_CURRENCIES}

if 'debts' not in st.session_state: 
    st.session_state.debts = [
        {"ID": 1, "Сана": "2026-07-08 11:00", "Исм": "Алишер", "Телефон": "+996772112233", "Валюта": "USD", "Аслий Қарз": 500.0, "Қолдиқ Қарз": 300.0, "Ҳолат": "Тўланмаган"}
    ]

# Ходим ва роллар рўйхати (Исмлар чиқиши учун созланди)
MANAGERS = ["Муҳаммад Али"]
DIRECTORS = ["Муҳаммад Диёр"]

# Саҳифа бошқаруви
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'current_role' not in st.session_state: st.session_state.current_role = None
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'current_shop' not in st.session_state: st.session_state.current_shop = None
if 'sub_page' not in st.session_state: st.session_state.sub_page = "Меню"

# Юқори сарлавҳа
st.markdown('<div class="app-title"><h2>ХОЛИД ФИНАНС</h2></div>', unsafe_allow_html=True)

# ==================== БОСҚИЧ 1: АВТОРИЗАЦИЯ САҲИФАСИ ====================
if not st.session_state.authenticated:
    st.markdown("<h3 style='text-align:center; font-size:18px;'>🔐 Тизимга кириш</h3>", unsafe_allow_html=True)
    
    auth_shop = st.selectbox("Дўконни танланг:", st.session_state.shops if st.session_state.shops else ["Филиал йўқ"])
    auth_role = st.selectbox("Сизнинг ролингиз:", ["Ходим", "Менежер", "Директор"])
    
    # Тўғриланган қисм: Исмларни танлаш имконияти қўшилди
    if auth_role == "Директор":
        auth_user = st.selectbox("Исмингиз:", DIRECTORS)
        password = st.text_input("Паролни киритинг:", type="password")
        if st.button("Кириш", use_container_width=True, type="primary"):
            if password == "1111":
                st.session_state.authenticated = True
                st.session_state.current_role = auth_role
                st.session_state.current_user = auth_user
                st.session_state.current_shop = auth_shop
                st.rerun()
            else: st.error("Хато парол!")
                
    elif auth_role == "Менежер":
        auth_user = st.selectbox("Исмингиз:", MANAGERS)
        password = st.text_input("Паролни киритинг:", type="password")
        if st.button("Кириш", use_container_width=True, type="primary"):
            if password == "2222":
                st.session_state.authenticated = True
                st.session_state.current_role = auth_role
                st.session_state.current_user = auth_user
                st.session_state.current_shop = auth_shop
                st.rerun()
            else: st.error("Хато парол!")
                
    else: # Ходим
        emp_names = [e["Исм"] for e in st.session_state.employees] if st.session_state.employees else ["Ходим мавжуд эмас"]
        auth_user = st.selectbox("Исмингиз:", emp_names)
        password = st.text_input("Паролни киритинг:", type="password")
        
        if st.button("Кириш", use_container_width=True, type="primary"):
            if st.session_state.employees and auth_user != "Ходим мавжуд эмас":
                emp_data = next(e for e in st.session_state.employees if e["Исм"] == auth_user)
                if password == emp_data.get("Пароль", ""):
                    st.session_state.authenticated = True
                    st.session_state.current_role = auth_role
                    st.session_state.current_user = auth_user
                    st.session_state.current_shop = auth_shop
                    st.rerun()
                else: st.error("Хато парол!")
            else: st.error("Тизимда ходим мавжуд эмас!")

# ==================== БОСҚИЧ 2: АСОСИЙ ИЛОВА ТИЗИМИ ====================
else:
    st.markdown(f"<p style='font-size:12px; text-align:center; color:#64748b;'>📍 Нуқта: {st.session_state.current_shop} | 👤 {st.session_state.current_user} ({st.session_state.current_role})</p>", unsafe_allow_html=True)
    
    if st.button("🚪 Тизимдан чиқиш", type="secondary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.sub_page = "Меню"
        st.rerun()
        
    st.markdown("---")

    # ---------------- САҲИФА: АСОСИЙ МЕНЮ ----------------
    if st.session_state.sub_page == "Меню":
        st.markdown("<h4 style='text-align:center; margin-bottom:10px;'>🖥️ Асосий Меню</h4>", unsafe_allow_html=True)
        
        if st.button("💸 Айирбошлаш", use_container_width=True, type="primary"):
            st.session_state.sub_page = "💸 Айирбошлаш"; st.rerun()
        if st.button("📋 Касса ва Ҳисоботлар", use_container_width=True):
            st.session_state.sub_page = "📋 Касса ва Ҳисоботлар"; st.rerun()
        if st.button("📕 Қарз Дафтари", use_container_width=True):
            st.session_state.sub_page = "📕 Қарз Дафтари"; st.rerun()
        if st.button("📉 Харажатлар", use_container_width=True):
            st.session_state.sub_page = "📉 Харажатлар"; st.rerun()
            
        if st.session_state.current_role in ["Менежер", "Директор"]:
            if st.button("⚙️ Курсларна Созлаш", use_container_width=True):
                st.session_state.sub_page = "⚙️ Курсларна Созлаш"; st.rerun()
            if st.button("🏢 Дўконларни Бошқариш", use_container_width=True):
                st.session_state.sub_page = "🏢 Дўконларни Бошқариш"; st.rerun()
            if st.button("👤 Ходимларни Бошқариш", use_container_width=True):
                st.session_state.sub_page = "👤 Ходимларни Бошқариш"; st.rerun()

    # ==================== БОЛИМ 1: АЙИРБОШЛАШ ====================
    if st.session_state.sub_page == "💸 Айирбошлаш":
        st.markdown("##### 📈 Жорий Курслар ва Тезкор Танлов")
        
        # 1. Кириш валютаси учун горизонталь тугмалар
        st.write("📥 Мижоз берадиган (Кириш):")
        cols_give = st.columns(len(ALL_CURRENCIES))
        if 'active_give' not in st.session_state: st.session_state.active_give = "USD"
        for idx, c in enumerate(ALL_CURRENCIES):
            btn_type = "primary" if st.session_state.active_give == c else "secondary"
            if cols_give[idx].button(c, key=f"btn_g_{c}", type=btn_type, use_container_width=True):
                st.session_state.active_give = c
                st.rerun()

        # 2. Чиқиш валютаси учун горизонталь тугмалар
        st.write("📤 Мижоз оладиган (Чиқиш):")
        cols_get = st.columns(len(ALL_CURRENCIES))
        if 'active_get' not in st.session_state: st.session_state.active_get = "KGS"
        for idx, c in enumerate(ALL_CURRENCIES):
            btn_type = "primary" if st.session_state.active_get == c else "secondary"
            if cols_get[idx].button(c, key=f"btn_gt_{c}", type=btn_type, use_container_width=True):
                st.session_state.active_get = c
                st.rerun()

        # Ҳисоблаш мантиқи
        g_curr = st.session_state.active_give
        get_curr = st.session_state.active_get

        if g_curr == get_curr:
            st.warning("⚠️ Илтимос, ҳар хил валюталарни танланг!")
        else:
            r_give = st.session_state.rates[g_curr]["buy"] if get_curr == "KGS" or g_curr != "KGS" else 1.0
            r_get = st.session_state.rates[get_curr]["sell"] if g_curr == "KGS" or get_curr != "KGS" else 1.0
            cross_rate = r_give / r_get
            
            st.info(f"ℹ️ Жорий курс: 1 {g_curr} = {cross_rate:.4f} {get_curr}")
            
            comment = st.text_input("💬 Изоҳ / Телефон / MBANK:")
            amount_give = st.number_input(f"💵 Мижоздан олинган маблағ ({g_curr}):", min_value=0.0, value=100.0)
            total_get = amount_give * cross_rate
            
            st.success(f"🧮 Мижозга бериладиган сумма: {total_get:,.2f} {get_curr}")
            
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
                    st.toast("Муваффақиятли бажарилди!", icon="✅")

    # ==================== БОЛИМ 2: КАССА ВА ҲИСОБОТЛАР ====================
    elif st.session_state.sub_page == "📋 Касса ва Ҳисоботлар":
        st.markdown("##### 💰 Касса Қолдиқлари")
        k_cols = st.columns(4)
        for idx, c in enumerate(ALL_CURRENCIES):
            k_cols[idx % 4].metric(label=c, value=f"{st.session_state.kassa[c]:,.2f}")

        st.markdown("---")
        st.markdown("##### 📝 Ҳисоботлар рўйхати (Excel кўринишида)")
        
        if st.session_state.history:
            # Танланган қаторларни бошқариш учун сессия
            selected_reports = []
            
            # HTML Жадвал Сарлавҳаси
            table_html = """<table class='excel-table'>
            <tr><th>☑️</th><th>ID</th><th>Вақт</th><th>Ходим</th><th>Кириш</th><th>Чиқиш</th><th>Изоҳ</th></tr>"""
            
            for rep in reversed(st.session_state.history):
                # Ҳар бир қатор учун уникал чекбокс (галичка) яратамиз
                ch_box = st.checkbox("", key=f"rep_chk_{rep['ID']}", label_visibility="collapsed")
                if ch_box:
                    selected_reports.append(rep)
                
                table_html += f"""<tr>
                    <td>📍</td>
                    <td>{rep['ID']}</td>
                    <td>{rep['Вақт']}</td>
                    <td>{rep['Ходим']}</td>
                    <td style='color:green;'>+{rep['Миқдор']:,} {rep['Берилди']}</td>
                    <td style='color:red;'>-{rep['Берилган Миқдор']:,.2f} {rep['Олинди']}</td>
                    <td>{rep['Изоҳ']}</td>
                </tr>"""
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
            
            # Агар галичка қўйилган бўлса, ўзгартириш/ўчириш тугмалари чиқади
            if selected_reports:
                st.markdown("##### ⚙️ Танланган ҳисоботларни бошқариш")
                col_del, col_edit = st.columns(2)
                
                if col_del.button("🗑️ Танланганларни Ўчириш", type="primary", use_container_width=True):
                    for r in selected_reports:
                        st.session_state.kassa[r["Берилди"]] -= r["Миқдор"]
                        st.session_state.kassa[r["Олинди"]] += r["Берилган Миқдор"]
                        st.session_state.history.remove(r)
                    st.success("Муваффақиятли ўчирилди!")
                    st.rerun()
                    
                if col_edit.button("✏️ Танланганни Тўғрилаш", use_container_width=True):
                    st.info("Қўлда тўғрилаш учун Кассани қўлда тўғрилаш бўлимидан фойдаланинг.")
        else:
            st.info("Ҳисоботлар мавжуд эмас.")

    # ==================== БОЛИМ 3: ҚАРЗ ДАФТАРИ ====================
    elif st.session_state.sub_page == "📕 Қарз Дафтари":
        with st.expander("➕ Янги Қарз Қўшиш"):
            d_name = st.text_input("Қарздор исми:")
            d_phone = st.text_input("Телефон:")
            d_curr = st.selectbox("Валюта:", ALL_CURRENCIES)
            d_amount = st.number_input("Миқдор:", min_value=0.0)
            if st.button("Сақлаш", type="primary"):
                if d_name and d_amount > 0:
                    st.session_state.debts.append({
                        "ID": len(st.session_state.debts) + 1, "Сана": datetime.now().strftime("%Y-%m-%d"),
                        "Исм": d_name, "Телефон": d_phone, "Валюта": d_curr, "Аслий Қарз": d_amount, "Қолдиқ Қарз": d_amount, "Ҳолат": "Тўланмаган"
                    })
                    st.session_state.kassa[d_curr] -= d_amount
                    st.success("Қарз ёзилди!"); st.rerun()

        st.markdown("##### 📋 Қарздорлар Рўйхати (Excel Жадвал)")
        if st.session_state.debts:
            selected_debts = []
            
            d_table = """<table class='excel-table'>
            <tr><th>📍</th><th>ID</th><th>Исм</th><th>Телефон</th><th>Валюта</th><th>Аслий Қарз</th><th>Қолдиқ</th><th>Ҳолат</th></tr>"""
            
            for debt in st.session_state.debts:
                ch_debt = st.checkbox("", key=f"debt_chk_{debt['ID']}", label_visibility="collapsed")
                if ch_debt:
                    selected_debts.append(debt)
                    
                d_table += f"""<tr>
                    <td>🔍</td>
                    <td>{debt['ID']}</td>
                    <td><b>{debt['Исм']}</b></td>
                    <td>{debt['Телефон']}</td>
                    <td>{debt['Валюта']}</td>
                    <td>{debt['Аслий Қарз']:,}</td>
                    <td style='color:red; font-weight:bold;'>{debt['Қолдиқ Қарз']:,}</td>
                    <td>{debt['Ҳолат']}</td>
                </tr>"""
            d_table += "</table>"
            st.markdown(d_table, unsafe_allow_html=True)
            
            if selected_debts:
                st.markdown("##### ⚙️ Танланган қарздорни бошқариш")
                target_debt = selected_debts[0]
                
                pay_amt = st.number_input(f"Тўлов суммасини киритинг ({target_debt['Валюта']}):", min_value=0.0, max_value=float(target_debt['Қолдиқ Қарз']))
                col_p, col_d = st.columns(2)
                
                if col_p.button("✅ Тўловни қабул қилиш", type="primary", use_container_width=True):
                    target_debt['Қолдиқ Қарз'] -= pay_amt
                    st.session_state.kassa[target_debt['Валюта']] += pay_amt
                    if target_debt['Қолдиқ Қарз'] <= 0:
                        target_debt['Ҳолат'] = "Ёпилган"
                    st.success("Тўлов қабул қилинди!"); st.rerun()
                    
                if col_d.button("🗑️ Қарзни Ўчириш", use_container_width=True):
                    st.session_state.debts.remove(target_debt)
                    st.success("Ўчирилди!"); st.rerun()
        else:
            st.info("Қарздорлар йўқ.")

    # ==================== БОЛИМ 4: ХАРАЖАТЛАР ====================
    elif st.session_state.sub_page == "📉 Харажатлар":
        with st.expander("➕ Янги Харажат"):
            ex_curr = st.selectbox("Валюта:", ALL_CURRENCIES)
            ex_amount = st.number_input("Сумма:", min_value=0.0)
            ex_reason = st.text_input("Сабаб:")
            if st.button("Харажатни ёзиш", type="primary"):
                if ex_amount > 0 and ex_reason:
                    st.session_state.kassa[ex_curr] -= ex_amount
                    st.session_state.expenses.append({
                        "Вақт": datetime.now().strftime("%m-%d %H:%M"), "Валюта": ex_curr, "Миқдор": ex_amount, "Сабаб": ex_reason
                    })
                    st.success("Сақланди!"); st.rerun()

        if st.session_state.expenses:
            st.markdown("##### 📋 Чиқимлар рўйхати")
            df_ex = pd.DataFrame(st.session_state.expenses)
            st.dataframe(df_ex, use_container_width=True)

    # ==================== БОЛИМ 5: КУРСЛАРНИ СОЗЛАШ ====================
    elif st.session_state.sub_page == "⚙️ Курсларна Созлаш":
        st.markdown("##### 🎛️ Созлаш учун валютани танланг:")
        
        # Горизонталь тугмалар орқали курсни танлаш
        cols_rate_edit = st.columns(len(ALL_CURRENCIES) - 1)
        if 'active_rate_edit' not in st.session_state: st.session_state.active_rate_edit = "USD"
        
        for idx, c in enumerate(ALL_CURRENCIES[1:]):
            btn_type = "primary" if st.session_state.active_rate_edit == c else "secondary"
            if cols_rate_edit[idx].button(c, key=f"btn_re_{c}", type=btn_type, use_container_width=True):
                st.session_state.active_rate_edit = c
                st.rerun()
                
        edit_c = st.session_state.active_rate_edit
        st.write(f"⚙️ **{edit_c}** курсларини ўзгартириш:")
        
        n_buy = st.number_input("📥 Янги ОЛИШ курси:", value=st.session_state.rates[edit_c]["buy"], format="%.4f")
        n_sell = st.number_input("📤 Янги СОТИШ курси:", value=st.session_state.rates[edit_c]["sell"], format="%.4f")
        
        if st.button("💾 Янги Курсни Сақлаш", type="primary", use_container_width=True):
            st.session_state.rates[edit_c]["buy"] = n_buy
            st.session_state.rates[edit_c]["sell"] = n_sell
            st.toast("Курслар муваффақиятли янгиланди!", icon="📝")

    # ==================== БОЛИМ 6: ДЎКОНЛАРНИ БОШҚАРИШ ====================
    elif st.session_state.sub_page == "🏢 Дўконларни Бошқариш":
        new_s = st.text_input("Янги дўкон номи:")
        if st.button("➕ Қўшиш", type="primary"):
            if new_s and new_s not in st.session_state.shops:
                st.session_state.shops.append(new_s)
                st.success("Қўшилди!"); st.rerun()
                
        st.write(st.session_state.shops)

    # ==================== БОЛИМ 7: ХОДИМЛАРНИ БОШҚАРИШ ====================
    elif st.session_state.sub_page == "👤 Ходимларни Бошқариш":
        with st.expander("➕ Янги ходим қўшиш"):
            emp_i = st.text_input("Ходим исми:")
            emp_p = st.text_input("Парол:")
            if st.button("Сақлаш"):
                if emp_i and emp_p:
                    st.session_state.employees.append({"Исм": emp_i, "Пароль": emp_p})
                    st.success("Ходим қўшилди!"); st.rerun()
                    
        st.write([e["Исм"] for e in st.session_state.employees])

    # ---------------- ОРҚАГА ҚАЙТИШ ТУГМАСИ (ЭНГ ПАСТДА) ----------------
    if st.session_state.sub_page != "Меню":
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("⬅️ Асосий Менюга Қайтиш", type="secondary", use_container_width=True):
            st.session_state.sub_page = "Меню"
            st.rerun()
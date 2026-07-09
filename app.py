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

# Замонавий Премиум Дизайн ва СТИЛЛАР (Телефон учун ихчамлаштирилган)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; color: #0f172a; }
    
    /* Валюталарни бир қаторда (горизонтал скролл) кўрсатиш учун контейнер */
    .scroll-container {
        display: flex;
        overflow-x: auto;
        white-space: nowrap;
        padding: 5px 0;
        gap: 8px;
        -webkit-overflow-scrolling: touch;
    }
    .scroll-card {
        flex: 0 0 auto;
        background: #ffffff;
        border-radius: 8px;
        padding: 8px 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        border-top: 3px solid #d4af37;
        text-align: center;
        min-width: 95px;
    }
    
    /* Ихчам ходимлар картаси */
    .emp-card {
        background: #ffffff; border-radius: 10px; padding: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        border-left: 4px solid #0284c7; margin-bottom: 8px;
        font-size: 13px;
    }
    
    /* Ихчам жадвал типидаги карталар */
    .table-card {
        background: #ffffff; border-radius: 8px; padding: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.02);
        border: 1px solid #e2e8f0; margin-bottom: 8px;
        font-size: 13px;
        line-height: 1.4;
    }
    
    .status-box {
        background-color: #f0fdf4; border-left: 4px solid #d4af37;
        padding: 10px; border-radius: 6px; margin: 8px 0; font-size: 14px;
    }
    .success-popup {
        background-color: #d1e7dd; color: #0f5132;
        border: 2px dashed #198754; padding: 12px; border-radius: 8px;
        text-align: center; font-size: 15px; font-weight: bold; margin: 8px 0;
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
        {"ID": 1, "Сана": "2026-07-08 11:00", "Исм": "Алишер", "Телефон": "+996772112233", "Валюта": "USD", "Аслий Қарз": 500.0, "Қолдиқ Қарз": 300.0, "Ҳолат": "Тўланмаган", "Тўловлар Тарихи": ["2026-07-08 12:00 куни 200.0 USD қайтарилди."]}
    ]

if 'pending_operation' not in st.session_state: st.session_state.pending_operation = None
if 'show_success_flash' not in st.session_state: st.session_state.show_success_flash = False

# Авторизация ҳолати
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'current_role' not in st.session_state: st.session_state.current_role = None
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'current_shop' not in st.session_state: st.session_state.current_shop = None

# Жорий фаол ойна
if 'sub_page' not in st.session_state: st.session_state.sub_page = "Меню"

# --- ЮҚОРИДАГИ САРЛАВҲА ---
st.markdown('<div class="app-title"><h2>ХОЛИД ФИНАНС</h2></div>', unsafe_allow_html=True)


# ==================== БОСҚИЧ 1: АВТОРИЗАЦИЯ САҲИФАСИ ====================
if not st.session_state.authenticated:
    st.markdown("<h3 style='text-align:center; font-size:18px;'>🔐 Тизимга кириш</h3>", unsafe_allow_html=True)
    
    auth_shop = st.selectbox("Дўконни танланг:", st.session_state.shops if st.session_state.shops else ["Филиал йўқ"])
    auth_role = st.selectbox("Сизнинг ролингиз:", ["Ходим", "Менежер", "Директор"])
    
    if auth_role == "Директор":
        auth_user = "Муҳаммад Диёр"
        password = st.text_input("Паролни киритинг:", type="password")
        if st.button("Кириш", use_container_width=True, type="primary"):
            if password == "1111":
                st.session_state.authenticated = True
                st.session_state.current_role = auth_role
                st.session_state.current_user = auth_user
                st.session_state.current_shop = auth_shop
                st.rerun()
            else:
                st.error("Хато парол!")
                
    elif auth_role == "Менежер":
        auth_user = "Муҳаммад Али"
        password = st.text_input("Паролни киритинг:", type="password")
        if st.button("Кириш", use_container_width=True, type="primary"):
            if password == "2222":
                st.session_state.authenticated = True
                st.session_state.current_role = auth_role
                st.session_state.current_user = auth_user
                st.session_state.current_shop = auth_shop
                st.rerun()
            else:
                st.error("Хато парол!")
                
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
                else:
                    st.error("Хато парол!")
            else:
                st.error("Тизимда ходим мавжуд эмас!")

# ==================== БОСҚИЧ 2: АСОСИЙ ИЛОВА ТИЗИМИ ====================
else:
    st.markdown(f"<p style='font-size:12px; text-align:center; color:#64748b; margin-bottom:5px;'>📍 Нуқта: {st.session_state.current_shop} | 👤 {st.session_state.current_user} ({st.session_state.current_role})</p>", unsafe_allow_html=True)
    
    if st.button("🚪 Тизимдан чиқиш", type="secondary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.sub_page = "Меню"
        st.rerun()
        
    st.markdown("---")

    # ---------------- САҲИФА: АСОСИЙ МЕНЮ ----------------
    if st.session_state.sub_page == "Меню":
        st.markdown("<h4 style='text-align:center; margin-bottom:10px;'>🖥️ Асосий Меню</h4>", unsafe_allow_html=True)
        
        if st.button("💸 Айирбошлаш", use_container_width=True, type="primary"):
            st.session_state.sub_page = "💸 Айирбошлаш"
            st.rerun()
            
        if st.button("📋 Касса ва Ҳисоботлар", use_container_width=True):
            st.session_state.sub_page = "📋 Касса ва Ҳисоботлар"
            st.rerun()
            
        if st.button("📕 Қарз Дафтари", use_container_width=True):
            st.session_state.sub_page = "📕 Қарз Дафтари"
            st.rerun()
            
        if st.button("📉 Харажатлар", use_container_width=True):
            st.session_state.sub_page = "📉 Харажатлар"
            st.rerun()
            
        # Менежер ва Директор тугмалари
        if st.session_state.current_role in ["Менежер", "Директор"]:
            if st.button("⚙️ Курсларна Созлаш", use_container_width=True):
                st.session_state.sub_page = "⚙️ Курсларна Созлаш"
                st.rerun()
                
            if st.button("🏢 Дўконларни Бошқариш", use_container_width=True):
                st.session_state.sub_page = "🏢 Дўконларни Бошқариш"
                st.rerun()
                
            if st.button("👤 Ходимларни Бошқариш", use_container_width=True):
                st.session_state.sub_page = "👤 Ходимларни Бошқариш"
                st.rerun()

    # ---------------- САҲИФАЛАР УЧУН ОРҚАГА ҚАЙТИШ ТУГМАСИ ----------------
    if st.session_state.sub_page != "Меню":
        if st.button("⬅️ Orqaga", type="secondary", use_container_width=True):
            st.session_state.sub_page = "Меню"
            st.session_state.pending_operation = None
            st.session_state.show_success_flash = False
            st.rerun()
        st.markdown(f"<h4 style='margin-top:5px;'>{st.session_state.sub_page}</h4>", unsafe_allow_html=True)

    # ==================== БОЛИМ 1: АЙИРБОШЛАШ ====================
    if st.session_state.sub_page == "💸 Айирбошлаш":
        if st.session_state.show_success_flash:
            st.success("✅ Амалиёт муваффақиятли бажарилди ва ҳисобот базасига ёзилди!")
            if st.button("Хабарни ёпиш"):
                st.session_state.show_success_flash = False
                st.rerun()

        st.markdown("<p style='font-size:13px; font-weight:bold; margin-bottom:4px;'>📈 Жорий Валюта Курслари (KGS га нисбатан):</p>", unsafe_allow_html=True)
        
        # ТЎҒИРЛАНГАН БЛОК: Энди рўйхатдаги барча валюталар USD каби кетма-кет чиқади
        cards_html = '<div class="scroll-container">'
        for c in ALL_CURRENCIES:
            if c == "KGS": 
                continue  # Асосий ўлчов бирлиги бўлгани учун ташлаб кетилади
            
            cards_html += f"""
                <div class="scroll-card">
                    <b style="font-size:14px; color:#0f172a;">{c}</b><br>
                    <span style="color:#16a34a; font-size:11px;">📥 {st.session_state.rates[c]['buy']:.2f}</span><br>
                    <span style="color:#dc2626; font-size:11px;">📤 {st.session_state.rates[c]['sell']:.2f}</span>
                </div>
            """
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)
            
        st.markdown("---")

        if 'give_curr' not in st.session_state: st.session_state.give_curr = "USD"
        if 'get_curr' not in st.session_state: st.session_state.get_curr = "KGS"

        st.session_state.give_curr = st.selectbox("📥 Мижоз берадиган (Кириш):", ALL_CURRENCIES, index=ALL_CURRENCIES.index(st.session_state.give_curr), key="sel_give_c")
        st.session_state.get_curr = st.selectbox("📤 Мижоз оладиган (Чиқиш):", ALL_CURRENCIES, index=ALL_CURRENCIES.index(st.session_state.get_curr), key="sel_get_c")

        if st.session_state.give_curr == st.session_state.get_curr:
            st.warning("⚠️ Илтимос, иккита ҳар хил валютани танланг!")
        else:
            r_give = st.session_state.rates[st.session_state.give_curr]["buy"] if st.session_state.get_curr == "KGS" or st.session_state.give_curr != "KGS" else 1.0
            r_get = st.session_state.rates[st.session_state.get_curr]["sell"] if st.session_state.give_curr == "KGS" or st.session_state.get_curr != "KGS" else 1.0
            cross_rate = r_give / r_get
            
            st.markdown(f"""<div class="status-box">ℹ️ Ҳисоб курси: 1 {st.session_state.give_curr} = <b>{cross_rate:.4f} {st.session_state.get_curr}</b></div>""", unsafe_allow_html=True)
            
            mbank_phone = st.text_input("💬 Изоҳ / MBANK телефон рақами:", placeholder="+996 ...")
            amount_give = st.number_input(f"💵 Мижоз берадиган миқдор ({st.session_state.give_curr}):", min_value=0.0, value=100.0)
            total_get = amount_give * cross_rate
            
            st.markdown(f"##### 🧮 Мижозга бериладиган сумма: <span style='color:#b45309;'><b>{total_get:,.2f} {st.session_state.get_curr}</b></span>", unsafe_allow_html=True)
            
            if st.button("🚀 Амалиётни Якунлаш", type="primary", use_container_width=True):
                if amount_give <= 0: 
                    st.error("Миқдор хато!")
                elif st.session_state.kassa[st.session_state.get_curr] < total_get: 
                    st.error("Кассада маблағ кам!")
                else:
                    st.session_state.pending_operation = {
                        "give_curr": st.session_state.give_curr, "amount_give": amount_give,
                        "get_curr": st.session_state.get_curr, "total_get": total_get, "comment": mbank_phone
                    }
                    st.rerun()

            if st.session_state.pending_operation:
                po = st.session_state.pending_operation
                st.markdown(f"""
                    <div class="success-popup">
                        ✔️ Амалиёт ҳисобланди!<br>
                        <b>Йўналиш:</b> {po['amount_give']:,} {po['give_curr']} ➡️ {po['total_get']:,.2f} {po['get_curr']}<br>
                        Ушбу амалиётни базага юборишни тасдиқлайсизми?
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("✅ Ҳа, юборилсин", type="primary", use_container_width=True):
                    st.session_state.kassa[po['give_curr']] += po['amount_give']
                    st.session_state.kassa[po['get_curr']] -= po['total_get']
                    
                    st.session_state.history.append({
                        "ID": len(st.session_state.history) + 1,
                        "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                        "Дўкон": st.session_state.current_shop, 
                        "Ходим": st.session_state.current_user,
                        "Берилди": po['give_curr'], "Миқдор": po['amount_give'], 
                        "Олинди": po['get_curr'], "Берилган Миқдор": po['total_get'], "Изоҳ": po['comment']
                    })
                    st.session_state.show_success_flash = True
                    st.session_state.pending_operation = None
                    st.rerun()
                    
                if st.button("❌ Бекор қилиш", type="secondary", use_container_width=True):
                    st.session_state.pending_operation = None
                    st.rerun()

    # ==================== БОЛИМ 2: КАССА ВА ҲИСОБОТЛАР ====================
    elif st.session_state.sub_page == "📋 Касса ва Ҳисоботлар":
        st.markdown("##### 💰 Дўкон Кассасидаги Жорий Қолдиқлар")
        
        k_cols = st.columns(2)
        for idx, c in enumerate(ALL_CURRENCIES):
            col_target = k_cols[idx % 2]
            with col_target:
                st.markdown(f"""
                    <div style='background:#ffffff; padding:6px; border-radius:6px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); margin-bottom:6px; text-align:center; border-left: 3px solid #0284c7; font-size:13px;'>
                        <b>{c}</b>: <span style='color:#0284c7; font-weight:bold;'>{st.session_state.kassa[c]:,.2f}</span>
                    </div>
                """, unsafe_allow_html=True)

        if st.session_state.current_role in ["Менежер", "Директор"]:
            with st.expander("🔧 Кассани қўлда тўғрилаш"):
                fix_curr = st.selectbox("Валюта:", ALL_CURRENCIES, key="k_fix_c")
                fix_amount = st.number_input("Янги қолдиқ миқдори:", value=float(st.session_state.kassa[fix_curr]), key="k_fix_a")
                if st.button("⚙️ Қолдиқни янгилаш", use_container_width=True, type="primary"):
                    st.session_state.kassa[fix_curr] = fix_amount
                    st.success("Касса янгиланди!")
                    st.rerun()

        st.markdown("---")
        st.markdown("##### 📝 Ҳисоботлар рўйхати (Ихчам)")
        
        if st.session_state.history:
            for idx, report in enumerate(reversed(st.session_state.history)):
                st.markdown(f"""
                    <div class="table-card">
                        <b>#ID: {report['ID']}</b> | <span style='color:#64748b;'>{report['Вақт']}</span><br>
                        📍 Нуқта: {report['Дўкон']} | 👤 Ходим: {report['Ходим']}<br>
                        <span style='color:#16a34a;'>📥 Олинди: {report['Миқдор']:,} {report['Берилди']}</span><br>
                        <span style='color:#b45309;'>📤 Берилди: {report['Берилган Миқдор']:,.2f} {report['Олинди']}</span><br>
                        💬 Изоҳ: {report['Изоҳ']}
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"⚙️ #{report['ID']} Бошқариш"):
                    if st.button("🗑️  Ўчириш", key=f"del_h_{idx}", use_container_width=True, type="primary"):
                        st.session_state.kassa[report["Берилди"]] -= report["Миқдор"]
                        st.session_state.kassa[report["Олинди"]] += report["Берилган Миқдор"]
                        st.session_state.history.pop(st.session_state.history.index(report))
                        st.warning("Ўчирилди!")
                        st.rerun()
        else:
            st.info("Ҳисоботлар мавжуд эмас.")

    # ==================== БОЛИМ 3: ҚАРЗ ДАФТАРИ ====================
    elif st.session_state.sub_page == "📕 Қарз Дафтари":
        with st.expander("➕  Янги Қарз Бериш"):
            d_name = st.text_input("Қарздор исми:")
            d_phone = st.text_input("Телефон рақами:", "+996")
            d_curr = st.selectbox("Валюта:", ALL_CURRENCIES, key="d_c")
            d_amount = st.number_input("Қарз миқдори:", min_value=0.0, key="d_a")
            if st.button("💾 Қарзни Сақлаш", type="primary", use_container_width=True):
                if d_name and d_amount > 0:
                    st.session_state.debts.append({
                        "ID": len(st.session_state.debts) + 1, "Сана": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Исм": d_name, "Телефон": d_phone, "Валюта": d_curr, 
                        "Аслий Қарз": d_amount, "Қолдиқ Қарз": d_amount, "Ҳолат": "Тўланмаган", "Тўловлар Тарихи": []
                    })
                    st.session_state.kassa[d_curr] -= d_amount
                    st.success("Қарз сақланди!")
                    st.rerun()

        st.markdown("##### 📋 Қарздорлар рўйхати")
        if st.session_state.debts:
            for d_idx, debt in enumerate(st.session_state.debts):
                st.markdown(f"""
                    <div class="table-card">
                        <b>👤 {debt['Исм']}</b> (<span style='color:#64748b;'>{debt['Сана']}</span>)<br>
                        📞 Тел: {debt['Телефон']}<br>
                        💰 Валюта: {debt['Валюта']} | Аслий қарз: {debt['Аслий Қарз']:,}<br>
                        🚨 <b>Қолдиқ қарз: {debt['Қолдиқ Қарз']:,}</b><br>
                        📊 Ҳолат: {"🔴 Тўланмаган" if debt['Ҳолат'] == "Тўланмаган" else "🟢 Ёпилган"}
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"⚙️ {debt['Исм']} Тўлов/Ўчириш"):
                    if debt["Ҳолат"] == "Тўланмаган":
                        pay_amount = st.number_input(f"Қайтарилган сумма ({debt['Валюта']}):", min_value=0.0, max_value=float(debt["Қолдиқ Қарз"]), key=f"pay_val_{d_idx}")
                        if st.button("✅ Тўловни тасдиқлаш", key=f"btn_pay_{d_idx}", type="primary", use_container_width=True):
                            if pay_amount > 0:
                                st.session_state.debts[d_idx]["Қолдиқ Қарз"] -= pay_amount
                                st.session_state.kassa[debt["Валюта"]] += pay_amount
                                st.session_state.debts[d_idx]["Тўловлар Тарихи"].append(f"{pay_amount} {debt['Валюта']} қайтарилди.")
                                if st.session_state.debts[d_idx]["Қолдиқ Қарз"] <= 0: 
                                    st.session_state.debts[d_idx]["Ҳолат"] = "Тўлиқ ёпилди"
                                st.success("Касса янгиланди!")
                                st.rerun()
                                
                    if st.button("🗑️ Қарзни ўчириш", key=f"del_debt_{d_idx}", use_container_width=True):
                        st.session_state.kassa[debt["Валюта"]] += debt["Қолдиқ Қарз"]
                        st.session_state.debts.pop(d_idx)
                        st.rerun()
        else:
            st.info("Қарздорлар рўйхати бўш.")

    # ==================== БОЛИМ 4: ХАРАЖАТЛАР ====================
    elif st.session_state.sub_page == "📉 Харажатлар":
        with st.expander("➕  Янги Харажат Киритиш"):
            ex_curr = st.selectbox("Валюта:", ALL_CURRENCIES, key="ex_c")
            ex_amount = st.number_input("Миқдор:", min_value=0.0, key="ex_a")
            ex_reason = st.text_input("Сабаб:")
            if st.button("📉 Харажатни Сақлаш", type="primary", use_container_width=True):
                if ex_amount > 0 and ex_reason:
                    st.session_state.kassa[ex_curr] -= ex_amount
                    st.session_state.expenses.append({
                        "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M"), 
                        "Ходим": st.session_state.current_user, 
                        "Дўкон": st.session_state.current_shop, 
                        "Валюта": ex_curr, "Миқдор": ex_amount, "Сабаб": ex_reason
                    })
                    st.success("Харажат сақланди!")
                    st.rerun()

        st.markdown("##### 📋 Харажатлар рўйхати")
        if st.session_state.expenses:
            for ex in reversed(st.session_state.expenses):
                st.markdown(f"""
                    <div class="table-card" style="border-left: 4px solid #dc2626;">
                        <b>🕒 {ex['Вақт']}</b> | Нуқта: {ex['Дўкон']}<br>
                        👤 Ходим: {ex['Ходим']}<br>
                        ⚠️ <span style='color:#dc2626; font-weight:bold;'>Чиқим: {ex['Миқдор']:,} {ex['Валюта']}</span><br>
                        📝 Сабаб: {ex['Сабаб']}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Харажатлар йўқ.")

    # ==================== БОЛИМ 5: КУРСЛАРНИ СОЗЛАШ ====================
    elif st.session_state.sub_page == "⚙️ Курсларна Созлаш":
        c_edit = st.selectbox("Валютани танланг:", ALL_CURRENCIES[1:], key="edit_c")
        n_buy = st.number_input("Янги ОЛИШ курси:", value=st.session_state.rates[c_edit]["buy"], format="%.4f")
        n_sell = st.number_input("Янги СОТИШ курси:", value=st.session_state.rates[c_edit]["sell"], format="%.4f")
        if st.button("💾 Курсни Сақлаш", type="primary", use_container_width=True):
            st.session_state.rates[c_edit]["buy"] = n_buy
            st.session_state.rates[c_edit]["sell"] = n_sell
            st.success("Курслар янгиланди!")
            st.rerun()

    # ==================== БОЛИМ 6: ДЎКОНЛАРНИ БОШҚАРИШ ====================
    elif st.session_state.sub_page == "🏢 Дўконларни Бошқариш":
        with st.expander("➕ Янги Дўкон Қўшиш"):
            new_shop_name = st.text_input("Дўкон номи:")
            if st.button("🏢 Дўконни Сақлаш", type="primary", use_container_width=True):
                if new_shop_name.strip() and new_shop_name not in st.session_state.shops:
                    st.session_state.shops.append(new_shop_name.strip())
                    st.success("Дўкон қўшилди!")
                    st.rerun()

        st.markdown("##### 📋 Мавжуд Дўконлар")
        for s_idx, s_name in enumerate(st.session_state.shops):
            st.markdown(f"<div style='font-size:13px; margin-bottom:2px;'>📍 {s_name} дўкони</div>", unsafe_allow_html=True)
            if st.button("🗑️ Ўчириш", key=f"del_shop_{s_idx}"):
                st.session_state.shops.pop(s_idx)
                st.rerun()

    # ==================== БОЛИМ 7: ХОДИМЛАРНИ БОШҚАРИШ ====================
    elif st.session_state.sub_page == "👤 Ходимларни Бошқариш":
        emp_action = st.radio("Амал танланг:", ["📋 Рўйхат", "➕ Қўшиш"])
        
        if emp_action == "➕ Қўшиш":
            e_name = st.text_input("Ходим исми:")
            e_phone = st.text_input("Телефон:")
            e_gmail = st.text_input("Gmail:")
            e_passport = st.text_input("Паспорт:")
            e_pass = st.text_input("Парол:", type="password")
            if st.button("👤 Ходимни Қўшиш", type="primary", use_container_width=True):
                if e_name and e_phone and e_pass:
                    st.session_state.employees.append({
                        "Исм": e_name, "Телефон": e_phone, "Gmail": e_gmail,
                        "Паспорт": e_passport, "Пароль": e_pass
                    })
                    st.success("Ходим қўшилди!")
                    st.rerun()
        else:
            st.markdown("##### 👥 Фаол Ходимлар")
            for idx, emp in enumerate(st.session_state.employees):
                st.markdown(f"""
                    <div class="emp-card">
                        <b>👤 {emp['Исм']}</b><br>
                        📞 Тел: {emp.get('Телефон', '-')}<br>
                        🪪 Паспорт: {emp.get('Паспорт','-')}<br>
                        🔑 Парол: <code>{emp.get('Пароль','****')}</code>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("🗑️ Ишдан бўшатиш", key=f"del_emp_{idx}", use_container_width=True):
                    st.session_state.employees.pop(idx)
                    st.rerun()
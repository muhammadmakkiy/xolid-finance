import streamlit as st
import pandas as pd
from datetime import datetime

# Саҳифа созламалари
st.set_page_config(
    page_title="Холид Финанс Обмен валюта",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Замонавий Премиум Дизайн ва СТИЛЛАР
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; color: #1e293b; }
    .crypto-card {
        background: #ffffff; border-radius: 12px; padding: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); text-align: center;
        border-top: 4px solid #d4af37;
        border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    .emp-card {
        background: #ffffff; border-radius: 12px; padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 5px solid #0284c7;
        margin-bottom: 15px;
    }
    .table-card {
        background: #ffffff; border-radius: 8px; padding: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        border: 1px solid #e2e8f0;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }
    .status-box {
        background-color: #f0fdf4; border-left: 5px solid #d4af37;
        padding: 14px; border-radius: 8px; margin: 12px 0; font-size: 16px; color: #1e293b;
    }
    .success-popup {
        background-color: #d1e7dd; color: #0f5132;
        border: 2px dashed #198754; padding: 20px; border-radius: 12px;
        text-align: center; font-size: 18px; font-weight: bold; margin: 15px 0;
    }
    .custom-table-header {
        background-color: #0f172a; color: white; padding: 10px; 
        font-weight: bold; text-align: center; border-radius: 6px;
        font-size: 14px; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Барча мавжуд пул бирликлари
ALL_CURRENCIES = ["KGS", "USD", "EUR", "RUB", "CNY", "KZT", "UZS", "MBANK"]

# --- СEССИЯ МАЪЛУМОТЛАРИНИ ИНИЦИАЛИЗАЦИЯ ҚИЛИШ ---
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
        {"Исм": "Одилжон", "Телефон": "+996558143464", "Gmail": "odiljon@gmail.com", "Паспорт": "AN1234567", "Сурат": "https://img.icons8.com/color/144/user-male-circle--v1.png", "Пароль": "7777"},
        {"Исм": "Ҳузайфа", "Телефон": "+996553707490", "Gmail": "huzaifa@gmail.com", "Паспорт": "AN7654321", "Сурат": "https://img.icons8.com/color/144/user-male-circle--v1.png", "Пароль": "8888"}
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

# --- СИДЕБАР ---
st.sidebar.markdown("<h2 style='color:#0284c7; font-size:22px; margin-bottom:0;'>🔐 Тизимга Кириш</h2>", unsafe_allow_html=True)
shop = st.sidebar.selectbox("Дўконни танланг:", st.session_state.shops if st.session_state.shops else ["Филиал йўқ"])
role = st.sidebar.selectbox("Сизнинг ролингиз:", ["Ходим", "Менежер", "Директор"])

access_granted = False
user_name = ""

if role == "Директор":
    user_name = st.sidebar.selectbox("Исмингиз:", ["Муҳаммад Диёр"])
    st.sidebar.markdown("📞 **Тел:** +996554070704")
    password = st.sidebar.text_input("Директор паролини киритинг:", type="password")
    access_granted = (password == "1111")
elif role == "Менежер":
    user_name = st.sidebar.selectbox("Исмингиз:", ["Муҳаммад Али"])
    st.sidebar.markdown("📞 **Тел:** +996999999026")
    password = st.sidebar.text_input("Менежер паролини киритинг:", type="password")
    access_granted = (password == "2222")
else:
    emp_names = [e["Исм"] for e in st.session_state.employees] if st.session_state.employees else ["Ходим мавжуд эмас"]
    user_name = st.sidebar.selectbox("Исмингиз:", emp_names)
    if st.session_state.employees and user_name != "Ходим мавжуд эмас":
        emp_data = next(e for e in st.session_state.employees if e["Исм"] == user_name)
        st.sidebar.markdown(f"📞 **Тел:** {emp_data['Телефон']}")
        emp_password = st.sidebar.text_input(f"{user_name} паролини киритинг:", type="password")
        access_granted = (emp_password == emp_data.get("Пароль", ""))

st.sidebar.markdown("---")

if access_granted:
    st.sidebar.markdown("<h3 style='color:#d4af37; font-size:18px;'>🖥️ АСОСИЙ МЕНЮ</h3>", unsafe_allow_html=True)
    menu_options = ["💸 Айирбошлаш", "📋 Касса ва Ҳисоботлар", "📕 Қарз Дафтари", "📉 Харажатлар"]
    if role in ["Менежер", "Директор"]:
        menu_options.extend(["⚙️ Курсларни Созлаш", "🏢 Дўконларни Бошқариш", "👤 Ходимларни Бошқариш"])

    if 'current_page' not in st.session_state: st.session_state.current_page = "💸 Айирбошлаш"

    for option in menu_options:
        if st.sidebar.button(option, width="stretch", type="primary" if st.session_state.current_page == option else "secondary"):
            st.session_state.current_page = option
            st.session_state.show_success_flash = False
            st.session_state.pending_operation = None
            st.rerun()

st.sidebar.markdown(f"<div style='background:#f8fafc; padding:10px; border-radius:8px; border-left:4px solid #d4af37;'><b>📍 Нуқта:</b> {shop}<br><b>👤 Жорий:</b> {user_name if access_granted else 'Авторизациядан ўтмаган'}</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; margin-bottom: 5px;'><h2 style='margin:0; font-size: 26px; color: #0f172a; font-weight: 900;'>✨ ХОЛИД ФИНАНС ✨</h2></div>", unsafe_allow_html=True)

if not access_granted:
    st.warning("🔒 Тизим ёпиқ! Илтимос, чап панелдан ролингизни танланг ва тўғри паролни киритинг.")
else:
    st.markdown(f"## {st.session_state.current_page}")

    if st.session_state.show_success_flash:
        st.success("✅ Амалиёт муваффақиятли бажарилди ва ҳисобот базасига ёзилди!")
        if st.button("Хабарни ёпиш"): 
            st.session_state.show_success_flash = False
            st.rerun()

    # ==================== ОЙНА 1: АЙИРБОШЛАШ ====================
    if st.session_state.current_page == "💸 Айирбошлаш":
        if shop == "Филиал йўқ" or user_name == "Ходим мавжуд эмас":
            st.error("Фаол ходим ёки дўкон мавжуд эмас!")
        else:
            st.markdown("#### 📈 Жорий Валюта Курслари (KGS га нисбатан)")
            rate_cols = st.columns(len(ALL_CURRENCIES) - 1)
            col_idx = 0
            for c in ALL_CURRENCIES:
                if c == "KGS": continue
                with rate_cols[col_idx]:
                    st.markdown(f"""
                        <div class="crypto-card">
                            <b style="font-size:16px; color:#0f172a;">{c}</b><br>
                            <span style="color:#16a34a; font-size:13px;">🟢 Олиш: <b>{st.session_state.rates[c]['buy']:.2f}</b></span><br>
                            <span style="color:#dc2626; font-size:13px;">🔴 Сотиш: <b>{st.session_state.rates[c]['sell']:.2f}</b></span>
                        </div>
                    """, unsafe_allow_html=True)
                col_idx += 1
            
            st.markdown("---")

            if 'give_curr' not in st.session_state: st.session_state.give_curr = "USD"
            if 'get_curr' not in st.session_state: st.session_state.get_curr = "KGS"

            st.write("**1. Мижоз Берадиган Валюта (Кириш):**")
            g_cols = st.columns(len(ALL_CURRENCIES))
            for i, c in enumerate(ALL_CURRENCIES):
                with g_cols[i]:
                    if st.button(f"📥 {c}", key=f"give_{c}", type="primary" if st.session_state.give_curr == c else "secondary", width="stretch"):
                        st.session_state.give_curr = c
                        st.session_state.pending_operation = None
                        st.rerun()

            st.write("**2. Мижоз Оладиган Валюта (Чиқиш):**")
            get_cols = st.columns(len(ALL_CURRENCIES))
            for i, c in enumerate(ALL_CURRENCIES):
                with get_cols[i]:
                    if st.button(f"📤 {c}", key=f"get_{c}", type="primary" if st.session_state.get_curr == c else "secondary", width="stretch"):
                        st.session_state.get_curr = c
                        st.session_state.pending_operation = None
                        st.rerun()

            if st.session_state.give_curr == st.session_state.get_curr:
                st.warning("Илтимос, иккита ҳар хил валютани танланг!")
            else:
                r_give = st.session_state.rates[st.session_state.give_curr]["buy"] if st.session_state.get_curr == "KGS" or st.session_state.give_curr != "KGS" else 1.0
                r_get = st.session_state.rates[st.session_state.get_curr]["sell"] if st.session_state.give_curr == "KGS" or st.session_state.get_curr != "KGS" else 1.0
                cross_rate = r_give / r_get
                
                st.markdown(f"""<div class="status-box">ℹ️ <b>Ҳисоб курси:</b> 1 {st.session_state.give_curr} = <b>{cross_rate:.4f} {st.session_state.get_curr}</b></div>""", unsafe_allow_html=True)
                
                mbank_phone = st.text_input("Изоҳ / МБАНК телефон рақами (агар бўлса):", placeholder="+996 ...")
                amount_give = st.number_input(f"Мижоз берадиган миқдор ({st.session_state.give_curr}):", min_value=0.0, value=100.0)
                total_get = amount_give * cross_rate
                
                st.markdown(f"### 🧮 Мижозга бериладиган сумма: <span style='color:#b45309;'><b>{total_get:,.2f} {st.session_state.get_curr}</b></span>", unsafe_allow_html=True)
                
                if st.button("🚀 Амалиётни Якунлаш", type="primary", width="stretch"):
                    if amount_give <= 0: st.error("Миқдор хато!")
                    elif st.session_state.kassa[st.session_state.get_curr] < total_get: st.error("Кассада маблағ кам!")
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
                            ✔️ Амалиёт муваффақиятли ҳисобланди!<br>
                            <b>Йўналиш:</b> {po['amount_give']:,} {po['give_curr']} ➡️ {po['total_get']:,.2f} {po['get_curr']}<br>
                            <span style='color:#0f5132;'>⚠️ Ушбу амалиётни ХИСОБОТЛАР БАЗАСИГА юборишни тасдиқлайсизми?</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    c_yes, c_no = st.columns([1, 1])
                    with c_yes:
                        if st.button("✅ Ҳа, юборилсин", type="primary", use_container_width=True):
                            st.session_state.kassa[po['give_curr']] += po['amount_give']
                            st.session_state.kassa[po['get_curr']] -= po['total_get']
                            
                            st.session_state.history.append({
                                "ID": len(st.session_state.history) + 1,
                                "Вақт": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Дўкон": shop, "Ходим": user_name,
                                "Берилди": po['give_curr'], "Миқдор": po['amount_give'], 
                                "Олинди": po['get_curr'], "Берилган Миқдор": po['total_get'], "Изоҳ": po['comment']
                            })
                            st.session_state.show_success_flash = True
                            st.session_state.pending_operation = None
                            st.rerun()
                    with c_no:
                        if st.button("❌ Йўқ, бекор қилинсин", type="secondary", use_container_width=True):
                            st.session_state.pending_operation = None
                            st.rerun()

    # ==================== ОЙНА 2: КАССА ВА ҲИСОБОТЛАР (КАТЕКЛИ ЖАДВАЛ) ====================
    elif st.session_state.current_page == "📋 Касса ва Ҳисоботлар":
        col_title, col_fix = st.columns([3, 1])
        with col_title:
            st.markdown("#### 💰 Дўкон Кассасидаги Жорий Қолдиқлар")
        
        with col_fix:
            if role in ["Менежер", "Директор"]:
                with st.popover("🔧 Қолдиқларни Тўғрилаш", use_container_width=True):
                    st.markdown("⚠️ **Кассани қўлда ўзгартириш**")
                    fix_curr = st.selectbox("Валюта:", ALL_CURRENCIES, key="fix_c")
                    fix_amount = st.number_input("Янги қолдиқ миқдори:", value=float(st.session_state.kassa[fix_curr]), key="fix_a")
                    if st.button("⚙️ Қолдиқни Янгилаш", type="primary", use_container_width=True):
                        st.session_state.kassa[fix_curr] = fix_amount
                        st.success(f"✅ {fix_curr} кассаси {fix_amount:,} га ўзгарди!")
                        st.rerun()

        kassa_data = [{"Валюта": c, "Қолдиқ пул миқдори": f"{st.session_state.kassa[c]:,.2f}"} for c in ALL_CURRENCIES]
        st.table(pd.DataFrame(kassa_data))
        
        st.markdown("---")
        st.markdown("#### 📝 Ҳисоботлар жадвали (Катаклар ичида)")
        
        if st.session_state.history:
            # Юқоридаги асосий сарлавҳалар блоги
            h_cols = st.columns([0.6, 1.4, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5])
            headers = ["ID", "Вақт", "Дўкон", "Ходим", "Олинди", "Миқдор", "Берилди", "Берилган сумма", "Ҳаракат"]
            for i, h in enumerate(headers):
                h_cols[i].markdown(f"<div class='custom-table-header'>{h}</div>", unsafe_allow_html=True)
            
            # Ҳар бир ҳисоботни алоҳида чиройли визуал катак (box) ичига чиқариш
            for idx, report in enumerate(st.session_state.history):
                st.markdown('<div class="table-card">', unsafe_allow_html=True)
                r_cols = st.columns([0.6, 1.4, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5])
                
                r_cols[0].write(f"**#{report['ID']}**")
                r_cols[1].caption(report['Вақт'])
                r_cols[2].write(report['Дўкон'])
                r_cols[3].write(report['Ходим'])
                r_cols[4].write(f"📥 {report['Берилди']}")
                r_cols[5].write(f"**{report['Миқдор']:,}**")
                r_cols[6].write(f"📤 {report['Олинди']}")
                r_cols[7].write(f"**{report['Берилган Миқдор']:,.2f}**")
                
                with r_cols[8]:
                    with st.popover("⚙️ Бошқариш", use_container_width=True):
                        edit_g_c = st.selectbox("Олинган валюта:", ALL_CURRENCIES, index=ALL_CURRENCIES.index(report["Берилди"]), key=f"h_gc_{idx}")
                        edit_g_a = st.number_input("Олинган миқдор:", value=float(report["Миқдор"]), key=f"h_ga_{idx}")
                        edit_get_c = st.selectbox("Берилган валюта:", ALL_CURRENCIES, index=ALL_CURRENCIES.index(report["Олинди"]), key=f"h_getc_{idx}")
                        edit_get_a = st.number_input("Берилган миқдор:", value=float(report["Берилган Миқдор"]), key=f"h_geta_{idx}")
                        edit_comm = st.text_input("Изоҳ:", value=report["Изоҳ"], key=f"h_comm_{idx}")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("💾 Сақлаш", key=f"save_h_{idx}", type="primary", use_container_width=True):
                                st.session_state.kassa[report["Берилди"]] -= report["Миқдор"]
                                st.session_state.kassa[report["Олинди"]] += report["Берилган Миқдор"]
                                
                                st.session_state.history[idx].update({
                                    "Берилди": edit_g_c, "Миқдор": edit_g_a,
                                    "Олинди": edit_get_c, "Берилган Миқдор": edit_get_a, "Изоҳ": edit_comm
                                })
                                st.session_state.kassa[edit_g_c] += edit_g_a
                                st.session_state.kassa[edit_get_c] -= edit_get_a
                                st.success("Янгиланди!")
                                st.rerun()
                        with c2:
                            if st.button("🗑️ Ўчириш", key=f"del_h_{idx}", type="primary", use_container_width=True):
                                st.session_state.kassa[report["Берилди"]] -= report["Миқдор"]
                                st.session_state.kassa[report["Олинди"]] += report["Берилган Миқдор"]
                                st.session_state.history.pop(idx)
                                st.warning("Ўчирилди!")
                                st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Ҳисоботлар мавжуд эмас.")

    # ==================== ОЙНА 3: ҚАРЗ ДАФТАРИ ====================
    elif st.session_state.current_page == "📕 Қарз Дафтари":
        q1, q2 = st.columns([1, 3])
        with q1:
            st.markdown("#### ➕ Янги Қарз Бериш")
            d_name = st.text_input("Қарздор исми:")
            d_phone = st.text_input("Телефон рақами:", "+996")
            d_curr = st.selectbox("Валюта:", ALL_CURRENCIES)
            d_amount = st.number_input("Қарз миқдори:", min_value=0.0)
            if st.button("💾 Қарзни Сақлаш", type="primary", use_container_width=True):
                if d_name and d_amount > 0:
                    st.session_state.debts.append({
                        "ID": len(st.session_state.debts) + 1, "Сана": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Исм": d_name, "Телефон": d_phone, "Валюта": d_curr, 
                        "Аслий Қарз": d_amount, "Қолдиқ Қарз": d_amount, "Ҳолат": "Тўланмаган", "Тўловлар Тарихи": []
                    })
                    st.session_state.kassa[d_curr] -= d_amount
                    st.success("Қарз сақланди ва кассадан чиқим қилинди!")
                    st.rerun()
                    
        with q2:
            st.markdown("#### 📋 Қарздорлар Жадвали")
            if st.session_state.debts:
                d_headers = st.columns([1, 1.5, 1, 1, 1, 1, 2])
                d_titles = ["Исм", "Тел / Сана", "Валюта", "Аслий Қарз", "Қолдиқ", "Ҳолат", "Амал ва Тарих"]
                for i, t in enumerate(d_titles):
                    d_headers[i].markdown(f"<div class='custom-table-header'>{t}</div>", unsafe_allow_html=True)
                
                for d_idx, debt in enumerate(st.session_state.debts):
                    d_cols = st.columns([1, 1.5, 1, 1, 1, 1, 2])
                    d_cols[0].write(f"**{debt['Исм']}**")
                    d_cols[1].write(f"{debt['Телефон']}\n{debt['Сана']}")
                    d_cols[2].write(debt['Валюта'])
                    d_cols[3].write(f"{debt['Аслий Қарз']:,}")
                    d_cols[4].write(f"**{debt['Қолдиқ Қарз']:,}**")
                    d_cols[5].write("🔴 Тўланмаган" if debt["Ҳолат"] == "Тўланмаган" else "🟢 Ёпилган")
                    
                    with d_cols[6]:
                        with st.popover("👁️ Тарих / Тўлов", use_container_width=True):
                            if debt["Тўловлар Тарихи"]:
                                for t in debt["Тўловлар Тарихи"]: st.caption(t)
                            else: st.caption("🚫 Тарих бўш.")
                                
                            if debt["Ҳолат"] == "Тўланмаган":
                                pay_amount = st.number_input(f"Сумма ({debt['Валюта']}):", min_value=0.0, max_value=float(debt["Қолдиқ Қарз"]), key=f"pay_val_{d_idx}")
                                if st.button("✅ Тўловни тасдиқлаш", key=f"btn_pay_{d_idx}", type="primary", use_container_width=True):
                                    if pay_amount > 0:
                                        st.session_state.debts[d_idx]["Қолдиқ Қарз"] -= pay_amount
                                        st.session_state.kassa[debt["Валюта"]] += pay_amount
                                        st.session_state.debts[d_idx]["Тўловлар Тарихи"].append(f"✅ {datetime.now().strftime('%m-%d %H:%M')} куни {pay_amount} {debt['Валюта']} қайтарилди.")
                                        if st.session_state.debts[d_idx]["Қолдиқ Қарз"] <= 0: 
                                            st.session_state.debts[d_idx]["Ҳолат"] = "Тўлиқ ёпилди"
                                        st.success("Касса янгиланди!")
                                        st.rerun()
                                        
                            if st.button("🗑️ Ўчириш", key=f"del_debt_{d_idx}", type="secondary", use_container_width=True):
                                st.session_state.kassa[debt["Валюта"]] += debt["Қолдиқ Қарз"]
                                st.session_state.debts.pop(d_idx)
                                st.rerun()
            else:
                st.info("Қарздорлар рўйхати бўш.")

    # ==================== ОЙНА 4: ХАРАЖАТЛАР ====================
    elif st.session_state.current_page == "📉 Харажатлар":
        ex1, ex2 = st.columns([1, 2])
        with ex1:
            st.markdown("#### ➕ Харажат киритиш")
            ex_curr = st.selectbox("Валюта:", ALL_CURRENCIES)
            ex_amount = st.number_input("Миқдор:", min_value=0.0)
            ex_reason = st.text_input("Сабаб:")
            if st.button("📉 Сақлаш", type="primary", use_container_width=True):
                if ex_amount > 0 and ex_reason:
                    st.session_state.kassa[ex_curr] -= ex_amount
                    st.session_state.expenses.append({"Вақт": datetime.now().strftime("%Y-%m-%d %H:%M"), "Ходим": user_name, "Дўкон": shop, "Валюта": ex_curr, "Миқдор": ex_amount, "Сабаб": ex_reason})
                    st.success("Харажат кассадан чиқим қилинди!")
                    st.rerun()
        with ex2:
            st.markdown("#### 📋 Харажатлар рўйхати")
            if st.session_state.expenses: st.dataframe(pd.DataFrame(st.session_state.expenses), use_container_width=True)
            else: st.info("Харажатлар йўқ.")

    # ==================== ОЙНА 5: КУРСЛАРНИ СОЗЛАШ ====================
    elif st.session_state.current_page == "⚙️ Курсларни Созлаш":
        c_edit = st.selectbox("Валютани танланг:", ALL_CURRENCIES[1:])
        n_buy = st.number_input("Янги ОЛИШ курси:", value=st.session_state.rates[c_edit]["buy"], format="%.4f")
        n_sell = st.number_input("Янги СОТИШ курси:", value=st.session_state.rates[c_edit]["sell"], format="%.4f")
        if st.button("💾 Курсни Сақлаш", type="primary"):
            st.session_state.rates[c_edit]["buy"] = n_buy
            st.session_state.rates[c_edit]["sell"] = n_sell
            st.success("Курслар янгиланди!")
            st.rerun()

    # ==================== ОЙНА 6: ДЎКОНЛАРНИ БОШҚАРИШ ====================
    elif st.session_state.current_page == "🏢 Дўконларни Бошқариш":
        sh1, sh2 = st.columns([1, 2])
        with sh1:
            st.markdown("#### ➕ Янги Дўкон/Филиал Қўшиш")
            new_shop_name = st.text_input("Дўкон (филиал) номини киритинг:", placeholder="Масалан: Марказ")
            if st.button("🏢 Филиални Сақлаш", type="primary", use_container_width=True):
                if new_shop_name.strip() == "":
                    st.error("Филиал номи бўш бўлиши мумкин эмас!")
                elif new_shop_name in st.session_state.shops:
                    st.warning("Бу номдаги филиал аллақачон мавжуд!")
                else:
                    st.session_state.shops.append(new_shop_name.strip())
                    st.success(f"✅ '{new_shop_name}' филиали муваффақиятли қўшилди!")
                    st.rerun()
        with sh2:
            st.markdown("#### 📋 Мавжуд Филиаллар Рўйхати")
            if st.session_state.shops:
                for s_idx, s_name in enumerate(st.session_state.shops):
                    s_col1, s_col2 = st.columns([3, 1])
                    s_col1.write(f"📍 **{s_name} филиали**")
                    if s_col2.button("🗑️ Ўчириш", key=f"del_shop_{s_idx}", type="secondary"):
                        st.session_state.shops.pop(s_idx)
                        st.warning(f"'{s_name}' ўчирилди!")
                        st.rerun()
            else:
                st.info("Ҳеч қандай филиал мавжуд эмас.")

    # ==================== ОЙНА 7: ХОДИМЛАРНИ БОШҚАРИШ ====================
    elif st.session_state.current_page == "👤 Ходимларни Бошқариш":
        emp_tab1, emp_tab2 = st.tabs(["📋 Ходимлар Рўйхати", "➕ Янги Ходим Қўшиш"])
        
        with emp_tab2:
            st.markdown("#### 👤 Янги Ходимни Ишга Рўйхатдан Ўтказиш")
            e_name = st.text_input("Ходим исм-шарифи:")
            e_phone = st.text_input("Телефон рақами (Масалан: +996...):")
            e_gmail = st.text_input("Gmail манзили:")
            e_passport = st.text_input("Паспорт серияси ва рақами:")
            e_avatar = st.text_input("Профиль сурати учун ҳавола (URL):", "https://img.icons8.com/color/144/user-male-circle--v1.png")
            e_pass = st.text_input("Тизимга кириш пароли:", type="password")
            
            if st.button("👤 Ходимни Базага Қўшиш", type="primary"):
                if e_name and e_phone and e_pass:
                    st.session_state.employees.append({
                        "Исм": e_name, "Телефон": e_phone, "Gmail": e_gmail,
                        "Паспорт": e_passport, "Сурат": e_avatar, "Пароль": e_pass
                    })
                    st.success(f"✅ Ходим {e_name} муваффақиятли қўшилди!")
                    st.rerun()
                else:
                    st.error("Илтимос, мажбурий майдонларни тўлдиринг!")
                    
        with emp_tab1:
            st.markdown("#### 👥 Тизимдаги Фаол Ходимлар")
            if st.session_state.employees:
                for idx, emp in enumerate(st.session_state.employees):
                    with st.container():
                        st.markdown(f"""
                            <div class="emp-card">
                                <table style="width:100%; border:none; border-collapse:collapse;">
                                    <tr>
                                        <td style="width:100px; vertical-align:middle; border:none;">
                                            <img src="{emp.get('Сурат', 'https://via.placeholder.com/150')}" width="80" style="border-radius:50%; border:2px solid #0284c7;"/>
                                        </td>
                                        <td style="vertical-align:middle; padding-left:15px; border:none;">
                                            <h4 style="margin:0; color:#0f172a;">{emp['Исм']}</h4>
                                            <p style="margin:4px 0; font-size:14px; color:#475569;">
                                                📞 <b>Тел:</b> {emp['Телефон']} | 📧 <b>Имейл:</b> {emp.get('Gmail','Киритилмаган')}<br>
                                                🪪 <b>Паспорт:</b> {emp.get('Паспорт','Киритилмаган')} | 🔑 <b>Кириш коди:</b> <code style="background:#f1f5f9; padding:2px 6px; border-radius:4px;">{emp.get('Пароль','****')}</code>
                                            </p>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"🗑️ {emp['Исм']}ни ишдан бўшатиш", key=f"del_emp_{idx}", type="secondary"):
                            st.session_state.employees.pop(idx)
                            st.warning(f"Ходим {emp['Исм']} базадан ўчирилди!")
                            st.rerun()
            else:
                st.info("Рўйхатда ҳеч қандай ходим топилмади.")
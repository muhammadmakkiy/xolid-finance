import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# --- BOT VA STRUKTURA SOZLAMALARI ---
TELEGRAM_TOKEN = "8880605493:AAHUPiaafyOONlrKiZoJN5TBKLOaYHAKTug"
ADMIN_ID = 5115206272  # Telegram ID raqamingiz

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- MA'LUMOTLAR BAZASI TIZIMI (XATOLIK TUZATILDI) ---
conn = sqlite3.connect("muhammad_makkiy_bot.db", check_same_thread=False)
cursor = conn.cursor()

# Jadvalni yaratish
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        lang TEXT DEFAULT 'uz'
    )
""")
conn.commit()

# ESKI BAZADA 'lang' USTUNI BO'LMASA, UNI QO'SHISH (ALTER TABLE)
try:
    cursor.execute("SELECT lang FROM users LIMIT 1")
except sqlite3.OperationalError:
    # Agar ustun bo'lmasa, xato beradi va shu yerda ustunni qo'shamiz
    cursor.execute("ALTER TABLE users ADD COLUMN lang TEXT DEFAULT 'uz'")
    conn.commit()
    print("Bazaga 'lang' ustuni muvaffaqiyatli qo'shildi.")

def add_user(user_id, username, full_name):
    try:
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, full_name, lang) VALUES (?, ?, ?, 'uz')", (user_id, username, full_name))
        conn.commit()
    except Exception as e:
        print(f"Baza xatosi (add_user): {e}")

def set_user_lang(user_id, lang):
    try:
        cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
        conn.commit()
    except Exception as e:
        print(f"Baza xatosi (set_user_lang): {e}")

def get_user_lang(user_id):
    try:
        cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else "uz"
    except Exception as e:
        print(f"Baza xatosi (get_user_lang): {e}")
        return "uz"


# --- MULTILINGUAL (KO'P TILLI) LUG'AT ---
LANGUAGES = {
    "uz": {
        "welcome": "✨ **Assalomu alaykum va rahmatullohi va barakatuh!**\n\n**Muhammad Makkiy Group** rasmiy botiga xush kelibsiz!",
        "main_menu": "✨ **Asosiy menyudasiz.** Quyidagi bo'limlardan birini tanlang.",
        "btn_calc": "🧮 Paket Kalkulyatori",
        "btn_hotels": "🏨 Mehmonxonalar",
        "btn_visa": "📄 Viza xizmatlari",
        "btn_trans": "🚌 Transport xizmati",
        "btn_tickets": "🎫 Aviachiptalar",
        "btn_food": "🇺🇿 O'zbek milliy taomlari",
        "btn_other": "⚙️ Boshqa xizmatlar",
        "btn_about": "ℹ️ Biz haqimizda",
        "btn_order": "📝 Ariza qoldirish",
        "contact_admin": "✉️ Admin bilan bog'lanish",
        "back": "⬅️ Ortga qaytish",
        "cancel": "❌ Bekor qilish",
        "back_main": "⬅️ Asosiy menyuga qaytish",
        "choose_city": "✨ Mehmonxona shahrini tanlang:",
        "mecca_hotels": "🕋 Makka Mehmonxonalari",
        "madina_hotels": "🕌 Madina Mehmonxonalari",
        "visa_title": "📄 **Viza xizmatlari turlari va narxlari:**",
        "trans_title": "🚌 **Professional transport xizmatlarimiz va tariflar:**",
        "other_title": "⚙️ **Qo'shimcha va xayriya xizmatlari:**",
        "about_text": "ℹ️ **Muhammad Makkiy Group** — 15 yillik ishonchli ziyorat xizmati.",
        "step_1_visa": "🧮 **Paket kalkulyatori**\n\n1-Bosqich: **Viza turini tanlang:**",
        "step_2_hotel": "2-Bosqich: **Mehmonxona toifasini tanlang:**",
        "step_3_food": "3-Bosqich: **Kunlik 3 mahal milliy taomlar xizmati kerakmi?**",
        "step_4_trans": "4-Bosqich: **Qaysi turdagi transport xizmati kerak?**",
        "yes_food": "🍲 Ha (3 mahal o'zbek taomlari)",
        "no_food": "❌ Yo'q (Ovqat kerak emas)",
        "no_trans": "❌ Transport kerak emas",
        "write_name": "Joy band qilish va ariza yuborish uchun ism-sharifingizni yozib yuboring:",
        "send_phone_btn": "📱 Telefon raqamni yuborish",
        "ask_phone": "Rahmat! Endi pastdagi tugma orqali telefon raqamingizni jo'nating:",
        "send_receipt_btn": "🧾 Chekni (Kvitansiyani) yuborish",
        "ask_receipt_photo": "🤖 Iltimos, to'lovingiz kvitansiyasini (skrinshot yoki rasmini) botga yuboring:",
        "receipt_success": "✅ Rahmat! Chek adminga yuborildi.",
        "ticket_step_1": "🎫 **Aviachipta qidirish tizimi**\n\n1-Bosqich: **Uchish shahrini tanlang:**",
        "ticket_step_2": "2-Bosqich: **Qo'nish shahrini tanlang:**",
        "ticket_step_3": "3-Bosqich: **Uchish oyini tanlang:**",
        "ticket_step_4": "4-Bosqich: **Uchish kunini tanlang:**",
        "ticket_success": "✅ Aviachipta uchun arizangiz muvaffaqiyatli qabul qilindi!\nTez orada operatorlarimiz eng maqbul variantlar bilan sizga aloqaga chiqishadi.",
        "order_start": "🤖 Arizangizni adminga yetkazish uchun ism-sharifingizni kiriting:",
        "order_success": "✅ Arizangiz muvaffaqiyatli yuborildi! Tez orada operatorlarimiz bog'lanishadi.",
        
        # Ichki ma'lumotlar tarjimalari
        "v_tourist": "✈️ **Sayohat (Turistik) vizasi**\n\n💰 Narxi: **120 USD** (1 kishi uchun)\n⚡️ Tayyor bo'lish muddati juda qisqa.",
        "v_umrah_ind": "🕋 **Umra vizasi (Alohida)**\n\n💰 Narxi: **160 USD** (1 kishi uchun alohida rasmiylashtirilganda).",
        "v_umrah_grp": "👥 **Umra vizasi (Guruh uchun)**\n\n💰 Narxi: **150 USD** (Guruh bo'lib topshirilganda 1 kishi uchun maxsus chegirmali narx).",
        
        "t_bus": "🚌 **Avtobus xizmati (Katta guruhlar uchun)**\n\n• Yili: **2026-yil** yangi shinam model\n• Sig'imi: **52 kishilik**\n💰 Narxi: **720$ (2700 SR)**",
        "t_hiace": "🚐 **Toyota Hiace xizmati**\n\n• Yili: **2026-yil** oilaviy va kichik guruhbop\n• Sig'imi: **12 kishilik**\n💰 Narxi: **615$ (2300 SR)**",
        "t_gmc": "⭐ **VIP GMC Yukon / Suburban**\n\n• Yili: **2026-yil** premium klass premium qulaylik\n• Sig'imi: **7 kishilik**\n💰 Narxi: **1000$ (3750 SR)**",
        "t_carnival": "🚗 **Kia Carnival xizmati**\n\n• Yili: **2024-yil** zamonaviy shinam transport\n• Sig'imi: **7 kishilik**\n💰 Narxi: **700$ (2600 SR)**",
        "t_taxi": "🚖 **Standart Taxi xizmati (Sedan)**\n\n• Yili: **2026-yil** tezkor va qulay\n• Sig'imi: **5 kishilik**\n💰 Narxi: **500$ (1850 SR)**",
        
        "s_umra": "🕋 **Umra badal qilish xizmati**\n\n💰 Qiymati: **100 USD**\n✨ Uzrli sabablarga ko'ra o'zi kela olmaydiganlar yoki o'tganlar nomidan Umra amalini ishonchli vakillar orqali ado etish.",
        "s_xurmo": "🌴 **Xurmo daraxti ektirish**\n\n💰 Qiymati: **200 USD**\n✨ Muborak zaminlarda sizning nomingizdan serhosil xurmo ko'chati o'tqaziladi (Sadaqai joriya).",
        "s_quron": "📖 **Qur'on vaqf qilish xizmati**\n\n💰 Qiymati: **15 USD**\n✨ Muqaddas masjidlarga Qur'oni Karim vaqf qilinadi.",
        "s_ehson": "🍲 **Miskinlarga ehson bo'limi (Taomlantirish)**\n\n💰 Qiymati: **3 - 5 USD**\n✨ Haram atrofidagi va muhtoj miskinlarga issiq taom ulashish xayriya loyihasi.",
        "s_qurbonlik": "🐐 **Qurbonlik qilish**\n\n💰 Qiymati: **200 USD**\n✨ Islomiy shartlarga to'liq amal qilgan holda qurbonlik so'yilib, go'shtlari tarqatiladi."
    },
    "ru": {
        "welcome": "✨ **Ассалому алайкум ва рахматуллохи ва баракатух!**\n\nДобро пожаловать на официальный бот **Muhammad Makkiy Group**!",
        "main_menu": "✨ **Вы в главном меню.** Выберите один из разделов ниже.",
        "btn_calc": "🧮 Калькулятор пакета",
        "btn_hotels": "🏨 Отели",
        "btn_visa": "📄 Визовые услуги",
        "btn_trans": "🚌 Транспортные услуги",
        "btn_tickets": "🎫 Авиабилеты",
        "btn_food": "🇺🇿 Узбекская национальная кухня",
        "btn_other": "⚙️ Другие услуги",
        "btn_about": "ℹ️ О нас",
        "btn_order": "📝 Оставить заявку",
        "contact_admin": "✉️ Связаться с админом",
        "back": "⬅️ Назад",
        "cancel": "❌ Отмена",
        "back_main": "⬅️ В главное меню",
        "choose_city": "✨ Выберите город отеля:",
        "mecca_hotels": "🕋 Отели Мекки",
        "madina_hotels": "🕌 Отели Медины",
        "visa_title": "📄 **Виды и стоимость визовых услуг:**",
        "trans_title": "🚌 **Наши профессиональные транспортные услуги и тарифы:**",
        "other_title": "⚙️ **Дополнительные и благотворительные услуги:**",
        "about_text": "ℹ️ **Muhammad Makkiy Group** — 15 лет надежного паломнического сервиса.",
        "step_1_visa": "🧮 **Калькулятор пакета**\n\nШаг 1: **Выберите тип визы:**",
        "step_2_hotel": "Шаг 2: **Выберите категорию отеля:**",
        "step_3_food": "Шаг 3: **Нужно ли 3-разовое национальное питание?**",
        "step_4_trans": "Шаг 4: **Какой вид транспорта вам необходим?**",
        "yes_food": "🍲 Да (3-разовое узбекское питание)",
        "no_food": "❌ Нет (Питание не нужно)",
        "no_trans": "❌ Транспорт не нужен",
        "write_name": "Для бронирования и отправки заявки введите свое имя и фамилию:",
        "send_phone_btn": "📱 Отправить номер телефона",
        "ask_phone": "Спасибо! Теперь отправьте свой номер телефона с помощью кнопки ниже:",
        "send_receipt_btn": "🧾 Отправить чек (квитанцию)",
        "ask_receipt_photo": "🤖 Пожалуйста, отправьте скриншот или фото квитанции об оплате в бот:",
        "receipt_success": "✅ Спасибо! Чек отправлен администратору.",
        "ticket_step_1": "🎫 **Система поиска авиабилетов**\n\nШаг 1: **Выберите город вылета:**",
        "ticket_step_2": "Шаг 2: **Выберите город прибытия:**",
        "ticket_step_3": "Шаг 3: **Выберите месяц вылета:**",
        "ticket_step_4": "Шаг 4: **Выберите день вылета:**",
        "ticket_success": "✅ Ваша заявка на авиабилет успешно принята!\nВ ближайшее время наши операторы свяжутся с вами.",
        "order_start": "🤖 Для отправки заявки админу введите свое имя и фамилию:",
        "order_success": "✅ Ваша заявка успешно отправлена! Скоро с вами свяжутся.",
        
        # Ichki ma'lumotlar tarjimalari
        "v_tourist": "✈️ **Туристическая виза**\n\n💰 Цена: **120 USD** (за 1 человека)\n⚡️ Очень короткие сроки оформления.",
        "v_umrah_ind": "🕋 **Умра виза (Индивидуальная)**\n\n💰 Цена: **160 USD** (при индивидуальном оформлении).",
        "v_umrah_grp": "👥 **Умра виза (Для группы)**\n\n💰 Цена: **150 USD** (специальная скидка на 1 человека при подаче группой).",
        
        "t_bus": "🚌 **Услуги автобуса (Для больших групп)**\n\n• Год: **2026**, новая комфортабельная модель\n• Вместимость: **52 места**\n💰 Цена: **720$ (2700 SR)**",
        "t_hiace": "🚐 **Услуги Toyota Hiace**\n\n• Год: **2026**, для семей и небольших групп\n• Вместимость: **12 мест**\n💰 Цена: **615$ (2300 SR)**",
        "t_gmc": "⭐ **VIP GMC Yukon / Suburban**\n\n• Год: **2026**, премиум класс и максимальный комфорт\n• Вместимость: **7 мест**\n💰 Цена: **1000$ (3750 SR)**",
        "t_carnival": "🚗 **Услуги Kia Carnival**\n\n• Год: **2024**, современный минивэн\n• Вместимость: **7 мест**\n💰 Цена: **700$ (2600 SR)**",
        "t_taxi": "🚖 **Стандартное такси (Седан)**\n\n• Год: **2026**, быстро и удобно\n• Вместимость: **5 мест**\n💰 Цена: **500$ (1850 SR)**",
        
        "s_umra": "🕋 **Умра Бадаль (Умра за другого человека)**\n\n💰 Стоимость: **100 USD**\n✨ Совершение Умры надежными доверенными лицами за тех, кто не может приехать сам или за усопших.",
        "s_xurmo": "🌴 **Посадка финиковой пальмы**\n\n💰 Стоимость: **200 USD**\n✨ От вашего имени на благословенной земле будет посажен саженец пальмы (Садака-и-джария).",
        "s_quron": "📖 **Вакф Корана (Благотворительность)**\n\n💰 Стоимость: **15 USD**\n✨ Оригинальные мусхафы будут переданы в дар священным мечетям.",
        "s_ehson": "🍲 **Раздача еды нуждающимся**\n\n💰 Стоимость: **3 - 5 USD**\n✨ Проект раздачи горячего питания беднякам и нуждающимся вокруг Харама.",
        "s_qurbonlik": "🐐 **Жертвоприношение (Курбанлик)**\n\n💰 Стоимость: **200 USD**\n✨ Заклание животного с полным соблюдением исламских правил и раздача мяса нуждающимся."
    },
    "en": {
        "welcome": "✨ **Assalamu alaykum wa rahmatullahi wa barakatuh!**\n\nWelcome to the official bot of **Muhammad Makkiy Group**!",
        "main_menu": "✨ **You are in the main menu.** Select one of the sections below.",
        "btn_calc": "🧮 Package Calculator",
        "btn_hotels": "🏨 Hotels",
        "btn_visa": "📄 Visa Services",
        "btn_trans": "🚌 Transport Services",
        "btn_tickets": "🎫 Flight Tickets",
        "btn_food": "🇺🇿 Uzbek National Food",
        "btn_other": "⚙️ Other Services",
        "btn_about": "ℹ️ About Us",
        "btn_order": "📝 Leave an Application",
        "contact_admin": "✉️ Contact Admin",
        "back": "⬅️ Back",
        "cancel": "❌ Cancel",
        "back_main": "⬅️ Back to Main Menu",
        "choose_city": "✨ Choose the hotel city:",
        "mecca_hotels": "🕋 Mecca Hotels",
        "madina_hotels": "🕌 Medina Hotels",
        "visa_title": "📄 **Visa services types and prices:**",
        "trans_title": "🚌 **Our professional transport services and rates:**",
        "other_title": "⚙️ **Additional and charitable services:**",
        "about_text": "ℹ️ **Muhammad Makkiy Group** — 15 years of reliable pilgrimage services.",
        "step_1_visa": "🧮 **Package Calculator**\n\nStep 1: **Choose visa type:**",
        "step_2_hotel": "Step 2: **Choose hotel category:**",
        "step_3_food": "Step 3: **Do you need 3-time daily national food service?**",
        "step_4_trans": "Step 4: **What type of transport do you need?**",
        "yes_food": "🍲 Yes (3-time Uzbek food)",
        "no_food": "❌ No (Food not needed)",
        "no_trans": "❌ Transport not needed",
        "write_name": "Please enter your full name to book and send your application:",
        "send_phone_btn": "📱 Send phone number",
        "ask_phone": "Thank you! Now send your phone number using the button below:",
        "send_receipt_btn": "🧾 Send Receipt (Invoice)",
        "ask_receipt_photo": "🤖 Please send a screenshot or photo of your payment receipt to the bot:",
        "receipt_success": "✅ Thank you! The receipt has been sent to the admin.",
        "ticket_step_1": "🎫 **Flight ticket search system**\n\nStep 1: **Select departure city:**",
        "ticket_step_2": "Step 2: **Select arrival city:**",
        "ticket_step_3": "Step 3: **Select departure month:**",
        "ticket_step_4": "Step 4: **Select departure day:**",
        "ticket_success": "✅ Your flight ticket application has been successfully received!\nOur operators will contact you shortly.",
        "order_start": "🤖 Enter your full name to submit your application to the admin:",
        "order_success": "✅ Your application has been successfully submitted! We will contact you soon.",
        
        # Ichki ma'lumotlar tarjimalari
        "v_tourist": "✈️ **Tourist Visa**\n\n💰 Price: **120 USD** (per person)\n⚡️ Very fast processing time.",
        "v_umrah_ind": "🕋 **Umrah Visa (Individual)**\n\n💰 Price: **160 USD** (when registered individually).",
        "v_umrah_grp": "👥 **Umrah Visa (For Group)**\n\n💰 Price: **150 USD** (special discounted price per person when submitting as a group).",
        
        "t_bus": "🚌 **Bus Service (For large groups)**\n\n• Year: **2026** new comfortable model\n• Capacity: **52 seats**\n💰 Price: **720$ (2700 SR)**",
        "t_hiace": "🚐 **Toyota Hiace Service**\n\n• Year: **2026** for families and small groups\n• Capacity: **12 seats**\n💰 Price: **615$ (2300 SR)**",
        "t_gmc": "⭐ **VIP GMC Yukon / Suburban**\n\n• Year: **2026** premium class maximum comfort\n• Capacity: **7 seats**\n💰 Price: **1000$ (3750 SR)**",
        "t_carnival": "🚗 **Kia Carnival Service**\n\n• Year: **2024** modern comfortable transport\n• Capacity: **7 seats**\n💰 Price: **700$ (2600 SR)**",
        "t_taxi": "🚖 **Standart Taxi Service (Sedan)**\n\n• Year: **2026** fast and convenient\n• Capacity: **5 seats**\n💰 Price: **500$ (1850 SR)**",
        
        "s_umra": "🕋 **Umra Badal Service**\n\n💰 Cost: **100 USD**\n✨ Performing Umrah by trusted proxies on behalf of those who cannot come or deceased ones.",
        "s_xurmo": "🌴 **Planting a Date Palm**\n\n💰 Cost: **200 USD**\n✨ A date palm sapling will be planted on the blessed land on your behalf (Sadaqah Jariyah).",
        "s_quron": "📖 **Quran Waqf Service**\n\n💰 Cost: **15 USD**\n✨ Original Mushafs will be donated to the holy mosques.",
        "s_ehson": "🍲 **Feeding the Poor (Charity)**\n\n💰 Cost: **3 - 5 USD**\n✨ Charity project providing hot meals to the poor around the Haram.",
        "s_qurbonlik": "🐐 **Sacrifice (Qurbanlik)**\n\n💰 Cost: **200 USD**\n✨ Animal sacrifice fully complying with Islamic rules and distribution of meat to the needy."
    }
}

# --- FSM HOLATLARI ---
class OrderForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()

class CalcStates(StatesGroup):
    choosing_viza = State()
    choosing_hotel = State()
    choosing_food = State()
    choosing_trans = State()
    waiting_for_calc_name = State()
    waiting_for_calc_phone = State()
    waiting_for_receipt = State()

class TicketStates(StatesGroup):
    choosing_from = State()
    choosing_to = State()
    choosing_month = State()
    choosing_day = State()
    waiting_for_ticket_name = State()
    waiting_for_ticket_phone = State()

# --- DOIMIYLAR VA STRUKTURALAR ---
PRICES = {
    "viza_tourist": 120,    
    "viza_umrah_ind": 160,  
    "viza_umrah_grp": 150,  
    "hotel_vip": 500,
    "hotel_std": 250,
    "hotel_eco": 120,
    "food_yes": 90,
    "food_no": 0,
    "trans_bus": 720,        
    "trans_hiace": 615,      
    "trans_gmc": 1000,       
    "trans_carnival": 700,   
    "trans_taxi": 500,       
    "trans_no": 0
}

TRANSPORT_NAMES = {
    "bus": "🚌 Avtobus 2026-yil (720$ / 2700 SR)",
    "hiace": "🚐 Toyota Hiace 2026-yil (615$ / 2300 SR)",
    "gmc": "⭐ VIP GMC 2026-yil (1000$ / 3750 SR)",
    "carnival": "🚗 Kia Carnival 2024-yil (700$ / 2600 SR)",
    "taxi": "🚖 Standart Taxi 2026-yil (500$ / 1850 SR)",
    "no": "❌ Kerak emas / Not needed"
}

TICKET_OPTIONS = {
    "Toshkent-Jedda": "550 USD",
    "Toshkent-Madina": "570 USD",
    "Namangan-Jedda": "540 USD",
    "Namangan-Madina": "560 USD",
    "Farg'ona-Jedda": "545 USD",
    "Farg'ona-Madina": "565 USD",
    "Andijon-Jedda": "550 USD",
    "Samarqand-Jedda": "530 USD"
}

CITIES_FROM = ["Toshkent", "Namangan", "Farg'ona", "Andijon", "Samarqand"]
CITIES_TO = ["Madina", "Jedda"]
MONTHS = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]

BANK_REKVIZITLARI = (
    "💳 **To'lov rekvizitlari / Payment details:**\n\n"
    "🇺🇿 **Uzcard/Humo:** `8600 1234 5678 9012` (F.I.SH)\n"
    "🇸🇦 **Al Rajhi Bank (SAR IBAN):** `SA12345678901234567890` (Muhammad Makkiy Group)\n\n"
    "⚠️ *To'lovni amalga oshirib, pastdagi tugma orqali chekni (kvitansiyani) yuboring.*"
)

ADMIN_CONTACTS = (
    "\n\n📞 **Murojaat uchun aloqa / Contacts:**\n"
    "💬 Telegram: [Muhammad Makkiy Group](https://t.me/Muhammad_Romiz)\n"
    "🟢 WhatsApp: [WhatsApp](https://wa.me/966500475023)\n"
    "📞 Telefon: +966500475023"
)

HADIS_TEXT = (
    "\n\n*Abu Hurayra r.a.dan rivoyat qilinadi:*\n"
    "«Inson vafot etganida uning amali to‘xtaydi, faqat uchta narsadan unga savob yetib turadi: "
    "joriya (davomli) sadaqa, manfaat keltiradigan ilm yoki uning haqiga duo qiladigan solih farzand».\n"
    "_(Imom Muslim rivoyati)_"
)

FOOD_TEXT = (
    "🇺🇿 **UZBEK HOUSE — Makkai Mukarramada Vatandoshlarimiz Uchun Maxsus Oshxona!**\n\n"
    "Muborak zaminlarda ziyorat amallarini ado etish davomida sog'lom va quvvatli bo'lishingiz uchun o'z uyingizdek shinam sharoitda, halol va milliy taomlarimizni taqdim etamiz!\n\n"
    "💰 **Siz uchun maxsus narx:** Kuniga 3 mahal issiq taom atigi **30 SAR (Riyol)**!\n"
    "⚡️ **Yetkazib berish mutlaqo bepul!**\n\n"
    "📋 **Taomnomamiz:** Nonushta, Tushlik (Palov/Sho'rva), Kechki ovqat (Lag'mon/Somsa)."
)


# --- REPLY ASOSIY MENYU (TILLI) ---
def get_main_reply_menu(lang: str):
    builder = ReplyKeyboardBuilder()
    builder.button(text=LANGUAGES[lang]["btn_calc"])
    builder.button(text=LANGUAGES[lang]["btn_hotels"])
    builder.button(text=LANGUAGES[lang]["btn_visa"])
    builder.button(text=LANGUAGES[lang]["btn_trans"])
    builder.button(text=LANGUAGES[lang]["btn_tickets"])
    builder.button(text=LANGUAGES[lang]["btn_food"])
    builder.button(text=LANGUAGES[lang]["btn_other"])
    builder.button(text=LANGUAGES[lang]["btn_about"])
    builder.button(text=LANGUAGES[lang]["btn_order"])
    builder.adjust(1, 2, 2, 2, 2)
    return builder.as_markup(resize_keyboard=True)


# --- INLINE MENYULAR VA TUGMALAR ---
def get_lang_inline_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    builder.adjust(1)
    return builder.as_markup()

def get_action_inline_buttons(lang: str, back_callback: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=LANGUAGES[lang]["contact_admin"], url="https://t.me/Muhammad_Romiz")
    builder.button(text=LANGUAGES[lang]["back"], callback_data=back_callback)
    builder.adjust(1)
    return builder.as_markup()

def get_inline_builder(items, prefix, back_cb, lang: str):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=str(item), callback_data=f"{prefix}_{item}")
    builder.button(text=LANGUAGES[lang]["cancel"], callback_data=back_cb)
    builder.adjust(2)
    return builder.as_markup()

def get_cities_inline(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=LANGUAGES[lang]["mecca_hotels"], callback_data="city_mecca")
    builder.button(text=LANGUAGES[lang]["madina_hotels"], callback_data="city_madina")
    builder.button(text=LANGUAGES[lang]["back_main"], callback_data="back_to_main_menu")
    builder.adjust(2, 1)
    return builder.as_markup()

def get_mecca_categories_inline(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="💎 VIP", callback_data="kat_mecca_vip")
    builder.button(text="🏢 Standart", callback_data="kat_mecca_std")
    builder.button(text="📉 Ekonom", callback_data="kat_mecca_eco")
    builder.button(text=LANGUAGES[lang]["back"], callback_data="back_to_cities")
    builder.adjust(1)
    return builder.as_markup()

def get_madina_categories_inline(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="⭐ VIP", callback_data="kat_madina_vip")
    builder.button(text="✨ Standart", callback_data="kat_madina_std")
    builder.button(text="🌙 Ekonom", callback_data="kat_madina_eco")
    builder.button(text=LANGUAGES[lang]["back"], callback_data="back_to_cities")
    builder.adjust(1)
    return builder.as_markup()

def get_hotels_inline(category, lang: str):
    builder = InlineKeyboardBuilder()
    if category == "mecca_vip":
        builder.button(text="🏨 Fairmont Clock Tower", callback_data="hotel_fairmont_mecca_vip")
        builder.button(text="🏨 Swissôtel Makkah", callback_data="hotel_swiss_mecca_vip")
        builder.button(text=LANGUAGES[lang]["back"], callback_data="city_mecca")
    elif category == "mecca_std":
        builder.button(text="🏨 Batul Ajiyat", callback_data="hotel_batul_mecca_std")
        builder.button(text=LANGUAGES[lang]["back"], callback_data="city_mecca")
    elif category == "mecca_eco":
        builder.button(text="🏨 Nuhba 1", callback_data="hotel_nuhba1_mecca_eco")
        builder.button(text=LANGUAGES[lang]["back"], callback_data="city_mecca")
    elif category == "madina_vip":
        builder.button(text="🏨 Oberoi Madina", callback_data="hotel_oberoi_madina_vip")
        builder.button(text=LANGUAGES[lang]["back"], callback_data="city_madina")
    elif category == "madina_std":
        builder.button(text="🏨 Al Aqeeq Madina", callback_data="hotel_aqeeq_madina_std")
        builder.button(text=LANGUAGES[lang]["back"], callback_data="city_madina")
    elif category == "madina_eco":
        builder.button(text="🏨 Diyar Al Madina", callback_data="hotel_diyar_madina_eco")
        builder.button(text=LANGUAGES[lang]["back"], callback_data="city_madina")
    builder.adjust(1)
    return builder.as_markup()

def get_visa_inline(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="✈️ Tourist Visa (120$)", callback_data="visa_tourist")
    builder.button(text="🕋 Umrah Visa (1 Kishi - 160$)", callback_data="visa_umrah_ind")
    builder.button(text="👥 Umrah Visa (Guruh - 150$)", callback_data="visa_umrah_grp")
    builder.button(text=LANGUAGES[lang]["back_main"], callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

def get_transport_inline(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="🚌 Avtobus (720$)", callback_data="trans_bus")
    builder.button(text="🚐 Toyota Hiace (615$)", callback_data="trans_hiace")
    builder.button(text="⭐ VIP GMC (1000$)", callback_data="trans_gmc")
    builder.button(text="🚗 Kia Carnival (700$)", callback_data="trans_carnival")
    builder.button(text="🚖 Standart Taxi (500$)", callback_data="trans_taxi")
    builder.button(text=LANGUAGES[lang]["back_main"], callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()

def get_other_services_inline(lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="🕋 Umra Badal (100$)", callback_data="srv_umra")
    builder.button(text="🌴 Xurmo Daraxti (200$)", callback_data="srv_xurmo")
    builder.button(text="📖 Qur'on Vaqf (15$)", callback_data="srv_quron")
    builder.button(text="🍲 Ehson / Taomlantirish (3-5$)", callback_data="srv_ehson")
    builder.button(text="🐐 Qurbonlik (200$)", callback_data="srv_qurbonlik")
    builder.button(text=LANGUAGES[lang]["back_main"], callback_data="back_to_main_menu")
    builder.adjust(1)
    return builder.as_markup()


# --- BOT HANDLERLARI ---

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer(
        "🌐 **Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please choose a language:**",
        reply_markup=get_lang_inline_menu()
    )

@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    set_user_lang(call.from_user.id, lang)
    
    await call.message.delete()
    await call.message.answer(
        LANGUAGES[lang]["welcome"],
        reply_markup=get_main_reply_menu(lang),
        parse_mode="Markdown"
    )
    await call.answer()


# --- AVIACHIPTALAR TIZIMI ---
@dp.message(F.text.in_([LANGUAGES["uz"]["btn_tickets"], LANGUAGES["ru"]["btn_tickets"], LANGUAGES["en"]["btn_tickets"]]))
async def ticket_start(message: types.Message, state: FSMContext):
    await state.clear()
    lang = get_user_lang(message.from_user.id)
    reply_markup = get_inline_builder(CITIES_FROM, "from", "back_to_main_menu", lang)
    await message.answer(LANGUAGES[lang]["ticket_step_1"], reply_markup=reply_markup)
    await state.set_state(TicketStates.choosing_from)

@dp.callback_query(TicketStates.choosing_from, F.data.startswith("from_"))
async def ticket_from_chosen(call: types.CallbackQuery, state: FSMContext):
    city_from = call.data.split("_")[1]
    await state.update_data(city_from=city_from)
    lang = get_user_lang(call.from_user.id)
    reply_markup = get_inline_builder(CITIES_TO, "to", "back_to_main_menu", lang)
    await call.message.edit_text(LANGUAGES[lang]["ticket_step_2"], reply_markup=reply_markup)
    await state.set_state(TicketStates.choosing_to)
    await call.answer()

@dp.callback_query(TicketStates.choosing_to, F.data.startswith("to_"))
async def ticket_to_chosen(call: types.CallbackQuery, state: FSMContext):
    city_to = call.data.split("_")[1]
    await state.update_data(city_to=city_to)
    lang = get_user_lang(call.from_user.id)
    reply_markup = get_inline_builder(MONTHS, "month", "back_to_main_menu", lang)
    await call.message.edit_text(LANGUAGES[lang]["ticket_step_3"], reply_markup=reply_markup)
    await state.set_state(TicketStates.choosing_month)
    await call.answer()

@dp.callback_query(TicketStates.choosing_month, F.data.startswith("month_"))
async def ticket_month_chosen(call: types.CallbackQuery, state: FSMContext):
    month = call.data.split("_")[1]
    await state.update_data(month=month)
    lang = get_user_lang(call.from_user.id)
    days = [str(i) for i in range(1, 32)]
    reply_markup = get_inline_builder(days, "day", "back_to_main_menu", lang)
    await call.message.edit_text(LANGUAGES[lang]["ticket_step_4"], reply_markup=reply_markup)
    await state.set_state(TicketStates.choosing_day)
    await call.answer()

@dp.callback_query(TicketStates.choosing_day, F.data.startswith("day_"))
async def ticket_day_chosen(call: types.CallbackQuery, state: FSMContext):
    day = call.data.split("_")[1]
    await state.update_data(day=day)
    lang = get_user_lang(call.from_user.id)
    data = await state.get_data()
    route_key = f"{data.get('city_from')}-{data.get('city_to')}"
    price_info = TICKET_OPTIONS.get(route_key, "TBD")
    await state.update_data(ticket_price=price_info)
    
    await call.message.edit_text(
        f"📊 **Route:** {route_key} | **Date:** {day}-{data.get('month')}\n"
        f"💰 **Price:** `{price_info}`\n\n"
        f"{LANGUAGES[lang]['write_name']}"
    )
    await state.set_state(TicketStates.waiting_for_ticket_name)
    await call.answer()

@dp.message(TicketStates.waiting_for_ticket_name)
async def process_ticket_name(message: types.Message, state: FSMContext):
    await state.update_data(ticket_name=message.text)
    lang = get_user_lang(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    builder.button(text=LANGUAGES[lang]["send_phone_btn"], request_contact=True)
    await message.answer(LANGUAGES[lang]["ask_phone"], reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(TicketStates.waiting_for_ticket_phone)

@dp.message(TicketStates.waiting_for_ticket_phone)
async def process_ticket_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    data = await state.get_data()
    lang = get_user_lang(message.from_user.id)
    
    try:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🎫 **AVIACHIPTA SO'ROVI**\n👤 Ism: {data.get('ticket_name')}\n📞 Tel: {phone}\n"
                f"🛫 Yo'nalish: {data.get('city_from')}-{data.get('city_to')}\n📅 Sana: {data.get('day')}-{data.get('month')}"
            )
        )
    except Exception as e:
        print(e)
        
    await state.clear()
    await message.answer(LANGUAGES[lang]["ticket_success"], reply_markup=get_main_reply_menu(lang))


# --- PAKET KALKULYATORI TIZIMI ---
@dp.message(F.text.in_([LANGUAGES["uz"]["btn_calc"], LANGUAGES["ru"]["btn_calc"], LANGUAGES["en"]["btn_calc"]]))
async def start_calculator(message: types.Message, state: FSMContext):
    await state.clear()
    lang = get_user_lang(message.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.button(text="✈️ Sayohat vizasi (120$)", callback_data="calc_viza_tourist")
    builder.button(text="🕋 Umra vizasi (160$)", callback_data="calc_viza_umrah_ind")
    builder.adjust(1)
    await message.answer(LANGUAGES[lang]["step_1_visa"], reply_markup=builder.as_markup())
    await state.set_state(CalcStates.choosing_viza)

@dp.callback_query(CalcStates.choosing_viza, F.data.startswith("calc_viza_"))
async def calc_viza_chosen(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(viza=call.data.replace("calc_viza_", ""))
    lang = get_user_lang(call.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.button(text="💎 VIP", callback_data="calc_hot_vip")
    builder.button(text="🏢 Standart", callback_data="calc_hot_std")
    builder.button(text="📉 Ekonom", callback_data="calc_hot_eco")
    builder.adjust(1)
    await call.message.edit_text(LANGUAGES[lang]["step_2_hotel"], reply_markup=builder.as_markup())
    await state.set_state(CalcStates.choosing_hotel)
    await call.answer()

@dp.callback_query(CalcStates.choosing_hotel, F.data.startswith("calc_hot_"))
async def calc_hotel_chosen(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(hotel=call.data.replace("calc_hot_", ""))
    lang = get_user_lang(call.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.button(text=LANGUAGES[lang]["yes_food"], callback_data="calc_food_yes")
    builder.button(text=LANGUAGES[lang]["no_food"], callback_data="calc_food_no")
    builder.adjust(1)
    await call.message.edit_text(LANGUAGES[lang]["step_3_food"], reply_markup=builder.as_markup())
    await state.set_state(CalcStates.choosing_food)
    await call.answer()

@dp.callback_query(CalcStates.choosing_food, F.data.startswith("calc_food_"))
async def calc_food_chosen(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(food=call.data.replace("calc_food_", ""))
    lang = get_user_lang(call.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.button(text="🚌 Avtobus (720$)", callback_data="calc_trans_bus")
    builder.button(text="🚐 Hiace (615$)", callback_data="calc_trans_hiace")
    builder.button(text=LANGUAGES[lang]["no_trans"], callback_data="calc_trans_no")
    builder.adjust(1)
    await call.message.edit_text(LANGUAGES[lang]["step_4_trans"], reply_markup=builder.as_markup())
    await state.set_state(CalcStates.choosing_trans)
    await call.answer()

@dp.callback_query(CalcStates.choosing_trans, F.data.startswith("calc_trans_"))
async def calc_trans_chosen(call: types.CallbackQuery, state: FSMContext):
    trans = call.data.replace("calc_trans_", "")
    await state.update_data(trans=trans)
    lang = get_user_lang(call.from_user.id)
    data = await state.get_data()
    
    total = PRICES.get(f"viza_{data['viza']}", 0) + PRICES.get(f"hotel_{data['hotel']}", 0) + PRICES.get(f"food_{data['food']}", 0) + PRICES.get(f"trans_{trans}", 0)
    await state.update_data(total_price=total)
    
    await call.message.edit_text(
        f"📊 **TOTAL PRICE:** `{total} USD`\n\n{LANGUAGES[lang]['write_name']}"
    )
    await state.set_state(CalcStates.waiting_for_calc_name)
    await call.answer()

@dp.message(CalcStates.waiting_for_calc_name)
async def process_calc_name(message: types.Message, state: FSMContext):
    await state.update_data(calc_name=message.text)
    lang = get_user_lang(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    builder.button(text=LANGUAGES[lang]["send_phone_btn"], request_contact=True)
    await message.answer(LANGUAGES[lang]["ask_phone"], reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(CalcStates.waiting_for_calc_phone)

@dp.message(CalcStates.waiting_for_calc_phone)
async def process_calc_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(calc_phone=phone)
    lang = get_user_lang(message.from_user.id)
    builder = InlineKeyboardBuilder()
    builder.button(text=LANGUAGES[lang]["send_receipt_btn"], callback_data="send_receipt_now")
    await message.answer(f"{BANK_REKVIZITLARI}", reply_markup=builder.as_markup())
    await state.set_state(CalcStates.waiting_for_receipt)

@dp.callback_query(CalcStates.waiting_for_receipt, F.data == "send_receipt_now")
async def ask_for_receipt_photo(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text(LANGUAGES[lang]["ask_receipt_photo"])
    await call.answer()

@dp.message(CalcStates.waiting_for_receipt, F.photo)
async def process_receipt_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    lang = get_user_lang(message.from_user.id)
    
    try:
        await bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_id,
            caption=f"💰 **YANGI PAKET TO'LOVI!**\n👤 Ism: {data.get('calc_name')}\n📞 Tel: {data.get('calc_phone')}\n💵 Summa: {data.get('total_price')} USD"
        )
    except Exception as e:
        print(e)
    await message.answer(LANGUAGES[lang]["receipt_success"], reply_markup=get_main_reply_menu(lang))
    await state.clear()


# --- HAR TILDAGI BOSHQA XIZMATLAR HANDLERLARI ---
@dp.message(F.text.in_([LANGUAGES["uz"]["btn_hotels"], LANGUAGES["ru"]["btn_hotels"], LANGUAGES["en"]["btn_hotels"]]))
async def reply_hotels(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    await message.answer(LANGUAGES[lang]["choose_city"], reply_markup=get_cities_inline(lang))

@dp.message(F.text.in_([LANGUAGES["uz"]["btn_visa"], LANGUAGES["ru"]["btn_visa"], LANGUAGES["en"]["btn_visa"]]))
async def reply_visa(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    await message.answer(LANGUAGES[lang]["visa_title"], reply_markup=get_visa_inline(lang))

@dp.message(F.text.in_([LANGUAGES["uz"]["btn_trans"], LANGUAGES["ru"]["btn_trans"], LANGUAGES["en"]["btn_trans"]]))
async def reply_transport(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    await message.answer(LANGUAGES[lang]["trans_title"], reply_markup=get_transport_inline(lang))

@dp.message(F.text.in_([LANGUAGES["uz"]["btn_other"], LANGUAGES["ru"]["btn_other"], LANGUAGES["en"]["btn_other"]]))
async def reply_other_services(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    await message.answer(LANGUAGES[lang]["other_title"], reply_markup=get_other_services_inline(lang))

@dp.message(F.text.in_([LANGUAGES["uz"]["btn_food"], LANGUAGES["ru"]["btn_food"], LANGUAGES["en"]["btn_food"]]))
async def reply_food(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    await message.answer(FOOD_TEXT, reply_markup=get_action_inline_buttons(lang, "back_to_main_menu"))

@dp.message(F.text.in_([LANGUAGES["uz"]["btn_about"], LANGUAGES["ru"]["btn_about"], LANGUAGES["en"]["btn_about"]]))
async def reply_about(message: types.Message):
    lang = get_user_lang(message.from_user.id)
    await message.answer(LANGUAGES[lang]["about_text"], reply_markup=get_action_inline_buttons(lang, "back_to_main_menu"))


# --- DINAMIK TARJIMA QILINGAN DETALLAR TIZIMI ---
@dp.callback_query(F.data.startswith("visa_"))
async def cb_visa_details(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    vtype = call.data.replace("visa_", "")
    txt = LANGUAGES[lang].get(f"v_{vtype}", "Visa service.") + ADMIN_CONTACTS
    await call.message.edit_text(txt, reply_markup=get_action_inline_buttons(lang, "back_to_visa_main"), parse_mode="Markdown")
    await call.answer()

@dp.callback_query(F.data.startswith("trans_"))
async def cb_transport_details(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    ttype = call.data.replace("trans_", "")
    txt = LANGUAGES[lang].get(f"t_{ttype}", "Transport service.") + ADMIN_CONTACTS
    await call.message.edit_text(txt, reply_markup=get_action_inline_buttons(lang, "back_to_trans_main"), parse_mode="Markdown")
    await call.answer()

@dp.callback_query(F.data.startswith("srv_"))
async def cb_services_details(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    stype = call.data.replace("srv_", "")
    txt = LANGUAGES[lang].get(f"s_{stype}", "Service.") + HADIS_TEXT + ADMIN_CONTACTS
    await call.message.edit_text(txt, reply_markup=get_action_inline_buttons(lang, "back_to_other_services"), parse_mode="Markdown")
    await call.answer()


# --- ORTGA QAYTISH NAVIGATSIYASI ---
@dp.callback_query(F.data == "back_to_main_menu")
async def cb_back_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text(LANGUAGES[lang]["main_menu"], reply_markup=None)
    await call.answer()

@dp.callback_query(F.data == "back_to_visa_main")
async def cb_back_visa(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text(LANGUAGES[lang]["visa_title"], reply_markup=get_visa_inline(lang))
    await call.answer()

@dp.callback_query(F.data == "back_to_trans_main")
async def cb_back_trans(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text(LANGUAGES[lang]["trans_title"], reply_markup=get_transport_inline(lang))
    await call.answer()

@dp.callback_query(F.data == "back_to_other_services")
async def cb_back_other_services(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text(LANGUAGES[lang]["other_title"], reply_markup=get_other_services_inline(lang))
    await call.answer()

@dp.callback_query(F.data == "back_to_cities")
async def cb_back_cities(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text(LANGUAGES[lang]["choose_city"], reply_markup=get_cities_inline(lang))
    await call.answer()

@dp.callback_query(F.data == "city_mecca")
async def cb_mecca(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text("🕋 Makkah Hotels:", reply_markup=get_mecca_categories_inline(lang))
    await call.answer()

@dp.callback_query(F.data == "city_madina")
async def cb_madina(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    await call.message.edit_text("🕌 Medina Hotels:", reply_markup=get_madina_categories_inline(lang))
    await call.answer()

@dp.callback_query(F.data.startswith("kat_"))
async def cb_categories(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    cat = call.data.replace("kat_", "")
    await call.message.edit_text("Hotels:", reply_markup=get_hotels_inline(cat, lang))
    await call.answer()

@dp.callback_query(F.data.startswith("hotel_"))
async def cb_hotels(call: types.CallbackQuery):
    lang = get_user_lang(call.from_user.id)
    raw_data = call.data.replace("hotel_", "").split("_")
    await call.message.edit_text(f"🏨 **{raw_data[0].upper()}**\n\nContact admin to book.", reply_markup=get_action_inline_buttons(lang, "back_to_main_menu"), parse_mode="Markdown")
    await call.answer()


# --- ARIZA TIZIMI ---
@dp.message(F.text.in_([LANGUAGES["uz"]["btn_order"], LANGUAGES["ru"]["btn_order"], LANGUAGES["en"]["btn_order"]]))
async def start_form(message: types.Message, state: FSMContext):
    await state.clear()
    lang = get_user_lang(message.from_user.id)
    await message.answer(LANGUAGES[lang]["order_start"])
    await state.set_state(OrderForm.waiting_for_name)

@dp.message(OrderForm.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    lang = get_user_lang(message.from_user.id)
    builder = ReplyKeyboardBuilder()
    builder.button(text=LANGUAGES[lang]["send_phone_btn"], request_contact=True)
    await message.answer(LANGUAGES[lang]["ask_phone"], reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(OrderForm.waiting_for_phone)

@dp.message(OrderForm.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    data = await state.get_data()
    lang = get_user_lang(message.from_user.id)
    
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=f"📝 **YANGI ARIZA:**\n👤 Ism: {data.get('name')}\n📞 Tel: {phone}")
    except Exception as e:
        print(e)
        
    await state.clear()
    await message.answer(LANGUAGES[lang]["order_success"], reply_markup=get_main_reply_menu(lang))

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
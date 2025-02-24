import os
import asyncio
import logging
import sqlite3
from datetime import datetime
from contextlib import contextmanager
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# 🔹 إعدادات البوت
API_TOKEN = ''  # رمز البوت
ADMIN_ID = 123456789  # معرفك الخاص (المسؤول)
DATABASE_NAME = 'user_data.db'

# 🔹 إعدادات التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔹 تهيئة البوت والموزع
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

# 🔹 إعداد قاعدة البيانات
@contextmanager
def database_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()

async def init_database():
    with database_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                city TEXT,
                country TEXT,
                problem_solving TEXT,
                creativity TEXT,
                decision_making TEXT,
                social_interaction TEXT,
                emotional_state TEXT,
                planning TEXT,
                flexibility TEXT,
                team_loyalty TEXT,
                control_preference TEXT,
                daily_judgment TEXT,
                tough_situations TEXT,
                submission_date TEXT
            )
        """)
    logger.info("Database initialized successfully")

# 🔹 تعريف الحالات
class TestState(StatesGroup):
    username = State()
    city = State()
    country = State()
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()
    question7 = State()
    question8 = State()  # الولاء
    question9 = State()  # السيطرة
    question10 = State() # الحكم
    question11 = State() # المواقف الصعبة

# 🔹 معالج الأمر /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    logger.info("Received /start command")
    await message.answer("👋 أهلاً بك! هذا اختبار شخصية بسيط.\nأرسل /test لبدء الاختبار.")

# 🔹 معالج الأمر /test
@dp.message(Command("test"))
async def test_command(message: types.Message, state: FSMContext):
    logger.info("Received /test command")
    await state.set_state(TestState.username)
    await state.update_data(first_name=message.from_user.first_name or "غير متوفر",
                          last_name=message.from_user.last_name or "غير متوفر",
                          telegram_id=message.from_user.id)
    await message.answer("🚀 أولاً، ما هو لقبك؟")

# 🔹 معالجات خطوات الاختبار
@dp.message(TestState.username)
async def process_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(TestState.city)
    await message.answer("🏙 من أي مدينة أنت؟")

@dp.message(TestState.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(TestState.country)
    await message.answer("🌍 من أي دولة؟")

@dp.message(TestState.country)
async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(TestState.question1)
    await message.answer("🔹 كيف تتعامل مع المشاكل الكبيرة؟\n(أ) أحللها بهدوء\n(ب) أتوتر لكن أحاول حلها\n(ج) أشعر بالعجز", parse_mode="HTML")

@dp.message(TestState.question1)
async def process_question1(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(problem_solving=message.text)
    await state.set_state(TestState.question2)
    await message.answer("🎨 كيف ترى الإبداع؟\n(أ) جزء أساسي من حياتي\n(ب) شيء أحترمه لكن لا أمارسه كثيرًا\n(ج) لا أهتم به", parse_mode="HTML")

@dp.message(TestState.question2)
async def process_question2(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(creativity=message.text)
    await state.set_state(TestState.question3)
    await message.answer("🧩 عند اتخاذ القرارات، ما هو دافعك الأساسي؟\n(أ) المنطق والعقلانية\n(ب) العاطفة والتجربة الشخصية\n(ج) ما يقرره الآخرون", parse_mode="HTML")

@dp.message(TestState.question3)
async def process_question3(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(decision_making=message.text)
    await state.set_state(TestState.question4)
    await message.answer("👥 كيف تشعر في التجمعات الاجتماعية؟\n(أ) مرتاح ومستمتع\n(ب) متوتر قليلاً\n(ج) أفضل أن أكون بمفردي", parse_mode="HTML")

@dp.message(TestState.question4)
async def process_question4(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(social_interaction=message.text)
    await state.set_state(TestState.question5)
    await message.answer("😊 كيف تصف مزاجك عادةً؟\n(أ) إيجابي ومتفائل\n(ب) متذبذب\n(ج) سلبي أو حزين", parse_mode="HTML")

@dp.message(TestState.question5)
async def process_question5(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(emotional_state=message.text)
    await state.set_state(TestState.question6)
    await message.answer("📅 هل تحب التخطيط لكل شيء؟\n(أ) نعم، أحب التنظيم\n(ب) أحيانًا\n(ج) لا، أفضل العفوية", parse_mode="HTML")

@dp.message(TestState.question6)
async def process_question6(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(planning=message.text)
    await state.set_state(TestState.question7)
    await message.answer("🔄 كيف تتعامل مع التغييرات المفاجئة؟\n(أ) أتكيف بسرعة\n(ب) أحتاج وقتًا للتأقلم\n(ج) أكره التغيير", parse_mode="HTML")

@dp.message(TestState.question7)
async def process_question7(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(flexibility=message.text)
    await state.set_state(TestState.question8)
    await message.answer("🤝 عندما تعمل في فريق، كيف تتصرف؟\n(أ) أضع أهداف الفريق أولاً\n(ب) أحب أن أكون مرنًا\n(ج) أركز على مصلحتي الخاصة", parse_mode="HTML")

@dp.message(TestState.question8)
async def process_question8(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(team_loyalty=message.text)
    await state.set_state(TestState.question9)
    await message.answer("🎯 كيف تتعامل مع مهمة تتطلب العمل مع شخص آخر؟\n(أ) أفضل قيادة العملية\n(ب) أشارك وأتعاون\n(ج) أترك الآخر يقود", parse_mode="HTML")

@dp.message(TestState.question9)
async def process_question9(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(control_preference=message.text)
    await state.set_state(TestState.question10)
    await message.answer("🗓 عند التخطيط ليومك، كيف تتصرف؟\n(أ) أضع جدولًا واضحًا\n(ب) أحدد بعض النقاط الرئيسية\n(ج) أترك الأمور تسير كما تشاء", parse_mode="HTML")

@dp.message(TestState.question10)
async def process_question10(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(daily_judgment=message.text)
    await state.set_state(TestState.question11)
    await message.answer("⚡ إذا واجهتك مشكلة غير متوقعة، ماذا تفعل؟\n(أ) أبقى هادئًا وأحلها\n(ب) أشعر بالقلق لكن أبحث عن حل\n(ج) أتجنب التعامل معها", parse_mode="HTML")

@dp.message(TestState.question11)
async def process_final_question(message: types.Message, state: FSMContext):
    if message.text not in ["أ", "ب", "ج"]:
        await message.answer("❌ يرجى اختيار (أ)، (ب)، أو (ج) فقط.")
        return
    await state.update_data(tough_situations=message.text)
    user_data = await state.get_data()
    submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        await save_results_to_database(message.from_user.id, user_data, submission_date)
        await message.answer("✅ شكرًا لوقتك! سيتم التواصل معك بعد 3 أيام.", parse_mode="HTML")
        await send_html_report(ADMIN_ID, user_data, message.from_user.username)
    except Exception as e:
        logger.error(f"Error in final step: {e}")
        await message.answer("❌ حدث خطأ أثناء معالجة بياناتك. يرجى المحاولة لاحقًا.")
    finally:
        await state.clear()

# 🔹 حفظ البيانات في قاعدة البيانات
async def save_results_to_database(user_id: int, user_data: dict, submission_date: str):
    with database_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO results (
                user_id, first_name, last_name, username, city, country,
                problem_solving, creativity, decision_making, social_interaction,
                emotional_state, planning, flexibility, team_loyalty,
                control_preference, daily_judgment, tough_situations, submission_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, user_data["first_name"], user_data["last_name"], user_data["username"],
            user_data["city"], user_data["country"],
            user_data["problem_solving"], user_data["creativity"], user_data["decision_making"],
            user_data["social_interaction"], user_data["emotional_state"], user_data["planning"],
            user_data["flexibility"], user_data["team_loyalty"], user_data["control_preference"],
            user_data["daily_judgment"], user_data["tough_situations"], submission_date
        ))
    logger.info(f"Data saved for user {user_id}")

# 🔹 تحليل الشخصية مع النسب المئوية
def analyze_personality(user_data: dict) -> dict:
    analysis = {}

    # تصنيف MBTI (E/I, S/N, T/F, J/P)
    if user_data["social_interaction"] == "أ":
        analysis["E_I"] = "E"
        analysis["introversion_extroversion"] = "منفتح (Extroverted)"
    elif user_data["social_interaction"] == "ج":
        analysis["E_I"] = "I"
        analysis["introversion_extroversion"] = "انطوائي (Introverted)"
    else:
        analysis["E_I"] = "I/E"
        analysis["introversion_extroversion"] = "مختلط (Ambivert)"

    if user_data["creativity"] == "أ":
        analysis["S_N"] = "N"
        analysis["sensing_intuition"] = "حدسي (Intuitive)"
    elif user_data["creativity"] == "ج":
        analysis["S_N"] = "S"
        analysis["sensing_intuition"] = "حسي (Sensing)"
    else:
        analysis["S_N"] = "S/N"
        analysis["sensing_intuition"] = "مختلط"

    if user_data["decision_making"] == "أ":
        analysis["T_F"] = "T"
        analysis["thinking_feeling"] = "منطقي (Thinking)"
    elif user_data["decision_making"] == "ب":
        analysis["T_F"] = "F"
        analysis["thinking_feeling"] = "عاطفي (Feeling)"
    else:
        analysis["T_F"] = "T/F"
        analysis["thinking_feeling"] = "مختلط"

    # تحسين J/P باستخدام الأسئلة الجديدة
    j_score = sum([1 if user_data[key] == "أ" else 0 for key in ["planning", "daily_judgment"]])
    p_score = 1 if user_data["flexibility"] == "أ" else 0
    if j_score > p_score:
        analysis["J_P"] = "J"
        analysis["judging_perceiving"] = "منظم (Judging)"
    elif p_score > j_score:
        analysis["J_P"] = "P"
        analysis["judging_perceiving"] = "مرن (Perceiving)"
    else:
        analysis["J_P"] = "J/P"
        analysis["judging_perceiving"] = "مختلط"

    analysis["mbti"] = f"{analysis['E_I']}{analysis['S_N']}{analysis['T_F']}{analysis['J_P']}"

    # الإبداع بالنسبة المئوية
    if user_data["creativity"] == "أ":
        analysis["creativity_level"] = "مبدع جدًا (100%)"
    elif user_data["creativity"] == "ب":
        analysis["creativity_level"] = "مبدع نسبيًا (50%)"
    else:
        analysis["creativity_level"] = "غير مبدع (0%)"

    # الوفاء بالنسبة المئوية (مع تحسين باستخدام الأسئلة الجديدة)
    loyalty_score = 0
    if user_data["planning"] == "أ":
        loyalty_score += 25  # التخطيط
    if user_data["flexibility"] == "ج":
        loyalty_score += 25  # كره التغيير
    if user_data["team_loyalty"] == "أ":
        loyalty_score += 50  # الولاء للفريق
    analysis["loyalty"] = f"{'مرتفع' if loyalty_score >= 75 else 'متوسط' if loyalty_score >= 50 else 'منخفض'} ({loyalty_score}%)"

    # السيطرة
    if user_data["control_preference"] == "أ":
        analysis["control"] = "يحب السيطرة (High Control)"
    elif user_data["control_preference"] == "ب":
        analysis["control"] = "متعاون (Moderate Control)"
    else:
        analysis["control"] = "غير مسيطر (Low Control)"

    # التعامل مع المواقف الصعبة
    if user_data["tough_situations"] == "أ":
        analysis["tough_situations"] = "قوي في المواقف الصعبة (Strong)"
    elif user_data["tough_situations"] == "ب":
        analysis["tough_situations"] = "متوسط في المواقف الصعبة (Moderate)"
    else:
        analysis["tough_situations"] = "ضعيف في المواقف الصعبة (Weak)"

    return analysis

# 🔹 إرسال تقرير HTML مع التحليل الموسع
async def send_html_report(admin_id: int, user_data: dict, telegram_username: str = None):
    analysis = analyze_personality(user_data)
    telegram_link = f"https://t.me/{telegram_username}" if telegram_username else "غير متوفر"
    report = f"""
    <b>📜 تقرير المستخدم</b>
    <pre>---------------------------</pre>
    <b>🆔 رقم التعريف في Telegram:</b> {user_data['telegram_id']}
    <b>🔗 رابط الحساب:</b> <a href="{telegram_link}">{telegram_link}</a>
    <b>👤 الاسم:</b> {user_data['first_name']} {user_data['last_name']}
    <b>🏷 اللقب:</b> {user_data['username']}
    <b>🏙 المدينة:</b> {user_data['city']}
    <b>🌍 الدولة:</b> {user_data['country']}
    <b>🔹 التعامل مع المشاكل:</b> {user_data['problem_solving']}
    <b>🎨 الإبداع:</b> {user_data['creativity']}
    <b>🧩 اتخاذ القرارات:</b> {user_data['decision_making']}
    <b>👥 التفاعل الاجتماعي:</b> {user_data['social_interaction']}
    <b>😊 الحالة العاطفية:</b> {user_data['emotional_state']}
    <b>📅 التخطيط:</b> {user_data['planning']}
    <b>🔄 المرونة:</b> {user_data['flexibility']}
    <b>🤝 الولاء في الفريق:</b> {user_data['team_loyalty']}
    <b>🎯 تفضيل السيطرة:</b> {user_data['control_preference']}
    <b>🗓 الحكم اليومي:</b> {user_data['daily_judgment']}
    <b>⚡ المواقف الصعبة:</b> {user_data['tough_situations']}
    <pre>---------------------------</pre>
    <b>🧠 تحليل الشخصية الأولي</b>
    <b>▸ نوع MBTI:</b> {analysis['mbti']}
    <b>▸ الانطواء/الانفتاح:</b> {analysis['introversion_extroversion']}
    <b>▸ الحس/الحدس:</b> {analysis['sensing_intuition']}
    <b>▸ التفكير/الشعور:</b> {analysis['thinking_feeling']}
    <b>▸ الحكم/الإدراك:</b> {analysis['judging_perceiving']}
    <b>▸ مستوى الإبداع:</b> {analysis['creativity_level']}
    <b>▸ مستوى الوفاء:</b> {analysis['loyalty']}
    <b>▸ مستوى السيطرة:</b> {analysis['control']}
    <b>▸ التعامل مع المواقف الصعبة:</b> {analysis['tough_situations']}
    """
    try:
        await bot.send_message(admin_id, report, parse_mode="HTML")
        logger.info(f"HTML report with analysis sent to admin {admin_id}")
    except Exception as e:
        logger.error(f"Failed to send HTML report: {e}")

# 🔹 معالج الرسائل غير المعروفة
@dp.message()
async def unknown_command(message: types.Message):
    logger.info(f"Unknown command received: {message.text}")
    await message.answer("❓ لم أفهم طلبك. استخدم /start أو /test.")

# 🔹 الدالة الرئيسية
async def main():
    try:
        await init_database()
        await bot.set_my_commands([
            BotCommand(command="start", description="ترحيب"),
            BotCommand(command="test", description="بدء الاختبار"),
        ])
        logger.info("Bot started successfully")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

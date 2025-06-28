
import telebot
from telebot import types

TOKEN = "7761830641:AAG3k2XOzH2Y-M4TczT_0z7CKuBqraEjKo8"
ADMIN_ID = 5538763128
USERNAME = "macalinnileyn"
PASSWORD = "1234"

bot = telebot.TeleBot(TOKEN)

user_data = {}
teacher_logged_in = {}

fasalo = ["Fasalka 3aad", "Fasalka 4aad", "Fasalka 5aad"]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👨‍🎓 Arday", "👨‍🏫 Macalin")
    bot.send_message(
        message.chat.id,
        "🏫 Soo Dhaweyn Qurux Badan oo Rasmi ah\n"
        "Ku soo dhawoow madasha rasmiga ah ee Nileyn Primary and Secondary!\n"
        "Waxaad joogtaa meel ay ka curato aqoonta, anshaxa iyo horumarka ardayga Soomaaliyeed.\n\n"
        "Botkan waxaa si gaar ah loogu sameeyay fududeynta adeegyada dugsiga sida:\n"
        "✅ Wargelinta macallimiinta iyo ardayda\n"
        "✅ Jadwalka fasallada\n"
        "✅ Ogeysiisyada imtixaanka iyo xafladaha\n"
        "✅ Diiwaangelinta iyo xog uruurinta\n\n"
        "👨‍🏫 Maamulka guud: Mudane Shaaciye\n"
        "Hoggaan firfircoon oo u taagan tayada waxbarasho iyo daryeelka jiilka berri.\n\n"
        "💡 Nileyn waa hoyga waxbarasho tayo leh, mustaqbal ifaya!"
    )
    bot.send_message(message.chat.id, "Fadlan dooro doorkaaga:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👨‍🎓 Arday")
def ask_full_name(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "1️⃣ Magacaaga oo dhameystiran:")
    bot.register_next_step_handler(message, ask_mother_name)

def ask_mother_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["full_name"] = message.text
    bot.send_message(chat_id, "2️⃣ Magaca hooyada:")
    bot.register_next_step_handler(message, ask_parent_number)

def ask_parent_number(message):
    chat_id = message.chat.id
    user_data[chat_id]["mother_name"] = message.text
    bot.send_message(chat_id, "3️⃣ Lambarada waalidka & kanaga (fadlan ku qor hal fariin):")
    bot.register_next_step_handler(message, ask_birth_place)

def ask_birth_place(message):
    chat_id = message.chat.id
    user_data[chat_id]["numbers"] = message.text
    bot.send_message(chat_id, "4️⃣ Goobta uu ku dhashay:")
    bot.register_next_step_handler(message, ask_location)

def ask_location(message):
    chat_id = message.chat.id
    user_data[chat_id]["birth_place"] = message.text
    bot.send_message(chat_id, "5️⃣ Goobta uu hadda joogo:")
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    chat_id = message.chat.id
    user_data[chat_id]["location"] = message.text
    bot.send_message(chat_id, "6️⃣ Da'diisa ama sanadkiisa:")
    bot.register_next_step_handler(message, ask_class)

def ask_class(message):
    chat_id = message.chat.id
    user_data[chat_id]["age"] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for f in fasalo:
        markup.add(f)
    bot.send_message(chat_id, "7️⃣ Fadlan dooro fasalka:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_reason)

def ask_reason(message):
    chat_id = message.chat.id
    user_data[chat_id]["class"] = message.text
    bot.send_message(chat_id, "8️⃣ Maxay tahay sababta aad is diiwaangelinayso?")
    bot.register_next_step_handler(message, finish_registration)

def finish_registration(message):
    chat_id = message.chat.id
    user_data[chat_id]["reason"] = message.text

    summary = "\n".join(f"{key}: {value}" for key, value in user_data[chat_id].items())
    bot.send_message(chat_id, "✅ Waad is diiwaangelisay. Mahadsanid!")
    bot.send_message(ADMIN_ID, f"🆕 Arday cusub ayaa is diiwaangeliyay:\n\n{summary}\n\nID: {chat_id}")

@bot.message_handler(func=lambda message: message.text == "👨‍🏫 Macalin")
def teacher_login(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "👨‍🏫 Geli *username*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, check_username)

def check_username(message):
    chat_id = message.chat.id
    if message.text == USERNAME:
        bot.send_message(chat_id, "✅ Username wuu saxnaa.\nHadda geli *password*:", parse_mode="Markdown")
        bot.register_next_step_handler(message, check_password)
    else:
        bot.send_message(chat_id, "❌ Username-ka waa khaldan. Dib isku day.")
        start(message)

def check_password(message):
    chat_id = message.chat.id
    if message.text == PASSWORD:
        teacher_logged_in[chat_id] = True
        bot.send_message(chat_id, "✅ Waad gashay. Ku soo dhawoow maamulka.")
        show_students(chat_id)
    else:
        bot.send_message(chat_id, "❌ Password-ka waa khaldan.")
        start(message)

def show_students(chat_id):
    if not user_data:
        bot.send_message(chat_id, "❌ Weli ma jiraan arday is diiwaangeliyay.")
    else:
        for id, data in user_data.items():
            summary = "\n".join(f"{key}: {value}" for key, value in data.items())
            bot.send_message(chat_id, f"👨‍🎓 Arday:\n{summary}\nID: {id}")

bot.polling()

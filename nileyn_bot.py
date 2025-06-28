import telebot
from telebot import types

TOKEN = "7761830641:AAG3k2XOzH2Y-M4TczT_0z7CKuBqraEjKo8"
ADMIN_ID = 5538763128

bot = telebot.TeleBot(TOKEN)

user_data = {}
teacher_logged_in = {}
first_admin_set = False

fasalo = ["Fasalka 3aad", "Fasalka 4aad", "Fasalka 5aad"]

@bot.message_handler(commands=['start'])
def start(message):
    global first_admin_set
    chat_id = message.chat.id

    if not first_admin_set:
        first_admin_set = True
        bot.send_message(ADMIN_ID, f"🛡️ Admin cusub ayaa la abuuray: ID={chat_id}")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👨‍🎓 Arday", "👨‍🏫 Macalin")
    bot.send_message(chat_id, """🏫 Soo Dhaweyn Qurux Badan oo Rasmi ah
Ku soo dhawoow madasha rasmiga ah ee Nileyn Primary and Secondary!
Waxaad joogtaa meel ay ka curato aqoonta, anshaxa iyo horumarka ardayga Soomaaliyeed.

Botkan waxaa si gaar ah loogu sameeyay fududeynta adeegyada dugsiga sida:

✅ Wargelinta macallimiinta iyo ardayda
✅ Jadwalka fasallada
✅ Ogeysiisyada imtixaanka iyo xafladaha
✅ Diiwaangelinta iyo xog uruurinta

👨‍🏫 Maamulka guud: Mudane Shaaciye
Hoggaan firfircoon oo u taagan tayada waxbarasho iyo daryeelka jiilka berri.

💡 Nileyn waa hoyga waxbarasho tayo leh, mustaqbal ifaya!""", reply_markup=markup)

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
    bot.send_message(chat_id, "✅ Mahadsanid! Waxaa isku diiwaangelisay sidii loo baahnaa.")
    bot.send_message(ADMIN_ID, f"🆕 Arday cusub ayaa is diiwaangeliyay:\n\n{summary}\n\nID: {chat_id}")

@bot.message_handler(func=lambda message: message.text == "👨‍🏫 Macalin")
def teacher_login(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "👨‍🏫 Magaca macalinka:")
    bot.register_next_step_handler(message, ask_subjects)

def ask_subjects(message):
    chat_id = message.chat.id
    user_data[chat_id]["teacher_name"] = message.text
    bot.send_message(chat_id, "📘 Maaddooyinka aad dhigto (hal ama laba):")
    bot.register_next_step_handler(message, finish_teacher_registration)

def finish_teacher_registration(message):
    chat_id = message.chat.id
    user_data[chat_id]["subjects"] = message.text
    summary = "\n".join(f"{key}: {value}" for key, value in user_data[chat_id].items())
    bot.send_message(chat_id, "✅ Waad is diiwaangelisay Macalin ahaan.")
    bot.send_message(ADMIN_ID, f"👨‍🏫 Macalin cusub ayaa is diiwaangeliyay:\n\n{summary}\n\nID: {chat_id}")

bot.polling()

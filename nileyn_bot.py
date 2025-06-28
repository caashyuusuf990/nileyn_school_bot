
import telebot
from telebot import types

TOKEN = "7761830641:AAG3k2XOzH2Y-M4TczT_0z7CKuBqraEjKo8"
bot = telebot.TeleBot(TOKEN)

user_data = {}
teacher_data = {}
admin_id = None
fasalo = ["Fasalka 3aad", "Fasalka 4aad", "Fasalka 5aad"]

@bot.message_handler(commands=['start'])
def start(message):
    global admin_id
    if admin_id is None:
        admin_id = message.chat.id
        bot.send_message(admin_id, "✅ Adiga ayaa noqday admin-ka bot-kan.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👨‍🎓 Arday", "👨‍🏫 Macalin")
    bot.send_message(message.chat.id, "🏫 Soo Dhaweyn Qurux Badan oo Rasmi ah
Ku soo dhawoow madasha rasmiga ah ee Nileyn Primary and Secondary!

Waxaad joogtaa meel ay ka curato aqoonta, anshaxa iyo horumarka ardayga Soomaaliyeed.

Botkan waxaa si gaar ah loogu sameeyay fududeynta adeegyada dugsiga sida:

✅ Wargelinta macallimiinta iyo ardayda
✅ Jadwalka fasallada
✅ Ogeysiisyada imtixaanka iyo xafladaha
✅ Diiwaangelinta iyo xog uruurinta

👨‍🏫 Maamulka guud: Mudane Shaaciye
Hoggaan firfircoon oo u taagan tayada waxbarasho iyo daryeelka jiilka berri.

💡 Nileyn waa hoyga waxbarasho tayo leh, mustaqbal ifaya!

Fadlan dooro doorkaaga:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "👨‍🎓 Arday")
def student_register(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "1️⃣ Magacaaga oo dhameystiran:")
    bot.register_next_step_handler(message, lambda m: collect_student_info(m, "full_name"))

def collect_student_info(message, key):
    chat_id = message.chat.id
    next_steps = {
        "full_name": ("2️⃣ Magaca hooyada:", "mother_name"),
        "mother_name": ("3️⃣ Lambarada waalidka & kanaga:", "numbers"),
        "numbers": ("4️⃣ Goobta uu ku dhashay:", "birth_place"),
        "birth_place": ("5️⃣ Goobta uu hadda joogo:", "location"),
        "location": ("6️⃣ Da'diisa ama sanadkiisa:", "age"),
        "age": ("7️⃣ Fadlan dooro fasalka:", "class"),
        "class": ("8️⃣ Maxay tahay sababta aad is diiwaangelinayso?", "reason"),
        "reason": None
    }
    user_data[chat_id][key] = message.text

    if key == "age":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for f in fasalo:
            markup.add(f)
        bot.send_message(chat_id, next_steps[key][0], reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: collect_student_info(m, next_steps[key][1]))
    elif key == "reason":
        bot.send_message(chat_id, "✅ Mahadsanid, waxaad is diiwaangelisay sidii loo baahnaa. Waxa aan kugu shaqeyn doonaa si hufan!")
    else:
        bot.send_message(chat_id, next_steps[key][0])
        bot.register_next_step_handler(message, lambda m: collect_student_info(m, next_steps[key][1]))

@bot.message_handler(func=lambda msg: msg.text == "👨‍🏫 Macalin")
def teacher_start(message):
    chat_id = message.chat.id
    teacher_data[chat_id] = {}
    bot.send_message(chat_id, "1️⃣ Magacaaga macalinimo:")
    bot.register_next_step_handler(message, ask_teacher_subject1)

def ask_teacher_subject1(message):
    chat_id = message.chat.id
    teacher_data[chat_id]["name"] = message.text
    bot.send_message(chat_id, "2️⃣ Maadada koowaad ee aad dhigto:")
    bot.register_next_step_handler(message, ask_teacher_subject2)

def ask_teacher_subject2(message):
    chat_id = message.chat.id
    teacher_data[chat_id]["subject1"] = message.text
    bot.send_message(chat_id, "3️⃣ Maadada labaad (ama qor 'ma jiro' haddii aanad dhigin):")
    bot.register_next_step_handler(message, finish_teacher_register)

def finish_teacher_register(message):
    chat_id = message.chat.id
    teacher_data[chat_id]["subject2"] = message.text
    summary = f"👨‍🏫 Macalin cusub:

Magac: {teacher_data[chat_id]['name']}
Maado 1: {teacher_data[chat_id]['subject1']}
Maado 2: {teacher_data[chat_id]['subject2']}
ID: {chat_id}"
    bot.send_message(chat_id, "✅ Waad is diiwaangelisay, macalinow.")
    if admin_id:
        bot.send_message(admin_id, summary)

bot.polling()

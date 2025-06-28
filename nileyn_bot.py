import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "7761830641:AAG3k2XOzH2Y-M4TczT_0z7CKuBqraEjKo8")
ADMIN_ID = int(os.getenv("ADMIN_ID", "5538763128"))
USERNAME = os.getenv("USERNAME", "macalinnileyn")
PASSWORD = os.getenv("PASSWORD", "1234")

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}
students = []

@bot.message_handler(commands=["start"])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("📚 Arday", "🧑‍🏫 Macalin")
    bot.send_message(message.chat.id, "👋 Ku soo dhawoow Nileyn Primary and Secondary School!
Fadlan dooro doorkaaga:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["📚 Arday", "🧑‍🏫 Macalin"])
def handle_role(message):
    chat_id = message.chat.id
    if message.text == "📚 Arday":
        user_data[chat_id] = {}
        bot.send_message(chat_id, "1. Fadlan geli *magacaaga oo dhameystiran*:", parse_mode="Markdown")
        bot.register_next_step_handler(message, ask_mother_name)
    elif message.text == "🧑‍🏫 Macalin":
        bot.send_message(chat_id, "👨‍🏫 Geli *username*:", parse_mode="Markdown")
        bot.register_next_step_handler(message, handle_teacher_login)

def handle_teacher_login(message):
    chat_id = message.chat.id
    if message.text == USERNAME:
        bot.send_message(chat_id, "✅ Username wuu saxnaa.
Hadda geli *password*:", parse_mode="Markdown")
        bot.register_next_step_handler(message, check_password)
    else:
        bot.send_message(chat_id, "❌ Username-ka waa khaldan. Isku day mar kale.")

def check_password(message):
    chat_id = message.chat.id
    if message.text == PASSWORD:
        text = "📋 Liiska Ardayda Diiwaangashan:

"
        for student in students:
            text += "\n".join([f"{k}: {v}" for k, v in student.items()]) + "\n---\n"
        bot.send_message(chat_id, text or "⚠️ Wali arday ma diiwaangashana.")
    else:
        bot.send_message(chat_id, "❌ Password-ka waa khaldan.")

def ask_mother_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["Magaca"] = message.text
    bot.send_message(chat_id, "2. Geli *magaca hooyadaa*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, ask_contacts)

def ask_contacts(message):
    chat_id = message.chat.id
    user_data[chat_id]["Magaca Hooyo"] = message.text
    bot.send_message(chat_id, "3. Geli *lambarkaaga* iyo *kan waalidka* (hal fariin ku qor):", parse_mode="Markdown")
    bot.register_next_step_handler(message, ask_birthplace)

def ask_birthplace(message):
    chat_id = message.chat.id
    user_data[chat_id]["Lambaro"] = message.text
    bot.send_message(chat_id, "4. Halkee ayaad ku dhalatay?")
    bot.register_next_step_handler(message, ask_location)

def ask_location(message):
    chat_id = message.chat.id
    user_data[chat_id]["Goobta Dhalashada"] = message.text
    bot.send_message(chat_id, "5. Halkee ayaad hadda ku nooshahay?")
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    chat_id = message.chat.id
    user_data[chat_id]["Goobta Degenaanshaha"] = message.text
    bot.send_message(chat_id, "6. Da'daada ama sanad dhalashadaada?")
    bot.register_next_step_handler(message, ask_class)

def ask_class(message):
    chat_id = message.chat.id
    user_data[chat_id]["Da'da/Sanadka"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Fasal 3aad", "Fasal 4aad", "Fasal 5aad")
    bot.send_message(chat_id, "7. Dooro fasalka aad rabto ama hadda dhigato:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_reason)

def ask_reason(message):
    chat_id = message.chat.id
    user_data[chat_id]["Fasal"] = message.text
    bot.send_message(chat_id, "8. Maxaa kugu dhiirrigeliyay inaad isdiiwaangeliso?")
    bot.register_next_step_handler(message, complete_registration)

def complete_registration(message):
    chat_id = message.chat.id
    user_data[chat_id]["Sababta"] = message.text
    user_data[chat_id]["Telegram ID"] = chat_id
    students.append(user_data[chat_id])
    bot.send_message(chat_id, "✅ Waad isdiiwaangelisay. Maamulka ayaa la socon doona. Mahadsanid!")
    bot.send_message(ADMIN_ID, f"🆕 Arday cusub ayaa isdiiwaangeliyey:

" + "\n".join([f"{k}: {v}" for k, v in user_data[chat_id].items()]))

bot.infinity_polling()
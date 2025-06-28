
import telebot
from telebot import types
import csv
import os

BOT_TOKEN = "7761830641:AAG3k2XOzH2Y-M4TczT_0z7CKuBqraEjKo8"
ADMIN_ID = 5538763128
bot = telebot.TeleBot(BOT_TOKEN)

SAVE_DIR = "data"
os.makedirs(SAVE_DIR, exist_ok=True)
CSV_FILE = os.path.join(SAVE_DIR, "registered_students.csv")

# Login credentials
TEACHER_USERNAME = "macalinnileyn"
TEACHER_PASSWORD = "1234"

# Store user role and states
user_data = {}
user_states = {}

# Ensure CSV file has headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Magac", "Magac Hooyo", "Number Arday", "Number Waalid",
            "Ku Dhashay", "Goobta Joogo", "Da'da/Sanad", "Fasal", "Sabab", "Telegram ID"
        ])

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📝 Diiwaangelin", "ℹ️ Info", "📞 La xiriir Maamulka")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_states[chat_id] = "choose_role"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Arday", "Macalin")
    bot.send_message(chat_id, "Fadlan dooro doorkaaga: Arday mise Macalin?", reply_markup=markup)

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "choose_role")
def choose_role(message):
    chat_id = message.chat.id
    if message.text.lower() == "macalin":
        user_states[chat_id] = "login_username"
        bot.send_message(chat_id, "Fadlan geli *username*-ka macalinka:", parse_mode="Markdown")
    elif message.text.lower() == "arday":
        user_states[chat_id] = "student"
        bot.send_message(chat_id, "📌 Dooro adeegga hoos ka muuqda:", reply_markup=main_menu())
    else:
        bot.send_message(chat_id, "Fadlan dooro mid sax ah: Arday ama Macalin.")

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "login_username")
def teacher_username(message):
    chat_id = message.chat.id
    if message.text.strip() == TEACHER_USERNAME:
        user_states[chat_id] = "login_password"
bot.send_message(chat_id, "✅ Username wuu saxnaa.\nHadda geli *password*:", parse_mode="Markdown")
Hadda geli *password*:", parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "❌ Username-ka waa khaldan. Dib u qor.")

@bot.message_handler(func=lambda m: user_states.get(m.chat.id) == "login_password")
def teacher_password(message):
    chat_id = message.chat.id
    if message.text.strip() == TEACHER_PASSWORD:
        user_states[chat_id] = "teacher_logged_in"
        show_registered_students(chat_id)
    else:
        bot.send_message(chat_id, "❌ Password-ka waa khaldan. Dib u qor.")

def show_registered_students(chat_id):
    if not os.path.exists(CSV_FILE):
        bot.send_message(chat_id, "❌ Weli lama diiwaangelin arday.")
        return

    bot.send_message(chat_id, "📋 Liiska Ardayda la Diiwaangeliyay:")
    with open(CSV_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            msg = (
                f"👤 Magac: {row[0]}
"
                f"👩 Hooyo: {row[1]}
"
                f"📱 Arday: {row[2]}
"
                f"📞 Waalid: {row[3]}
"
                f"🌍 Ku Dhashay: {row[4]}
"
                f"📍 Joogo: {row[5]}
"
                f"🎂 Da': {row[6]}
"
                f"🏫 Fasal: {row[7]}
"
                f"📝 Sabab: {row[8]}
"
                f"🆔 ID: {row[9]}"
            )
            bot.send_message(chat_id, msg)

@bot.message_handler(func=lambda m: m.text == "ℹ️ Info")
def show_info(message):
    bot.send_message(message.chat.id,
        "🏫 *Nileyn Primary and Secondary School*
- Waxbarasho tayo sare leh
- Macallimiin khibrad leh

👉 Isticmaal '📝 Diiwaangelin' si aad isdiiwaangeliso.",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == "📞 La xiriir Maamulka")
def contact_admin(message):
    bot.send_message(message.chat.id, "📬 Fadlan la xiriir maamulka: @your_admin_username")

@bot.message_handler(func=lambda m: m.text == "📝 Diiwaangelin")
def register(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, "📄 Diiwaangelinta: Fadlan geli magacaaga oo dhameystiran:")
    bot.register_next_step_handler(message, get_full_name)

def get_full_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['magac'] = message.text.strip()
    bot.send_message(chat_id, "👩 Magaca hooyadaa oo dhameystiran:")
    bot.register_next_step_handler(message, get_mother_name)

def get_mother_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['magac_hooyo'] = message.text.strip()
    bot.send_message(chat_id, "📱 Numberkaaga:")
    bot.register_next_step_handler(message, get_student_number)

def get_student_number(message):
    chat_id = message.chat.id
    user_data[chat_id]['number_arday'] = message.text.strip()
    bot.send_message(chat_id, "📞 Numberka waalidka:")
    bot.register_next_step_handler(message, get_parent_number)

def get_parent_number(message):
    chat_id = message.chat.id
    user_data[chat_id]['number_waalid'] = message.text.strip()
    bot.send_message(chat_id, "🌍 Halka aad ku dhalatay:")
    bot.register_next_step_handler(message, get_birth_place)

def get_birth_place(message):
    chat_id = message.chat.id
    user_data[chat_id]['ku_dhashay'] = message.text.strip()
    bot.send_message(chat_id, "📍 Goobta aad hadda joogto:")
    bot.register_next_step_handler(message, get_current_location)

def get_current_location(message):
    chat_id = message.chat.id
    user_data[chat_id]['goobta_hadda'] = message.text.strip()
    bot.send_message(chat_id, "🎂 Da'daada ama sanadkii dhalashada:")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    chat_id = message.chat.id
    user_data[chat_id]['da'] = message.text.strip()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Fasalka 3aad", "Fasalka 4aad", "Fasalka 5aad")
    msg = bot.send_message(chat_id, "🏫 Door fasalka aad rabto:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_class)

def get_class(message):
    chat_id = message.chat.id
    user_data[chat_id]['fasal'] = message.text.strip()
    bot.send_message(chat_id, "📝 Maxay tahay sababta aad u rabto inaad isdiiwaangeliso:")
    bot.register_next_step_handler(message, get_reason)

def get_reason(message):
    chat_id = message.chat.id
    user_data[chat_id]['sabab'] = message.text.strip()

    data = user_data[chat_id]
    text = (
        f"📥 *Diiwaangelin Cusub*
"
        f"👤 Magac: {data['magac']}
"
        f"👩 Magaca Hooyo: {data['magac_hooyo']}
"
        f"📱 Number Arday: {data['number_arday']}
"
        f"📞 Number Waalid: {data['number_waalid']}
"
        f"🌍 Ku Dhashay: {data['ku_dhashay']}
"
        f"📍 Goobta Joogo: {data['goobta_hadda']}
"
        f"🎂 Da'da: {data['da']}
"
        f"🏫 Fasalka: {data['fasal']}
"
        f"📝 Sabab: {data['sabab']}
"
        f"🆔 Telegram ID: {chat_id}"
    )

    bot.send_message(ADMIN_ID, text, parse_mode="Markdown")

    with open(CSV_FILE, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            data['magac'], data['magac_hooyo'], data['number_arday'], data['number_waalid'],
            data['ku_dhashay'], data['goobta_hadda'], data['da'], data['fasal'], data['sabab'], chat_id
        ])

    bot.send_message(chat_id, "✅ Mahadsanid! Xogtaada waa la diiwaan geliyay.", reply_markup=main_menu())

bot.infinity_polling()

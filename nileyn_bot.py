import telebot

TOKEN = "7761830641:AAG3k2XOzH2Y-M4TczT_0z7CKuBqraEjKo8"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🏫 Soo Dhaweyn Qurux Badan oo Rasmi ah
Ku soo dhawoow madasha rasmiga ah ee Nileyn Primary and Secondary!
Waxaad joogtaa meel ay ka curato aqoonta, anshaxa iyo horumarka ardayga Soomaaliyeed.

Botkan waxaa si gaar ah loogu sameeyay fududeynta adeegyada dugsiga sida:

📌 Wargelinta macallimiinta iyo ardayda  
📌 Jadwalka fasallada  
📌 Ogeysiisyada imtixaanka iyo xafladaha  
📌 Diiwaangelinta iyo xog uruurinta

👤 Maamulka guud: Mudane Shaaciye  
💼 Hoggaan firfircoon oo u taagan tayada waxbarasho iyo daryeelka jiilka berri.

💡 Nileyn waa hoyga waxbarasho tayo leh, mustaqbal ifaya!
"""
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(func=lambda msg: msg.text.lower() in ["diwaan", "register"])
def register_student(message):
    response = """
🎉 Mahadsanid! Waxaad isku diiwaangelisay sidii loo baahnaa.
🤝 Waxa aan kugu shaqeyn doonaa si hufan!
"""
    bot.send_message(message.chat.id, response)

bot.polling()

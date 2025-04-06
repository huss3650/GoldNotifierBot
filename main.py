import os
import time
import requests
import telebot
from keep_alive import keep_alive

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

def get_gold_price():
    url = os.getenv("GOLD_API_URL")
    headers = {"x-access-token": os.getenv("GOLD_API_KEY")}
    response = requests.get(url, headers=headers)
    data = response.json()
    price = data['price']
    exchange_rate = float(os.getenv("EXCHANGE_RATE", 1))
    return round(price * exchange_rate, 2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    # تخزين الـ chat_id
    with open("chat_id.txt", "w") as f:
        f.write(str(chat_id))

    # رسالة ترحيبية وفكرة البوت
    welcome_msg = (
        "مرحباً بك في بوت أسعار الذهب 💰\n\n"
        "📌 فكرة البوت:\n"
        "نرسل لك مرتين يوميًا *سعر الذهب بالريال القطري* بناءً على سعر السوق العالمي محدث بالدولار.\n\n"
        "✅ لا تحتاج لعمل أي شيء، فقط انتظر الرسائل التلقائية.\n"
        "🟢 تم تسجيلك بنجاح لاستلام التحديثات.\n"
    )
    bot.reply_to(message, welcome_msg, parse_mode="Markdown")

def send_daily_price():
    while True:
        try:
            with open("chat_id.txt", "r") as f:
                chat_id = f.read().strip()
            price = get_gold_price()
            msg = f"📈 سعر الذهب الحالي هو: {price} ريال قطري للغرام."
            bot.send_message(chat_id=chat_id, text=msg)
            time.sleep(43200)  # كل 12 ساعة
        except Exception as e:
            print("Error:", e)
            time.sleep(60)

keep_alive()
send_daily_price()

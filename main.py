from config import BOT_TOKEN
from keep_alive import keep_alive
import requests
import time
import telebot
import os

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلًا بك! سأقوم بإرسال أسعار الذهب يوميًا إن شاء الله.")

def get_gold_price():
    url = os.getenv("GOLD_API_URL")
    headers = {"x-access-token": os.getenv("GOLD_API_KEY")}
    response = requests.get(url, headers=headers)
    data = response.json()
    price = data['price']
    exchange_rate = float(os.getenv("EXCHANGE_RATE", 1))
    return round(price * exchange_rate, 2)

def send_daily_price():
    while True:
        try:
            price = get_gold_price()
            message = f"🔔 سعر الذهب اليوم هو: {price} ريال قطري للغرام."
            bot.send_message(chat_id='@GoldNotifierPrice_Channel', text=message)
            time.sleep(43200)  # كل 12 ساعة
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

keep_alive()
send_daily_price()

import os
import telebot
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    try:
        text = "Какой ваш знак зодиака?\nВыберите один: *Овен*, *Телец*, *Близнецы*, *Рак*, *Лев*, *Дева*, *Весы*, *Скорпион*, *Стрелец*, *Козерог*, *Водолей*, и *Рыбы*."
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, day_handler)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

def day_handler(message):
    try:
        sign = message.text
        text = "Какой день вы хотите узнать?\nВыберите один: *Сегодня*, *Завтра*, *Вчера*, или дату в формате ГГГГ-ММ-ДД."
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

def fetch_horoscope(message, sign):
    try:
        day = message.text
        horoscope = get_daily_horoscope(sign, day)
        if "error" in horoscope:
            bot.send_message(message.chat.id, horoscope["error"])
        else:
            data = horoscope["data"]
            horoscope_message = f'*Гороскоп:* {data["horoscope_data"]}\\n*Знак:* {sign}\\n*День:* {data["date"]}'
            bot.send_message(message.chat.id, "Вот ваш гороскоп!")
            bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

def get_daily_horoscope(sign: str, day: str) -> dict:
    try:
        url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
        params = {"sign": sign, "day": day}
        response = requests.get(url, params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

bot.infinity_polling()

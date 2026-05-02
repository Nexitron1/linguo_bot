from pydoc import text
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Error: there is no TELEGRAM_BOT_TOKEN in .env")

bot = telebot.TeleBot(BOT_TOKEN)

print("Бот начал работу")

@bot.message_handler(commands=['start'])
def send_welkome(message):
    bot.reply_to(message, "Hi")

@bot.message_handler(content_types=['text'])
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    bot.polling()

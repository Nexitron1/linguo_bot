from pydoc import text
import telebot
import os
from dotenv import load_dotenv
import PolzaRequests

load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Error: there is no TELEGRAM_BOT_TOKEN in .env")
bot = telebot.TeleBot(BOT_TOKEN)


POLZA_API_KEY = os.getenv("POLZA_API_KEY")
if not POLZA_API_KEY:
    raise ValueError("Error: there is no POLZA_API_KEY in .env")
polza = PolzaRequests.PolzaAI(POLZA_API_KEY)

file = open('./character.txt', 'r', encoding='utf-8')
character_description = file.read()
file.close()

print("Бот начал работу")

@bot.message_handler(commands=['start'])
def send_welkome(message):
    bot.reply_to(message, "Hi")

@bot.message_handler(commands=['гпт', 'gpt'])
def send_gpt_response(message):
    history = [{"role":"system", "content":character_description}, {"role":"user", "content":message.text}]
    resp = polza.SimpleGenerateText(history, "openai/gpt-5-nano")
    bot.reply_to(message, resp)

@bot.message_handler(content_types=['text'])
def echo_all(message):
    pass
    #bot.reply_to(message, message.text)

if __name__ == "__main__":
    bot.polling()

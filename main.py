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
    resp = polza.SimpleGenerateText(history, "openai/gpt-4o-mini")
    bot.reply_to(message, resp)

@bot.message_handler(commands=['донос', 'delation'])
def send_delation(message):
    history = [{"role":"system", "content":character_description}, {"role":"user", "content":message.text}]
    resp = polza.SimpleGenerateText(history, "openai/gpt-4o-mini")
    bot.send_message(message.chat.id, resp)

def send_rusophobian_sticker(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAM9afWHoiUkI92BeJbV_JNBlr8ribgAAooRAAIdo8BKEVrJTo6y_vg7BA", reply_to_message_id=message.id)

"""
@bot.message_handler(content_types=['sticker'])
def get_sticker_id(message):
    sticker_file_id = message.sticker.file_id
    print(f"File ID стикера: {sticker_file_id}")
    # Сохраните этот ID для дальнейшего использования
"""

@bot.message_handler(content_types=['text'])
def echo_all(message):
    resp = polza.MegaSimpleGenerateText("Если указанный далее текст содержит в себе признаки русофобии (отказ от использования только русских слов, оскорбления русской нации), то ответь только одним словом: ДА   если нет, то ответь НЕТ     вот текст для проверки: " + message.text, "openai/gpt-4o-mini")
    if resp == "ДА":
        send_rusophobian_sticker(message)
    #bot.reply_to(message, resp)

if __name__ == "__main__":
    bot.polling()

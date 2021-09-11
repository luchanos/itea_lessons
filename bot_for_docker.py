import telebot
import requests
from datetime import datetime
from envparse import Env

env = Env()

ADMIN_CHAT_ID = 362857450
TOKEN = "1732311949:AAFothWVXVBFbwDuxa7ObGUIzlqcZkj7evs"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def echo(message):
    bot.reply_to(message=message, text=f"{message.chat.username}, приветствую!")


while True:
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text=завожу бота")
        bot.polling()
    except Exception as err:
        log_msg = f"Бот упал ({err}), но не был сломлен, поэтому поднялся вновь: {datetime.now()}\n"
        print(log_msg)
        with open("logfile.txt", "a") as logfile:
            logfile.write(log_msg)
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={log_msg}")

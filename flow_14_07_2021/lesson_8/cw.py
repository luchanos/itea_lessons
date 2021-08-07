from telebot import TeleBot
from envparse import Env
from datetime import datetime
import requests
import psycopg2

from flow_14_07_2021.lesson_7.db_client import DbClientV2
from flow_14_07_2021.lesson_7.settings import DB_URL


env = Env()

TOKEN = env.str("TOKEN")
ADMIN_CHAT_ID = 362857450

# обвязка для работы с ботом на сервере телеграмм
bot = TeleBot(TOKEN)
db_client = DbClientV2(DB_URL)
db_client.setup()


@bot.message_handler(commands=["get_chat_id"])
def get_chat_id(message):
    params = message.text.split()[1:]
    print(f"Я получил новое сообщение из чата {message.chat.id} от {message.from_user.username} с параметрами: {params}")
    msg_for_user = f"Я общаюсь с тобой в чате {message.chat.id}"
    bot.reply_to(message, text=msg_for_user)


@bot.message_handler(commands=["create_new_book"])
def create_new_book(message):
    params = message.text.split("|")[1:]
    err_msg = ""
    try:
        params_for_insertion = dict()
        params_for_insertion['book_name'] = params[0].strip()
        params_for_insertion['author'] = params[1].strip()
        params_for_insertion['genre'] = params[2].strip()
        params_for_insertion['sheets_cnt'] = int(params[3].strip())
        params_for_insertion['added_by'] = message.from_user.username

        db_client.insert_book(**params_for_insertion)

        answer = f"Книга была добавлена:\n" \
                 f"Название: {params_for_insertion['book_name']}\n" \
                 f"Автор: {params_for_insertion['author']}\n" \
                 f"Жанр: {params_for_insertion['genre']}\n" \
                 f"Количество страниц: {params_for_insertion['sheets_cnt']}\n" \
                 f"Добавлено: {params_for_insertion['added_by']}"
        print(answer)
        bot.reply_to(message, text=answer)

    except IndexError:
        err_msg = "Параметры не были прокинуты!"
        print(err_msg)
    except ValueError:
        err_msg = "Ошибка типа! Пользователь отправил не число!"
        print(err_msg)
    if err_msg:
        bot.reply_to(message, text=err_msg)


# bot.polling()


while True:
    try:
        bot.polling()
    except Exception as err:
        log_msg = f"Бот упал ({err}), но не был сломлен, поэтому поднялся вновь: {datetime.now()}\n"
        print(log_msg)
        with open("logfile.txt", "a") as logfile:
            logfile.write(log_msg)
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ADMIN_CHAT_ID}&text={log_msg}")

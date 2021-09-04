import telebot

from flow_14_07_2021.lesson_7.app_example import MyDbClient

TOKEN = "1732311949:AAFothWVXVBFbwDuxa7ObGUIzlqcZkj7evs"
DB_URL = 'postgresql://newuser:qwerty@127.0.0.1:5432/postgres'

bot = telebot.TeleBot(TOKEN)
my_db_client = MyDbClient(DB_URL)
my_db_client.setup()


# 1. пользователь пишет боту.
# 2. бот спрашивает, хочет ли пользователь подписать на уведомления?
# 3. если да, то вносим соответствующую запись в таблицу БД


@bot.message_handler(commands=["subscribe"])
def subscribe_user(message):
    chat_id = message.chat.id
    username = message.chat.username
    print(f"Пользователь {username} из чата {chat_id} пытается подписаться на уведомления")
    my_db_client.subscribe_user_notifications(chat_id, username)
    bot.reply_to(message, text=f"Я подписал тебя на уведомления, {username}")


@bot.message_handler(commands=["unsubscribe"])
def unsubscribe_user(message):
    chat_id = message.chat.id
    username = message.chat.username
    print(f"Пользователь {username} из чата {chat_id} пытается отписаться от уведомлений")
    my_db_client.unsubscribe_user_notifications(chat_id, username)
    bot.reply_to(message, text=f"Я отписал тебя от уведомлений, {username}")


bot.polling()

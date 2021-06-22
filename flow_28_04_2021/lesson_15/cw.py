# Flask-SQLAlchemy
# Alembic

# для генерации скриптов миграций вводим: alembic init alembic - появится папка alembic и файл alembic.ini
# в ини айле нас интересует sqlalchemy.url = driver://user:pass@localhost/dbname - это путь к БД

# для создания телеграм-ботов используется BotFather
# для управления отправками сообщений ботом используется PyTelegramBotApi (ещё его называют telebot)
# ещё у Телеграмм есть сырая API, можно использовать её и писать свои клиенты для взаимодействия с ним.

# пусть при создании
from telebot import TeleBot
from envparse import Env

from app_2 import db

env = Env()

TOKEN = env.str("TOKEN")

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['subscribe'])
def subscribe_user(message):
    c = 1
    print("Запрос на подписку")
    bot.send_message(chat_id=message.chat.id, text="ахахахахаха")


bot.polling()

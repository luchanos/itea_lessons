# Flask-SQLAlchemy
# Alembic

# для генерации скриптов миграций вводим: alembic init alembic - появится папка alembic и файл alembic.ini
# в ини айле нас интересует sqlalchemy.url = driver://user:pass@localhost/dbname - это путь к БД

# для создания телеграм-ботов используется BotFather
# для управления отправками сообщений ботом используется PyTelegramBotApi (ещё его называют telebot)
# ещё у Телеграмм есть сырая API, можно использовать её и писать свои клиенты для взаимодействия с ним.

# пусть при создании
from telebot import TeleBot  # pip install pyTelegramBotAPI
from envparse import Env
from logging import getLogger
from app_2 import db, Profiles

env = Env()
logger = getLogger(__name__)
TOKEN = env.str("TOKEN")
bot = TeleBot(TOKEN)


def subscribe_profile(message):
    """Подписываем пользака на уведомления"""
    profile = Profiles.query.get(int(message.text))
    profile.is_subscribed = True
    profile.profile_tg_chat_id = message.chat.id
    db.session.commit()


def unsubscribe_profile(message):
    """Отписываем пользака от уведомлений"""
    profile = Profiles.query.get(int(message.text))
    profile.is_subscribed = False
    profile.profile_tg_chat_id = None
    db.session.commit()


@bot.message_handler(commands=['subscribe'])
def subscribe_user(message):
    """Обрабатываем запрос на подписку"""
    logger.info("Запрос на подписку")
    bot.reply_to(message, "Введите id своего профиля:")
    bot.register_next_step_handler(message, subscribe_profile)


@bot.message_handler(commands=['unsubscribe'])
def subscribe_user(message):
    """Обрабатываем запрос на отписку"""
    logger.info("Запрос на отписку")
    bot.reply_to(message, "Введите id своего профиля:")
    bot.register_next_step_handler(message, unsubscribe_profile)


bot.polling()

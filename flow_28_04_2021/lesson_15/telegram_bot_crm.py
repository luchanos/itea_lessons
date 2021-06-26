from telebot import TeleBot
from envparse import Env

from app_2 import Profiles, Users, db


# from flow_28_04_2021 import user_profiles_list, user_data_list, UserProfile, User

from secrets import token_hex

token = token_hex()
print(token)
env = Env()
TOKEN = env.str("TOKEN")

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=["subscribe_me"])
def subscribe_profile(message):
    """Подписываем пользака на уведомления"""
    profile = Profiles.query.get(int(message.text.split()[1]))
    profile.is_subscribed = True
    profile.profile_tg_chat_id = message.chat.id
    db.session.commit()


@bot.message_handler(commands=["unsubscribe_me"])
def unsubscribe_profile(message):
    """Отписываем пользака от уведомлений"""
    profile = Profiles.query.get(int(message.text.split()[1]))
    profile.is_subscribed = False
    profile.profile_tg_chat_id = None
    db.session.commit()

cnt = 0


def my_shiny_func(message):
    global cnt
    if cnt < 3:
        print("Я принял сообщение!")
        bot.reply_to(message=message, text=f"{message.chat.username}, ты выбрал {message.text}")
        bot.register_next_step_handler(message, my_shiny_func)
        cnt += 1


def planner(message):
    print(f"Для нового дня: {message.text}")


@bot.message_handler(commands=["planner"])
def echo(message):
    global cnt
    cnt = 0
    bot.reply_to(message=message, text=f"{message.chat.username}, давай запланируемся на 3 дней?")
    bot.register_next_step_handler(message, my_shiny_func)


@bot.message_handler(commands=["echo"])
def echo(message):
    bot.reply_to(message=message, text=f"{message.chat.username}, выбери одно из двух: курица или рыба?")
    bot.register_next_step_handler(message, my_shiny_func)


def notify(chat_id):
    message_to_send = input("Введите сообщение для отправки пользователю: ")
    bot.send_message(chat_id=chat_id, text=message_to_send)


@bot.message_handler(commands=["notify_all"])
def notify_all(message):
    """Хороший способ для оповещения всех пользователей по команде от админа"""
    _, user_token = message.text.split()
    if user_token == token:
        print("Я пошел в базу данных и вытащил всех, кто подписан на уведомления")
        profiles = Profiles.query.filter_by(is_subscribed=True)
        for profile in profiles:
            notify(chat_id=profile.profile_tg_chat_id)


if __name__ == "__main__":
    bot.polling()

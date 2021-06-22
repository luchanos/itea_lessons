# отправлять сообщения в Телегу можно и по-босяцки
# https://api.telegram.org/bot{ВАШ ТОКЕН}/sendMessage?chat_id={ВАШ ЧАТ ID}&parse_mode=Markdown&text=TEST

import requests
from app_2 import NotificationTasks, db
from envparse import Env
from time import sleep

env = Env()

TOKEN = env.str("TOKEN")
BASE_URL = 'https://api.telegram.org'
CHAT_ID = 362857450


def notify_users():
    # ламповый воркер для отправки уведомлений
    notifications = NotificationTasks.query.filter_by(status=None).all()
    for notification in notifications:
        requests.post(f"{BASE_URL}/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=Markdown&text={notification.message}")
        notification.status = "done"
        db.session.commit()


while True:
    notify_users()
    sleep(60)

# отправлять сообщения в Телегу можно и по-босяцки
# https://api.telegram.org/bot{ВАШ ТОКЕН}/sendMessage?chat_id={ВАШ ЧАТ ID}&parse_mode=Markdown&text=TEST

import requests
from app_2 import NotificationTasks, db
from envparse import Env
from time import sleep
import json

env = Env()

TOKEN = "1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM"
BASE_URL = 'https://api.telegram.org'
CHAT_ID = 362857450


def notify_users():
    # ламповый воркер для отправки уведомлений
    notifications = NotificationTasks.query.filter_by(status=None).all()
    for notification in notifications:
        url = f"{BASE_URL}/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={notification.message}"
        res = requests.post(url)
        result_dict = json.loads(res.content.decode())
        if result_dict["ok"] is True:
            notification.status = "done"
        else:
            notification.status = "errored"
        db.session.commit()


if __name__ == "__main__":
    while True:
        notify_users()
        sleep(30)

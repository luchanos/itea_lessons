import pytest
from app_2 import app, NotificationTasks, db
import psycopg2
import responses

from flow_28_04_2021.lesson_16.notification_worker import notify_users


# @pytest.fixture()
# def cleaner():
#     conn = psycopg2.connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")
#     with conn:
#         cursor = conn.cursor()
#         with cursor:
#             cursor.execute("""DELETE FROM users WHERE user_id > 0""")
#             cursor.execute("""DELETE FROM profiles WHERE profile_id > 0""")
#             cursor.execute("""TRUNCATE TABLE notification_tasks""")


def test_create_user(cleaner):
    payload = {
        "login": "Sviridov2",
        "password": "qwerty",
        "about_me": "engineer",
        "first_name": "Nikolai",
        "last_name": "Sviridov",
        "interests": "coding, blogging",
        "age": 29
               }
    test_client = app.test_client()
    resp = test_client.post('/create_user', json=payload)
    assert resp.status == '200 OK'


@responses.activate
def test_tg_worker_sender(cleaner):
    url = 'https://api.telegram.org/bot1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM/sendMessage?' \
          'chat_id=362857450&parse_mode=Markdown&text=тестовое сообщение'
    responses.add(responses.POST, url,
                  json={"success": True}, status=200)
    task = {'message': 'тестовое сообщение',
            'profile_tg_chat_id': '362857450'}
    notification_task = NotificationTasks(**task)
    db.session.add(notification_task)
    db.session.commit()
    notify_users()
    notified = NotificationTasks.query.filter_by(status="done")
    notified_list = list(notified)
    assert len(notified_list) == 1
    assert notified_list[0].message == 'тестовое сообщение'
    assert notified_list[0].profile_tg_chat_id == '362857450'

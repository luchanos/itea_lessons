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
def test_tg_worker_sender():
    """Тест на воркера. Он нуждается в:
    - задаче на нотификацию, которая ещё не обработана (status = NULL)
    Проверяем:
    - что статус отправки поменялся на done
    """
    json_expected = {
  "ok": True,
  "result": {
    "message_id": 265,
    "from": {
      "id": 1818338603,
      "is_bot": True,
      "first_name": "ITEA_TEST_BOT",
      "username": "ITEA_TEST_2_BOT"
    },
    "chat": {
      "id": 362857450,
      "first_name": "Nikolas",
      "last_name": "Luchanos",
      "username": "Luchanos",
      "type": "private"
    },
    "date": 1625071674,
    "text": "тестовое сообщение"
  }
}
    url = 'https://api.telegram.org/bot1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM/sendMessage?chat_id=362857450&text=test_message'
    responses.add(responses.POST, url,
                  json={"ok": True}, status=200)
    task = {'message': 'test_message',
            'profile_tg_chat_id': '362857450'}
    notification_task = NotificationTasks(**task)
    db.session.add(notification_task)
    db.session.commit()
    notify_users()
    notified = NotificationTasks.query.filter_by(status="done")
    notified_list = list(notified)
    assert len(notified_list) == 1
    assert notified_list[0].message == 'test_messag'
    assert notified_list[0].profile_tg_chat_id == '362857450'

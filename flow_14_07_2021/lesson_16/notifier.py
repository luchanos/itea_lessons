from flow_14_07_2021.lesson_7.app_example import MyTgClient, MyDbClient
from time import sleep

TOKEN = "1732311949:AAFothWVXVBFbwDuxa7ObGUIzlqcZkj7evs"
DB_URL = 'postgresql://newuser:qwerty@127.0.0.1:5432/postgres'

my_db_client = MyDbClient(DB_URL)
my_db_client.setup()
my_tg_client = MyTgClient(TOKEN)

while True:
    tasks = my_db_client.get_notification_tasks()
    for task in tasks:
        my_tg_client.send_text_message(chat_id=task[0], message=task[1])
        my_db_client.mark_notification_task_result(result=True, notification_task_id=task[2])
    sleep(3600)

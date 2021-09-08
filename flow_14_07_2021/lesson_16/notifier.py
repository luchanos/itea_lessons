from flow_14_07_2021.lesson_15.cw import MyAsyncDbClient
from flow_14_07_2021.lesson_17.async_tg_client import TgClientAsync
import asyncio
import json

TOKEN = "1732311949:AAFothWVXVBFbwDuxa7ObGUIzlqcZkj7evs"
DB_URL = 'postgresql://newuser:qwerty@127.0.0.1:5432/postgres'


async def mark_notification_task_result(db_client: MyAsyncDbClient, result, notification_task_id):
    await db_client.mark_notification_task_result(result, notification_task_id)


async def main():
    db_client = MyAsyncDbClient(DB_URL)
    tg_client = TgClientAsync(TOKEN)
    await db_client.setup()
    await tg_client.setup()

    # оповещаем пользователей
    tasks = await db_client.get_notification_tasks()
    tasks_for_async_exec = [tg_client.send_text_message(**dict(el)) for el in tasks]
    res = await asyncio.gather(*tasks_for_async_exec)

    # обрабатываем статусы отправок наших уведомлений
    notif_tasks_id_list = [dict(el)["notification_task_id"] for el in tasks]
    res_task_list = [json.loads(el)["ok"] for el in res]
    total = list(zip(res_task_list, notif_tasks_id_list))
    tasks_for_notif_status_upd = [db_client.mark_notification_task_result(*el) for el in total]
    await asyncio.gather(*tasks_for_notif_status_upd)


async def make_notification(tg_client, db_client, chat_id, message, notification_task_id):
    res = await tg_client.send_text_message(chat_id=chat_id, message=message)
    encoded_res = json.loads(res)["ok"]
    await db_client.mark_notification_task_result(encoded_res, notification_task_id)


async def main_2():
    db_client = MyAsyncDbClient(DB_URL)
    tg_client = TgClientAsync(TOKEN)
    await db_client.setup()
    await tg_client.setup()

    # оповещаем пользователей
    tasks = await db_client.get_notification_tasks()
    tasks_for_notification = [make_notification(tg_client,
                                                db_client,
                                                dict(el)["chat_id"],
                                                dict(el)["message"],
                                                dict(el)["notification_task_id"])
                              for el in tasks]
    await asyncio.gather(*tasks_for_notification)

asyncio.run(main_2())


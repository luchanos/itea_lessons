import psycopg2
import requests
from envparse import Env

env = Env()

# DB_URL = env.str("DB_URL")
# TOKEN = env.str("TOKEN")


class MyDbClient:
    PRODUCT_SELECT_QUERY = "SELECT * FROM products LIMIT %d"
    PRODUCT_INSERT_QUERY = "INSERT INTO products (description, quantity) VALUES ('%s', %d)"
    PRODUCT_DELETE_BY_ID_QUERY = "DELETE FROM products WHERE product_id = %d"

    SUBSCRIBE_USER = "INSERT INTO users_subs (username, chat_id, is_subs_active) VALUES ('%s', %d, true)"
    UNSUBSCRIBE_USER = "UPDATE users_subs SET is_subs_active = false WHERE chat_id = %d"
    GET_SUBSCRIBED_USERS_QUERY = "SELECT * FROM users_subs WHERE is_subs_active is true"

    GET_NOTIFICATIONS_TASKS_QUERY = "SELECT chat_id, message, notification_task_id  " \
                                    "FROM notification_tasks WHERE success is NULL"
    MARK_NOTIFICATION_TASK_RESULT_QUERY = "UPDATE notification_tasks SET success = %s WHERE notification_task_id = %d"

    def __init__(self, db_url):
        self.db_url = db_url
        self.connect = None

    def setup(self):
        self.connect = psycopg2.connect(self.db_url)

    def _check_connection(self):
        if not self.connect:
            print("Connection has not been set up! Please, user client.setup method to install connection!")
            return

    def get_products(self, limit: int) -> list:
        """Получает заданное количество записей из таблица products"""
        self._check_connection()
        with self.connect.cursor() as cursor:
            cursor.execute(self.PRODUCT_SELECT_QUERY % limit)
            return cursor.fetchall()

    def insert_new_product(self, description, quantity, *args, **kwargs):
        """Создаёт новый продукт в таблице products"""
        self._check_connection()
        with self.connect.cursor() as cursor:
            cursor.execute(self.PRODUCT_INSERT_QUERY % (description, quantity))
            self.connect.commit()

    def delete_product_by_id(self, product_id):
        """Удаляет продукт в таблице products"""
        self._check_connection()
        with self.connect.cursor() as cursor:
            cursor.execute(self.PRODUCT_DELETE_BY_ID_QUERY % product_id)
            self.connect.commit()

    def subscribe_user_notifications(self, chat_id, username):
        self._check_connection()
        with self.connect.cursor() as cursor:
            cursor.execute(self.SUBSCRIBE_USER % (username, chat_id))
            self.connect.commit()

    def unsubscribe_user_notifications(self, chat_id, username):
        self._check_connection()
        with self.connect.cursor() as cursor:
            cursor.execute(self.UNSUBSCRIBE_USER % chat_id)
            self.connect.commit()

    def get_subcribed_users(self):
        self._check_connection()
        with self.connect.cursor() as cursor:
            cursor.execute(self.GET_SUBSCRIBED_USERS_QUERY)
            return cursor.fetchall()

    def get_notification_tasks(self):
        self._check_connection()
        with self.connect.cursor() as cursor:
            cursor.execute(self.GET_NOTIFICATIONS_TASKS_QUERY)
            return cursor.fetchall()

    def mark_notification_task_result(self, result: bool, notification_task_id: int):
        self._check_connection()
        with self.connect.cursor() as cursor:
            cursor.execute(self.MARK_NOTIFICATION_TASK_RESULT_QUERY % (result, notification_task_id))
            self.connect.commit()


class MyTgClient:
    def __init__(self, token):
        self.token = token

    def send_text_message(self, message, chat_id):
        requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}")


class MyApplication:
    def __init__(self, db_client, tg_client):
        self.db_client = db_client
        self.tg_client = tg_client

    def setup_all_components(self):
        self.db_client.setup()

    def create_new_product(self):
        params = dict()
        params['description'] = input("Enter description: ")
        params['quantity'] = int(input("Enter quantity: "))
        self.db_client.insert_new_product(**params)
        message = f"New product: {params} has been created"
        self.tg_client.send_text_message(message)

    def run(self):
        self.setup_all_components()
        choice_mapper = {
            "q": exit,
            "1": self.create_new_product
        }

        print("Привет! Это приложение продуктового магазина! Введите команду для работы с ним или q для завершения.")
        print("q - завершить работу с приложением\n"
              "1 - создать новый продукт")
        while True:
            try:
                user_choice = input("Введите ваш выбор: ")
                choice_mapper[user_choice]()
            except KeyError:
                print("Вы ввели что-то не то, попробуйте ещё раз! ")


# if __name__ == "__main__":
#     my_tg_client = MyTgClient(TOKEN, [362857450, 308251648])
#     my_db_client = MyDbClient(DB_URL)
#     my_application = MyApplication(db_client=my_db_client, tg_client=my_tg_client)
#     my_application.run()

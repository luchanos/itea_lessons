import asyncpg
import asyncio
from logging import getLogger, StreamHandler
import sys

logger = getLogger(__name__)

stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")

DB_URL = 'postgresql://newuser:qwerty@127.0.0.1:5432/postgres'


class MyAsyncDbClient:
    PRODUCT_SELECT_QUERY = "SELECT * FROM products LIMIT $1"
    PRODUCT_BY_ID_SELECT_QUERY = "SELECT * FROM products WHERE product_id = $1"
    PRODUCT_INSERT_QUERY = "INSERT INTO products (description, quantity) VALUES ($1, $2)"
    PRODUCT_DELETE_BY_ID_QUERY = "DELETE FROM products WHERE product_id = $1"
    GET_SUBSCRIBED_USERS_QUERY = "SELECT * FROM users_subs WHERE is_subs_active is true"
    NOTIFICATION_TASK_CREATE_QUERY = "INSERT INTO notification_tasks (chat_id, message) VALUES ($1, $2)"
    NOTIFICATION_TASKS_SELECT_QUERY = "SELECT chat_id, message, notification_task_id " \
                                      "FROM notification_tasks WHERE success is NULL"
    MARK_NOTIFICATION_TASK_RESULT_QUERY = "UPDATE notification_tasks SET success = $1 WHERE notification_task_id = $2"

    def __init__(self, db_url):
        self.db_url = db_url
        self.db_pool = None

    async def setup(self):
        logger.info("Db client had been set up!")
        self.db_pool = await asyncpg.create_pool(DB_URL)

    def _check_connection(self):
        if not self.db_pool:
            logger.warning("Pool has not been set up! Please, user client.setup method to create pool!")
            return False
        return True

    async def get_subcribed_users(self):
        if self._check_connection():
            return await self.db_pool.fetch(self.GET_SUBSCRIBED_USERS_QUERY)

    async def get_products(self, limit: int) -> list:
        """Получает заданное количество записей из таблица products"""
        if self._check_connection():
            return await self.db_pool.fetch(self.PRODUCT_SELECT_QUERY, limit)

    async def get_product_by_id(self, product_id: int) -> list:
        """Получает продукт по id из таблицы products"""
        product_id = int(product_id)
        if self._check_connection():
            return await self.db_pool.fetch(self.PRODUCT_BY_ID_SELECT_QUERY, product_id)

    async def insert_new_product(self, description: str, quantity: int, *args, **kwargs):
        """Создаёт новый продукт в таблице products"""
        self._check_connection()
        await self.db_pool.execute(self.PRODUCT_INSERT_QUERY, description, quantity)

    async def get_subscribed_users(self):
        if self._check_connection():
            return await self.db_pool.fetch(self.GET_SUBSCRIBED_USERS_QUERY)

    async def delete_product_by_id(self, product_id: int):
        """Удаляет продукт в таблице products"""
        self._check_connection()
        product_id = int(product_id)
        return await self.db_pool.fetch(self.PRODUCT_DELETE_BY_ID_QUERY, product_id)

    async def create_notification_task(self, chat_id, message):
        self._check_connection()
        await self.db_pool.execute(self.NOTIFICATION_TASK_CREATE_QUERY, chat_id, message)

    async def get_notification_tasks(self):
        self._check_connection()
        return await self.db_pool.fetch(self.NOTIFICATION_TASKS_SELECT_QUERY)

    async def mark_notification_task_result(self, result, notification_task_id):
        self._check_connection()
        await self.db_pool.execute(self.MARK_NOTIFICATION_TASK_RESULT_QUERY, result, notification_task_id)

    async def close(self):
        await self.db_pool.close()


async def tasker(db_client: MyAsyncDbClient):
    tasks = [db_client.get_products(1) for _ in range(100)]
    res = await asyncio.gather(*tasks)
    for el in res:
        print(el)


async def main():
    db_client = MyAsyncDbClient(DB_URL)
    await db_client.setup()
    ls = [tasker(db_client), tasker(db_client)]
    await asyncio.gather(*ls)

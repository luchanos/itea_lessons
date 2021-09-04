import asyncpg
import asyncio
from datetime import datetime


DB_URL = 'postgresql://newuser:qwerty@127.0.0.1:5432/postgres'
num = 0


class MyAsyncDbClient:
    PRODUCT_SELECT_QUERY = "SELECT * FROM products LIMIT $1"
    PRODUCT_BY_ID_SELECT_QUERY = "SELECT * FROM products WHERE product_id = $1"
    PRODUCT_INSERT_QUERY = "INSERT INTO products (description, quantity) VALUES ($1, $2)"
    PRODUCT_DELETE_BY_ID_QUERY = "DELETE FROM products WHERE product_id = $1"
    GET_SUBSCRIBED_USERS_QUERY = "SELECT * FROM users_subs WHERE is_subs_active is true"

    def __init__(self, db_url):
        self.db_url = db_url
        self.db_pool = None

    async def setup(self):
        print("Client had been set up!")
        self.db_pool = await asyncpg.create_pool(DB_URL)

    def _check_connection(self):
        if not self.db_pool:
            print("Pool has not been set up! Please, user client.setup method to create pool!")
            return False
        return True

    async def get_products(self, limit: int) -> list:
        """Получает заданное количество записей из таблица products"""
        global num
        num += 1
        print(num)
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
        async with self.db_pool:
            await self.db_pool.execute(self.PRODUCT_INSERT_QUERY, description, quantity)

    async def get_subscribed_users(self):
        if self._check_connection():
            return await self.db_pool.fetch(self.GET_SUBSCRIBED_USERS_QUERY)

    async def delete_product_by_id(self, product_id: int):
        """Удаляет продукт в таблице products"""
        self._check_connection()
        product_id = int(product_id)
        async with self.db_pool:
            res = await self.db_pool.execute(self.PRODUCT_DELETE_BY_ID_QUERY, product_id)
            return res


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


# start = datetime.now()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# print(datetime.now() - start)

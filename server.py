"""Sanic он про производительность, простоту использования и гибкость

Особенности:
- синхронную функцию тоже можно подсовывать в обработчики, но лучше использовать асинхронную
- первым аргументом в обработчике должен быть объект request
- мы всегда в ответе должны отдавать объект типа response
- сервер, который мы пишем, сразу будет доступен для развёртки в продакшене"""


from sanic import Sanic, Request
from sanic.response import HTTPResponse, text  # text - тип ответа на запрос
from datetime import datetime

from flow_14_07_2021.lesson_15.cw import MyAsyncDbClient, DB_URL

app = Sanic("CRM_tech_app")

db_client = MyAsyncDbClient(DB_URL)
app.db_client = db_client
# app.before_server_start(app.db_client.setup())

# app.config.DB_NAME = 'appdb'
# app.config['DB_USER'] = 'appuser'
#
# db_settings = {
#     'DB_HOST': 'localhost',
#     'DB_NAME': 'appdb2',
#     'DB_USER': 'appuser2'
# }
# app.config.update(db_settings)


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


@app.get("/my_params/<param_1>")
async def hello_world(request, param_1):
    return text(f"{param_1}")


@app.get("/write_to_file")
async def write_to_file(request):
    with open("testfile.txt", "a") as f_o:
        f_o.write(str(datetime.now()) + "\n")
    return text("OK. I wrote it!")


@app.get("/read_from_file")
async def read_from_file(request):
    with open("testfile.txt", "r") as f_o:
        lines = f_o.readlines()
    if len(lines) == 0:
        return text("The file is empty!")
    return text("".join(lines))


@app.get("/clean_file")
async def clean_file(request):
    with open("testfile.txt", "w") as f_o:
        pass
    return text("File cleaned")


@app.get("/home")
async def main_page(request: Request) -> HTTPResponse:
    return text("Домашняя страница")


@app.get("/setup_resources")
async def setup_resources(request):
    await app.db_client.setup()


@app.get("/get_products")
async def get_products(request):
    res = await app.db_client.get_products(1)
    if not res:
        return text("Not OK!")
    return text("OK")


# команда sanic server.app поднимает сервер саника
# app.run()

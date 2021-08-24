"""Sanic он про производительность, простоту использования и гибкость

Особенности:
- синхронную функцию тоже можно подсовывать в обработчики, но лучше использовать асинхронную
- первым аргументом в обработчике должен быть объект request
- мы всегда в ответе должны отдавать объект типа response
- сервер, который мы пишем, сразу будет доступен для развёртки в продакшене"""


from sanic import Sanic, Request
from sanic.response import HTTPResponse, text  # text - тип ответа на запрос

app = Sanic("CRM_tech_app")

app.config.DB_NAME = 'appdb'
app.config['DB_USER'] = 'appuser'

db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb2',
    'DB_USER': 'appuser2'
}
app.config.update(db_settings)


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


@app.get("/home")
async def main_page(request: Request) -> HTTPResponse:
    return text("Домашняя страница")

# команда sanic server.app поднимает сервер саника
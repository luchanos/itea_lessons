"""Sanic он про производительность, простоту использования и гибкость

Особенности:
- синхронную функцию тоже можно подсовывать в обработчики, но лучше использовать асинхронную
- первым аргументом в обработчике должен быть объект request
- мы всегда в ответе должны отдавать объект типа response
- сервер, который мы пишем, сразу будет доступен для развёртки в продакшене"""


from sanic import Sanic, Request
from sanic.response import HTTPResponse, text, json  # text - тип ответа на запрос
from datetime import datetime

from logging import getLogger, StreamHandler
import sys

logger = getLogger(__name__)

stdout_handler = StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)
logger.setLevel("DEBUG")

app = Sanic("CRM_tech_app")


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


@app.get("/my_params/<param_1>")
async def my_params(request, param_1):
    return text(f"{param_1}")


@app.get("/write_to_file")
async def write_to_file(request):
    with open("opt/testfile.txt", "a") as f_o:
        f_o.write(str(datetime.now()) + "\n")
    return text("OK. I wrote it!")


@app.get("/read_from_file")
async def read_from_file(request):
    with open("opt/testfile.txt", "r") as f_o:
        lines = f_o.readlines()
    if len(lines) == 0:
        return text("The file is empty!")
    return text("".join(lines))


@app.get("/clean_file")
async def clean_file(request):
    with open("opt/testfile.txt", "w") as f_o:
        pass
    return text("File cleaned")


@app.get("/home")
async def main_page(request: Request) -> HTTPResponse:
    return text("Домашняя страница")

# команда sanic server.app поднимает сервер саника
# app.run()

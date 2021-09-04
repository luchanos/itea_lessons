"""Sanic он про производительность, простоту использования и гибкость

Особенности:
- синхронную функцию тоже можно подсовывать в обработчики, но лучше использовать асинхронную
- первым аргументом в обработчике должен быть объект request
- мы всегда в ответе должны отдавать объект типа response
- сервер, который мы пишем, сразу будет доступен для развёртки в продакшене"""


from sanic import Sanic, Request
from sanic.response import HTTPResponse, text, json  # text - тип ответа на запрос
from datetime import datetime
import json as json_original

from flow_14_07_2021.lesson_15.cw import MyAsyncDbClient, DB_URL
from flow_14_07_2021.lesson_7.app_example import MyTgClient, MyDbClient

TOKEN = "1732311949:AAFothWVXVBFbwDuxa7ObGUIzlqcZkj7evs"

app = Sanic("CRM_tech_app")

# db_client = MyAsyncDbClient(DB_URL)
db_client = MyDbClient(DB_URL)
db_client.setup()
tg_client = MyTgClient(TOKEN)
app.db_client = db_client
app.tg_client = tg_client
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
async def my_params(request, param_1):
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
    app.db_client.setup()
    return text("Resources has been set up!")


@app.get("/get_products")
async def get_products(request):
    res = app.db_client.get_products(10)
    if not res:
        return text("Not OK!")
    return text("OK")


# @app.post("/get_product_by_id")
# async def get_product_by_id(request):
#     data_from_request = json_original.loads(request.body)
#     res = app.db_client.get_product_by_id(data_from_request["product_id"])
#     product = res[0]
#     if not res:
#         return text("Not OK!")
#     return text(f"Продукт: {product['description']}\nКоличество: {product['quantity']}")


# @app.post("/get_product_by_id_json")
# async def get_product_by_id_json(request):
#     data_from_request = json_original.loads(request.body)
#     res = await app.db_client.get_product_by_id(data_from_request["product_id"])
#     product = res[0]
#     if not res:
#         return text("Not OK!")
#     return json(dict(product))


# @app.get("/get_product_by_id_json_2/<product_id>")
# async def get_product_by_id_json_2(request, product_id):
#     res = await app.db_client.get_product_by_id(product_id)
#     if not res:
#         return text("Product has not been found in database!")
#     return json(dict(res[0]))


# @app.delete("/delete_product_by_id/<product_id>")
# async def delete_product_by_id(request, product_id):
#     res = await app.db_client.delete_product_by_id(product_id)
#     if not res:
#         return text("Product has not been found in database!")
#     return json(dict(res[0]))

def users_notification(message_to_users):
    subscribed_users = app.db_client.get_subcribed_users()
    for user in subscribed_users:
        app.tg_client.send_text_message(f"{user[1]}! {message_to_users}", user[2])


@app.post("/add_product")
async def add_product(request):
    data_from_request = json_original.loads(request.body)
    app.db_client.insert_new_product(data_from_request["description"],
                                     data_from_request["quantity"])
    message_to_users = f"Мы получили новый продукт на склад: {data_from_request['description']}" \
                       f" в количестве {data_from_request['quantity']}"
    users_notification(message_to_users)
    return json({"success": True})


@app.post("/force_users_notification")
async def force_users_notification(request):
    data_from_request = json_original.loads(request.body)
    users_notification(data_from_request["message"])
    return json({"success": True})

# команда sanic server.app поднимает сервер саника
app.run()

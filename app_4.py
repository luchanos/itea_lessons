import json

from flask import Flask, Response, Request, request

from flow_14_07_2021.lesson_7.app_example import MyDbClient, MyTgClient


TOKEN = "1818338603:AAEv3AOttf2NqRSSphapItXr-ADv3sbL0tM"
DB_URL = 'postgresql://postgres:dbpass@127.0.0.1:5432/postgres'

app = Flask("my_shiny_app")

my_db_client = MyDbClient(DB_URL)
my_db_client.setup()

app.products_db_client = my_db_client


@app.route("/")
def homepage():
    print("Тест")
    return Response(status=404, response="<h1>Oops!</h2>"
                                         "<div>https://www.youtube.com/watch?v=dQw4w9WgXcQ</div>")
    # return "<h1>Hello, World!</h2>"

# {"error": "Need auth!"}


@app.route("/get_products")
def get_products():
    res = app.products_db_client.get_products(10)
    return Response(status=200, response=json.dumps(res))


class TokenError(Exception):
    def __str__(self):
        return "No token!"

    def __repr__(self):
        return "No token!"


TOKEN_LIST = [
    "11c786c0-0a03-4699-b838-b71fc931ceb5",
    "17e10009-c687-4729-ae13-04982e65bfe6"
]


def get_token_from_db(token):
    """Ходит в базу и проверяет есть ли там такой токен или хэш токена"""
    return token in TOKEN_LIST


def check_token(request_data):
    token = request_data.get("token")
    if not get_token_from_db(token):
        raise TokenError()


@app.route("/add_product", methods=["POST"])
def add_product():
    request_data = request.json
    try:
        check_token(request_data)
    except TokenError as err:
        return Response(status=403, response=str(err))
    product_data = request_data["product_info"]
    app.products_db_client.insert_new_product(description=product_data["description"],
                                              quantity=product_data["quantity"])
    return Response(status=200, response="OK")


if __name__ == "__main__":
    app.run(debug=True)

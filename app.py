# магазинное приложения на Flask
from uuid import uuid4

from flask import Flask, render_template, url_for, request, current_app, make_response, redirect
import json

# request - контекстная переменная. Это такой тип переменных, который ведёт себя, как глобальная, но таковой она не
# является. Обращаясь к такой переменной мы получаем её значение в конкретном потоке. Технически такая переменная
# локальная или внутрипоточная.

# существует 2 вида контекстов: контекст приложения и контекст запроса.
# Контекст приложения используется для хранения: подключение к БД, настройки приложения и т.д.
# Контекст запроса: запрос и сессия.

# todo luchanos прочитать про контексты приложения и контексты запроса https://pythonru.com/uroki/4-konteksty-vo-flask

app = Flask("my_shiny_shop_corp_app")  # можно задать параметр template_folder, чтобы указать откуда подтягивать шаблоны

# todo вот это зачем?
# with app.test_request_context('/create_department'):
#     print("ПУТЬ", request.path)
#     print("МЕТОД", request.method)
#     print("ИМЯ", current_app.name)


@app.route("/main")
@app.route("/home")
@app.route("/")
def main_page():
    return render_template("base.html")


@app.route("/shop/<int:shop_id>")
def get_shop(shop_id):
    return render_template("shop.html", shop_id=shop_id)


@app.route("/ping")
def ping():
    return "OK"  # автоматически будет сконвертировано в объект ответа со статусом ответа 200 text/html в заголовке

# варианты ответа на запрос:
# - В виде строки или с помощью шаблонизатора
# - Объекта ответа
# - Кортежа в формате (response, status, headers) или (response, headers)


@app.route("/create_department")
def create_department():
    res = make_response("Департамент создан!", 200)
    res.headers['Content-Type'] = 'text/plain'
    res.headers['Server'] = 'Foobar'
    return res


# настройка куки (базовая задача для любого веб-приложения). Будут активны до конца сессии в браузере.
# При желании можно задать срок истечения кук вручную.
@app.route("/set_cookie")
def set_cookie():
    res = make_response("Cookie setter")
    res.set_cookie("cas_id", uuid4(), 60*60*24*15)  # стухнут через 15 дней
    return res


# если не залогинен
@app.route('/admin')
def admin():
    if not request.cookies:
        return redirect(url_for('login'))  # если не залогинен, выполнять редирект на страницу входа
    return render_template('base.html')


@app.route('/login')
def login_page():
    return "Страница для авторизации"


# todo luchanos надо понять чем редирект 301 отличается от редиректа 302

# существуют специальные декораторы, которые позволяют исполнить опреелённый код до или после запроса.


# hooks - это штуки, которые перехватывают запросы.
@app.before_first_request
def before_first_request():
    print("before_first_request() called")


@app.before_request
def before_request():
    print("before_request() called")


@app.after_request
def after_request(response):
    print("after_request() called")
    return response


@app.route("/")
def index():
    print("index() called")
    return '<p>Testings Request Hooks</p>'

# использование url_for для создания URL


# print(app.url_map)  # покажет мапу обработчиков запросов:
"""
 <Rule '/main' (HEAD, GET, OPTIONS) -> main_page>,
 <Rule '/' (HEAD, GET, OPTIONS) -> main_page>,
 <Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/shop/<shop_id>' (HEAD, GET, OPTIONS) -> get_shop>])
"""


if __name__ == "__main__":
    # так создаётся простое приложение на Flask, которое при запуске поднимет серверочек
    app.run(debug=True)

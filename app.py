from flask import Flask, request, render_template, Response
import json
from flow_28_04_2021 import me, UserProfile, User, user_data_list, user_profiles_list

app = Flask(__name__)


@app.route("/ping")
def ping():
    return "OK"


# @app.route("/main")
# @app.route("/homepage")
# def homepage():
#     return "<h1>Домашняя страница</h1>"


# вариант с шаблоном
# @app.route("/")
# @app.route("/main")
# @app.route("/homepage")
# def homepage():
#     return render_template("mainpage.html")


@app.route("/")
@app.route("/main")
@app.route("/homepage")
def homepage():
    return render_template("mainpage.html")  # не забывайте указывать формат файла!!!
    # return "<h1>Главная страница</h1>"


@app.route("/create_test_data", methods=["POST"])
def create_test_data_in_mongo():
    for user_profile_data in zip(user_profiles_list, user_data_list):
        user_profile = UserProfile(**user_profile_data[0]).save()
        User(user_profile=user_profile, **user_profile_data[1]).save()
    return "OK"


def notify_registered_user():
    print("Отправка сообщения в Телеграмм пользователю, который зарегался")


def proccess_interests(interests_list):
    print(f"Логика обработки интересов пользователя {interests_list}")


def moderate_interests(interests_list):
    if "bad interest" in interests_list:
        pass  # можете подумать над способом исключить элемент из списка
    return interests_list


# для прокидывания информации в теле запроса можно кидать json вида:
# {"name": "Николай",
# "surname": "Свиридов",
# "position": "Главный инженер"}
@app.route("/create_user", methods=["POST"])
def create_user():
    """Будем одновременно создаать пользователя с его учетной записью"""

    # работаем сразу с 3мя компонентами:
    # - веб-фреймворк (Flask)
    # - БД-библиотека (mongoengine)
    # - бизнес-логика или бизнес-контекст (это всё, что мы пишем дополнительно)
    if request.method == "POST":
        user_data = json.loads(request.data)
        user_profile = UserProfile(login=user_data["login"],
                                   password=user_data["password"],
                                   about_me=user_data["about_me"],).save()
        interests_list = moderate_interests(user_data["interests"])
        user = User(user_profile=user_profile,
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    interests=interests_list,
                    age=user_data["age"]).save()
        notify_registered_user()
        # return f"Пользователь {json.loads(request.data)} создан!"  # используем json модуль, чтобы получить структуру
        return render_template("create_user.html", user_data=user)


@app.route('/search_user_by_id/<string:user_id>')
def search_user_by_id(user_id):
    return str(User.objects(pk=user_id))


# сервисные ручки, которые требуют проверки специального токена:
@app.route('/srv/personal_info')
def personal_info():
    token = json.loads(request.data)["token"]
    if token == "TOKEN":
        return "Персональные данные"
    return Response(status=403, response=json.dumps({"error": "Need auth!"}))  # если хотим что-то отдавать обратно


# УРОК 12
# @app.route("/ten_users")
# def ten_users():
#     users_list = User.objects.all()[:2]
#     print(users_list)
#     return render_template("ten_users.html", users_list=users_list)  # не забывайте указывать формат файла!!!

@app.route("/base")
def base():
    return render_template("base.html")  # не забывайте указывать формат файла!!!


@app.route("/ten_users")
def ten_users():
    users_list = User.objects.all()[:2]
    print(users_list)
    return render_template("ten_users_ext.html", users_list=users_list)  # не забывайте указывать формат файла!!!


app.run(debug=True)

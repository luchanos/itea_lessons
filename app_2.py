from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, Response
import json
from logging import getLogger

# pip install Flask-SQLAlchemy==2.5.1

DB_URL = 'postgresql://postgres:dbpass@127.0.0.1:5432/postgres'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL  # определит тип БД и подключение к ней

# то есть если нам надо будет поменять БД, то всё, что потребуется сделать - просто поменять строку подключения

# подключили алхимию к нашему приложению
db = SQLAlchemy(app)
logger = getLogger(__name__)


class Profiles(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    about_me = db.Column(db.String(100))
    is_subscribed = db.Column(db.Boolean, default=False)
    profile_tg_chat_id = db.Column(db.String(10), nullable=True)  # тут будем хранить id чата в Телеге для оповещения
    # пользователя о чём-либо


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    interests = db.Column(db.String(100))
    age = db.Column(db.Integer)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'))  # указание внешнего ключа


class NotificationTasks(db.Model):
    notification_task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(100)) # сюда будем писать сообщения для отправки
    status = db.Column(db.String(10), default=None)
    profile_tg_chat_id = db.Column(db.String(10), nullable=True)  # не делал Foreign Key, вдруг chat id изменится


# после написания моделей, открываем консольку Python для нашего проекта
# импортируем туда db -> db.create_all() - создадутся базы
@app.route("/create_user", methods=["POST"])
def create_user():
    """Будем одновременно создаать пользователя с его учетной записью"""
    if request.method == "POST":
        user_data = json.loads(request.data)
        user_profile = Profiles(login=user_data["login"],
                                password=user_data["password"],
                                about_me=user_data["about_me"],)
        db.session.add(user_profile)  # пока запишет в сессию, но не в базу
        db.session.flush()
        user = Users(profile_id=user_profile.profile_id,
                     first_name=user_data["first_name"],
                     last_name=user_data["last_name"],
                     interests=user_data["interests"],
                     age=user_data["age"])
        db.session.add(user)  # пока запишет в сессию, но не в базу
        db.session.flush()
        db.session.commit()  # коммитим наши изменения
        return render_template("create_user.html", user_data=user_data)


@app.route("/register_notification_task", methods=["POST"])
def create_notification_task():
    if request.method == 'POST':
        data = json.loads(request.data)
        profile_id = data['user_id']
        profile = Profiles.query.get(profile_id)
        if profile.is_subscribed:
            message = data['message']
            notification_task = NotificationTasks(message=message,
                                                  profile_tg_chat_id=profile.profile_tg_chat_id)
            db.session.add(notification_task)
            db.session.commit()
        else:
            print(f"Profile with id {profile.profile_id} is not subscripted!")
            logger.info(f"Profile with id {profile.profile_id} is not subscripted!")
    return Response("OK")


if __name__ == '__main__':
    app.run(debug=True)

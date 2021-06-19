from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template
import json

DB_URL = 'postgresql://postgres:dbpass@127.0.0.1:5432/postgres'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL  # определит тип БД и подключение к ней

# то есть если нам надо будет поменять БД, то всё, что потребуется сделать - просто поменять строку подключения

# подключили алхимию к нашему приложению
db = SQLAlchemy(app)


class Profiles(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50))
    about_me = db.Column(db.String(100))


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    interests = db.Column(db.String(100))
    age = db.Column(db.Integer)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profile_id'))  # указание внешнего ключа


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


if __name__ == '__main__':
    app.run(debug=True)

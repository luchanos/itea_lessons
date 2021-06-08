from flask import Flask, request
from datetime import datetime
import mongoengine as me

me.connect("LESSON_9_DB")

user_profiles_list = [
    {"login": "lol",
     "password": "123",
     "about_me": "some lol",
     "likes": 3},
    {"login": "kek",
     "password": "1234",
     "about_me": "some kek",
     "likes": 5},
    {"login": "cheburek",
     "password": "12345",
     "about_me": "some cheburek",
     "likes": 6},
    {"login": "some_user",
     "password": "1234567",
     "about_me": "some some_user",
     "likes": 0}
]


user_data_list = [
    {"first_name": "Nikolai",
     "last_name": "Sviridov",
     "interests": ["mma", "programming", "blogging"],
     "age": 29
     },
    {"first_name": "Anna",
     "last_name": "Prozorova",
     "interests": ["smimming", "dancing", "singing"],
     "age": 35
     },
    {"first_name": "Semen",
     "last_name": "Ivanov",
     "interests": ["fishing", "riding"],
     "age": 21
     },
    {"first_name": "Chubaka",
     "last_name": "Chubakov",
     "interests": ["barking"],
     "age": 12
     }
]

# нет понятия таблица, вместо неё понятие коллекция
class UserProfile(me.Document):
    login = me.StringField(required=True, min_length=3, max_length=120, unique=True)
    password = me.StringField(required=True, min_length=2)  # в таком виде хранить пароли не стоит, надо хэшировать
    about_me = me.StringField()
    likes = me.IntField(default=0)


class User(me.Document):
    # объявляем поля коллекций
    first_name = me.StringField(min_length=1, max_length=100, required=True)
    last_name = me.StringField(min_length=1, max_length=100)
    interests = me.ListField()
    age = me.IntField(min_value=12, max_value=99)
    created_at = me.DateTimeField()
    user_profile = me.ReferenceField(UserProfile, reverse_delete_rule=me.CASCADE)

    # CASCADE - удалит юзера при удалении профайла
    # подробнее - https://docs.mongoengine.org/apireference.html

    def say_hello(self):
        return f"Hello, {self.first_name}"

    def __str__(self):
        return f"{self.first_name}, {self.last_name}, {self.interests}, {self.age}"

    def save(self, *args, **kwargs):
        self.created_at = datetime.now()
        return super().save(*args, **kwargs)

# http://127.0.0.1:5000/ping
my_app = Flask("my_shiny_app")


@my_app.route("/ping")
def ping():
    return f"OK {datetime.now()}"


@my_app.route("/check_method", methods=["GET", "POST", "UPDATE", "DELETE", "PUT"])
def check_method():
    return f"{request.method}"


@my_app.route("/crete_test_data", methods=["POST"])
def create_test_data_in_mongo():
    for user_profile_data in zip(user_profiles_list, user_data_list):
        user_profile = UserProfile(**user_profile_data[0]).save()
        User(user_profile=user_profile, **user_profile_data[1]).save()
    return "OK"


@my_app.route("/delete_test_data", methods=["DELETE"])
def delete_all_data_in_test_db():
    User.objects.all().delete()
    UserProfile.objects.all().delete()
    return "OK"


@my_app.route('/search_user_by_id/<string:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def search_user_by_id(user_id):
    c = request
    res = User.objects(id=user_id)
    return f"Результат: {res}"


if __name__ == "__main__":
    my_app.run(debug=True)

from app_2 import app, Users, Profiles
import responses

from tests.utils import test_page


def test_create_user():
    user_data = {"login": "Sviridov3",
                 "password": "qwerty",
                 "about_me": "engineer",
                 "first_name": "Nikolai",
                 "last_name": "Sviridov",
                 "interests": "coding, blogging",
                 "age": 29}
    test_client = app.test_client()
    resp = test_client.post('/create_user', json=user_data)

    assert resp.status == '200 OK'

    profiles_records = Profiles.query.filter_by(login=user_data['login'])
    profiles_list = list(profiles_records)
    assert len(profiles_list)
    test_profile = profiles_list[0]
    assert test_profile.login == user_data["login"]
    users_records = Users.query.filter_by(profile_id=test_profile.profile_id)
    users_list = list(users_records)
    assert len(users_list) == 1
    test_user = users_list[0]

    # в тестах хоро проверять все поля, которые возвращаются из БД,
    # если вы с ней работаете и тест на это заточен

    # проверяем данные в таблице users
    assert test_user.first_name == user_data["first_name"]
    assert test_user.last_name == user_data["last_name"]
    assert test_user.interests == user_data["interests"]
    assert test_user.age == user_data["age"]


@responses.activate
def test_outer_request():
    test_client = app.test_client()
    responses.add(responses.GET, "http://google.com",
                  body=test_page, status=200)
    resp = test_client.get('/test_bp')
    assert resp.data == b'\nOK\n'

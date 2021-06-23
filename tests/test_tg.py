import pytest
from app_2 import app
import psycopg2


@pytest.fixture()
def cleaner():
    conn = psycopg2.connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")
    with conn:
        cursor = conn.cursor()
        with cursor:
            cursor.execute("""DELETE FROM users WHERE user_id > 0""")
            cursor.execute("""DELETE FROM profiles WHERE profile_id > 0""")


def test_tg_totifications(cleaner):
    payload = {
        "login": "Sviridov2",
        "password": "qwerty",
        "about_me": "engineer",
        "first_name": "Nikolai",
        "last_name": "Sviridov",
        "interests": "coding, blogging",
        "age": 29
               }
    test_client = app.test_client()
    resp = test_client.post('/create_user', json=payload)
    assert resp.status == '200 OK'

import psycopg2
import pytest


@pytest.fixture(autouse=True)
def cleaner():
    conn = psycopg2.connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")
    with conn:
        cursor = conn.cursor()
        with cursor:
            cursor.execute("""DELETE FROM users WHERE user_id > 0""")
            cursor.execute("""DELETE FROM profiles WHERE profile_id > 0""")
            cursor.execute("""TRUNCATE TABLE notification_tasks""")

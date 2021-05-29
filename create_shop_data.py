import psycopg2

CREATE_SHOP_TABLE = """
CREATE TABLE shops (
shop_id SERIAL NOT NULL,
shop_name TEXT,
created_dt DATE,
updated_dt DATE
)
"""


if __name__ == '__main__':
    conn = psycopg2.connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")
    table_querries = [CREATE_SHOP_TABLE]
    with conn:
        with conn.cursor() as cursor:
            for query_list in [table_querries]:
                for query in query_list:
                    cursor.execute(query)


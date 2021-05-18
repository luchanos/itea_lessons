import psycopg2

CREATE_DEPARTMENT_TABLE = """
CREATE TABLE IF NOT EXISTS departments (
department_id SERIAL PRIMARY KEY,
department_name TEXT NOT NULL,
UNIQUE (department_name)
);
"""

CREATE_EMPLOYEES_TABLE = """
CREATE TABLE IF NOT EXISTS employees (
employee_id SERIAL PRIMARY KEY,
fio TEXT NOT NULL,
position TEXT NOT NULL,
department_id INTEGER NOT NULL,
FOREIGN KEY (department_id) REFERENCES departments (department_id)
ON DELETE CASCADE);
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY NOT NULL,
    created_dt DATE NOT NULL,
    updated_dt DATE NOT NULL,
    order_type TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    serial_no INTEGER NOT NULL,
    creator_id INTEGER NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES employees (employee_id)
    );
"""

INSERT_TEST_DEPARTMENT_DATA = """
INSERT INTO departments (department_name) 
VALUES 
('Информационный отдел'), 
('Продажи'), 
('Маркетинг'), 
('Сервис'), 
('Бухгалтерия'),
('Логистика'), 
('Служба безопасности')
"""

INSERT_TEST_EMPLOYEES_DATA = """
INSERT INTO employees (fio, position, department_id)
VALUES ('Иванов Иван Иванович', 'грузчик', 6),
('Петров Пётр Петрович', 'грузчик', 6),
('Сидоров Сидор Сидорович', 'грузчик', 6),
('Свиридов Николай Нколаевич', 'ведущий разработчик', 1),
('Бегунов Семён Валерьевич', 'разработчик', 1),
('Киримов Иван Сергеевич', 'младший разработчик', 1),
('Лавров Игорь Геннадьевич', 'сервисный инженер', 4),
('Бугров Антон Николаевич', 'главный сервисный инженер', 4),
('Сажин Марат Игнатьевич', 'инженер технической поддержки', 4)
"""

TEST_INSERT_ORDERS_DATA = """

"""

if __name__ == '__main__':
    conn = psycopg2.connect("postgres://postgres:dbpass@0.0.0.0:5432/postgres")
    table_querries = [CREATE_DEPARTMENT_TABLE, CREATE_EMPLOYEES_TABLE, CREATE_ORDERS_TABLE]
    data_querries = [INSERT_TEST_DEPARTMENT_DATA, INSERT_TEST_EMPLOYEES_DATA]
    with conn:
        with conn.cursor() as cursor:
            for query_list in [table_querries, data_querries]:
                for query in query_list:
                    cursor.execute(query)

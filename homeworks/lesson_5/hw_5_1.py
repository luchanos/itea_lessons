"""Создать базу данных с названием order_service_db. Создать в ней несколько таблиц:

Таблица ЗАЯВКИ (orders)
- id заявки (order_id) - целое число
- дата создания (created_dt) - текст
- дата обновления заявки (updated_dt) - текст
- тип заявки (order_type) - текст
- описание (description) - текст
- статус заявки (status) - текст
- серийный номер аппарата (serial_no) - целое число
- id создателя заявки (creator_id) - целое число

Таблица СОТРУДНИКИ (employees)
- id сотрудника (employee_id) - целое число
- ФИО (fio) - текст
- должность (position) - текст
- id подразделения (department_id) - целое число

Таблица ПОДРАЗДЕЛЕНИЯ (departments)
- id подразделения (department_id) - целое число
- название подразделения (department_name) - текст

Написать код создания таблиц на языке SQL, предусмотреть необходимые ограничения."""

DEPARTMENTS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS departments (
department_id SERIAL PRIMARY KEY,
department_name TEXT NOT NULL,
UNIQUE (department_name)
);
"""

EMPLOYEES_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS employees (
employee_id SERIAL PRIMARY KEY,
fio TEXT NOT NULL,
position TEXT NOT NULL,
department_id INTEGER NOT NULL,
FOREIGN KEY (department_id) REFERENCES departments (department_id)
ON DELETE CASCADE);
"""

ORDERS_TABLE_QUERY = """
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

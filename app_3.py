"""Продолжаем работу над нашей CRM. Теперь нужно реализовать несколько web-ручек для управления нашей системой:
создание департамента, заявки, сотрудника
редактирование информации о департаменте, заявке сотруднике
удаление данных о заявке, департаменте и сотруднике
поиск по id/дате/любому другому параметру (на ваш выбор) департамента, сотрудника, зявки
Для выполнения ДЗ можно использовать интеграцию с любой изученной БД (sqlite, Postgresql, Mongo)"""

from flask import Flask, request
import mongoengine as me
import json
from datetime import datetime as dt

me.connect("home9")

app = Flask(__name__)

department = [
    {"department_name": "IT1"},
    {"department_name": "IT2"},
    {"department_name": "IT1"},
    {"department_name": "IT3"},
    {"department_name": "IT1"},
    {"department_name": "IT3"},
    {"department_name": "IT2"}
]

employees = [
    {"fio": "Andrii",
     "position": "chef"
     },
    {"fio": "Nikolai",
     "position": "zam"
     },
    {"fio": "Vasia",
     "position": "worker"
     },
    {"fio": "Igor",
     "position": "svarchik"
     },
    {"fio": "Sasha",
     "position": "komputorshchik"
     },
    {"fio": "Jenia",
     "position": "gamer"
     },
    {"fio": "Dmitriy",
     "position": "proffesor"
     },
]

orders = [
    {"created_dt": '2021-01-07',
     "order_type": "order_type_1",
     "description": "some",
     "status": "Active",
     "serial_no": 11111
     },
    {"created_dt": '2021-01-07',
     "order_type": "order_type_2",
     "description": "some",
     "status": "Active",
     "serial_no": 22222
     },
    {"created_dt": '2021-01-07',
     "order_type": "order_type_3",
     "description": "some",
     "status": "Active",
     "serial_no": 33333
     },
    {"created_dt": '2021-01-07',
     "order_type": "order_type_4",
     "description": "some",
     "status": "Active",
     "serial_no": 44444
     },
    {"created_dt": '2021-01-07',
     "order_type": "order_type_5",
     "description": "some",
     "status": "Closed",
     "serial_no": 55555
     }
]


class Department(me.Document):
    created_dt = me.DateTimeField(required=None)
    updated_dt = me.DateTimeField(default=None)
    department_name = me.StringField(required=True)

    def __str__(self):
        return f"department_name: {self.department_name}"


class Employees(me.Document):
    created_dt = me.DateTimeField(required=True)
    updated_dt = me.DateTimeField(default=None)
    fio = me.StringField(required=True)
    position = me.StringField(required=True)
    department_id = me.ReferenceField(Department, reverse_delete_rule=me.CASCADE)

    def save(self, *args, **kwargs):
        self.updated_dt = datetime.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"fio: {self.fio} | position: {self.position}"


class Orders(me.Document):
    created_dt = me.DateTimeField(required=True)
    updated_dt = me.DateTimeField(default=None)
    order_type = me.StringField(required=True)
    description = me.StringField()
    status = me.StringField(required=True)
    serial_no = me.IntField(default=0)
    creator_id = me.ReferenceField(Employees, reverse_delete_rule=me.CASCADE)

    def __str__(self):
        return f"created_dt: {self.created_dt} | order_type: {self.order_type} | description: {self.description} | " \
               f"status: {self.status} | serial_no: {self.serial_no} | creator_id: {self.creator_id}"

# РУЧКИ :


@app.route('/')
def time():
    return f"{dt.now()}"


@app.route("/check_method", methods=["GET", "POST", "UPDATE", "DELETE", "PUT"])
def check_method():
    return f"{request.method}"


@app.route('/create_employees_data', methods=["POST"])
def create_employees_data():
    for user_profile_data in zip(department, employees):
        department_id = Department(**user_profile_data[0]).save()
        Employees(department_id=department_id, **user_profile_data[1]).save()
    return "OK"


@app.route('/create_orders_data', methods=["POST"])
def create_orders_data():
    for orders_data in zip(employees, orders):
        creator_id = Employees(**orders_data[0]).save()
        Orders(creator_id=creator_id, **orders_data[1]).save()
    return "OK"


@app.route('/create_department', methods=["GET", "POST"])
def create_department():
    Department(created_dt=dt.now(), department_name='IT1').save()
    return "OK"


@app.route('/update_department')
def update_department():
    dep = Department.objects(department_name='IT16')
    dep.update(updated_dt=dt.now(), department_name='IT17')
    return "OK"


@app.route("/delete_department_data", methods=["GET", "DELETE"])
def delete_department_data():
    Department.objects.all().delete()
    return "OK"


@app.route('/department_by_id/<string:department_id>', methods=['GET', 'POST'])
def department_by_id(department_id):
    dep = Department.objects(id=department_id)
    return f"Result: {dep}"


@app.route('/create_employee', methods=["GET", "POST"])
def create_employee():
    Employees(created_dt=dt.now(), fio='Volodia', position='gamer').save()
    return "OK"

@app.route('/update_employees')
def update_employees():
    emp = Employees.objects(fio='Volodia', position='gamer' )
    emp.update(updated_dt=dt.now(), department_name='Zhenia', position='fytbotbolist')
    return "OK"


@app.route("/delete_employees_data", methods=["GET", "DELETE"])
def delete_employees_data():
    Employees.objects.all().delete()
    return "OK"


@app.route("/employee_by_fio/<string:fio>", methods=['GET'])
def employee_by_fio(fio):
    emp = Employees.objects(fio=fio)
    print(emp)
    return f"Result: {emp}"


@app.route('/create_orders', methods=["GET", "POST"])
def create_orders():
    Orders(created_dt=dt.now(), order_type='order_type_1', description='something', status='Active', serial_no='99999',
           creator_id='60d45cef06e8462e85692ac9').save()
    return "OK"


@app.route('/update_orders')
def update_orders():
    orde = Orders.objects(status='Active', serial_no='99999')
    orde.update(updated_dt=dt.now(), status='Closed', serial_no='78521')
    return "OK"


@app.route("/delete_orders_data", methods=["GET", "DELETE"])
def delete_orders_data():
    Orders.objects.all().delete()
    return "OK"


@app.route("/orders_by_serial_no/<int:serial_no>", methods=['GET'])
def orders_by_serial_no(serial_no):
    orde = Orders.objects(serial_no=serial_no)
    print(orde)
    return f"Result: {orde}"


if __name__ == "__main__":
    app.run(debug=True)
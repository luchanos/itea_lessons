"""
2. Давайте представим, что мы занимаемся проектированием CRM для сервисного центра по обслуживанию и ремонту техники.
Реализуйте класс Заявка (Order). Каждая заявка должна иметь следующие поля: уникальный идентификатор order_id
(присваивается в момент создания заявки автоматически, дата и время создания заявки (автоматически) created_dt,
имя пользователя (creator_name), серийный номер оборудования (serial_no), статус (status активная заявка или закрытая
например, статусов может быть больше). Id заявки сделать приватным полем.
У заявки должны быть следующие методы:
- метод, возвращающий, сколько заявка находится в активном статусе (если она в нём) - check_ctatus
- метод, изменяющий статус заявки - change_status
- метод, возвращающий id заявки - get_order_id
"""
from uuid import uuid4
from datetime import datetime


class Order:
    def __init__(self, creator_name, serial_no, status):
        self.creator_name = creator_name
        self.serial_no = serial_no
        self.status = status
        self.__order_id = uuid4()
        self.created_dt = datetime.now()

    def check_status(self):
        return self.status

    def change_status(self, value):
        self.status = value

    def get_order_id(self):
        return self.__order_id

# class Ticket:
#     """Класс описывающий поведеие билета"""
#     def __init__(self, event_name, event_date, price):  # тут прокинули значения нашего экземпляра
#         """
#         Этот метод инициализирует значения полей объекта.
#         self - это уже сам объект нашего класса! его сюда автоматически передал метод __new__! Поэтому на
#         первой позиции стоил self - это и есть этот самый уже созданный экземпляр, который мы с вами будем шатать!
#         """
#         self.event_name = event_name  # объявили первое поле у экземпляра и присвоили ему значение
#         self.event_date = event_date  # объявили второе поле у экземпляра и присвоили ему значение
#         self.price = price
#
#     def __new__(cls, *args, **kwargs):
#         """Отвечает за создание объекта в памяти.
#         Этот метод собирает 'болванку' экземпляра! И отдает её потом в метод __init__, чтобы проинициализировать.
#         Про то, что тут написано ещё поговорим, пока просто подебажьтесь тут и убедитесь, что данный метод
#         запускается ПЕРВЫМ и отдает результат своего выполнения в __init__.
#
#         Вы спросите, что такое cls? Отвечу вам - это ЭКЗЕМПЛЯР класса type, которым является любой
#         кастомный (пользовательский класс). То есть как функция является объектом, так и сам класс, по
#         которому вы потом будете собирать свой объект тоже является объектом! И 'болванку' мы собираем на его основе
#
#         ВНИМАНИЕ! ОБЫЧНО ПЕРЕОПРЕДЕЛЯТЬ ЭТОТ МЕТОД НЕ НУЖНО! ТОЛЬКО В ИСКЛЮЧИТЕЛЬНЫХ СЛУЧАЯХ (например при
#         использовании паттерна SINGLETONE)"""
#         return super().__new__(cls)
# ticket = Ticket(1, 2, 3)
# print(ticket)
# print(type(ticket))
# print(type(Ticket))
# ticket_list = [Ticket(1, 2, 3) for x in range(10)]
# print(ticket_list)
from abc import ABC, abstractmethod


class BaseTicket(ABC):
    expiry_map = {
        True: "Да",
        False: "Нет"
    }

    @abstractmethod
    def __init__(self):
        pass

    def use_me(self):
        self.is_expired = True

    def is_used(self):
        return self.is_expired

    @abstractmethod
    def show_info(self):
        pass


class EventTicket(BaseTicket):
    """Класс описывающий поведеие билета на мероприятие"""
    total_ticket_cnt = 0

    def __init__(self, event_name, event_date, price):  # тут прокинули значения нашего экземпляра
        self.event_name = event_name  # объявили первое поле у экземпляра и присвоили ему значение
        self.event_date = event_date  # объявили второе поле у экземпляра и присвоили ему значение
        self.price = price
        self.is_expired = False

    def show_info(self):
        return f"""Мероприятие: {self.event_name}
Дата: {self.event_date}
Цена: {self.price}
Погашен: {BaseTicket.expiry_map[self.is_expired]}"""

    def __new__(cls, *args, **kwargs):
        cls.total_ticket_cnt += 1
        return super().__new__(cls)


class FlightTicket(BaseTicket):
    """Класс описывающий поведеие билета"""
    total_ticket_cnt = 0

    def __init__(self, flight_number, flight_date, price, doc_no):  # тут прокинули значения нашего экземпляра
        self.flight_number = flight_number  # объявили первое поле у экземпляра и присвоили ему значение
        self.flight_date = flight_date  # объявили второе поле у экземпляра и присвоили ему значение
        self.price = price
        self.doc_no = doc_no
        self.is_expired = False

    def show_info(self):
        return f"""Рейс: {self.flight_number}
Дата: {self.flight_date}
Цена: {self.price}
Номер документа: {self.mask_doc_no(self.doc_no)}
Погашен: {BaseTicket.expiry_map[self.is_expired]}"""

    @staticmethod
    def mask_doc_no(doc_no):
        return doc_no[:3] + "****"

    def __new__(cls, *args, **kwargs):
        cls.total_ticket_cnt += 1
        return super().__new__(cls)


class DiplomaticFlightTicket(FlightTicket):
    def show_info(self):
        return f"""Засекречено"""


# print(Ticket.total_ticket_cnt)
# ticket = Ticket(event_name="Кино", event_date="2021-11-11", price=100)
# print(Ticket.total_ticket_cnt)
# ticket_1 = Ticket(event_name="Театр", event_date="2021-11-11", price=100)
# print(Ticket.total_ticket_cnt)
# print(ticket.is_used(), ticket_1.is_used())
# ticket.use_me()
# print(ticket.is_used(), ticket_1.is_used())
# print(EventTicket.total_ticket_cnt)


event_ticket = EventTicket(event_name="Кино", event_date="2021-11-11", price=100)
flight_ticket = FlightTicket(flight_number=1234, flight_date="2021-11-11", price=100, doc_no="435685")
diplomatic_ticket = DiplomaticFlightTicket(flight_number=1234, flight_date="2021-11-11", price=100, doc_no="435685")
# event_ticket.use_me()
# print(event_ticket.show_info())
# flight_ticket.use_me()
# print(flight_ticket.show_info())
diplomatic_ticket.use_me()
print(diplomatic_ticket.show_info())
c = 1
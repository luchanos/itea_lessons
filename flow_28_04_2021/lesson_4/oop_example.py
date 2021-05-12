from uuid import uuid4
from abc import ABC, abstractmethod


class AbstractTicket(ABC):
    @abstractmethod
    def use_me(self):
        pass


class EventTicket(AbstractTicket):
    def __init__(self, ticket_id, place):
        self.ticket_id = ticket_id
        self.place = place

    def __str__(self):
        return f"Билет {self.ticket_id}"

    def check_quality(self):
        print(f"Произвожу проверку подлинности билета {self.ticket_id} Запрос во внешние сервисы театральных касс...")

    def use_me(self):
        self.check_quality()
        print(f"Билет с id {self.ticket_id} на мероприятие погашен")


class FlightTicket(AbstractTicket):
    def __init__(self, ticket_id, document_number, document_type):
        self.ticket_id = ticket_id
        self.document_number = document_number
        self.document_type = document_type

    def __str__(self):
        return f"Билет {self.ticket_id}"

    def use_me(self):
        print(f"Билет с id {self.ticket_id} на самолет погашен")


class BusTicket(AbstractTicket):
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        self.value = 10

    def __str__(self):
        return f"Билет {self.ticket_id}"

    def check_expiry(self):
        print(f"Проверка на то, что билет {self.ticket_id} не истек по сроку годности")

    def use_me(self):
        self.check_expiry()
        self.value -= 1
        print(f"Билет с id {self.ticket_id} на автобус погашен. Осталось поездок: {self.value}")


TICKET_MAPPING = {
    "event": EventTicket,
    "bus": BusTicket,
    "flight": FlightTicket
}


class TicketVendor:
    """Отвечает за реализацию билетов"""

    log_ticket = []  # это аналог базы данных в нашем случае

    def sell_ticket(self, ticket_type, *args, **kwargs):
        ticket_id = uuid4()
        print(f"id: {ticket_id} {ticket_type} {args}, {kwargs} создан!")
        class_to_be_used = TICKET_MAPPING[ticket_type]
        return class_to_be_used(ticket_id=ticket_id, *args, **kwargs)

    def use_ticket(self, ticket):
         ticket.use_me()


vendor = TicketVendor()
flight_ticket = vendor.sell_ticket(ticket_type='flight', document_type='passport', document_number=123)
bus_ticket = vendor.sell_ticket(ticket_type='bus')
vendor.use_ticket(flight_ticket)
vendor.use_ticket(bus_ticket)

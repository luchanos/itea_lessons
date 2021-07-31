from enum import Enum
from uuid import uuid4
from datetime import date


class EventTicketCategory(Enum):
    VIP = 1
    COMMON = 2


class FlightTicketCategory(Enum):
    ECONOMY = 0
    BUSINESS = 1
    FIRST_CLASS = 2


class EventTicket:
    def __init__(self, event_date: date, event_name: str, category: EventTicketCategory, price: float):
        self.event_date = event_date
        self.event_name = event_name
        self.category = category
        self.price = price
        self.ticket_id = uuid4()
        self.is_active = True

    @property
    def is_vip(self):
        return self.category == EventTicketCategory.VIP

    @property
    def is_common(self):
        return self.category == EventTicketCategory.COMMON


class FlightTicket:
    def __init__(self, flight_number, flight_date, passenger_fio, passport_no):
        self.flight_number = flight_number
        self.flight_date = flight_date
        self.passenger_fio = passenger_fio
        self.passport_no = passport_no
        self.ticket_id = uuid4()
        self.is_active = True


class EventTicketContext:
    def __call__(self, *args, **kwargs):
        print("Продажа билета на мероприятие")
        ticket_params = dict()
        ticket_params["event_date"] = input("Введите дату мероприятия: ")
        ticket_params["event_name"] = input("Введите название мероприятия: ")
        ticket_params["category"] = EventTicketCategory(int(input("Введите категорию билета: ")))
        ticket_params["price"] = float(input("Введите цену билета: "))
        ticket = EventTicket(**ticket_params)
        print(f"Билет на мероприятие {ticket.ticket_id} продан!")


class FlightTicketContext:
    def __call__(self, *args, **kwargs):
        ticket_params = dict()
        ticket_params["flight_number"] = input("Введите номер рейса: ")
        ticket_params["flight_date"] = input("Введите дату рейса: ")
        ticket_params["passenger_fio"] = input("Введите ФИО пассажира: ")
        ticket_params["passport_no"] = input("Введите номер паспорта пассажира: ")
        ticket = FlightTicket(**ticket_params)
        print(f"Билет на рейс {ticket.ticket_id} продан!")


class SellDaemon:
    """Демон для продажи товаров"""

    def __init__(self, context_mapper):
        self.context_mapper = context_mapper

    def __call__(self, *args, **kwargs):
        user_choice = input("Какой товар вам нужен? ")
        context = self.context_mapper[user_choice]()
        context()


# ticket = EventTicket(event_date=date.today(), event_name="Хакатон", category=TicketCategory.VIP, price=100.5)
# print(ticket.is_vip)

context_mapper = {
    "мероприятие": EventTicketContext,
    "рейс": FlightTicketContext
}

sell_daemon = SellDaemon(context_mapper)
sell_daemon()

"""
1. classmethod
2. модификаторы доступа
3. магические методы
4. простой клиент к БД
5. телеграм-клиент
"""
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
    __total_ticket_cnt = 0

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
        cls.__total_ticket_cnt += 1
        return super().__new__(cls)

    @classmethod
    def show_total_ticket_cnt(cls):
        print("Отправляю метрику в базу о том, что пользователь обратился к служебному полю")
        return cls.__total_ticket_cnt


class FlightTicket(BaseTicket):
    """Класс описывающий поведеие билета"""
    __total_ticket_cnt = 0

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
        cls.__total_ticket_cnt += 1
        return super().__new__(cls)


class DiplomaticFlightTicket(FlightTicket):
    def show_info(self):
        return f"""Засекречено"""


# res = EventTicket.show_total_ticket_cnt()
# print(res)
# print(EventTicket.__total_ticket_cnt)

class A:
    __secret = 1

    @classmethod
    def show_secret(cls):
        return cls.__secret


class B(A):
    __secret = 2

    # @classmethod
    # def show_secret(cls):
    #     return cls.__secret


# a = A()
# b = B()
# print(a.show_secret())
# print(b.show_secret())
# print(a._A__secret)


class Point2D:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __str__(self):
        return f"x coord: {self.x_coord} y_coord: {self.y_coord}"

    def __add__(self, other: 'Point2D'):
        """РЕЗУЛЬТАТОМ ТАКОГО МЕТОДА ДОЛЖЕН БЫТЬ ОБЪЕКТ ТОГО ЖЕ ТИПА, ЧТО И ТОТ КЛАСС, В КОТОРОМ ЭТО МЕТОД НАХОДИТСЯ"""
        if type(other) != Point2D:
            raise TypeError(f"Unsupported type for summarize with type Point! {type(other)}")
        return Point2D(self.x_coord + other.x_coord,
                       self.y_coord + other.y_coord)

    def __sub__(self, other: 'Point2D'):
        """РЕЗУЛЬТАТОМ ТАКОГО МЕТОДА ДОЛЖЕН БЫТЬ ОБЪЕКТ ТОГО ЖЕ ТИПА, ЧТО И ТОТ КЛАСС, В КОТОРОМ ЭТО МЕТОД НАХОДИТСЯ"""
        if type(other) != Point2D:
            raise TypeError(f"Unsupported type for summarize with type Point! {type(other)}")
        return Point2D(self.x_coord - other.x_coord,
                       self.y_coord - other.y_coord)

    def __mul__(self, other: int):
        """РЕЗУЛЬТАТОМ ТАКОГО МЕТОДА ДОЛЖЕН БЫТЬ ОБЪЕКТ ТОГО ЖЕ ТИПА, ЧТО И ТОТ КЛАСС, В КОТОРОМ ЭТО МЕТОД НАХОДИТСЯ"""
        if type(other) not in [int, float]:
            raise TypeError
        return Point2D(self.x_coord * other,
                       self.y_coord * other)

    def __enter__(self):
        print("Выполняю что-то перед контекстом")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Выполняю что-то после контекста")


class Point3D(Point2D):
    def __init__(self, x_coord, y_coord, z_coord):
        super().__init__(x_coord, y_coord)
        self.z_coord = z_coord

    def __str__(self):
        return f"{super().__str__()} z_coord: {self.z_coord}"

    def __add__(self, other: 'Point3D'):
        """РЕЗУЛЬТАТОМ ТАКОГО МЕТОДА ДОЛЖЕН БЫТЬ ОБЪЕКТ ТОГО ЖЕ ТИПА, ЧТО И ТОТ КЛАСС, В КОТОРОМ ЭТО МЕТОД НАХОДИТСЯ"""
        if type(other) != Point3D:
            raise TypeError(f"Unsupported type for summarize with type Point3D! {type(other)}")
        return Point3D(self.x_coord + other.x_coord,
                       self.y_coord + other.y_coord,
                       self.z_coord + other.z_coord)

    def __sub__(self, other: 'Point3D'):
        """РЕЗУЛЬТАТОМ ТАКОГО МЕТОДА ДОЛЖЕН БЫТЬ ОБЪЕКТ ТОГО ЖЕ ТИПА, ЧТО И ТОТ КЛАСС, В КОТОРОМ ЭТО МЕТОД НАХОДИТСЯ"""
        if type(other) != Point3D:
            raise TypeError
        return Point3D(self.x_coord - other.x_coord,
                       self.y_coord - other.y_coord,
                       self.z_coord - other.z_coord)

    def __mul__(self, other: int):
        """РЕЗУЛЬТАТОМ ТАКОГО МЕТОДА ДОЛЖЕН БЫТЬ ОБЪЕКТ ТОГО ЖЕ ТИПА, ЧТО И ТОТ КЛАСС, В КОТОРОМ ЭТО МЕТОД НАХОДИТСЯ"""
        if type(other) not in [int, float]:
            raise TypeError
        return Point3D(self.x_coord * other,
                       self.y_coord * other,
                       self.z_coord * other)

    # def __iter__(self):
    #     yield self.x_coord
    #     yield self.y_coord
    #     yield self.z_coord

    def __iter__(self):
        """Альтернативный протокол итерации"""
        return iter([self.x_coord, self.y_coord, self.z_coord])


point_1 = Point2D(1, 2)
point_2 = Point2D(3, 4)
# point_3 = point_1 + point_2
# point_3 = point_1 + point_2 + point_1
# print(point_3)
# point_3 = point_1 - point_2 - point_1
# print(point_3)
# point_3 = point_1 * 100
# print(point_3)
# with point_1:
#     print("Выполняется контекст")
# print("Закончили")
# l = [1, 2, 3]
# l1 = [4, 5, 6]
# l2 = l1 + l
# print(l2)


def func():
    yield 1
    yield 2
    yield 3


point_3d = Point3D(1, 2, 3)
# print(point_3d)
for el in point_3d:
    print(el)

# it = iter(point_3d)
# print(it)

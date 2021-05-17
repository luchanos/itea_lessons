"""2. Создайте абстрактный класс «Оргтехника», который будет базовым для классов-наследников.
Эти классы — конкретные типы оргтехники (принтер, сканер, ксерокс). В базовом классе определите абстрактные методы,
общие для приведённых типов. В классах-наследниках реализуйте их, а также добавьте уникальные для каждого
типа оргтехники функциональные возможности.

Также создайте класс «Склад», экземпляр которого будет способен принимать в себя объекты техники на хранение.
Организуйте для него протокол итерации (чтобы объекты вашего склада можно было бы перебирать).
"""
from abc import ABC, abstractmethod


class Orgtechnics(ABC):
    @abstractmethod
    def switch_on(self):
        pass

    @abstractmethod
    def switch_off(self):
        pass


class Printer(Orgtechnics):
    def __init__(self, serial_no):
        self.serial_no = serial_no
        self.is_active = False

    def switch_off(self):
        self.is_active = False
        print("Теперь принтер выключен")

    def switch_on(self):
        self.is_active = True
        print("Теперь принтер включен")

    def print_some(self, msg):
        print(f"Принтер s/n {self.serial_no} печатает: {msg}")

    def __str__(self):
        return f"Принтер s/n {self.serial_no}"


class Scanner(Orgtechnics):
    def __init__(self, serial_no):
        self.serial_no = serial_no
        self.is_active = False

    def switch_off(self):
        self.is_active = False
        print("Теперь сканер выключен")

    def switch_on(self):
        self.is_active = True
        print("Теперь сканер включен")

    def scan_some(self, msg):
        print(f"Сканер s/n {self.serial_no} сканирует: {msg}")

    def __str__(self):
        return f"Сканнер s/n {self.serial_no}"


class Xerox(Orgtechnics):
    def __init__(self, serial_no):
        self.serial_no = serial_no
        self.is_active = False

    def switch_off(self):
        self.is_active = False
        print("Теперь ксерокс выключен")

    def switch_on(self):
        self.is_active = True
        print("Теперь ксерокс включен")

    def copy_some(self, msg):
        print(f"Ксерокс s/n {self.serial_no} копирует: {msg}")

    def __str__(self):
        return f"Ксерокс s/n {self.serial_no}"


class Warehouse:
    def __init__(self, name):
        self.name = name
        self.stock = []

    def add_to_stock(self, technic):
        self.stock.append(technic)

    def __iter__(self):
        return iter(self.stock)


xerox = Xerox(1)
printer = Printer(2)
scanner = Scanner(3)
warehouse = Warehouse("Логистика")
warehouse.add_to_stock(xerox)
warehouse.add_to_stock(printer)
warehouse.add_to_stock(scanner)
for tech in warehouse:
    print(tech)

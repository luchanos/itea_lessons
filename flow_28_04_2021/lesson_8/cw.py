"""
1. Напишите декоратор для класса, который бы при создании экземпляра этого класса осуществлял бы запись информации об
этом в текстовый файл. Пример записи: 2012-01-01 15:04 Создан экземпляр класса TestClass по адресу памяти x01223342

2. На основе прошлых ДЗ необходимо создать модели представлений для классов ДЕПАРТАМЕНТЫ (Departments),
СОТРУДНИКИ (Employees), ЗАЯВКИ (Orders). Реализовать магические методы вывода информации на экран как для пользователя,
так и для "машинного" отображения.
"""

# json - замечательный формат данных, напоминающий словарь
# Один из наиболее распространённых форматов, используемых в web, наряду с XML
# пример ответа "ручки" сайта Авито, которая располагается в свободном доступе и отдаёт json в составе своего ответа:
# https://www.avito.ru/js/v1/side_block?locationId=653240&showWaitRating=true
# json позволяет web приложениям общаться между собой.

# получим вот такой результат:
"""
{
  "recentlyViewed": {
    "hash": "p47rxtx97qscs8484s84ook0ocs00wk",
    "engine": "recently_viewed",
    "position": 1
  },
  "navbar": {
    "hash": "jcaa8qr457cc8800gg8c0ss8s4scwo0",
    "shouldShowOfferLink": false
  },
  "servicesInfo": {
    "hash": "1o2sgt0561s080kcckog0cwkgs04kso"
  }
}
"""

# Для работы с документами подобного вида в Python предусмотрен модуль json:

import json


products = {
    'Onion': {
        'price': 12,
        'in_stock': 1000,
        'description': 'Лук'
    },
    'Tomato': {
        'price': 4,
        'in_stock': 10000,
        'description': 'Помидоры'
    },
    'Cucumber': {
        'price': 10,
        'in_stock': 500,
        'description': 'Огурцы',
        # 'test': {1, 2, 3}
    }
}

# предположим, что на стороне нашего прекрасного Питонячьего сервиса мы сформировали словарь и ли список и хотим
# хранить его на диске или передавать его в виде json по сети. Сначала нужно привести наши данные в пригодный для этого
# вид:

# сериализация - процесс перегонки питоновских данных в НЕпитоновские
# json_object = json.dumps(products)  # сериализовать в строку (dumpS)
# print(json_object)
# print(type(json_object))  # это класс СТРОКА!

# как мы уже говорили ранее эту строку можно преобразовать в байты и отправить, скажем, по сети)

# with open("products_data.json", "w", encoding="UTF-8") as json_f:
#     json.dump(products, json_f)  # превратит данные из словаря в файл

# encoding - это параметр кодировки. Их бывает великое множество, они отвечают за правила, по которым машина будет
# читать данные из файла. Помните ситуацию, когда вы открываете файл, а там крокозябры? Всё дело в том, что кодировка,
# в которой он был записан и кодировка, в которой файл читается - не совпадают, поэтому лучше задавать её всегда явно.
# Кодировка по умолчанию может быть своя в каждой системе (настраивается): UTF-8 (Mac), cp-1251 (Windows).

# Кортеж и множество - не сериализуется, они будут преобразованы в список, если находятся в составе сериализуемой
# структуры

l1 = [1, 2, 3]
t1 = (1, 2, 3)  # будет преобразовано в список
s1 = {1, 2, 3}  # не будет сериализовано - вылезет ошибка

# with open("products_data.json", "w", encoding="UTF-8") as json_f:
#     json.dump(s1, json_f)  # превратит данные из словаря в файл

# Обратный процесс - десериализация. Когда мы получили json-данные и теперь надо превратить их во что-то, с чем
# можно было бы работать в виде хорошо знакомых питоновских типов данных
# with open("products_data.json", "r", encoding="UTF-8") as json_f:
#     products_dict = json.load(json_f)  # превратит данные из файла в словарь

# print(products_dict, type(products_dict))

# допустим нам прилетела по сети строка

b_str = b'{"Onion": {"price": 12, "in_stock": 1000, "description": "\u041b\u0443\u043a"}, ' \
        b'"Tomato": {"price": 4, "in_stock": 10000, "description": "\u041f\u043e\u043c\u0438\u0434\u043e\u0440\u044b"}, ' \
        b'"Cucumber": {"price": 10, "in_stock": 500, "description": "\u041e\u0433\u0443\u0440\u0446\u044b"}}'

# или

s_str = '{"Onion": {"price": 12, "in_stock": 1000, "description": "\u041b\u0443\u043a"}, ' \
        '"Tomato": {"price": 4, "in_stock": 10000, "description": "\u041f\u043e\u043c\u0438\u0434\u043e\u0440\u044b"}, ' \
        '"Cucumber": {"price": 10, "in_stock": 500, "description": "\u041e\u0433\u0443\u0440\u0446\u044b"}}'

with open("products_data.json", "r", encoding="UTF-8") as json_f:
    products_dict = json.loads(b_str)  # превратит данные из строки/байт-строки в словарь
print(type(products_dict), products_dict)

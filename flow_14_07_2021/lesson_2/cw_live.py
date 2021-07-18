# def func():
#     print("Тестовое сообщение!")


# lambda: print("Тестовое сообщение!")

# print(func)
# res = func()
# print(res)


# порядок объявления функции: DEF - говорит, что функция именная! Дальше идёт <ИМЯ>, потом <ПАРАМЕТРЫ>,
# потом <КОНТЕКСТ ВЫПОЛНЕНИЯ>
# def summarizer(a, b):
#     return a + b

# с лямбдой (анонимной функцией) всё аналогично! Только пропущен шаг с именем!
# print(lambda a, b: a + b)


# lambda_summarizer = lambda a, b: a if a % 2 == 1 else b
# print(lambda_summarizer(4, 2))

# тернарный оператор
# a = 1
# b = 2
# c = a if a % 2 == 1 else b
# def povidlo_eat_func():
#     print("Бабушка сходила в магазин за повидлом")
#     print("Приготовила пирожки")
#     print("ПОКАЗ РЕКЛАМЫ")
#     print("юзер поел пирожок с повидлом")


# answer_mapper = {
#     "с мясом": lambda: print("юзер поел пирожок с мясом"),
#     "с повидлом": povidlo_eat_func,
#     "с капустой": lambda: print("юзер поел пирожок с капустой")
# }

# answer = input("Хочешь пирожок? ")
# if answer == "да":
#     answer = input("А с чем? ")
#     try:
#         answer_mapper[answer]()
#     except KeyError:
#         print("Такой начинки сегодня нет")
# else:
#     print("юзер не поел")
# print("программа завершена")


# def bogatyr_choice(direction="left"):
#     if direction == "left":
#         return "Horse loss!"
#     elif direction == "right":
#         return "Mind loss!"
#     elif direction == "straight":
#         return "Life loss!"


# print(bogatyr_choice("right"))


# ПОЧЕМУ 1 ФУНКЦИЯ ЛУЧШЕ ВСЕХ? ПОТОМУ ЧТО ИМЕННО ОНА ДЕЛАЕТ ТО, ЧТО ПРОСЯТ!!!
# def summarizer(a, b):
#     return a + b


# def summarizer(a, b):
#     print(a + b)


# def summarizer(a, b):
#     return f"Сумма чисел: {a + b}"

# Никогда не передавайте в качестве дефолтного аргумента изменяемый тип!!
# def some_f(a, l=[]):
#     # if not l:
#     #     l = []
#     l.append(a)
#     return l

# [1, [...], [...]] - вот что будет при выводе
# print(some_f(some_f(some_f(1))))
# print(some_f(1))
# print(some_f(1))
# print(some_f(1))


# def func(a, b, c, d, e, *args, **kwargs):
#     print(a, b)


# func(1, 2, b=2, m=100, k=1000)
# func(b=2, a=1)

# params = {
#     'a': 1,
#     'b': 2,
#     'c': 3,
#     'd': 4,
#     'e': 5,
#     'outer_param': 'outer_value'
# }

# params_t = (1, 2, 3, 4, 5, 6, 7, 8, 9)

# func(**params)
# func(*params_t)
# func(*params)

# for el in params_t:
#     print(el)

# for el in params:
#     print(el)

# DATABASE_URL = "postgres://asdfas:dfafs@localhost:5555/db"
TOTAL = 0  # глобальная. доступна НА ЧТЕНИЕ отовсюду в модуле!
# EXECUTED = 0

# def func():
#     TOTAL = 10
#     cnt = 0
#     while cnt < 10:
#         print(TOTAL)
#         cnt += 1
#         TOTAL += 1


# def func():
#     global EXECUTED
#     # global cnt
#     EXECUTED += 1
#     global TOTAL
#     cnt = 0
#     while cnt < 10:
#         cnt += 1
#         TOTAL = TOTAL + 1
#         print(TOTAL)


# def func_2():
#     print(cnt)
#     global EXECUTED
#     EXECUTED += 1
#     print(TOTAL)


# print("Текущее значение:", TOTAL)
# func_2()
# print(f"Всего запусков моих функций: {EXECUTED}")


# def func():
#     inner_total = TOTAL
#     cnt = 0
#     while cnt < 10:
#         cnt += 1
#         inner_total = inner_total + 1
#         print(inner_total)
#     return inner_total


# def func():
#     return print


# print(func)
# print(func())
# res = func()
# print(res)
# res("Тестовое сообщение")


# def func_to_return(text):
#     return f"Тестовое сообщение: {text}, <num>"
#
#
# def func(num):
#     return func_to_return
#
#
# print(func)
# res = func(10)
# print(res)
# print(res("тестовый текст"))

# def func(num):
#     c = 1
#     def func_to_return(text):
#         nonlocal num
#         num += 1
#         return f"Тестовое сообщение: {text}, {num}"
#
#     return func_to_return


# print(func)
# res = func(10)
# print(res)
# print(res("тестовый текст"))
# def summarizer(a, b):
#     return a + b
#
#
# def func(other_func, *args, **kwargs):
#     print("РЕКЛАМА!")
#     return other_func(*args, **kwargs)
#
#
# print(func(summarizer, 1, 2))


# def outer(func):
#     def inner(*args, **kwargs):
#         print("РЕКЛАМА!")
#         return func(*args, **kwargs)
#     return inner


# @outer
# def summarizer(a, b):
#     return a + b
#
#
# @outer
# def multiplier(a, b, c):
#     return a * b * c

# res = outer(summarizer)
# print(res)
# print(res(1, 2))
#
# res = outer(multiplier)
# print(res)
# print(res(1, 2, 3))


def adv_dec(message):
    def outer(func):
        def inner(*args, **kwargs):
            print(message)
            return func(*args, **kwargs)
        return inner
    return outer


@adv_dec("Реклама доширака")
def summarizer(a, b):
    return a + b


@adv_dec("Реклама Мивина")
def multiplier(a, b, c):
    return a * b * c


print(summarizer(1, 2))
print(multiplier(1, 2, 3))

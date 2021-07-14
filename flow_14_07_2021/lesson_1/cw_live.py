# a = 1
# print(type(a))

# print(1 + True)
# print(False * 100000 * "adfgsdfg")
# print("ABC " * 10)
# print(True is True)
# print(0 is False)  # проверка принадлежности одному и тому же участку памяти
#
# print(1 == True)  # проверка на равенство по значениям
# print(0 == False)

# print(True in ["1", 2, 3, 4])
# print(False in [1, 1, 2])
# print(1 in [True, 2, 3, 4])

# _ = 0
# a = 1
# b = 2
# c = 3
# l = [1, 2, 3]
# print(l[0] is a)
# a = 0
# print(l)
# print(l[0] is a)
# print(a is _)

# a = 1
# b = 2
# c = 3
# l = [a, b, c]
# a = 100
# print(l)

# a = [-100, -200]
# b = 2
# c = 3
# l = [a, b, c]
# a[0] = 100
# print(l)

# a = [-100, -200]
# b = 2
# c = 3
# l = [a, b, c]
# l[0][0] = 100
# print(a)


# a = [-100, -200]
# b = 2
# c = 3
# t = (a, b, c)
# t[0][0] = 100
# print(a)

# a = [-100, -200]
# b = 2
# c = 3
# t = (a, b, c)
# a[0] = 100
# print(t)


# a = [-100, -200]
# b = 2
# c = 3
# s = {a, b, c}
# a[0] = 100
# print(s)

# a = (-100, (1, 2, []))
# b = 2
# c = 3
# s = {a, b, c}
# print(s)

# s1 = frozenset([1, 2, 2, [1, 2], 2, 2])
# print(s1)

# d = {
#     "Апельсин": 100,
#     "Банан": 20,
#     "Абрикос": 50
# }

# l = [1, 2, 2, [1, 2], 2, 2]
# print(l[0:3])
l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10]
# print(l[0::2])
# print(l[::-1])
# print(l[0:len(l):1])
# print(l[-2::-2])

# Comprehensions
# new_l = [el for el in l if el % 2 == 0]
# print(new_l)

# s = {el for el in l if el % 2 == 0}
# print(s)

# t = (el for el in l if el % 2 == 0)
# print(t)

# print(next(t))
# print(next(t))
# print(next(t))
# print(next(t))
# print(next(t))
# print(next(t))
# print(next(t))
# print(next(t))
# print(next(t))
enum_obj = enumerate(["lol", "kek", "cheburek"])

# <постобработка того, что получили справа> FOR <что, откуда и при каких условиях мы будем использовать для построения коллекции>
# d = {k * 10: str(v) * 3 for k, v in enum_obj}
# print(d)

# if {k * 10: str(v) * 3 for k, v in enum_obj}:
#     print("ОГО! Непустой словарь!")


# answer = input("Хочешь пирожок? ")
# if (answer == "да"):
#     answer = input("А с чем? ")
#     if answer == "с мясом":
#         print("юзер поел пирожок с мясом")
#     elif answer == "с повидлом":
#         print("юзер поел пирожок с повидлом")
#     elif answer == "с капустой":
#         print("юзер поел пирожок с капустой")
#     else:
#         print("Такой начинки сегодня нет")
# else:
#     print("юзер не поел")
# print("программа завершена")

# while True:
#     try:
#         num = int(input("Введите число повторений: "))
#         break
#     except:
#         print("Вы ввели не число!")
#
# while num != 0:
#     print("Hello, World!")
#     num -= 1
# else:
#     print("Мы вышли!")

answer_mapper = {
    "с мясом": "юзер поел пирожок с мясом",
    "с повидлом": "юзер поел пирожок с повидлом",
    "с капустой": "юзер поел пирожок с капустой"
}

answer = input("Хочешь пирожок? ")
if answer == "да":
    answer = input("А с чем? ")
    try:
        print(answer_mapper[answer])
    except KeyError:
        print("Такой начинки сегодня нет")
else:
    print("юзер не поел")
print("программа завершена")

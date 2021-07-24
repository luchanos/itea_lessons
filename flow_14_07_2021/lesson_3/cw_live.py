"""Это третий урок"""
from io import TextIOWrapper

# some_num_value = 1
#
# file_object = open("lesson_3_file.txt", "r")
# print(file_object, file_object.closed)
#
#
# data = file_object.read()
# print(data)
#
# file_object.close()
# print(file_object.closed)

# open_files = [open("lesson_3_file.txt", "r") for _ in range(20_000)]

file_status = {
    True: "Файл закрыт",
    False: "Файл открыт"
}

# file_object = open("lesson_3_file.txt", "r")
# file_object_2 = open("lesson_3_file_2.txt", "w")


def show_files_status():
    print(file_status[file_object.closed], file_status[file_object_2.closed])
#
#
# show_files_status()
# with file_object, file_object_2:
#     print("Это исполнение контекста")
#     data = file_object.read()
#     file_object_2.write(data)
#     print(data)
#     show_files_status()
#
#
# show_files_status()

# try:
#     print("Это исполнение контекста")
#     data = file_object.read()
#     print(data)
#     raise OSError("Ошибка в системе!")
#     show_file_status()
# except Exception:
#     print("Ошибка!")
#     show_file_status()
# finally:
#     print("Сработал блок finally")
#     file_object.close()
#     show_file_status()
# c = 1


# file_object = open("lesson_3_file.txt", "r")
# file_object_2 = open("lesson_3_file_2.txt", "w")

with open("lesson_3_file.txt", "r") as file_object, open("lesson_3_file_2.txt", "w") as file_object_2:
    print("Это исполнение контекста")
    data = file_object.read()
    file_object_2.write(data)
    print(data)
print(file_object.closed, file_object_2.closed)

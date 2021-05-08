s = "test_string"
f_o = open("testfile.txt", "r")
c = 1
# [open("testfile.txt", "w") for _ in range(100_000)]
# some_str = f_o.readlines()  # вычитывает построчно в лист
# some_str = f_o.read()  # вычитывает в строку
# print(f_o.tell())
# some_str = f_o.readline()  # читает очередную строчку
# print(f_o.tell())
# some_str = f_o.readline()
# print(f_o.tell())
# f_o.seek(0)
# print(f_o.tell())
# print(some_str)
# f_o.write(s)
# f_o.close()

for stroka in f_o:
    print(stroka, end="")

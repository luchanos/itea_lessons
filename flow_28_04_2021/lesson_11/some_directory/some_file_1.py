def my_shiny_func():
    print("Вызываю my_shiny_func")


print("Это исполняемый код внутри some_file_1")
print(__name__)

if __name__ == '__main__':
    print("Этот код выполняется, значит some_file_1 был вызван на исполнение напрямую")

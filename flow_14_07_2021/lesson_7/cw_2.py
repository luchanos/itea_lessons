from flow_14_07_2021.lesson_7.db_client import DbClient
from flow_14_07_2021.lesson_7.settings import DB_URL


class MyApplication:
    MENU_STRING = "\n1 - работа с базой\n"

    def __init__(self, db_client: DbClient):
        self.db_client = db_client

    def setup_all_components(self):
        self.db_client.setup()

    def all_book_selector(self):
        print(self.db_client.select_all_books())

    def book_inserter(self):
        book_params = dict()
        book_params["book_name"] = input("Введите название книги: ")
        book_params["author"] = input("Введите автора книги: ")
        book_params["genre"] = input("Введите жанр книги: ")
        book_params["sheets_cnt"] = int(input("Введите количество страниц книги: "))
        self.db_client.insert_book(**book_params)

    def delete_book_by_id(self):
        book_id = int(input("Введите id книги для удаления: "))
        self.db_client.delete_book_by_id(book_id)
        print(f"Книга с id {book_id} успешно удалена из базы!")

    def run(self):
        self.setup_all_components()

        choice_mapper = {"1": self.all_book_selector,
                         "2": self.book_inserter,
                         "3": self.delete_book_by_id}

        while True:
            user_choice = input(f"Введите желаемое действие: {self.MENU_STRING}или q для выхода: ")
            if user_choice.lower() == "q":
                break
            elif user_choice == "1":
                user_choice = input(f"1 - вывести все книги\n2 - добавить новую книгу\n3 - удалить книгу по id ")
                choice_mapper[user_choice]()

        print("Спасибо за пользованием нашим софтом!")


db_client = DbClient(DB_URL)
MyApplication(db_client=db_client).run()

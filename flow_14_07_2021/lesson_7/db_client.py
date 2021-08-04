import psycopg2


class DbClient:
    BOOK_SELECT_QUERY = """SELECT * FROM books"""
    BOOK_INSERT_QUERY = """INSERT INTO books (book_name, author, genre, sheets_cnt)
             VALUES ('%s', '%s', '%s', %d)"""
    BOOK_DELETE_QUERY = """DELETE FROM books WHERE book_id = %d"""

    def __init__(self, dsn):
        self.dsn = dsn
        self.connect = None

    def setup(self):
        self.connect = psycopg2.connect(self.dsn)

    def select_all_books(self):
        with self.connect.cursor() as cursor:
            cursor.execute(self.BOOK_SELECT_QUERY)
            return list(cursor)

    def insert_book(self, book_name: str, author: str, genre: str, sheets_cnt: int):
        with self.connect.cursor() as cursor:
            cursor.execute(self.BOOK_INSERT_QUERY % (book_name, author, genre, sheets_cnt))
            self.connect.commit()

    def delete_book_by_id(self, book_id: int):
        with self.connect.cursor() as cursor:
            cursor.execute(self.BOOK_DELETE_QUERY % book_id)
            self.connect.commit()

    def close(self):
        self.connect.close()
        self.connect = None

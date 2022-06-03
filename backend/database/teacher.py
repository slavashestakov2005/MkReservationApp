from .database import Table, Row
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Teacher(Row, UserMixin):
    """
        Строка таблицы ListenersTable
        id          INT     NOT NULL    PK  AI  UNIQUE
        name1       TEXT    NOT NULL                        (Фамилия)
        name2       TEXT    NOT NULL                        (Имя)
        name3       TEXT    NOT NULL                        (Отчество)
        login       TEXT    NOT NULL
        password    TEXT    NOT NULL
    """
    fields = ['id', 'name1', 'name2', 'name3', 'login', 'password']

    def __init__(self, row):
        Row.__init__(self, Teacher, row)

    def check_password(self, password) -> bool:
        if self.__is_none__:
            return False
        return check_password_hash(self.password, password)

    def set_password(self, password) -> None:
        if self.__is_none__:
            return
        self.password = generate_password_hash(password)

    def name(self):
        return '{} {}. {}.'.format(self.name1, self.name2[0], self.name3[0])


class TeachersTable:
    table = "teacher"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(TeachersTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "name1"	TEXT NOT NULL,
        "name2"	TEXT NOT NULL,
        "name3"	TEXT NOT NULL,
        "login"	TEXT NOT NULL,
        "password"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select(id: int) -> Teacher:
        return Table.select_one(TeachersTable.table, Teacher, 'id', id)

    @staticmethod
    def select_by_login(login: str) -> Teacher:
        return Table.select_one(TeachersTable.table, Teacher, 'login', login)

    @staticmethod
    def update(teacher: Teacher) -> None:
        return Table.update(TeachersTable.table, teacher)

    @staticmethod
    def insert(teacher: Teacher) -> None:
        return Table.insert(TeachersTable.table, teacher)

    @staticmethod
    def delete(teacher: Teacher) -> None:
        return Table.delete(TeachersTable.table, teacher)

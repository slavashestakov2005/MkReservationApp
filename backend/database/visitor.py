from .database import Table, Row


class Visitor(Row):
    """
        Строка таблицы VisitorsTable
        id          INT     NOT NULL    PK  AI  UNIQUE
        event       INT     NOT NULL
        name1       TEXT    NOT NULL                        (Фамилия)
        name2       TEXT    NOT NULL                        (Имя)
        vclass      TEXT    NOT NULL                        (Класс)
        status      INT     NOT NULL                        (0 - Зарегистрирован; 1 - Оплачено; <... что-то ещё ...>)
    """
    fields = ['id', 'event', 'name1', 'name2', 'vclass', 'status']
    SIGN_UP = 0
    STATUSES = ['Зарегистрирован']

    def __init__(self, row):
        Row.__init__(self, Visitor, row)

    def name(self):
        return '{} {}'.format(self.name1, self.name2)

    def get_status(self):
        return Visitor.STATUSES[self.status]


class VisitorsTable:
    table = "visitor"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(VisitorsTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "event"	INTEGER NOT NULL,
        "name1"	TEXT NOT NULL,
        "name2"	TEXT NOT NULL,
        "vclass"	TEXT NOT NULL,
        "status"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(VisitorsTable.table, Visitor)

    @staticmethod
    def select_by_data(visitor: Visitor) -> Visitor:
        return Table.select_one(VisitorsTable.table, Visitor, 'event', visitor.event, 'name1', visitor.name1, 'name2',
                                visitor.name2, 'vclass', visitor.vclass)

    @staticmethod
    def select_by_event(event: int) -> list:
        return Table.select_list(VisitorsTable.table, Visitor, 'event', event)

    @staticmethod
    def insert(visitor: Visitor) -> None:
        return Table.insert(VisitorsTable.table, visitor)

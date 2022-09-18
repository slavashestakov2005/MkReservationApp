from .database import Row, Table, Query
from datetime import datetime


class Visitor(Row):
    """
        Строка таблицы VisitorsTable
        id          INT     NOT NULL    PK  AI  UNIQUE
        event       INT     NOT NULL
        name1       TEXT    NOT NULL                        (Фамилия)
        name2       TEXT    NOT NULL                        (Имя)
        vclass      TEXT    NOT NULL                        (Класс)
        status      INT     NOT NULL                        (Перечислено ниже)
        payment     INT     NOT NULL
        time        INT     NOT NULL
        telephone   TEXT    NOT NULL
    """
    fields = ['id', 'event', 'name1', 'name2', 'vclass', 'status', 'payment', 'time', 'telephone']
    add_form = [Row.NONE, Row.NONE, Row.NE_STR, Row.NE_STR, Row.NE_STR, Row.NONE, Row.NONE, Row.NONE, Row.NE_STR]
    SIGN_UP, PAID, NOT_PAID, ERROR = 0, 1, 2, 3
    STATUSES = ['Зарегистрирован', 'Оплачено', 'Не оплачено', 'Ошибка']

    def __init__(self, row):
        Row.__init__(self, Visitor, row)

    def name(self):
        return '{} {}'.format(self.name1, self.name2)

    def get_status(self):
        return Visitor.STATUSES[self.status]

    def get_time(self):
        return datetime.fromtimestamp(self.time).strftime('%Y.%m.%d %H:%M:%S')


class VisitorsTable(Table):
    table = "visitor"
    row = Visitor
    create = '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "event"	INTEGER NOT NULL,
        "name1"	TEXT NOT NULL,
        "name2"	TEXT NOT NULL,
        "vclass"	TEXT NOT NULL,
        "status"	INTEGER NOT NULL,
        "payment"	INTEGER NOT NULL,
        "time"	INTEGER NOT NULL,
        "telephone"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );'''

    @staticmethod
    def select_by_data(visitor: Visitor) -> Visitor:
        return Query.select_one(VisitorsTable.table, Visitor, 'event', visitor.event, 'name1', visitor.name1, 'name2',
                                visitor.name2, 'vclass', visitor.vclass)

    @staticmethod
    def select_by_event(event: int) -> list:
        return Query.select_list(VisitorsTable.table, Visitor, 'event', event)

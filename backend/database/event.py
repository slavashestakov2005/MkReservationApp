from .database import Table, Row
from datetime import datetime
from ..help.help import mouth_name


class Event(Row):
    """
        Строка таблицы EventsTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        teacher         INT     NOT NULL
        master_class    INT     NOT NULL
        places          INT     NOT NULL
        booked          INR     NOT NULL
        cost            INT     NOT NULL
        start           INT     NOT NULL                        (Unix, секунды)
    """
    fields = ['id', 'teacher', 'master_class', 'places', 'booked', 'cost', 'start']

    def __init__(self, row):
        Row.__init__(self, Event, row)

    @staticmethod
    def sort_by_start(event):
        return event.start

    def date(self):
        return datetime.fromtimestamp(self.start).strftime('%Y.%m.%d %H:%M')

    def mouth(self):
        dt = datetime.fromtimestamp(self.start)
        return dt.year, dt.month

    def mouth_name(self):
        return mouth_name(self.mouth()[1] - 1)


class EventsTable:
    table = "event"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(EventsTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "teacher"	INTEGER NOT NULL,
        "master_class"	INTEGER NOT NULL,
        "places"	INTEGER NOT NULL,
        "booked"	INTEGER NOT NULL,
        "cost"	INTEGER NOT NULL,
        "start"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(EventsTable.table, Event)

    @staticmethod
    def select(id: int):
        return Table.select_one(EventsTable.table, Event, 'id', id)

    @staticmethod
    def select_by_time_limits(start: int, end: int) -> list:
        return Table.select_list_with_where(EventsTable.table, Event, 'start', start, end)

    @staticmethod
    def insert(event: Event) -> None:
        return Table.insert(EventsTable.table, event)

    @staticmethod
    def update(event: Event) -> None:
        return Table.update(EventsTable.table, event)

    @staticmethod
    def delete(event: Event) -> None:
        return Table.delete(EventsTable.table, event)

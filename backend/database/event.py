from .database import Table, Row


class Event(Row):
    """
        Строка таблицы ListenersTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        teacher         INT     NOT NULL
        master_class    INT     NOT NULL
        places          INT     NOT NULL
        cost            INT     NOT NULL
        start           INT     NOT NULL                        (Unix, секунды)
    """
    fields = ['id', 'teacher', 'master_class', 'places', 'cost', 'start']

    def __init__(self, row):
        Row.__init__(self, Event, row)


class EventsTable:
    table = "event"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(EventsTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "teacher"	INTEGER NOT NULL,
        "master_class"	INTEGER NOT NULL,
        "places"	INTEGER NOT NULL,
        "cost"	INTEGER NOT NULL,
        "start"	INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select(id: int):
        return Table.select_one(EventsTable.table, Event, 'id', id)

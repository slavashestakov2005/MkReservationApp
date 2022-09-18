from .database import Row, Table, Query
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
        revenue         INT     NOT NULL
        start           INT     NOT NULL                        (Unix, секунды)
        classes         TEXT    NOT NULL
    """
    fields = ['id', 'teacher', 'master_class', 'places', 'booked', 'cost', 'revenue', 'start', 'classes']
    add_form = [Row.NONE, Row.NE_INT, Row.NE_INT, Row.NE_INT, Row.NONE, Row.NE_INT, Row.NONE, Row.NE_DATETIME, Row.STR]
    edit_form = [Row.NE_INT, Row.INT, Row.INT, Row.INT, Row.NONE, Row.INT, Row.NONE, Row.DATETIME, Row.STR]

    def __init__(self, row):
        Row.__init__(self, Event, row)

    @staticmethod
    def sort_by_start(event):
        return event.start

    def short_date(self):
        return datetime.fromtimestamp(self.start).strftime('%Y.%m.%d')

    def date(self):
        return datetime.fromtimestamp(self.start).strftime('%Y.%m.%d %H:%M')

    def mouth(self):
        dt = datetime.fromtimestamp(self.start)
        return dt.year, dt.month

    def mouth_name(self):
        return mouth_name(self.mouth()[1] - 1)

    @staticmethod
    def parse_classes(text: str):
        return ' | '.join(_.strip() for _ in text.strip().strip('|').split('|'))

    def get_classes(self):
        return self.classes if self.classes else 'Все'

    def can_visit(self, cls: str):
        if not self.classes:
            return True
        for x in self.classes.split(' | '):
            if cls == x or x.isdigit() and cls.startswith(x):
                return True
        return False


class EventsTable(Table):
    table = "event"
    row = Event
    create = '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "teacher"	INTEGER NOT NULL,
        "master_class"	INTEGER NOT NULL,
        "places"	INTEGER NOT NULL,
        "booked"	INTEGER NOT NULL,
        "cost"	INTEGER NOT NULL,
        "revenue"	INTEGER NOT NULL,
        "start"	INTEGER NOT NULL,
        "classes"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );'''

    @staticmethod
    def select_by_time_limits(start: int, end: int) -> list:
        return Query.select_list_with_where(EventsTable.table, Event, 'start', start, end)

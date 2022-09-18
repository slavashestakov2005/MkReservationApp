from .database import Row, Table
from markdown import markdown


class MasterClass(Row):
    """
        Строка таблицы MasterClassesTable
        id                  INT     NOT NULL    PK  AI  UNIQUE
        name                TEXT    NOT NULL
        short_description   TEXT    NOT NULL
        description         TEXT    NOT NULL
        duration            INT                                 (минуты)
        file                TEXT    NOT NULL
    """
    fields = ['id', 'name', 'short_description', 'description', 'duration', 'file']
    add_form = [Row.NONE, Row.NE_STR, Row.NE_STR, Row.NE_STR, Row.NE_INT, Row.FILE]
    edit_form = [Row.NE_INT, Row.STR, Row.STR, Row.STR, Row.INT, Row.FILE]

    def __init__(self, row):
        Row.__init__(self, MasterClass, row)

    def get_html(self):
        return markdown(self.description)

    def get_short_html(self):
        return markdown(self.short_description)


class MasterClassesTable(Table):
    table = "master_class"
    row = MasterClass
    create = '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL,
        "short_description"	TEXT NOT NULL,
        "description"	TEXT NOT NULL,
        "duration"	INTEGER NOT NULL,
        "file"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );'''

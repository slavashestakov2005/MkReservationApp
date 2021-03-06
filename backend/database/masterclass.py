from .database import Table, Row
from markdown import markdown


class MasterClass(Row):
    """
        Строка таблицы MasterClassesTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        name            TEXT    NOT NULL
        photo           TEXT    NOT NULL
        description     TEXT    NOT NULL
        duration        INT                                 (минуты)
        file            TEXT    NOT NULL
    """
    fields = ['id', 'name', 'photo', 'description', 'duration', 'file']

    def __init__(self, row):
        Row.__init__(self, MasterClass, row)

    def get_html(self):
        return markdown(self.description)


class MasterClassesTable:
    table = "master_class"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(MasterClassesTable.table, '''(
        "id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL,
        "photo"	TEXT NOT NULL,
        "description"	TEXT NOT NULL,
        "duration"	INTEGER NOT NULL,
        "file"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(MasterClassesTable.table, MasterClass)

    @staticmethod
    def select(id: int) -> MasterClass:
        return Table.select_one(MasterClassesTable.table, MasterClass, 'id', id)

    @staticmethod
    def select_last() -> MasterClass:
        return Table.select_last(MasterClassesTable.table, MasterClass)

    @staticmethod
    def insert(mc: MasterClass) -> None:
        return Table.insert(MasterClassesTable.table, mc)

    @staticmethod
    def update(mc: MasterClass) -> None:
        return Table.update(MasterClassesTable.table, mc)

    @staticmethod
    def delete(mc: MasterClass) -> None:
        return Table.delete(MasterClassesTable.table, mc)

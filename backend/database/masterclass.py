from .database import Table, Row


class MasterClass(Row):
    """
        Строка таблицы ListenersTable
        id              INT     NOT NULL    PK  AI  UNIQUE
        name            TEXT    NOT NULL
        photo           TEXT    NOT NULL
        description     TEXT    NOT NULL
        duration        INT                                 (минуты)
    """
    fields = ['id', 'name', 'photo', 'description', 'duration']

    def __init__(self, row):
        Row.__init__(self, MasterClass, row)


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
        PRIMARY KEY("id" AUTOINCREMENT)
        );''')

    @staticmethod
    def select(id: int) -> MasterClass:
        return Table.select_one(MasterClassesTable.table, MasterClass, 'id', id)

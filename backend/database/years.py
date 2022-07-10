from .database import Table, Row


class Year(Row):
    """
        Строка таблицы YearsTable
        year            INT     NOT NULL    PK      UNIQUE
        months          INT     NOT NULL                        (битовое представление, месяца [0;11])
        mc_count        TEXT    NOT NULL                        (<#0>|<#1>|...|<#11>)
        visitors        TEXT    NOT NULL                        (<#0>|<#1>|...|<#11>)
        revenue         TEXT    NOT NULL                        (<#0>|<#1>|...|<#11>)
    """
    fields = ['year', 'months', 'mc_count', 'visitors', 'revenue']
    ALL_MONTHS = (1 << 12) - 1
    NONE_MOUTHS = 0
    ZERO12 = '0|' * 11 + '0'

    def __init__(self, row):
        Row.__init__(self, Year, row)

    def exists(self, month):
        return (self.months >> month) % 2

    def set_months(self, mouths):
        self.months = Year.NONE_MOUTHS
        for mouth in mouths:
            self.months += (1 << mouth)
        return self.months

    def copy(self):
        return Year([self.year, self.months, self.mc_count, self.visitors, self.revenue])

    def get_mc_count(self, mouth: int):
        return int(self.mc_count.split('|')[mouth])

    def set_mc_count(self, mouth: int, mc_count: int):
        vis = self.mc_count.split('|')
        vis[mouth] = str(mc_count)
        self.mc_count = '|'.join(vis)

    def get_visitors(self, mouth: int):
        return int(self.visitors.split('|')[mouth])

    def set_visitors(self, mouth: int, visitor: int):
        vis = self.visitors.split('|')
        vis[mouth] = str(visitor)
        self.visitors = '|'.join(vis)

    def get_revenue(self, mouth: int):
        return int(self.revenue.split('|')[mouth])

    def set_revenue(self, mouth: int, revenue: int):
        revs = self.revenue.split('|')
        revs[mouth] = str(revenue)
        self.revenue = '|'.join(revs)


class YearsTable:
    table = "year"

    @staticmethod
    def create_table() -> None:
        Table.drop_and_create(YearsTable.table, '''(
        "year"	INTEGER NOT NULL UNIQUE,
        "months"	INTEGER NOT NULL,
        "mc_count"	TEXT NOT NULL,
        "visitors"	TEXT NOT NULL,
        "revenue"	TEXT NOT NULL,
        PRIMARY KEY("year")
        );''')

    @staticmethod
    def select_all() -> list:
        return Table.select_list(YearsTable.table, Year)

    @staticmethod
    def select(year: int) -> Year:
        return Table.select_one(YearsTable.table, Year, 'year', year)

    @staticmethod
    def left(year: int) -> list:
        return Table.select_list_with_simple_where(YearsTable.table, Year, 'year', '<', year)

    @staticmethod
    def right(year: int) -> list:
        return Table.select_list_with_simple_where(YearsTable.table, Year, 'year', '>', year)

    @staticmethod
    def update(year: Year) -> None:
        return Table.update(YearsTable.table, year, 'year')

    @staticmethod
    def insert(year: Year) -> None:
        return Table.insert(YearsTable.table, year)

    @staticmethod
    def delete(year: Year) -> None:
        return Table.delete(YearsTable.table, 'year', year.year)

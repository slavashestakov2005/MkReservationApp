from .config import *
from .database import *
from .event import *
from .masterclass import *
from .teacher import *
from .visitor import *
from .years import *


def create_tables():
    if Config.DROP_DB:
        EventsTable.create_table()
        MasterClassesTable.create_table()
        TeachersTable.create_table()
        VisitorsTable.create_table()
        YearsTable.create_table()

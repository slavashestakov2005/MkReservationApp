from ..database import EventsTable, MasterClassesTable, TeachersTable
from datetime import datetime, timedelta
import locale
locale.setlocale(category=locale.LC_ALL, locale="Russian")


class EventPopup:
    def __init__(self, event):
        self.event = event
        self.title, self.start, self.end, self.date = '', '', '', ''
        self.description, self.cost, self.places, self.teacher = '', '', '', ''
        ev = EventsTable.select(event)
        if not ev.__is_none__:
            self.cost, self.places = ev.cost, ev.places
            self.date, self.start = EventPopup.start(ev.start)
            t = TeachersTable.select(ev.teacher)
            mc = MasterClassesTable.select(ev.master_class)
            if not t.__is_none__:
                self.teacher = t.name()
            if not mc.__is_none__:
                self.title, self.description = mc.name, mc.description
                self.end = EventPopup.end(ev.start, mc.duration)

    @staticmethod
    def start(stamp):
        s = datetime.fromtimestamp(stamp)
        return s.strftime('%Y.%m.%d'), s.strftime('%H:%M')

    @staticmethod
    def end(stamp, delta):
        template = '%H:%M'
        s = datetime.fromtimestamp(stamp)
        d = timedelta(minutes=delta)
        return (s + d).time().strftime(template)

    def data(self):
        return {'title': 'Ёлочка', 'time': '10:00 - 12:00', 'desc': 'Будем делать ёолчка своими руками из фанеры', 'cost':
        '250 Р', 'child': 'Осталось мест 10 / 30', 'teacher': 'Вахитова Е.Ю.'}

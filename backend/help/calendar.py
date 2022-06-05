from datetime import datetime, timedelta
from calendar import monthrange
from ..database import Event, EventsTable, MasterClassesTable


MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
         'Декабрь']


def correct_form(mouth):
    mouth %= 12
    return mouth if mouth else 12


class EventInfo:
    def __init__(self, id, name):
        self.id, self.name = id, name

    def __repr__(self):
        return "EventInfo('id': {}, 'name': {})".format(self.id, self.name)


class DayInfo:
    def __init__(self, day=0, events=None):
        if events is None:
            events = []
        self.events, self.day = events, day

    def __repr__(self):
        return "DayInfo('day': {}, 'days': {})".format(self.day, self.days)


class MonthInfo:
    def __init__(self, m):
        self.id, self.name = m + 1, MONTH[m]
        self.mc_count, self.visitors, self.unique_visitors, self.revenue, self.profit = 0, 0, 0, 0, 0


class YearInfo:
    def __init__(self, year):
        self.year = year
        self.months = [MonthInfo(m) for m in range(12)]


class Calendar:
    def __init__(self, year, month):
        self.year, self.month = year, month
        self.a = datetime(self.year, self.month, 1)
        self.first_day, self.days = monthrange(self.year, self.month)
        self.b = self.a + timedelta(days=self.days)

    def prepare_events(self):
        events = EventsTable.select_by_time_limits(int(self.a.timestamp()), int(self.b.timestamp()))
        events.sort(key=Event.sort_by_start)
        days_info = {}
        for event in events:
            event.start = datetime.fromtimestamp(event.start)
            d = event.start.day
            if d not in days_info:
                days_info[d] = []
            days_info[d].append(event)
        return days_info

    def create(self):
        mc = {_.id: _ for _ in MasterClassesTable.select_all()}
        events_days_info = self.prepare_events()
        calendar = [[DayInfo() for _ in range(self.first_day + 1)]]
        for day in range(1, 1 + self.days):
            if len(calendar[-1]) == 8:
                calendar[-1].append(DayInfo())
                calendar.append([])
                calendar[-1].append(DayInfo())
            if day not in events_days_info:
                calendar[-1].append(DayInfo(day))
            else:
                info = [EventInfo(_.id, mc[_.master_class].name) for _ in events_days_info[day]]
                calendar[-1].append(DayInfo(day, info))
        while len(calendar[-1]) != 9:
            calendar[-1].append(DayInfo())
        calendar[-3][0].events = [MONTH[(self.month + 10) % 12], correct_form(self.month - 1),
                                  self.year - (1 if self.month == 1 else 0)]
        calendar[-3][8].events = [MONTH[self.month % 12], correct_form(self.month + 1),
                                  self.year + (1 if self.month == 12 else 0)]
        calendar[-3][0].day = calendar[-3][8].day = -1
        return MONTH[(self.month + 11) % 12], calendar


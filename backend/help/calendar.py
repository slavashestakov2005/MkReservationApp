from datetime import datetime, timedelta
from calendar import monthrange
from ..database import Event, EventsTable, MasterClassesTable
from ..config import Config
from .help import save_template


MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
         'Декабрь']


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
        self.year = year.year
        self.months = [MonthInfo(m) for m in range(12) if year.exists(m)]


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

    def create(self, left, right, mc):
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
        calendar[-3][0].events = [MONTH[left[1] - 1], left[1], left[0]]
        calendar[-3][8].events = [MONTH[right[1] - 1], right[1], right[0]]
        calendar[-3][0].day = calendar[-3][8].day = -1
        return MONTH[(self.month + 11) % 12], calendar


def update_mouth(this, prev, next, mc):
    filename = Config.TEMPLATES_FOLDER + '/{}/{}.html'
    c = Calendar(*this)
    name, data = c.create(prev, next, mc)
    cur_file = filename.format(*this)
    save_template('template_calendar.html', cur_file, 5, name=name, calendar=data, year=this[0])


class CalendarUpdater:
    def __init__(self):
        self.mouths_old, self.mouths_new = [], []

    def parse_mouths(self, years_old, years_new):
        for year in years_old:
            for i in range(12):
                if year.exists(i):
                    self.mouths_old.append((year.year, i + 1))
        for year in years_new:
            for i in range(12):
                if year.exists(i):
                    self.mouths_new.append((year.year, i + 1))
        self.mouths_old.sort()
        self.mouths_new.sort()

    def update(self):
        mc = {_.id: _ for _ in MasterClassesTable.select_all()}
        ln_old, ln_new = len(self.mouths_old), len(self.mouths_new)
        for i in range(ln_new):
            this = self.mouths_new[i]
            found = this in self.mouths_old
            if not found:
                prev1, next1 = (0, 0), (0, 0)
            else:
                idx = self.mouths_old.index(this)
                prev1 = self.mouths_old[idx - 1] if idx else (0, 0)
                next1 = self.mouths_old[idx + 1] if idx + 1 < ln_old else (0, 0)
            prev2, next2 = self.mouths_new[i - 1] if i else (0, 0), self.mouths_new[i + 1] if i + 1 < ln_new else (0, 0)
            if not found or prev1 != prev2 or next1 != next2:
                update_mouth(this, prev2, next2, mc)

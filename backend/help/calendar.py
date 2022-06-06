from datetime import datetime, timedelta
from calendar import monthrange
from ..database import Event, EventsTable, MasterClassesTable, TeachersTable, YearsTable
from ..config import Config
from .help import save_template


MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
         'Декабрь']


class EventInfo:
    def __init__(self, event, mc, teacher):
        self.id, self.places, self.cost = event.id, event.places, event.cost
        self.date, self.start = EventInfo.start(event.start)
        self.end = EventInfo.end(event.start, mc.duration)
        self.name, self.description = mc.name, mc.get_html()
        self.teacher = teacher.name()

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
            d = datetime.fromtimestamp(event.start).day
            if d not in days_info:
                days_info[d] = []
            days_info[d].append(event)
        return days_info

    def create(self, left, right, mc, teachers):
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
                info = [EventInfo(_, mc[_.master_class], teachers[_.teacher]) for _ in events_days_info[day]]
                calendar[-1].append(DayInfo(day, info))
        while len(calendar[-1]) != 9:
            calendar[-1].append(DayInfo())
        calendar[-3][0].events = [MONTH[left[1] - 1], left[1], left[0]]
        calendar[-3][8].events = [MONTH[right[1] - 1], right[1], right[0]]
        calendar[-3][0].day = calendar[-3][8].day = -1
        return MONTH[(self.month + 11) % 12], calendar


def update_mouth(this, prev, next, mc, teachers):
    filename = Config.TEMPLATES_FOLDER + '/{}/{}.html'
    c = Calendar(*this)
    name, data = c.create(prev, next, mc, teachers)
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

    def update(self, mouth=None):
        mc = {_.id: _ for _ in MasterClassesTable.select_all()}
        teachers = {_.id: _ for _ in TeachersTable.select_all()}
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
            if mouth is None and (not found or prev1 != prev2 or next1 != next2) or \
                    mouth == 'all' or type(mouth) == list and this in mouth:
                update_mouth(this, prev2, next2, mc, teachers)


def calendar_update_all():
    c = CalendarUpdater()
    years = YearsTable.select_all()
    c.parse_mouths(years, years)
    c.update('all')


def calendar_update_mouths(mouths):
    c = CalendarUpdater()
    years = YearsTable.select_all()
    c.parse_mouths(years, years)
    c.update(mouths)

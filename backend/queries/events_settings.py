from backend import app
from flask import render_template
from flask_cors import cross_origin
from flask_login import login_required
from datetime import datetime
from ..help import calendar_update_all, calendar_update_mouths, parse_checkbox, SplitFile, copy_fields, form_add,\
    form_edit, form_delete
from ..database import MasterClassesTable, EventsTable, Event, TeachersTable, YearsTable
from ..config import Config
'''
            TEMPLATE            Имя шаблона с настройкой мастер классов и событий.
            params()            Постоянные параметры этого шаблона.
            update_mc_count()   Обновляет количество событий в месяце.
    /events                     Пересылает на страницу с этим шаблоном.
    /add_mc                     Создаёт мастер-класс.
    /edit_mc                    Редактирует мастер-класс.
    /delete_mc                  Удаляет мастер-класс.
    /add_event                  Создаёт событие.
    /edit_event                 Редактирует событие.
    /delete_event               Удаляет событие.
'''


TEMPLATE = 'settings_events.html'


def params():
    return {'mc': MasterClassesTable.select_all(), 'e': EventsTable.select_all()}


def update_mc_count(mouth: list, dv: int = 1):
    year = YearsTable.select(mouth[0])
    year.set_mc_count(mouth[1] - 1, year.get_mc_count(mouth[1] - 1) + dv)
    YearsTable.update(year)
    f = SplitFile(Config.TEMPLATES_FOLDER + '/' + str(mouth[0]) + '/main.html')
    f.insert_after_comment(' {}-{} '.format(mouth[1], 'mc_count'), str(year.get_mc_count(mouth[1] - 1)))
    f.save_file()


@app.route('/events')
@cross_origin()
@login_required
def events():
    return render_template(TEMPLATE, **params())


@app.route('/add_mc', methods=['POST'])
@cross_origin()
@login_required
@form_add(MasterClassesTable)
def add_mc(row):
    if row.__is_none__:
        return render_template(TEMPLATE, error_add_mc='Поля заполнены не правильно', **params())
    if row.duration < 1 or row.duration > 240:
        return render_template(TEMPLATE, error_add_mc='Мастер класс не может столько длиться', **params())
    MasterClassesTable.insert(row)
    row = MasterClassesTable.select_last()
    row.file = parse_checkbox(row.id, 'logo.png', folder='MasterClass/')
    MasterClassesTable.update(row)
    return render_template(TEMPLATE, error_add_mc='Мастер класс добавлен', **params())


@app.route('/edit_mc', methods=['POST'])
@cross_origin()
@login_required
@form_edit(MasterClassesTable)
def edit_mc(old_row, new_row):
    if new_row.__is_none__:
        return render_template(TEMPLATE, error_edit_mc='Поля заполнены не правильно', **params())
    if old_row.__is_none__:
        return render_template(TEMPLATE, error_edit_mc='Не верный ID мастер класса', **params())
    if new_row.duration is not None and (new_row.duration < 1 or new_row.duration > 240):
        return render_template(TEMPLATE, error_edit_mc='Мастер класс не может столько длиться', **params())
    new_row = copy_fields(new_row, old_row)
    new_row.file = parse_checkbox(new_row.id, new_row.file, folder='MasterClass/')
    MasterClassesTable.update(new_row)
    calendar_update_all()
    return render_template(TEMPLATE, error_edit_mc='Мастер класс изменён', **params())


@app.route('/delete_mc', methods=['POST'])
@cross_origin()
@login_required
@form_delete(MasterClassesTable)
def delete_mc(row):
    if row.__is_none__:
        return render_template(TEMPLATE, error_delete_mc='Не верный ID мастер класса', **params())
    MasterClassesTable.delete(row)
    calendar_update_all()
    return render_template(TEMPLATE, error_delete_mc='Мастер класс удалён', **params())


@app.route('/add_event', methods=['POST'])
@cross_origin()
@login_required
@form_add(EventsTable)
def add_event(row):
    if row.__is_none__:
        return render_template(TEMPLATE, error_add_event='Поля заполнены не правильно', **params())
    if TeachersTable.select(row.teacher).__is_none__:
        return render_template(TEMPLATE, error_add_event='Не верный ID преподавателя', **params())
    if MasterClassesTable.select(row.master_class).__is_none__:
        return render_template(TEMPLATE, error_add_event='Не верный ID мастер класса', **params())
    if row.places < 1 or row.places > 50:
        return render_template(TEMPLATE, error_add_event='В событии не может участвовать столько людей', **params())
    if row.cost < 0 or row.cost > 5000:
        return render_template(TEMPLATE, error_add_event='Событие не может столько стоить', **params())
    if row.start[0][0] < 2022 or row.start[0][0] > 2100:
        return render_template(TEMPLATE, error_add_event='Событие не может быть запланировано на такую дату', **params())
    row.booked, row.revenue, row.classes = 0, 0, Event.parse_classes(row.classes)
    row.start = int(datetime(*row.start[0], *row.start[1]).timestamp())
    m = row.mouth()
    EventsTable.insert(row)
    calendar_update_mouths([m])
    update_mc_count(m)
    return render_template(TEMPLATE, error_add_event='Событие добавлено', **params())


@app.route('/edit_event', methods=['POST'])
@cross_origin()
@login_required
@form_edit(EventsTable)
def edit_event(old_row, new_row):
    if new_row.__is_none__:
        return render_template(TEMPLATE, error_edit_event='Поля заполнены не правильно', **params())
    if old_row.__is_none__:
        return render_template(TEMPLATE, error_edit_event='Не верный ID события', **params())
    if new_row.teacher and TeachersTable.select(new_row.teacher).__is_none__:
        return render_template(TEMPLATE, error_edit_event='Не верный ID преподавателя', **params())
    if new_row.master_class and MasterClassesTable.select(new_row.master_class).__is_none__:
        return render_template(TEMPLATE, error_edit_event='Не верный ID мастер класса', **params())
    if new_row.places is not None and (new_row.places < 1 or new_row.places > 50):
        return render_template(TEMPLATE, error_edit_event='В событии не может участвовать столько людей', **params())
    if new_row.cost is not None and (new_row.cost < 0 or new_row.cost > 5000):
        return render_template(TEMPLATE, error_edit_event='Событие не может столько стоить', **params())
    if new_row.start[0] is not None and (new_row.start[0][0] < 2022 or new_row.start[0][0] > 2100):
        return render_template(TEMPLATE, error_edit_event='Событие не может быть запланировано на такую дату', **params())
    old_mouth, old_time = old_row.mouth(), old_row.date().split()
    date, time = new_row.start
    new_row = copy_fields(new_row, old_row)
    if date and time:
        new_row.start = int(datetime(*date, *time).timestamp())
    elif date:
        new_row.start = int(datetime(*date, *list(map(int, old_time[1].split(':')))).timestamp())
    elif time:
        new_row.start = int(datetime(*list(map(int, old_time[0].split('.'))), *time).timestamp())
    EventsTable.update(new_row)
    new_mouth = new_row.mouth()
    if old_mouth != new_mouth:
        calendar_update_mouths([old_mouth, new_mouth])
        update_mc_count(old_mouth, -1)
        update_mc_count(new_mouth)
    else:
        calendar_update_mouths([old_mouth])
    return render_template(TEMPLATE, error_edit_event='Событие изменено', **params())


@app.route('/delete_event', methods=['POST'])
@cross_origin()
@login_required
@form_delete(EventsTable)
def delete_event(row):
    if row.__is_none__:
        return render_template(TEMPLATE, error_delete_event='Не верный ID события', **params())
    EventsTable.delete(row)
    m = row.mouth()
    calendar_update_mouths([m])
    update_mc_count(m, -1)
    return render_template(TEMPLATE, error_delete_event='Событие удалено', **params())

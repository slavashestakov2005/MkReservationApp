from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required
from datetime import datetime
from ..help import empty_checker
from ..database import MasterClassesTable, MasterClass, EventsTable, Event, TeachersTable
'''
                    TEMPLATE            Имя шиблона с настройкой мастер-классов и событий.
                    params()            Постоянные параметры этого шаблона.
    /events         events()            Пересылает на страницы с этим шаблоном.
    /add_mc         add_mc()            Создаёт мастер-класс.
    /edit_mc        edit_mc()           Редактирует мастер-класс.
    /edit_mc        edit_mc()           Удаляет мастер-класс.
    /add_event      add_event()         Создаёт событие.
    /edit_event     edit_event()        Редактирует событие.
    /delete_event   delete_event()      Удаляет событие.
'''


TEMPLATE = 'events_settings.html'


def params():
    return {'mc': MasterClassesTable.select_all(), 'e': EventsTable.select_all()}


@app.route('/events')
@cross_origin()
@login_required
def events():
    return render_template(TEMPLATE, **params())


@app.route('/add_mc', methods=['POST'])
@cross_origin()
@login_required
def add_mc():
    try:
        name = request.form['name']
        description = request.form['description']
        duration = int(request.form['duration'])
        empty_checker(name, description)
    except Exception:
        return render_template(TEMPLATE, error_add_mc='Поля заполнены не правильно', **params())

    if duration < 1 or duration > 240:
        return render_template(TEMPLATE, error_add_mc='Мастер-класс не может столько длиться', **params())
    mc = MasterClass([None, name, '', description, duration])
    MasterClassesTable.insert(mc)
    return render_template(TEMPLATE, error_add_mc='Мастер-класс добавлен', **params())


@app.route('/edit_mc', methods=['POST'])
@cross_origin()
@login_required
def edit_mc():
    try:
        id = int(request.form['id'])
        name = request.form['name']
        description = request.form['description']
        duration = int(request.form['duration']) if request.form['duration'] else None
    except Exception:
        return render_template(TEMPLATE, error_edit_mc='Поля заполнены не правильно', **params())

    mc = MasterClassesTable.select(id)
    if mc.__is_none__:
        return render_template(TEMPLATE, error_edit_mc='Не верный ID мастер-класса', **params())
    if duration is not None and (duration < 1 or duration > 240):
        return render_template(TEMPLATE, error_edit_mc='Мастер-класс не может столько длиться', **params())
    if name:
        mc.name = name
    if description:
        mc.description = description
    if duration:
        mc.duration = duration
    MasterClassesTable.update(mc)
    return render_template(TEMPLATE, error_edit_mc='Мастер-класс изменён', **params())


@app.route('/delete_mc', methods=['POST'])
@cross_origin()
@login_required
def delete_mc():
    try:
        id = int(request.form['id'])
    except Exception:
        return render_template(TEMPLATE, error_delete_mc='Поля заполнены не правильно', **params())

    mc = MasterClassesTable.select(id)
    if mc.__is_none__:
        return render_template(TEMPLATE, error_delete_mc='Не верный ID мастер-класса', **params())
    MasterClassesTable.delete(mc)
    return render_template(TEMPLATE, error_delete_mc='Мастер-класс удалён', **params())


@app.route('/add_event', methods=['POST'])
@cross_origin()
@login_required
def add_event():
    try:
        teacher = int(request.form['teacher'])
        master_class = int(request.form['master_class'])
        places = int(request.form['places'])
        cost = int(request.form['cost'])
        date = [int(_) for _ in request.form['date'].split('-')]
        time = [int(_) for _ in request.form['time'].split(':')]
        start = int(datetime(*date, *time).timestamp())
    except Exception:
        return render_template(TEMPLATE, error_add_event='Поля заполнены не правильно', **params())

    if TeachersTable.select(teacher).__is_none__:
        return render_template(TEMPLATE, error_add_event='Не верный ID преподавателя', **params())
    if MasterClassesTable.select(master_class).__is_none__:
        return render_template(TEMPLATE, error_add_event='Не верный ID мастер-класса', **params())
    if places < 1 or places > 50:
        return render_template(TEMPLATE, error_add_event='В событии не может участвовать столько людей', **params())
    if cost < 0 or cost > 5000:
        return render_template(TEMPLATE, error_add_event='Событие не может столько стоить', **params())
    if date[0] < 2022 or date[0] > 2100:
        return render_template(TEMPLATE, error_add_event='Событие не может быть запланировано на такую дату', **params())
    ev = Event([None, teacher, master_class, places, cost, start])
    EventsTable.insert(ev)
    return render_template(TEMPLATE, error_add_event='Событие добавлено', **params())


@app.route('/edit_event', methods=['POST'])
@cross_origin()
@login_required
def edit_event():
    try:
        id = int(request.form['id'])
        teacher = int(request.form['teacher']) if request.form['teacher'] else 0
        master_class = int(request.form['master_class']) if request.form['master_class'] else 0
        places = int(request.form['places']) if request.form['places'] else None
        cost = int(request.form['cost']) if request.form['cost'] else None
        date = [int(_) for _ in request.form['date'].split('-')] if request.form['date'] else 0
        time = [int(_) for _ in request.form['time'].split(':')] if request.form['time'] else 0
    except Exception:
        return render_template(TEMPLATE, error_edit_event='Поля заполнены не правильно', **params())

    event = EventsTable.select(id)
    if event.__is_none__:
        return render_template(TEMPLATE, error_edit_event='Не верный ID события', **params())
    if teacher and TeachersTable.select(teacher).__is_none__:
        return render_template(TEMPLATE, error_edit_event='Не верный ID преподавателя', **params())
    if master_class and MasterClassesTable.select(master_class).__is_none__:
        return render_template(TEMPLATE, error_edit_event='Не верный ID мастер-класса', **params())
    if places is not None and (places < 1 or places > 50):
        return render_template(TEMPLATE, error_edit_event='В событии не может участвовать столько людей', **params())
    if cost is not None and (cost < 0 or cost > 5000):
        return render_template(TEMPLATE, error_edit_event='Событие не может столько стоить', **params())
    if date != 0 and (date[0] < 2022 or date[0] > 2100):
        return render_template(TEMPLATE, error_edit_event='Событие не может быть запланировано на такую дату', **params())
    if teacher:
        event.teacher = teacher
    if master_class:
        event.master_class = master_class
    if places:
        event.places = places
    if cost:
        event.cost = cost
    old_time = event.date().split()
    if date != 0 and time != 0:
        event.start = int(datetime(*date, *time).timestamp())
    elif date != 0:
        event.start = int(datetime(*date, *list(map(int, old_time[1].split(':')))).timestamp())
    elif time != 0:
        event.start = int(datetime(*list(map(int, old_time[0].split('.'))), *time).timestamp())
    EventsTable.update(event)
    return render_template(TEMPLATE, error_edit_event='Событие изменено', **params())


@app.route('/delete_event', methods=['POST'])
@cross_origin()
@login_required
def delete_event():
    try:
        id = int(request.form['id'])
    except Exception:
        return render_template(TEMPLATE, error_delete_event='Поля заполнены не правильно', **params())

    event = EventsTable.select(id)
    if event.__is_none__:
        return render_template(TEMPLATE, error_delete_event='Не верный ID события', **params())
    EventsTable.delete(event)
    return render_template(TEMPLATE, error_delete_event='Событие удалено', **params())

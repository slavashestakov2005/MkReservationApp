from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required
from datetime import datetime
from ..help import empty_checker, calendar_update_all, calendar_update_mouths, generate_filename, SplitFile
from ..database import MasterClassesTable, MasterClass, EventsTable, Event, TeachersTable, YearsTable
from ..config import Config
'''
                    TEMPLATE            Имя шиблона с настройкой мастер-классов и событий.
                    params()            Постоянные параметры этого шаблона.
                    get_image_name()    Генерирует имя файла для логотипа МК.
                    update_mc_count()   Обновляет количество событий в месяце.
    /events         events()            Пересылает на страницу с этим шаблоном.
    /add_mc         add_mc()            Создаёт мастер-класс.
    /edit_mc        edit_mc()           Редактирует мастер-класс.
    /delete_mc      delete_mc()         Удаляет мастер-класс.
    /add_event      add_event()         Создаёт событие.
    /edit_event     edit_event()        Редактирует событие.
    /delete_event   delete_event()      Удаляет событие.
'''


TEMPLATE = 'settings_events.html'


def params():
    return {'mc': MasterClassesTable.select_all(), 'e': EventsTable.select_all()}


def get_image_name(new, default='logo.png'):
    if request.form.get('is_file') is not None:
        file = request.files['file-file']
        file_name, tail = generate_filename(file.filename, str(new))
        file.save(file_name)
        return tail
    tail = request.form['file-name']
    return tail if tail else default


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
    mc = MasterClass([None, name, '', description, duration, ''])
    MasterClassesTable.insert(mc)
    mc = MasterClassesTable.select_last()
    mc.file = get_image_name(mc.id)
    MasterClassesTable.update(mc)
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
    mc.file = get_image_name(mc.id, mc.file)
    MasterClassesTable.update(mc)
    calendar_update_all()
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
    calendar_update_all()
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
        classes = Event.parse_classes(request.form['classes'])
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
    ev = Event([None, teacher, master_class, places, 0, cost, 0, start, classes])
    m = ev.mouth()
    EventsTable.insert(ev)
    calendar_update_mouths([m])
    update_mc_count(m)
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
        classes = Event.parse_classes(request.form['classes']) if request.form['classes'] else ''
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
    old_mouth = event.mouth()
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
    if classes:
        event.classes = classes
    EventsTable.update(event)
    new_mouth = event.mouth()
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
def delete_event():
    try:
        id = int(request.form['id'])
    except Exception:
        return render_template(TEMPLATE, error_delete_event='Поля заполнены не правильно', **params())

    event = EventsTable.select(id)
    if event.__is_none__:
        return render_template(TEMPLATE, error_delete_event='Не верный ID события', **params())
    EventsTable.delete(event)
    m = event.mouth()
    calendar_update_mouths([m])
    update_mc_count(m, -1)
    return render_template(TEMPLATE, error_delete_event='Событие удалено', **params())

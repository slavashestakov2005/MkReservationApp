from backend import app
from flask import render_template, request, jsonify
from flask_cors import cross_origin
from flask_login import login_required
from ..help import forbidden_error, unix_time, EventInfo, TinkoffCard, SplitFile, form_add
from ..database import Visitor, VisitorsTable, EventsTable, MasterClassesTable, TeachersTable, YearsTable
from ..config import Config

'''
            TEMPLATE1           Имя шаблона с регистрацией участника.
            TEMPLATE2           Имя шаблона со списком участников.
            get_info(e)         Получает описание события.
            is_closing(e)       Проверяет, что до события ещё осталось время.
    /visitors                   Пересылает на страницу регистрации на событие.
    /add_visitor                Регистрирует участника на событие.
    /show_visitors              Пересылает на страницу со списком зарегистрированных.
    /update_visitors            Обновляет статусы участников события.
    /visitors_count             Возвращает json: {'status': 'OK', 'value': <кол-во свободных мест>}.
    /t_success + /t_fail        Обновляет статус переданного участника.
'''


TEMPLATE1, TEMPLATE2 = 'visitors.html', 'show_visitors.html'


def get_info(event: int):
    event = EventsTable.select(event)
    if event.__is_none__:
        return None, None
    mc = MasterClassesTable.select(event.master_class)
    if mc.__is_none__:
        return None, None
    teacher = TeachersTable.select(event.teacher)
    if teacher.__is_none__:
        return None, None
    return event, EventInfo(event, mc, teacher)


def is_closing(event: int):
    return unix_time() + Config.EVENT_CLOSING > event.start


@app.route('/visitors')
@cross_origin()
def visitors():
    try:
        event = int(request.args.get('event'))
    except Exception:
        return forbidden_error()

    ev, info = get_info(event)
    if info is None:
        return render_template(TEMPLATE1)
    if info.places <= info.booked:
        return render_template(TEMPLATE1, msg='Все места уже заняты :(')
    if is_closing(ev):
        return render_template(TEMPLATE1, msg='Запись уже закончилась :(')
    return render_template(TEMPLATE1, event=ev, info=info)


@app.route('/add_visitor', methods=['POST'])
@cross_origin()
@form_add(VisitorsTable)
def add_visitor(row):
    try:
        row.event = int(request.form['event'])
    except Exception:
        return forbidden_error()
    ev, info = get_info(row.event)
    if info is None:
        return render_template(TEMPLATE1)
    if row.__is_none__:
        return render_template(TEMPLATE1, event=ev, info=info, error_add_visitor='Поля заполнены не правильно')
    row.status, row.payment, row.time = Visitor.SIGN_UP, -1, unix_time()
    if is_closing(ev):
        return render_template(TEMPLATE1, event=ev, info=info, error_add_visitor='Запись уже закончилась')
    if not VisitorsTable.select_by_data(row).__is_none__:
        return render_template(TEMPLATE1, event=ev, info=info, error_add_visitor='Такой ребёнок уже зарегистрирован')
    if info.places <= info.booked:
        return render_template(TEMPLATE1, event=ev, info=info, error_add_visitor='Все места заняты')
    if not ev.can_visit(row.vclass):
        return render_template(TEMPLATE1, event=ev, info=info, error_add_visitor='Такому классу нельзя записаться')
    VisitorsTable.insert(row)
    row = VisitorsTable.select_by_data(row)
    desc = 'Событие: {} Ребёнок: {} {} {}'.format(info.receipt_description(), row.name1, row.name2, row.vclass)
    error, url, payment = TinkoffCard.receipt(info.cost, row.id, desc)
    if error != '0':
        row.status = Visitor.ERROR
        VisitorsTable.update(row)
        return render_template(TEMPLATE1, event=ev, info=info, error_add_visitor='Ошибка :(')
    row.payment = payment
    VisitorsTable.update(row)
    info.booked += 1
    ev.booked += 1
    EventsTable.update(ev)
    return render_template(TEMPLATE1, event=ev, info=info, url=url, error_add_visitor='Ребёнок зарегистрирован')


@app.route('/show_visitors')
@login_required
@cross_origin()
def show_visitors():
    try:
        event = int(request.args.get('event'))
    except Exception:
        return forbidden_error()

    ev, info = get_info(event)
    if info is None:
        return render_template(TEMPLATE2)
    return render_template(TEMPLATE2, data=VisitorsTable.select_by_event(info.id), event=ev, info=info)


@app.route('/update_visitors')
@cross_origin()
def update_visitors():
    try:
        event = int(request.args.get('id'))
    except Exception:
        return forbidden_error()

    ev, info = get_info(event)
    ev_update, new_visitors, new_revenue = False, 0, 0
    if info is None:
        return render_template(TEMPLATE2)
    date = ev.date().split('.')
    y, m = int(date[0]), int(date[1]) - 1
    year = YearsTable.select(y)
    old_visitors, old_revenue = year.get_visitors(m) - ev.revenue // ev.cost, year.get_revenue(m) - ev.revenue
    visitors = VisitorsTable.select_by_event(ev.id)
    for visitor in visitors:
        error, status = TinkoffCard.get_state(visitor.payment)
        status = TinkoffCard.get_status(status)
        if status and status != visitor.status:
            visitor.status = status
            VisitorsTable.update(visitor)
        if visitor.status == Visitor.PAID:
            new_visitors += 1
            new_revenue += ev.cost
        if visitor.status == Visitor.SIGN_UP and unix_time() - visitor.time > Config.EXPIRE_TIME:
            visitor.status = Visitor.NOT_PAID
            VisitorsTable.update(visitor)
            ev.booked -= 1
            ev_update = True
    if ev.revenue != new_revenue:
        ev.revenue = new_revenue
        ev_update = True
    if ev_update:
        EventsTable.update(ev)
        year.set_visitors(m, old_visitors + new_visitors)
        year.set_revenue(m, old_revenue + new_revenue)
        YearsTable.update(year)
        f = SplitFile(Config.TEMPLATES_FOLDER + '/' + str(y) + '/main.html')
        f.insert_after_comment(' {}-{} '.format(m + 1, 'visitors'), str(year.get_visitors(m)))
        f.insert_after_comment(' {}-{} '.format(m + 1, 'revenue'), str(year.get_revenue(m)))
        f.save_file()
    return render_template(TEMPLATE2, data=VisitorsTable.select_by_event(info.id), event=ev, info=info)


@app.route('/visitors_count')
@cross_origin()
def visitors_count():
    try:
        event = int(request.args.get('id'))
    except Exception:
        return forbidden_error()

    event = EventsTable.select(event)
    if event.__is_none__:
        return forbidden_error()
    return jsonify({'status': 'OK', 'value': event.places - event.booked, 'closing': is_closing(event)})


@app.route('/t_success')
@app.route('/t_fail')
@cross_origin()
def tinkoff():
    try:
        visitor_id = int(request.args.get('id'))
    except Exception:
        return forbidden_error()

    visitor = VisitorsTable.select(visitor_id)
    if visitor.__is_none__:
        return forbidden_error()
    old_status = visitor.status
    error, status = TinkoffCard.get_state(visitor.payment)
    if status in Config.PAID_STATES:
        visitor.status = Visitor.PAID
    elif status in Config.NOT_PAID_STATES:
        visitor.status = Visitor.NOT_PAID
    new_status = TinkoffCard.get_status(status)
    ev, info = get_info(visitor.event)
    if info is None:
        return forbidden_error()
    if new_status and old_status != new_status:
        visitor.status = new_status
        VisitorsTable.update(visitor)
        if new_status == Visitor.NOT_PAID:
            ev.blocked -= 1
            EventsTable.update(ev)
    return render_template(TEMPLATE1, event=ev, info=info, msg=visitor.get_status())

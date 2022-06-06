from backend import app
from flask import render_template, request, jsonify
from flask_cors import cross_origin
from ..help import forbidden_error, empty_checker
from ..database import Visitor, VisitorsTable, EventsTable
'''
                        TEMPLATE1           Имя шиблона с регистрацией участника.
                        TEMPLATE2           Имя шиблона со списком участников.
                        gen_url(v)          Генерирует ссылку на оплату.
    /visitors           visitors()          Пересылает на страницу регистрации.
    /add_visitor        add_visitor()       Регистрирует участника на событие.
    /show_visitors      edit_user()         Пересылает на страницу со списком зарегистрированных.
    /visitors_count     visitors_count()    Возвращает json: {'status': 'OK', 'value': <кол-во свободных мест>}.
'''


TEMPLATE1, TEMPLATE2 = 'visitors.html', 'show_visitors.html'


def gen_url(visitor):
    return 'http://example.com?visitor={}'.format(visitor)


@app.route('/visitors')
@cross_origin()
def visitors():
    try:
        event = int(request.args.get('event'))
    except Exception:
        return forbidden_error()

    event = EventsTable.select(event)
    if event.__is_none__:
        return render_template(TEMPLATE1)
    if event.places <= len(VisitorsTable.select_by_event(event.id)):
        return render_template(TEMPLATE1)
    return render_template(TEMPLATE1, event=event)


@app.route('/add_visitor', methods=['POST'])
@cross_origin()
def add_visitor():
    try:
        event = int(request.form['event'])
    except Exception:
        return forbidden_error()
    event = EventsTable.select(event)
    if event.__is_none__:
        return render_template(TEMPLATE1)
    try:
        name1 = request.form['name1']
        name2 = request.form['name2']
        cls = request.form['class']
        empty_checker(name1, name2, cls)
    except Exception:
        return render_template(TEMPLATE1, event=event, error_add_visitor='Поля заполнены не правильно')

    visitor = Visitor([None, event.id, name1, name2, cls, Visitor.SIGN_UP])
    if not VisitorsTable.select_by_data(visitor).__is_none__:
        return render_template(TEMPLATE1, event=event, error_add_visitor='Такой ребёнок уже зарегистрирован')
    if event.places <= len(VisitorsTable.select_by_event(event.id)):
        return render_template(TEMPLATE1, event=event, error_add_visitor='Все места заняты')
    VisitorsTable.insert(visitor)
    visitor = VisitorsTable.select_by_data(visitor)
    return render_template(TEMPLATE1, event=event, url=gen_url(visitor.id), error_add_visitor='Ребёнок зарегистрирован')


@app.route('/show_visitors')
@cross_origin()
def show_visitors():
    try:
        event = int(request.args.get('event'))
    except Exception:
        return forbidden_error()

    event = EventsTable.select(event)
    if event.__is_none__:
        return render_template(TEMPLATE2)
    return render_template(TEMPLATE2, data=VisitorsTable.select_by_event(event.id), event=event)


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
    return jsonify({'status': 'OK', 'value': event.places - len(VisitorsTable.select_by_event(event.id))})

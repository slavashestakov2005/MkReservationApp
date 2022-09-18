from backend import app
from flask import render_template
from flask_cors import cross_origin
from jinja2 import TemplateNotFound
from ..help import not_found_error
from ..database import EventsTable, MasterClassesTable, TeachersTable
'''
            index_params()      Параметры главного шаблона.
            teacher_params()    Параметры шаблона с учителями.
    / + /index.html             Возвращает главную страницу.
    /Info/teachers.html         Возвращает страницу с учителями.
    /<path>                     Возвращает страницу или файл.
'''


def index_params():
    events = EventsTable.select_all()
    mc = {_.id: _ for _ in MasterClassesTable.select_all()}
    return {'events': events, 'mc': mc}


def teacher_params():
    return {'teachers': TeachersTable.select_all()}


@app.route('/index.html')
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html', **index_params())


@app.route('/Info/teachers.html')
@cross_origin()
def teachers():
    return render_template('Info/teachers.html', **teacher_params())


@app.route('/<path:path>')
@cross_origin()
def static_file(path):
    parts = [x.lower() for x in path.rsplit('.', 1)]
    try:
        if len(parts) >= 2 and parts[1] == 'html':
            return render_template(path)
        return app.send_static_file(path)
    except TemplateNotFound:
        return not_found_error()

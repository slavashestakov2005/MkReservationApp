from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from jinja2 import TemplateNotFound
from ..help import not_found_error, forbidden_error, EventPopup
'''
    /               index()             Возвращает стартовую страницу.
    /<path>         static_file(path)   Возвращает страницу или файл.
    /event_popup    event_popup()       Возвращает описание события.
'''


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


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


@app.route('/event_popup')
@cross_origin()
def event_popup():
    try:
        event = EventPopup(int(request.args.get('id')))
    except Exception:
        return forbidden_error()
    return render_template('event.html', obj=event)

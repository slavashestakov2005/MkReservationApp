import os
import re
from datetime import datetime
from flask import render_template, request
from .splithtml import SplitFile
from ..config import Config


def start_debug():
    os.environ["FLASK_DEBUG"] = "1"


def stop_debug():
    os.environ["FLASK_DEBUG"] = "0"


def correct_new_line(s: str):
    return re.sub(r'[\n\r](\s*[\n\r])*', r'\n', s.strip())


def correct_template(template, **data):
    s = render_template(template, **data)
    return correct_new_line(s)


def empty_checker(*args):
    for x in args:
        if not x or not len(x):
            raise ValueError


FILES_TEMPLATE = '''{{% extends "page2.html" %}}
{{% block content %}}
{}
{{% endblock %}}
'''


def save_template(template, filename, head_size=3, **data):
    s = correct_template(template, **data).split('\n')
    t = FILES_TEMPLATE.format('\n'.join(s))
    with open(filename, 'w', encoding='UTF-8') as f:
        f.write(t)


def edit_template(template, comment, example, **data):
    s = correct_template(example, **data)
    f = SplitFile(Config.TEMPLATES_FOLDER + '/' + template)
    f.insert_after_comment(comment, '\n' + s + '\n')
    f.save_file()


MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
         'Декабрь']


def mouth_name(month):
    return MONTH[month]


def unix_time():
    return int(datetime.now().timestamp())


def current_mouth():
    return list(map(int, datetime.now().strftime('%Y.%m').split('.')))


def generate_filename(old_name, new_name, folder=''):
    parts = [x.lower() for x in old_name.rsplit('.', 1)]
    if len(parts) < 2 or parts[1] not in Config.ALLOWED_EXTENSIONS:
        return None
    tail = new_name + '.' + parts[1]
    return Config.UPLOAD_FOLDER + '/Images/' + folder + tail, folder + tail


def parse_checkbox(new_filename, default_filename, folder='', form_checkbox='is_file',
                   form_file='file-file', form_name='file-name'):
    if request.form.get(form_checkbox) is not None:
        file = request.files[form_file]
        file_name, tail = generate_filename(file.filename, str(new_filename), folder)
        file.save(file_name)
        return tail
    tail = request.form[form_name]
    return tail or default_filename

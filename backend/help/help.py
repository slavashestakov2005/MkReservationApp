import os
import re
from datetime import datetime
from flask import render_template
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
{{% block header %}}
{}
{{% endblock %}}

{{% block content %}}
{}
{{% endblock %}}
'''


def save_template(template, filename, head_size=3, **data):
    s = correct_template(template, **data).split('\n')
    t = FILES_TEMPLATE.format('\n'.join(s[:head_size]), '\n'.join(s[head_size:]))
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

from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required
from ..help import parse_checkbox, form_add, form_edit, form_delete, copy_fields
from ..database import TeachersTable, Teacher
'''
            TEMPLATE        Имя шаблона с настройкой пользователей.
            params()        Постоянные параметры этого шаблона.
    /users                  Пересылает на страницу с этим шаблоном.
    /add_user               Создаёт пользователя.
    /edit_user              Редактирует пользователя.
    /delete_user            Удаляет пользователя.
'''


TEMPLATE = 'settings_users.html'


def params():
    return {'users': TeachersTable.select_all()}


@app.route("/users")
@cross_origin()
@login_required
def users():
    return render_template(TEMPLATE, **params())


@app.route("/add_user", methods=['POST'])
@cross_origin()
@login_required
@form_add(TeachersTable)
def add_user(row):
    if row.__is_none__:
        return render_template(TEMPLATE, error_add_user='Поля заполнены не правильно', **params())
    if not TeachersTable.select_by_login(row.login).__is_none__:
        return render_template(TEMPLATE, error_add_user='Такой логин занят', **params())
    row.set_password(row.password)
    TeachersTable.insert(row)
    row = TeachersTable.select_last()
    row.file = parse_checkbox(row.id, 'face.png', folder='Teacher/')
    TeachersTable.update(row)
    return render_template(TEMPLATE, error_add_user='Пользователь добавлен', **params())


@app.route("/edit_user", methods=['POST'])
@cross_origin()
@login_required
@form_edit(TeachersTable)
def edit_user(old_row, new_row):
    try:
        password1 = request.form['password1']
        password2 = request.form['password2']
        password3 = request.form['password3']
    except Exception:
        new_row = Teacher([])
    if new_row.__is_none__:
        return render_template(TEMPLATE, error_edit_user='Поля заполнены не правильно', **params())
    if old_row.__is_none__:
        return render_template(TEMPLATE, error_edit_user='Не верный ID пользователя', **params())
    if password1 and not old_row.check_password(password1):
        return render_template(TEMPLATE, error_edit_user='Не верный пароль', **params())
    if password2 != password3:
        return render_template(TEMPLATE, error_edit_user='Новые пароли не совпадают', **params())
    new_row = copy_fields(new_row, old_row)
    if password1 and password2:
        new_row.set_password(password2)
    new_row.file = parse_checkbox(new_row.id, new_row.file, folder='Teacher/')
    TeachersTable.update(new_row)
    return render_template(TEMPLATE, error_edit_user='Пользователь изменён', **params())


@app.route("/delete_user", methods=['POST'])
@cross_origin()
@login_required
@form_delete(TeachersTable)
def delete_user(row):
    if row.__is_none__:
        return render_template(TEMPLATE, error_delete_user='Не верный ID пользователя', **params())
    TeachersTable.delete(row)
    return render_template(TEMPLATE, error_delete_user='Пользователь удалён', **params())

from backend import app, login
from flask import render_template, redirect, request
from flask_cors import cross_origin
from flask_login import current_user, login_user, logout_user, login_required
from ..help import empty_checker, parse_checkbox
from ..database import TeachersTable, Teacher
'''
    /login          login()             Вход пользователя.
    /logout         logout()            Выход пользователя.
                    TEMPLATE            Имя шиблона с настройкой пользователей.
                    params()            Постоянные параметры этого шаблона.
    /users          users()             Пересылает на страницу с этим шаблоном.
    /add_user       add_user()          Создаёт пользователя.
    /edit_user      edit_user()         Редактирует пользователя.
    /delete_user    delete_user()       Удаляет пользователя.
'''


@login.user_loader
def load_user(id):
    return TeachersTable.select(int(id))


@app.route("/login", methods=['GET', 'POST'])
@cross_origin()
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        try:
            user_login = request.form['login']
            user_password = request.form['password']
            empty_checker(user_login, user_password)
        except Exception:
            return render_template('login.html', error='Некорректные данные')

        u = TeachersTable.select_by_login(user_login)
        if not u.__is_none__ and u.check_password(user_password):
            login_user(u)
            return redirect('/')
        else:
            return render_template('login.html', error='Пользователя с логином {0} и паролем {1} не существует'
                                   .format(user_login, user_password))
    return render_template('login.html')


@app.route("/logout")
@cross_origin()
def logout():
    logout_user()
    return render_template('index.html')


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
def add_user():
    try:
        name1 = request.form['name1']
        name2 = request.form['name2']
        name3 = request.form['name3']
        u_login = request.form['login']
        password = request.form['password']
        empty_checker(name1, name2, name3, u_login, password)
    except Exception:
        return render_template(TEMPLATE, error_add_user='Поля заполнены не правильно', **params())

    if not TeachersTable.select_by_login(u_login).__is_none__:
        return render_template(TEMPLATE, error_add_user='Такой логин занят', **params())
    teacher = Teacher([None, name1, name2, name3, u_login, password, ''])
    teacher.set_password(password)
    TeachersTable.insert(teacher)
    teacher = TeachersTable.select_last()
    teacher.file = parse_checkbox(teacher.id, 'face.png', folder='Teacher/')
    TeachersTable.update(teacher)
    return render_template(TEMPLATE, error_add_user='Пользователь добавлен', **params())


@app.route("/edit_user", methods=['POST'])
@cross_origin()
@login_required
def edit_user():
    try:
        id = int(request.form['id'])
        name1 = request.form['name1']
        name2 = request.form['name2']
        name3 = request.form['name3']
        password1 = request.form['password1']
        password2 = request.form['password2']
        password3 = request.form['password3']
    except Exception:
        return render_template(TEMPLATE, error_edit_user='Поля заполнены не правильно', **params())

    teacher = TeachersTable.select(id)
    if teacher.__is_none__:
        return render_template(TEMPLATE, error_edit_user='Не верный ID пользователя', **params())
    if password1 and not teacher.check_password(password1):
        return render_template(TEMPLATE, error_edit_user='Не верный пароль', **params())
    if password2 != password3:
        return render_template(TEMPLATE, error_edit_user='Новые пароли не совпадают', **params())
    if name1:
        teacher.name1 = name1
    if name2:
        teacher.name2 = name2
    if name3:
        teacher.name3 = name3
    if password1 and password2:
        teacher.set_password(password2)
    teacher.file = parse_checkbox(teacher.id, teacher.file, folder='Teacher/')
    TeachersTable.update(teacher)
    return render_template(TEMPLATE, error_edit_user='Пользователь изменён', **params())


@app.route("/delete_user", methods=['POST'])
@cross_origin()
@login_required
def delete_user():
    try:
        id = int(request.form['id'])
    except Exception:
        return render_template(TEMPLATE, error_delete_user='Поля заполнены не правильно', **params())

    teacher = TeachersTable.select(id)
    if teacher.__is_none__:
        return render_template(TEMPLATE, error_delete_user='Не верный ID пользователя', **params())
    TeachersTable.delete(teacher)
    return render_template(TEMPLATE, error_delete_user='Пользователь удалён', **params())

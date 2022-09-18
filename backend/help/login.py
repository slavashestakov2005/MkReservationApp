from backend import login, app
from flask import redirect, request, render_template
from flask_login import current_user, login_user, logout_user, login_required
from flask_cors import cross_origin
from ..help import empty_checker
from ..database import TeachersTable
'''
            TEMPLATE        Страница входа на сайт.
    /load_user              Загружает пользователя.
    /login                  Вход пользователя.
    /logout                 Выход пользователя.
'''


TEMPLATE = 'login.html'


@login.user_loader
def load_user(_id):
    return TeachersTable.select(int(_id))


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
            return render_template(TEMPLATE, error='Некорректные данные')

        u = TeachersTable.select_by_login(user_login)
        if not u.__is_none__ and u.check_password(user_password):
            login_user(u)
            return redirect('/')
        else:
            return render_template(TEMPLATE, error='Пользователя с логином {0} и паролем {1} не существует'
                                   .format(user_login, user_password))
    return render_template(TEMPLATE)


@app.route("/logout")
@cross_origin()
@login_required
def logout():
    logout_user()
    return redirect('/')

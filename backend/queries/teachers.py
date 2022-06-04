from backend import app, login
from flask import render_template, redirect, request
from flask_cors import cross_origin
from flask_login import current_user, login_user, logout_user
from ..help import empty_checker
from ..database import TeachersTable
'''
    /login          login()             Вход пользователя.
    /logout         logout()            Выход пользователя.
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

from backend import app
from flask import render_template, request
from flask_cors import cross_origin
from flask_login import login_required
from os import makedirs, path, remove
from shutil import rmtree
from ..config import Config
from ..database import YearsTable, Year
from ..help import YearInfo, save_template, edit_template, CalendarUpdater, form_add, form_delete
'''
            [[maybe_unused]]
            TEMPLATE                    Имя шаблона с настройкой пользователей.
            update_pages_()             Обновляет списки годов.
            update_years_(y, o, n)      Обновляет годовые файлы.
            create_year_(year)          Создаёт годовые файлы.
            delete_year_(year)          Удаляет годовые файлы.
            params()                    Постоянные параметры этого шаблона.
    /calendar                           Пересылает на страницу с этим шаблоном.
    /add_year                           Создаёт год.
    /edit_year                          Редактирует все годы.
    /delete_year                        Удаляет год.
'''


TEMPLATE = 'settings_calendar.html'


def update_pages_():
    years = YearsTable.select_all()
    edit_template('page1.html', ' list of months (1) ', 'template_page.html', years=years, cnt=0)
    edit_template('page2.html', ' list of months (2) ', 'template_page.html', years=years, cnt=1)


def update_years_(years: list, old: list, new: list):
    mp = {_.year: _ for _ in new}
    for year in years:
        if year not in mp:
            break
        directory = path.join(Config.TEMPLATES_FOLDER, str(year))
        y = YearInfo(mp[year])
        save_template('template_year.html', directory + '/main.html', info=y)
        for i in range(1, 13):
            cur_file = directory + '/{}.html'.format(i)
            if path.exists(cur_file) and not mp[year].exists(i - 1):
                remove(cur_file)
    updater = CalendarUpdater()
    updater.parse_mouths(old, new)
    updater.update()


def create_year_(year: int, old: list):
    directory = path.join(Config.TEMPLATES_FOLDER, str(year))
    makedirs(directory)
    update_years_([year], old, YearsTable.select_all())
    update_pages_()


def delete_year_(year: int, old: list):
    directory = path.join(Config.TEMPLATES_FOLDER, str(year))
    rmtree(directory)
    update_years_([year], old, YearsTable.select_all())
    update_pages_()


def params():
    return {'years': YearsTable.select_all()}


@app.route("/calendar")
@cross_origin()
@login_required
def calendar():
    return render_template(TEMPLATE, **params())


@app.route("/add_year", methods=['POST'])
@cross_origin()
@login_required
@form_add(YearsTable)
def add_year(row):
    if row.__is_none__:
        return render_template(TEMPLATE, error_add_year='Поля заполнены не правильно', **params())
    if not YearsTable.select(row.year).__is_none__:
        return render_template(TEMPLATE, error_add_year='Такой год уже есть', **params())
    if row.year < 2022 or row.year > 2100:
        return render_template(TEMPLATE, error_add_year='Такой год создать нельзя', **params())
    row = Year([row.year, Year.ALL_MONTHS, Year.ZERO12, Year.ZERO12, Year.ZERO12])
    old = YearsTable.select_all()
    YearsTable.insert(row)
    create_year_(row.year, old)
    return render_template(TEMPLATE, error_add_year='Год добавлен', **params())


@app.route("/edit_year", methods=['POST'])
@cross_origin()
@login_required
def edit_year():
    try:
        months = request.form.getlist('months')
    except Exception:
        return render_template(TEMPLATE, error_edit_year='Поля заполнены не правильно', **params())

    year_data = {}
    for now in months:
        y, m = map(int, now.split('-'))
        if y not in year_data:
            year_data[y] = []
        year_data[y].append(m - 1)
    years = YearsTable.select_all()
    old = [_.copy() for _ in years]
    need_update = []
    for year in years:
        old_months = year.months
        months = year_data[year.year] if year.year in year_data else []
        new_mouths = year.set_months(months)
        if old_months != new_mouths:
            YearsTable.update(year)
            need_update.append(year.year)
    update_years_(need_update, old, years)
    return render_template(TEMPLATE, error_edit_year='Месяцы сохранены', **params())


@app.route("/delete_year", methods=['POST'])
@cross_origin()
@login_required
@form_delete(YearsTable)
def delete_year(row):
    if row.__is_none__:
        return render_template(TEMPLATE, error_delete_year='Поля заполнены не правильно', **params())
    old = YearsTable.select_all()
    YearsTable.delete(row)
    delete_year_(row.year, old)
    return render_template(TEMPLATE, error_delete_year='Год удалён', **params())

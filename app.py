from flask import Flask, render_template, request, redirect, g, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from templates.forms.employees.register import *
from templates.forms.employees.auth import *
from templates.forms.tasks.edit import *
from templates.forms.tasks.create import *
from templates.forms.tasks.report import *
from user_login import *
from db import *
import psycopg2

import sys
sys.dont_write_bytecode = True

app = Flask(__name__)
app.config['SECRET_KEY'] = "9d3fc4c15037cf54e9e6ca948d99dda7f1823d1d"
login_manager = LoginManager(app)
login_manager.login_view = "employees_auth"
login_manager.login_message = "Авторизируйтесь для доступа ко всем страницам"
login_manager.login_message_category = "danger"

print(generate_password_hash("333"))

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, db)

@app.route("/")
def index():
    return redirect(url_for("tasks"))

@app.route("/tasks")
@login_required
def tasks():
    tasks = db.get_user_tasks(current_user.get_id())
    return render_template("tasks/index.html", user=current_user.user, tasks=tasks)

@app.route("/tasks/report", methods=["POST", "GET"])
@login_required
def tasks_report():
    if current_user.user.get("role_title") != "Менеджер":
        return redirect(url_for("tasks"))

    form = TasksReport()

    if form.validate_on_submit() and request.method == "POST":
        report = db.get_tasks_report(form.first_date.data, form.second_date.data)
        return render_template("tasks/report.html", user=current_user.user, form=form, report=report)

    return render_template("tasks/report.html", user=current_user.user, form=form)

@app.route("/tasks/create", methods=["POST", "GET"])
@login_required
def tasks_create():
    form = buildTasksCreate(db)
    if form.validate_on_submit() and request.method == "POST":
        task_id = db.task_create({field.name: field for field in form if field.name not in ["csrf_token", "submit"]}, current_user.get_id())
        flash("Задание добавлено", "success")
        return redirect(url_for("tasks_show", task_id=task_id))
    return render_template("tasks/create.html", user=current_user.user, form=form)

@app.route("/tasks/finish/<int:task_id>", methods=["POST", "GET"])
@login_required
def tasks_finish(task_id):
    if current_user.user.get("role_title") != "Менеджер":
        return redirect(url_for("tasks"))
    task = db.get_user_task_by_id(current_user.get_id(), task_id)
    if not task or task.get("completed"):
        return redirect(url_for("tasks"))
    db.task_finish(task)
    flash("Задание завершено", "success")
    return redirect(url_for("tasks"))

@app.route("/tasks/edit/<int:task_id>", methods=["POST", "GET"])
@login_required
def tasks_edit(task_id):
    if current_user.user.get("role_title") != "Менеджер":
        return redirect(url_for("tasks"))
    task = db.get_user_task_by_id(current_user.get_id(), task_id)
    form = buildTasksEdit(task, db)
    if not task or task.get("completed"):
        return redirect(url_for("tasks"))
    if form.validate_on_submit() and request.method == "POST":
        db.update_task(task_id, {field.name: field for field in form if field.name not in ["csrf_token", "submit"]})
        flash("Задание обновлено", "success")
        return redirect(url_for("tasks_show", task_id=task_id))
    return render_template("tasks/edit.html", user=current_user.user, task=task, form=form)

@app.route("/tasks/<int:task_id>")
@login_required
def tasks_show(task_id):
    task = db.get_user_task_by_id(current_user.get_id(), task_id)
    if not task:
        return redirect(url_for("tasks"))
    return render_template("tasks/show.html", user=current_user.user, task=task)

@app.route("/employees/logout")
@login_required
def employees_logout():
    logout_user()
    flash("Вы вышли из учетной записи", "success")
    return redirect(url_for("employees_auth"))

@app.route("/employees/auth", methods=["POST", "GET"])
def employees_auth():
    if current_user.is_authenticated:
        return redirect(url_for("tasks"))
    form = EmployeesAuth()
    if form.validate_on_submit() and request.method == "POST":
        user = db.get_user_by_email(form.email.data)
        if user and check_password_hash(user.get("password"), form.pswd.data):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(request.args.get("next") or url_for("tasks"))
        flash("Логин или пароль введен неверно", "danger")
    return render_template("employees/auth.html", form=form)

@app.route("/employees/register", methods=["POST", "GET"])
def employees_register():
    if current_user.is_authenticated:
        return redirect(url_for("tasks"))
    form = EmployeesRegister()
    if form.validate_on_submit() and request.method == "POST":
        if db.get_user_by_email(form.email.data):
            form.email.errors.append("Пользователь с данным E-Mail уже зарегистрирован")
        db.register_user({field.name: field for field in form if field.name not in ["csrf_token", "submit"]})
        flash("Пользователь зарегистрирован", "success")
        return redirect(url_for("employees_auth"))
    return render_template("employees/register.html", form=form)

db = None
@app.before_request
def before_request():
    global db
    db = DB(get_db())

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

def connect_db():
    return psycopg2.connect("dbname=Labs user=postgres password=1234 host=localhost")

def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db

if __name__ == "__main__":
    app.run(debug=True)
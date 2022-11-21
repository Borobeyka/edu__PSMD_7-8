from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, SelectField
from wtforms.validators import Length, DataRequired

def buildTasksCreate(db):
    class TasksCreate(FlaskForm):
        title = StringField("Название:", validators=[DataRequired(), Length(4, 32, "Минимальная и максимальная длина задания 4 и 32 символа соответственно")])
        planned_date = DateField("Плановая дата завершения:", validators=[DataRequired()])
        executor_id = SelectField("Исполнитель:", choices=[(executor.get("id"), executor.get("name") + " " + executor.get("surname")) for executor in db.get_all_employees()])
        client_id = SelectField("Клиент:", choices=[(client.get("id"), client.get("name") + " " + client.get("surname")) for client in db.get_all_clients()])
        priority_id = SelectField("Приоритет:", choices=[(priority.get("id"), priority.get("priority")) for priority in db.get_all_task_priority()])
        type_id = SelectField("Тип задания:", choices=[(type.get("id"), type.get("type")) for type in db.get_all_task_types()])
        submit = SubmitField("Создать задание", render_kw={"class": "btn btn-primary"})
    return TasksCreate()
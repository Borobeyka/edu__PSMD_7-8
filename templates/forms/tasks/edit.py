from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, SelectField
from wtforms.validators import Email, Length, DataRequired

def buildTasksEdit(data, db):
    class TasksEdit(FlaskForm):
        title = StringField("Название:", default=data.get("title"), validators=[DataRequired()])
        start_date = DateField("Дата начала:", default=data.get("start_date"), validators=[DataRequired()])
        planned_date = DateField("Плановая дата завершения:", default=data.get("planned_date"), validators=[DataRequired()])
        executor_id = SelectField("Исполнитель:", default=data.get("executor_id"), choices=[(executor.get("id"), executor.get("name") + " " + executor.get("surname")) for executor in db.get_all_employees()])
        priority_id = SelectField("Приоритет:", default=data.get("priority_id"), choices=[(priority.get("id"), priority.get("priority")) for priority in db.get_all_task_priority()])
        type_id = SelectField("Тип задания:", default=data.get("type_id"), choices=[(type.get("id"), type.get("type")) for type in db.get_all_task_types()])
        submit = SubmitField("Сохранить изменения", render_kw={"class": "btn btn-primary"})
    return TasksEdit()
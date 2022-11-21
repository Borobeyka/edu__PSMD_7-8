from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, SelectField
from wtforms.validators import Length, DataRequired

class TasksReport(FlaskForm):
    first_date = DateField("С:", validators=[DataRequired()])
    second_date = DateField("По:", validators=[DataRequired()])
    submit = SubmitField("Сформировать отчет", render_kw={"class": "btn btn-primary"})
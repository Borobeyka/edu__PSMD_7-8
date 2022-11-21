from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Email, Length, EqualTo, NumberRange

class EmployeesAuth(FlaskForm):
    email = StringField("Email:", validators=[Email("E-Mail введен неверно")])
    pswd = PasswordField("Пароль:", validators=[Length(4, 32, "Пароль не может быть короче 4 и б")])
    submit = SubmitField("Войти", render_kw={"class": "btn btn-primary"})
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Email, Length, EqualTo, NumberRange

class EmployeesRegister(FlaskForm):
    name = StringField("Имя:", validators=[Length(2, 32, "Имя не может быть короче 2 и более 32 символов")])
    surname = StringField("Фамилия:", validators=[Length(4, 64, "Фамилия не может быть короче 4 и более 64 символов")])
    phone = StringField("Телефон:", validators=[Length(11, 11, "Телефон введен неверно. Длина номера должна быть 11 символов")])
    email = StringField("Email:", validators=[Email("E-Mail введен неверно")])
    pswd = PasswordField("Пароль:", validators=[Length(4, 32, "Пароль не может быть короче 4 и более 32 символов")])
    cfm_pswd = PasswordField("Повторите пароль", validators=[EqualTo("pswd", "Введенные пароли не совпадают")])
    address = StringField("Адрес:", validators=[Length(8, 128, "Адрес не может быть короче 8 и более 128 символов")])
    company = SelectField("Компания:", choices=[(-1, "Выберите компанию"), (1, "Компания #1"), (2, "Компания #2")])
    role = SelectField("Должность:", choices=[(-1, "Выберите должность"), (1, "Сотрудник"), (2, "Менеджер")])
    submit = SubmitField("Зарегистрироваться", render_kw={"class": "btn btn-primary"})
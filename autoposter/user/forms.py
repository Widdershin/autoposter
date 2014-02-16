from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, FormField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.orm import model_form
from .models import User, Post, DaysOfWeek
from autoposter.database import db


class RegisterForm(Form):
    username = TextField('Username',
                         validators=[DataRequired(), Length(min=3, max=25)])

    email = TextField('Email', validators=[
        DataRequired(), Email(), Length(min=6, max=40)])

    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=40)])

    confirm = PasswordField('Verify password', [
        DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False

        self.user = user
        return True


DaysOfWeekBaseForm = model_form(
    DaysOfWeek, db_session=db.session, base_class=Form)


class DaysOfWeekForm(DaysOfWeekBaseForm):
    pass


NewPostBaseForm = model_form(Post, db_session=db.session, base_class=Form)


class NewPostForm(NewPostBaseForm):
    body = TextAreaField('Body')
    days = FormField(DaysOfWeekForm)

    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.days.form.csrf_enabled = False

from collections import OrderedDict
from flask_wtf import Form
from wtforms import (TextField, PasswordField, TextAreaField,
                     BooleanField, IntegerField)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.ext.sqlalchemy.orm import model_form
from .models import User, DaysOfWeek
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


class DaysOfWeekForm(Form):
    post_id = None


class DayField(BooleanField):

    def populate_obj(self, obj, name):
        setattr(obj.days, name, self.data)


class NewPostForm(Form):
    title = TextField('Title', validators=[
        DataRequired(), Length(min=3, max=300)])

    subreddit = TextField('Subreddit', validators=[
        DataRequired(), Length(min=3, max=300)])

    distinguish = BooleanField('Distinguish')
    sticky = BooleanField('Sticky')

    scheduled_hour = IntegerField('Hour')
    scheduled_minute = IntegerField('Minute')

    body = TextAreaField('Body', validators=[
        Length(max=10000)])

    monday = DayField('Mon')
    tuesday = DayField('Tue')
    wednesday = DayField('Wed')
    thursday = DayField('Thu')
    friday = DayField('Fri')
    saturday = DayField('Sat')
    sunday = DayField('Sun')

    #days = FormField(DaysOfWeekForm)

    def __init__(self, obj=None, **kwargs):
        super(NewPostForm, self).__init__(obj=obj, **kwargs)
        self.days = OrderedDict([
            ("monday", self.monday), ("tuesday", self.tuesday),
            ("wednesday", self.wednesday), ("thursday", self.thursday),
            ("friday", self.friday), ("saturday", self.saturday),
            ("sunday", self.sunday)
        ])

        if obj:
            for day, other_day in zip(self.days.values(), obj.days):
                day.process_data(other_day)

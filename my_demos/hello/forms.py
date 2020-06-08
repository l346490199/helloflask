#!/bin/python3
#-*- coding: utf-8 -*-
# forms.py
# @author 刘秋
# @email lq@aqiu.info
# @description
# @created 2020-05-28T11:35:25.791Z+08:00
# @last-modified 2020-06-08T13:06:55.264Z+08:00
#

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, Length


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class LoginForm(MyBaseForm):
    username = StringField('Username',
                    validators=[DataRequired()],
                    render_kw={'placeholder': "Your Username"})
    password = PasswordField("password",
                    validators=[DataRequired(),
                                Length(8, 128)],
                    render_kw={'placeholder': "Your Password"})
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class UploadForm(MyBaseForm):
    photo = FileField('Upload Image',
                validators=[
                    FileRequired(),
                    FileAllowed(['jpg', 'jpeg', 'png', 'gif'])
                ])
    submit = SubmitField()
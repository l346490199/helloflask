#!/bin/python3
#-*- coding: utf-8 -*-
# forms.py
# @author 刘秋
# @email lq@aqiu.info
# @description
# @created 2020-05-28T11:35:25.791Z+08:00
# @last-modified 2020-05-28T11:54:17.736Z+08:00
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],render_kw={'placeholder':"Your Username"})
    password = PasswordField("password",validators=[DataRequired(),Length(8,128)],render_kw={'placeholder':"Your Password"})
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

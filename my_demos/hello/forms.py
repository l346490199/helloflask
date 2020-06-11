#!/bin/python3
#-*- coding: utf-8 -*-
# forms.py
# @author 刘秋
# @email lq@aqiu.info
# @description
# @created 2020-05-28T11:35:25.791Z+08:00
# @last-modified 2020-06-10T15:55:13.036Z+08:00
#

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class LoginForm(MyBaseForm):
    """表格
    """
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
    """上传单个文件
    """
    photo = FileField('Upload Image',
                validators=[
                    FileRequired(),
                    FileAllowed(['jpg', 'jpeg', 'png', 'gif'])
                ])
    submit = SubmitField()


############
# 上传多个文件
from wtforms import MultipleFileField
class MultiUploadForm(FlaskForm):
    """上传多个文件

    Args:
        FlaskForm ([type]): [description]
    """
    photo = MultipleFileField("Upload Image", validators=[DataRequired()])
    submit = SubmitField()
    

###############
# 富文本编辑器
from flask_ckeditor import CKEditorField
class RichTextForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,50)])
    body = CKEditorField("Body",validators=[DataRequired()])
    submit = SubmitField("Publish")
class RichTextForm2(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,50)])
    body = CKEditorField("Body",validators=[DataRequired()])
    save = SubmitField("Save")
    publish = SubmitField("Publish")
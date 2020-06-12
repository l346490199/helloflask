#!/bin/python3
#-*- coding: utf-8 -*-
# app.py
# @author 刘秋
# @email lq@aqiu.info
# @description
# @created 2020-06-11T10:29:07.161Z+08:00
# @last-modified 2020-06-12T10:52:32.611Z+08:00
#

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired
from flask import Flask, request, render_template, session, redirect, url_for, abort, make_response, flash
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "secret_key")
app.config['WTF_I18N_ENABLED'] = False  # 错误信息中文相关设定
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def __repr__(self):
        return "<Note %r>" % self.body


class NewNoteForm(FlaskForm):
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("seve")


class EditNoteForm(NewNoteForm):
    submit = SubmitField("Update")


class DeleteNoteForm(FlaskForm):
    submit = SubmitField("Delete")


@app.route('/')
def instal():
    form = DeleteNoteForm()
    notes = Note.query.all()
    return render_template("index.html", notes=notes, form=form)


@app.route('/new', methods=["GET", "POST"])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved')
        return redirect(url_for('instal'))
    return render_template("new_note.html", form=form)


@app.route('/edit/<int:note_id>', methods=["GET", "POST"])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash("Your note is update.!")
        return redirect(url_for("instal"))
    form.body.data = note.body
    return render_template('edit_note.html', form=form)


@app.route('/delete_note/<int:note_id>', methods=["GET", "POST"])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash("Your note is Delete.!")
    else:
        abort(400)
    return redirect(url_for("instal"))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Note, Author=Author, Article=Article, 
        Student=Student, Teacher=Teacher, )


import click


@app.cli.command()
@click.option("--drop", is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database.
    """
    if drop:
        click.confirm("This operation will delete the database, do you want to continue?", abort=True)
        db.drop_all()
        click.echo('Drip tables.')
    db.create_all()
    click.echo('Initialized database.')


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20))
    articles = db.relationship("Article")

    def __repr__(self):
        return "<Author %r>" % self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return "<Article %r>" % self.title

# 多对多关系
association_table = db.Table(
    'association',
    db.Column("student_id", db.Integer, db.ForeignKey('student.id')),
    db.Column("teacher_id", db.Integer, db.ForeignKey('teacher.id')))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True) # uniquer->不重复
    grade = db.Column(db.String(20))
    teachers = db.relationship("Teacher",secondary = association_table,
                back_populates='students')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    office = db.Column(db.String(70))
    students = db.relationship("Student", secondary = association_table,
                back_populates='teachers')
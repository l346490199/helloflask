#!/bin/python3
# -*- coding: utf-8 -*-
'''
    author: LiuQiu
'''

from flask import Flask, request, render_template, session, redirect, url_for, abort, make_response, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "secret_key")
app.config['WTF_I18N_ENABLED'] = False  # 错误信息中文相关设定


@app.route('/')
def instal():
    response = make_response(render_template("instal.html"))
    return response


@app.route("/greet/<name>")
@app.route("/greet", defaults={'name': 'Programmer'})  ## 设定name的默认为programmer
def greet(name):
    return render_template('hello.html', name=name)


@app.route('/greet2/<name>')
def greet2(name='world'):
    response = make_response(
        render_template("hello.html", name=name, my_url=[request.referrer]))
    return response


@app.route("/hello", methods=['GET', 'POST'])  # 监听HTTP方法  默认只监听GET
def hello():
    name = request.args.get("name", "Programmer")
    if name == "Programmer":
        name = request.cookies.get('name', 'Programmer')
    response = make_response(
        render_template("hello.html", name=name, my_url=[request.referrer]))
    return response


@app.route('/he')
def he():
    return redirect(url_for('hello'))


@app.route('/goback/<int:year>')
def goback(year):
    return "Welcome to {0}".format(2020 - year)


@app.route("/acc")
def acc():
    return render_template("acc.html")


@app.route('/404')
def not_found():
    abort(404)


@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for("hello")))
    response.set_cookie('name', name)
    return response


###############################################################################
# 表格
@app.route('/html', methods=['GET', "POST"])
def html():
    return render_template("html_form.html")


from forms import LoginForm, UploadForm
from flask import send_from_directory
import uuid


@app.route('/basic', methods=['GET', "POST"])
def basic():
    form = LoginForm()
    # if request.method=="POST" and form.validate():
    if form.validate_on_submit():  # 验证
        username = form.username.data
        flash('Welcome home,{0}'.format(username))
        response = make_response(redirect(url_for('hello')))
        response.set_cookie('name', username)

        return response
    else:
        pass
    return render_template('basic.html', form=form)


# 存储地址
app.config["UPLOAD_PATH"] = os.path.join(app.root_path, "uploads")


#上传文件
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():  # 验证
        f = form.photo.data
        # f.flename获取文件名 random_filename 同一命名
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))  # 存储
        flash('Upload success.')  # 显示短语存储
        session['filenames'] = [filename]  # 在cookie中加密session中存储文件名
        return redirect(url_for('show_images'))
    else:
        pass
    return render_template('upload.html', form=form)


def random_filename(filename):
    """同一命名文件

    Args:
        filename (string): 文件名称

    Returns:
        new_filename(string): [新文件名称]
    """
    ext = os.path.splitext(filename)[1]
    # uuid4 第四版UUID 不接收参数而生成随机UUID
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@app.route('/upload/<path:filename>')
def get_file(filename):
    # send_from_directory 获取文件的函数 传入地址和文件名
    return send_from_directory(app.config["UPLOAD_PATH"], filename)


@app.route('/uploaded-images')
def show_images():
    """显示传入文件的视图

    """
    return render_template('uploaded.html')


# 上传多个文件
from forms import MultiUploadForm
from wtforms import ValidationError  # 验证错误
from flask_wtf.csrf import validate_csrf  # 验证csrf令牌


@app.route('/multi-upload', methods=["GET", "POST"])
def multi_upload():
    form = MultiUploadForm()
    # 检查csrf令牌
    if request.method == 'POST':
        filenames = []
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash("CSRF token error")
            return redirect(url_for('multi_upload'))
        # 检车文件是否存在
        if 'photo' not in request.files:
            flash("This field is required.")

        for f in request.files.getlist("photo"):
            # 检查文件类型
            if f and allowed_file(f.filename):
                filename = random_filename(f.filename)
                f.save(os.path.join(app.config["UPLOAD_PATH"], filename))
                filenames.append(filename)
            else:
                flash("Invalid file type.")
                return redirect(url_for("multi_upload"))
        flash("Upload success.")
        session["filenames"] = filenames
        return redirect(url_for("show_images"))
    return render_template("upload.html", form=form)


app.config["ALLOWED_EXTENSIONS"] = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    """检查文件类型

    """
    return '.' in filename and filename.rsplit(
        ".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


###################################3
# 集成富文本编辑器 Flask-CKEditor
app.config["CKEDITOR_SERVE_LOCAL"] = True

from flask_ckeditor import CKEditor
from forms import RichTextForm, RichTextForm2
ckeditor = CKEditor(app)


@app.route('/two_submits', methods=["GET", "POST"])
def two_submit():
    form = RichTextForm2()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        if form.save.data:
            flash("You click the \"Save\" button. ")
        elif form.publish.data:
            flash('You click the "Publish" button.')
        flash('Your post is published!')
        return render_template('post.html', title=title, body=body)
    return render_template("ckeditor2.html", form=form)


@app.route('/ckeditor', methods=["GET", "POST"])
def ckeditor():
    form = RichTextForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        flash("You post is published!")
        return render_template("post.html", title=title, body=body)
    return render_template("ckeditor.html", form=form)

############################
# 数据库 SQLite Flask_SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL','sqlite:///'+os.path.join(app.root_path,'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

    def __repr__(self):
        return "<Note %r>"% self.body

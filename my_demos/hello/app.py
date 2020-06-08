#!/bin/python3
# -*- coding: utf-8 -*-
'''
    author: LiuQiu
'''

from flask import Flask, request, render_template, redirect, url_for, abort, make_response, flash
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


@app.route('/basic', methods=['GET', "POST"])
def basic():
    form = LoginForm()
    # if request.method=="POST" and form.validate():
    if form.validate_on_submit(): # 验证
        username = form.username.data
        flash('Welcome home,{0}'.format(username))
        response = make_response(redirect(url_for('hello')))
        response.set_cookie('name',username)

        return response
    else:
        pass
    return render_template('basic.html', form=form)


#上传文件
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit(): # 验证
        return redirect(url_for('hello'))
    else:
        pass
    return render_template('upload.html', form=form)

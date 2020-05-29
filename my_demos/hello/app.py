#!/bin/python3
# -*- coding: utf-8 -*-
'''
    author: LiuQiu
'''

from flask import Flask, request, render_template, redirect, url_for, abort,make_response, flash
import os

app = Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY',"secret_key")
app.config['WTF_I18N_ENABLED']=False  # 错误信息中文相关设定

@app.route('/')
def instal():
    return render_template("instal.html")


@app.route("/greet/<name>")
@app.route("/greet", defaults={'name': 'Programmer'})
def greet(name):
    return '<h1>Hello,{0}</h1>'.format(name)


@app.route("/hello", methods=['GET', 'POST'])  # 监听HTTP方法
def hello():
    name = request.args.get("name", "Flask")
    if name == "Flask":
        name = request.cookies.get('name','Flask')
    response = make_response(render_template("hello.html", name=name,my_url=[request.referrer]))
    return response


@app.route('/hello/<name>')
def helloword(name='world'):
    return redirect(url_for("instal"))


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
    response.set_cookie('name',name)
    return response

###############################################################################    
# 表格
@app.route('/html',methods=['GET',"POST"])
def html():
    return render_template("html_form.html")

from forms import LoginForm

@app.route('/basic',methods=['GET',"POST"])
def basic():
    form = LoginForm()
    # if request.method=="POST" and form.validate():
    if form.validate_on_submit():
        username= form.username.data
        flash('Welcome home,{0}'.format(username))
        return redirect(url_for('hello')+'?name={0}'.format(username))
    else:
        pass
    return render_template('basic.html',form=form)
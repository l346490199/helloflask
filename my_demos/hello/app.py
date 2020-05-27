#!/bin/python3
# -*- coding: utf-8 -*-
'''
    author: LiuQiu
'''

from flask import Flask, request, render_template, redirect, url_for, abort,make_response
import os

app = Flask(__name__)
app.secret_key=os.getenv('SECRET_KEY',"secret_key")

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
    response = make_response(render_template("hello.html", name=name))
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


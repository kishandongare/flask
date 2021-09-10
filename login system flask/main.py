from typing import Any, Union

import mysql.connector
from flask import Flask, render_template, request, redirect, session
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(host="localhost", user="root", password="", database="login")
cursor = conn.cursor()


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/home')  # user come over here after login
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])  # we are receive data from user for throug post method
def login_validation():
    email = request.form.get('email')  # received as name and password through get method
    password = request.form.get('password')

    cursor.execute("""SELECT * FROM `login` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,
                                                                                                       password))  # checking this is exist in db or not

    users = cursor.fetchall()
    # main logic only one user is in db
    if len(users) > 0:
        session['username'] = users[0][0]  # session set
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/add_users', methods=['POST'])
def add_user():
    username = request.form.get('username')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute(
        """INSERT INTO `login` (`username`,`name`,`email`,`password`) VALUES('{}','{}','{}','{}')""".format(username, name, email, password))
    conn.commit()
    # i am also want to user session can start after registration
    # fetch from db
    cursor.execute(""" SELECT * FROM `login` WHERE `email` LIKE '{}'""".format(email))
    users = cursor.fetchall()
    session['username'] = users[0][0]
    return redirect('/home')


@app.route('/logout')  # for logout
def logout():
    session.pop('username')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

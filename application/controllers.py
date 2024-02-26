from flask import Flask, render_template, redirect, request 
from flask import current_app as app
from .models import *

# http://127.0.0.1:5000/  base url
# http://127.0.0.1:5000/userlogin 


# @app.route('/')
# def something():

@app.route('/userlogin', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        u_name = request.form.get("u_name")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username = u_name).first() # or .all()
        if this_user:
            if this_user.password == pwd:
                return render_template("user_dash.html", u_name = u_name) 
            else:
                return "incorrect Password"
        else:
            return "user does not exist!"
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        u_name = request.form.get("u_name")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(username = u_name).first()
        if this_user:
            return "user already exists!"
        else:
            new_user = User(username = u_name, password = pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin') 
    return render_template('register.html')



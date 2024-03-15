from flask import Flask, render_template, redirect, request 
from flask import current_app as app
from .models import *
import datetime

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
                if this_user.type == "admin":
                    return redirect('/admin')
                else:
                    return redirect(f'/user/{this_user.id}') 
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

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    admin = User.query.filter_by(type = "admin").first()
    requested_trans = Transaction.query.filter_by(internal_status = "requested").all()
    quoted_trans = Transaction.query.filter_by(internal_status = "quoted").all()
    paid_trans = Transaction.query.filter_by(internal_status = "paid").all()
    return render_template("admin_dash.html", requested_trans = requested_trans,
                                              quoted_trans = quoted_trans,
                                              paid_trans = paid_trans)

@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):
    user = User.query.get(user_id)
    transactions = user.trans
    return render_template('user_dash.html', user = user, transactions = transactions)

@app.route('/transaction_create/<int:user_id>', methods=['GET', 'POST'])
def trans_create(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        t_name = request.form.get('t_name')
        t_type = request.form.get('t_type')
        s_city = request.form.get('s_city')
        d_city = request.form.get('d_city')
        description = request.form.get('description')
        new_trans = Transaction(t_name = t_name, t_type = t_type, t_date = datetime.datetime.now(), s_city = s_city, d_city = d_city, decription = description, user_id = user.id)
        db.session.add(new_trans)
        db.session.commit()
        return redirect(f'/user/{user.id}')

    return render_template('create_transac.html', user = user)

@app.route('/review/<int:trans_id>', methods = ['GET', 'POST'])
def review(trans_id):
    this_trans = Transaction.query.get(trans_id)
    if request.method == "POST":
        d_date = request.form.get('d_date')
        amt = request.form.get('amt')
        this_trans.delivery_date = d_date
        this_trans.amount = amt
        this_trans.internal_status = "quoted"
        db.session.commit()
        return redirect('/admin')

    return render_template('review.html', this_trans = this_trans)

# @app.route('')


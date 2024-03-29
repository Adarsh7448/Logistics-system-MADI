from flask import Flask, render_template, redirect, request 
from flask import current_app as app
from .models import *
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg") #tkAgg

# http://127.0.0.1:5000/  base url
# http://127.0.0.1:5000/userlogin 


# @app.route('/')
# def something():

# Transaction One ----> transactionone

def raw(text): # text = Transaction One
    split_list = text.split() #----> list ['Transaction', 'One']
    src_word = ''
    for word in split_list:
        src_word += word.lower()
    return src_word

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
        new_trans = Transaction(t_name = t_name, t_search_name = raw(t_name), t_type = t_type, t_date = datetime.datetime.now(), s_city = s_city, d_city = d_city, decription = description, user_id = user.id)
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

@app.route('/delete/<int:id>')
def cancel_trans(id):
    del_trans = Transaction.query.get(id)
    del_trans.internal_status = "cancelled"
    db.session.commit()
    return redirect('/admin')

@app.route('/search')
def text_search():
    srch_word = request.args.get('srch_word')
    srch_word = "%"+raw(srch_word)+"%"
    srch_city = "%"+srch_word.lower()+"%"
    srch_type = "%"+srch_word.lower()+"%"
    t_names = Transaction.query.filter(Transaction.t_search_name.like(srch_word)).all()
    t_s_city = Transaction.query.filter(Transaction.s_city.like(srch_city)).all()
    t_d_city = Transaction.query.filter(Transaction.d_city.like(srch_city)).all()
    t_types = Transaction.query.filter(Transaction.t_type.like(srch_type)).all() # searches for raw transaction name
    search_results = t_names + t_s_city + t_d_city + t_types
    return render_template('srch_result.html', search_results = search_results)

    # records with transaction name 
    
    # records with transaction type --->
    # records based on source cities ---->

    # records based on destination cities ---->
    
    # transaction

@app.route('/stats')
def show_stats():
    transactions = Transaction.query.all()
    # liquid = 0
    types = []
    s_cities = []
    for trans in transactions:
        # if trans.t_type == "liquid":
        #     liquid+=1
        types.append(trans.t_type)
        s_cities.append(trans.s_city)
    plt.clf()
    plt.hist(types)
    plt.savefig('static/img1.png')
    plt.clf()
    plt.hist(s_cities)
    plt.savefig('static/img2.png')
    
    return render_template('summary.html')



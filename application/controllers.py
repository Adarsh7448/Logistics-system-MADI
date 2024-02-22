from flask import Flask, render_template, redirect, request 
from flask import current_app as app

# http://127.0.0.1:5000/  base url
# http://127.0.0.1:5000/userlogin 


# @app.route('/')
# def something():

sample_data = [
    {"u_name": "Yash", "pwd": "1234"},
    
]


@app.route('/userlogin', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        u_name = request.form.get("u_name")
        pwd = request.form.get("pwd")
        for data in sample_data:
            if data["u_name"] == u_name:
                if data["pwd"] == pwd:
                    return render_template("user_dash.html", u_name = u_name) 
                else:
                    return "incorrect Password"
            else:
                return "user does not exist!"
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def user_register():
    return render_template('register.html')

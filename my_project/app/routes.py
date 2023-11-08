from flask import render_template, flash, request, url_for, redirect
from app.models import User, Post
from app.forms import SignupForm, LoginForm
from app import app


post = [

        {'title': 'Menopuse', 
        'author': 'Mobola',
        'date_posted': '30/10/23'
         },


        {'title': 'Mensuration',
         'author': 'Sandra',
         'date_posted': '31/10/23'
        }

        ] 


@app.route('/')
def home():
    return render_template('home.html', post=post)

@app.route('/about')
def about():
    return '<h1>About Page</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@totalwoman.com" and form.password.data == "Password":
            flash(f"Successfully logged in", "success")
            return redirect(url_for("home"))
        else:
            flash(f"Login not successful", "danger")
    return render_template("login.html", title='Login', form=form)


@app.route('/logout')
def logout():
    return "<p>logout</p>"


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()   
    if form.validate_on_submit():
        flash(f"Account Created {form.username.data}!", "success")
        return redirect(url_for("home"))    
    return render_template("sign_up.html", title='Sign Up', form=form)
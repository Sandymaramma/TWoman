from flask import Flask, render_template, flash, request, url_for, redirect
from forms import SignupForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '0c4bdc6795503f3d38a8cc9992879d9a'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{tWoman_db}'

db = SQLAlchemy(app)


class User(db.Model): # Usermixin is provided by flask_login extension managing user authentication
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def _repr_(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def _repr_(self):
        return f"Post('{self.title}', '{self.date_posted}')"



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







if __name__ == '__main__':
    app.run(debug=True)

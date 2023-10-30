from flask import Flask, render_template, flash, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'imeagert0'
#app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

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
    return render_template("login.html", boolean=True)


@app.route('/logout')
def logout():
    return "<p>logout</p>"


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='success')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            flash('Account created.', category='success')
        
    return render_template("sign_up.html")







if __name__ == '__main__':
    app.run(debug=True)

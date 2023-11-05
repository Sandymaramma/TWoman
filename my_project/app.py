from flask import Flask, render_template, flash, request
from forms import SignupForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '0c4bdc6795503f3d38a8cc9992879d9a'
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
    form = SignupForm()
    
        

        
        
    return render_template("sign_up.html", title='Sign Up', form=form)







if __name__ == '__main__':
    app.run(debug=True)

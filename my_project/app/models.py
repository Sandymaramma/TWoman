from datetime import datetime
from app import db

class User(db.Model): # Usermixin is provided by flask_login extension managing user authentication
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

"""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
"""

"""
def get_reset_token(self):
        payload = {
            'sub': self.id,
            'iss': current_app.config['SECRET_KEY'],
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }
        secret_key = current_app.config['SECRET_KEY']
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    @staticmethod
    def verify_reset_token(token):
        try:
            secret_key = current_app.config['SECRET_KEY']
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])

            # Verify the 'iss' (issuer) claim
            if payload['iss'] != secret_key:
                return None  # Token was not issued by the expected issuer

            # Verify the 'exp' (expiration time) claim
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                return None  # Token has expired

            # Retrieve the user based on user_id from the token's 'sub' (subject) claim
            user_id = payload['sub']
            user = User.query.get(user_id)
            return user
        except jwt.ExpiredSignatureError:
            return None # Token has expired
        except jwt.InvalidTokenError:
            return None # Invalid token or signature
        #return None


    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"
"""

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

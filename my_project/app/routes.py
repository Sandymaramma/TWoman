from flask import render_template, flash, request, url_for, redirect
from app.models import User, Post
from app.forms import SignupForm, LoginForm, UpdateAccountForm, PostForm
from app import app, db, bcrypt
from flask_login import current_user, login_user, logout_user, login_required
from PIL import Image
import os
import secrets


"""
posts = [

        {'title': 'Menopuse', 
        'author': 'Mobola',
        'date_posted': '30/10/23'
         },


        {'title': 'Mensuration',
         'author': 'Sandra',
         'date_posted': '31/10/23'
        }

        ] 
    """


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # Enables Pagination
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return '<h1>About Page</h1>'


@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('sign_up'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit() 
        flash(f'{form.username.data}, your account has been created!', 'success')
        return redirect(url_for('sign_up'))
    return render_template('sign_up.html', title="Sign Up", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # Directs user to the requested page using query parameter 'next'
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful, Pls check your email and password', 'danger')
    return render_template('login.html', title="Login", form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/account', methods=['GET', 'POST'])
@login_required # Ensures you must be logged in to access the acounts page
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # Loads update form with user's username & password
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # For naming our picture files
    _, f_ext = os.path.splitext(form_picture.filename) # To grab the picture file extension, the 'f_name' is not needed so we changed it to underscore ""
    picture_filename = random_hex + f_ext # Giving the picture a name with filename + extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename) # Choosing how to save the picture
    
    # Used to resize the image to 125x125 before saving it
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename

@app.route('/post/new', methods=['Get', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # Ensures only author of a post can update it
        abort(403)
    form = PostForm() # Initializing the form
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title # Ensures post title is loaded for update
        form.content.data = post.content # Ensures post content is loaded for update
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


# Enables the possibility of seeing all the post from a particular author
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # Enables Pagination
    return render_template('user_posts.html', posts=posts, user=user)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # Ensures only author of a post can update it
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')
    return redirect(url_for('home'))






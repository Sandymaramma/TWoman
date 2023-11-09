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


@posts.route('/post/new', methods=['Get', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title # Ensures post title is loaded for update
        form.content.data = post.content # Ensures post content is loaded for update
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


"""
@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # Loads update form with user's username & password
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)

"""

"""
# Enables the possibility of seeing all the post from a particular author
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # Enables Pagination
    return render_template('user_posts.html', posts=posts, user=user)

"""





@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # Ensures only author of a post can update it
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')
    return redirect(url_for('main.home'))


"""

@posts.route('/post/new', methods=['Get', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title # Ensures post title is loaded for update
        form.content.data = post.content # Ensures post content is loaded for update
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # Ensures only author of a post can update it
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')
    return redirect(url_for('main.home'))
"""

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # Enables Pagination
    return render_template('home.html', posts=posts)

import os
import logging
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import database

app = Flask(__name__)
app.secret_key = 'very secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs.log')
logging.basicConfig(filename=filename, level=logging.DEBUG,
                    format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


@app.route('/')
@app.route('/homepage')
def homepage():
    app.logger.info('Loading homepage')

    return render_template('homepage.html')


# registration/login
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        app.logger.info('Loading registration form')
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        name = request.form.get('name')
        age = request.form.get('age')
        education = request.form.get('education')
        position = request.form.get('position')
        about = request.form.get('about')

        new_user = database.Users(username=username, password=hashed_password, name=name, age=age, education=education,
                                  position=position, about=about)

        try:
            db.session.add(new_user)
            db.session.commit()
            app.logger.info('Registration successful')
            return redirect('/homepage')  # will redirect it to a different page at a later date
        except:
            app.logger.info('Registration failed')
            return "<h1>Something went wrong while registering</h1>"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = database.Users.query.filter_by(username=username).first()

        if not user:
            app.logger.info('Login failed')
            return render_template('login.html')

        if check_password_hash(user.password, password):
            session['user'] = username
            app.logger.info('Login successful')
            return redirect(url_for('profile', user_id=user.id))

    if request.method == 'GET':
        app.logger.info('Loading login page')
        return render_template('login.html')


@app.route('/logout')  # currently not used since we only have a single page
def logout():
    app.logger.info('User logged out')
    session.pop('user')
    return redirect('/login')


# profile
@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'GET':
        if 'user' in session:
            user = database.Users.query.filter_by(id=user_id).first_or_404()

            return render_template('profile.html', user=user)
        else:
            return render_template('login.html')
    if request.method == 'POST':
        return redirect(url_for('profile_editing', user_id=user_id))


@app.route('/profile_edit/<user_id>', methods=['GET', 'POST'])
def profile_edit(user_id):
    if request.method == 'GET':
        if 'user' in session:
            user = database.Users.query.filter_by(id=user_id).first_or_404()

            return render_template('profile_editing.html', user=user)
        else:
            return render_template('login.html')
    if request.method == 'POST':
        user = db.session.query(database.Users).filter_by(id=user_id).first_or_404()

        user.name = request.form.get('name')
        user.age = request.form.get('age')
        user.education = request.form.get('education')
        user.position = request.form.get('position')
        user.about = request.form.get('about')

        try:
            db.session.commit()
            app.logger.info('Successfully changed user information')
            return redirect(url_for('profile', user_id=user_id))
        except:
            app.logger.info('Editing failed')
            return redirect(url_for('profile', user_id=user.id))


# posts
def search(keyword):
    search_tag = "%{}%".format(keyword)
    results = database.Post.query.filter(database.Post.title.ilike(search_tag)).all()
    return results

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        posts = database.Post.query.all()

        app.logger.info('Loading posts')
        return render_template('post.html', posts=posts)
    if request.method == 'POST':
        results = search(request.form.get('keyword'))

        app.logger.info('Loading posts from search')
        return render_template('post.html', posts=results)



@app.route('/view_post/<post_id>', methods=['GET'])
def view_post(post_id):
    post = database.Post.query.filter_by(id=post_id).first_or_404()

    app.logger.info('Loading post <post_id>')
    return render_template('view_post.html', post=post)


@app.route('/create_post/<user_id>', methods=['GET', 'POST'])
def create_post(user_id):
    if request.method == 'GET':
        if 'user' in session:
            user = database.Users.query.filter_by(id=user_id).first_or_404()

            return render_template('create_post.html', user=user)
        else:
            return render_template('login.html')

    if request.method == 'POST':
        user = database.Users.query.filter_by(id=user_id).first_or_404()

        author_id = user_id
        title = request.form.get('title')
        content = request.form.get('content')

        new_post = database.Post(author_id=author_id, title=title, content=content)

        try:
            db.session.add(new_post)
            db.session.commit()
            app.logger.info('Post created successfully')
            return redirect('/post')
        except:
            app.logger.info('Post creation failed')
            return "<h1>Something went wrong while uploading your post</h1>"





if __name__ == "__main__":
    app.run(debug=True)

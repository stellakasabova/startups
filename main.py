import os
import logging
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs.log')
logging.basicConfig(filename=filename, level=logging.DEBUG,
                    format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(80), nullable=False)
    about = db.Column(db.String(350), nullable=True)
    position = db.Column(db.String(40), nullable=False)


@app.route('/')
@app.route('/homepage')
def homepage():
    app.logger.info('Loading homepage')
    return render_template('homepage.html')


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

        new_user = Users(username=username, password=hashed_password, name=name, age=age, education=education,
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

        user = Users.query.filter_by(username=username).first()

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


@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'GET':
        if 'user' in session:
            user = Users.query.filter_by(id=user_id).first_or_404()

            return render_template('profile.html', user=user)
        else:
            return render_template('login.html')
    if request.method == 'POST':
        return redirect(url_for('profile_editing', user_id))

@app.route('/profile_edit/<user_id>', methods=['GET', 'POST'])
def profile_edit(user_id):
    if request.method == 'GET':
        if 'user' in session:
            user = Users.query.filter_by(id=user_id).first_or_404()

            return render_template('profile_editing.html', user=user)
        else:
            return render_template('login.html')
    if request.method == 'POST':
        user = Users.query.filter_by(id=user_id).first_or_404()

        user.name = request.form.get('name')
        user.age = request.form.get('age')
        user.education = request.form.get('education')
        user.position = request.form.get('position')
        user.about = request.form.get('about')

        try:
            db.session.commit()
            app.logger.info('Successfully changed user information')
            return redirect(url_for('profile', user_id))
        except:
            app.logger.info('Editing failed')
            return "<h1>Something went wrong while editing</h1>"


if __name__ == "__main__":
    app.run(debug=True)
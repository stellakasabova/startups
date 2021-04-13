<<<<<<< Updated upstream
from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
=======
import os
import logging
from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
>>>>>>> Stashed changes

app = Flask(__name__)
app.secret_key = 'very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

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
    return render_template('homepage.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
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
            return redirect('/homepage')  # will redirect it to a different page at a later date
        except:
            return "<h1>Something went wrong while registering</h1>"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username).first()

        if not user:
<<<<<<< Updated upstream
            return "<h1>Wrong username or password</h1>"
        else:
            session['user'] = username
            return redirect('/homepage')  # will redirect it to a different page at a later date
=======
            app.logger.info('Login failed')
            return flash('Wrong username or password')

        if check_password_hash(user.password, password):
            session['user'] = user.id
            app.logger.info('Login successful')
            return redirect('/homepage')
>>>>>>> Stashed changes

    if request.method == 'GET':
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)

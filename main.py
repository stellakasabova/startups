from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    name = db.Column(db.String(80), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    education = db.Column(db.String(80), nullable = False)   
    about  = db.Column(db.String(350), nullable = True)
    position = db.Column(db.String(40), nullable = False)

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:
            session['user'] = username
            return redirect('/homepage')

        return "<h1>Wrong username or password</h1>"

    return render_template('login.html')


@app.route('/homepage')
def homepage():
    if 'user' in session and session['user'] == user['username']:
        return '<h1>Homepage</h1>'  # this is a placeholder

    return '<h1>You are not logged in.</h1>'

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)

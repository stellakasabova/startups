from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)
app.secret_key = 'very secret key'

user = {"username": "abc", "password": "xyz"}  # temporary dictionary for testing until we add a db


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

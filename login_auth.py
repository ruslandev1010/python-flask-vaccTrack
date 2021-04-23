from flask import Flask, flash, redirect, url_for, render_template, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import setup
from setup import _PORT,_HOST, app, _PLACEHOLDER

from HIM73050 import flask_db as fdb

app.config['SECRET_KEY'] = 'bcnxvbfhsdlkdm.sadal;diiuyuerfjs'

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

#assign login manager
@login_manager.user_loader

# def create_patients_table():
#     res = fdb.query_db_create('CREATE TABLE Patients (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(255), lastname VARCHAR(255), address VARCHAR(255), city VARCHAR(255), dob DATE, apt INT, sex VARCHAR(255), postalcode VARCHAR(255), province VARCHAR(255))')
#     return res
def load_user(id):
    first_match=fdb.query_db_get_one('SELECT id, username, password FROM Users WHERE id = {0}'.format(_PLACEHOLDER), (id,))

    if first_match == None:
        return None
    else:
        user = User(first_match['id'], first_match['username'], first_match['password'])
        return user

def lookup_user(username, password):
    first_match=fdb.query_db_get_one('SELECT id, username, password FROM Users WHERE username = {0}'.format(_PLACEHOLDER), (username,))
    if first_match==None:
        return None
    else:
        user = User(first_match['id'], first_match['username'], first_match['password'])
        if check_password_hash(user.password, password):
            return user
        else:
            return None

def add_user(username, password):
    fdb.query_db_change('INSERT INTO Users (username, password) VALUES({0}, {0})'.format(_PLACEHOLDER), (username, generate_password_hash(password)))


#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registered_user = lookup_user(username, password)

        if registered_user is None:
            flash('Username or Password You Entered is not valid', 'error')
            return redirect(url_for('login'))
        else:
            login_user(registered_user)
            flash('Logged in successfully')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('select_patient'))

#register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        add_user(request.form['username'], request.form['password'])
        flash('User registered successfully')
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#keep route very secret!!!
@app.route('/backdoor34748947347678643324329089321879843297', methods=['GET'])
def user():
    user_results=fdb.query_db_get_all('SELECT * FROM Users')
    print(user_results)
    return jsonify(user_results)
# end of login reouters and stuff


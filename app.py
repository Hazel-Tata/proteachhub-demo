
from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
user_file = 'users.json'

def load_users():
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open(user_file, 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "Username already exists."
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

if __name__ == '__main__':
    app.run(debug=True)

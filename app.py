from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
# from werkzeug.security import generate_password_hash, check_password_hash
import os
import arxiv

import hashlib

SALT = "your-unique-app-level-salt"

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/avatars'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DATABASE_FILE = 'database.txt'


def save_user(username, password_hash, avatar_filename, field, position, level, linkedin):
    with open(DATABASE_FILE, 'a') as f:
        f.write(f"{username}|{password_hash}|{avatar_filename}|{field}|{position}|{level}|{linkedin}\n")


def load_users():
    users = {}
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            for line in f:
                data = line.strip().split('|')
                if len(data) == 7:
                    username, password_hash, avatar, field, position, level, linkedin = data
                    users[username] = {
                        'password': password_hash,
                        'avatar': avatar,
                        'field': field,
                        'position': position,
                        'level': level,
                        'linkedin': linkedin
                    }
    return users


def update_user(username, user_data):
    users = load_users()
    users[username] = user_data
    with open(DATABASE_FILE, 'w') as f:
        for user, data in users.items():
            f.write(f"{user}|{data['password']}|{data['avatar']}|{data['field']}|{data['position']}|{data['level']}|{data['linkedin']}\n")


def get_papers(user_query="deep learning"):
    search = arxiv.Search(
        query=user_query,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = []
    for result in search.results():
        results.append({
            'title': result.title,
            'authors': ', '.join(author.name for author in result.authors),
            'published': result.published.strftime('%Y-%m-%d'),
            'pdf_url': result.pdf_url
        })
    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    users = load_users()
    user = users.get(session['username'])

    if user is None:
        session.pop('username', None)
        return redirect(url_for('login'))

    results = []

    if request.method == 'POST':
        query = request.form['query']
        results = get_papers(query)

    return render_template('index.html', username=session['username'], avatar=user['avatar'], results=results)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        avatar = request.files['avatar']
        field = request.form['field']
        position = request.form['position']
        level = request.form['level']
        linkedin = request.form['linkedin']

        users = load_users()
        if username in users:
            return "Username already exists."

        hashed = hashlib.sha256((password + SALT).encode()).hexdigest()
        avatar_filename = secure_filename(avatar.filename)
        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))

        save_user(username, hashed, avatar_filename, field, position, level, linkedin)
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    users = load_users()
    user = users.get(session['username'])

    message = ""

    if request.method == 'POST':
        field = request.form['field']
        position = request.form['position']
        level = request.form['level']
        linkedin = request.form['linkedin']
        avatar = request.files.get('avatar')

        avatar_filename = user['avatar']
        if avatar and avatar.filename:
            avatar_filename = secure_filename(avatar.filename)
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))

        users[session['username']].update({
            'field': field,
            'position': position,
            'level': level,
            'linkedin': linkedin,
            'avatar': avatar_filename
        })
        update_user(session['username'], users[session['username']])
        message = "Profile updated successfully!"

    return render_template('profile.html', username=session['username'], user=user, message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        user = users.get(username)

        hash_attempt = hashlib.sha256((password + SALT).encode()).hexdigest()
        if user and user['password'] == hash_attempt:
            session['username'] = username
            return redirect(url_for('index'))
        return "Invalid username or password."
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

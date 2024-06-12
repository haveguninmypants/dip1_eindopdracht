from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, LoginManager, UserMixin
import sqlite3

def create_db():
    conn = sqlite3.connect("./database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS login (id INTEGER PRIMARY KEY, username TEXT, password INTEGER)''')
    conn.commit()
    conn.close()

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
@login_required
def inloggen():
    return render_template('login.html')

@app.route('/register')
@login_required
def registreren():
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return '''Hij doet het niet...
            <p>
            <a href="/">
            <button>Home</button>
            </a></p>'''

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return None


@login_manager.request_loader
def request_loader(request):
    user = User()
    return None

create_db()

if __name__ == '__main__':
    app.run(debug=True)
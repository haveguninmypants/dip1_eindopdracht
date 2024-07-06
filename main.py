
from os import read
from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user
import sqlite3

def create_db():
    conn = sqlite3.connect("./database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS login (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS films ( id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,url TEXT NOT NULL)''')
    conn.commit()
    conn.close()

app = Flask(__name__)
app.secret_key = 'supersecretkey'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def user_loader(username):
    conn = sqlite3.connect("./database.db")
    c = conn.cursor()
    c.execute("SELECT username FROM login WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(username)
    return None

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to display the list of films
@app.route('/ADB')
@login_required
def index():
    conn = get_db_connection()
    films = conn.execute('SELECT * FROM films').fetchall()
    conn.close()
    return films[0]

# Route to handle adding new films
@app.route('/add_app', methods=['POST'])
def add_app():
    title = request.form['title']
    url = request.form['url']
    conn = get_db_connection()
    conn.execute('INSERT INTO films (title, url) VALUES (?, ?)', (title, url))
    conn.commit()
    conn.close()
    return "posted!"

@app.route("/minecraft")
@login_required
def minecraft():
    return render_template("minecraft.html")

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username:
        conn = sqlite3.connect("./database.db")
        c = conn.cursor()
        c.execute("SELECT username, password FROM login WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and user[1] == request.form.get('password'):
            return User(username)
    return None

@app.route('/')
def home():
    return render_template('home.html')

def get_db():
    conn = sqlite3.connect('./database.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

@app.route('/log', methods=[ 'POST'])
def log():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db()
    c = conn.cursor()
    
    try:
        c.execute("SELECT username, password FROM login WHERE username = ?", (username,))
        user = c.fetchone()
        
        if user and user['password'] == password:
            user_obj = User(username)
            login_user(user_obj)
            
            # Redirect based on specific usernames
            if username == '123':
                return render_template("Routing.html")
            elif username == 'Administrator':
                return render_template("CNBT.html")
            elif username == 'rick':
                return 'https://youtube.com'
            else:
                return redirect(url_for('dashboard'))  # Default redirect
            
        else:
            return redirect(url_for('login'))  # Redirect back to login page on authentication failure
    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect(url_for('login'))
    finally:
        conn.close()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def registreren():
    return render_template('register.html')

@app.route('/maakuser', methods=['POST'])
def maakuser():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT username FROM login WHERE username = ?", (username,))
        existing_user = c.fetchone()
        if existing_user:
        
            return redirect(url_for('registreren'))
        
        c.execute('INSERT INTO login (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        
        return redirect(url_for('login'))
    except Exception as e:
        print(f"An error occurred: {e}")
        
        return redirect(url_for('registreren'))
    finally:
        conn.close()

@app.route('/GPT')
@login_required
def GPT():
    return render_template('gpt.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("login.html")

create_db()

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=80)
    

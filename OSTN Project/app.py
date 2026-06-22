import sqlite3
db = sqlite3.connect("app.db", check_same_thread=False)
cr = db.cursor()
cr.execute("CREATE TABLE if not exists users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
cr.execute("CREATE TABLE if not exists skills (username TEXT, skill VARCHAR(15))")
def commit_and_exit():
    db.commit()
    db.close()
from flask import Flask, render_template, url_for, request, session, redirect, send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OSTN_HAS_SKILL_ISSUE'

def create_account(username, password):
    cr.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    db.commit()

def check_session():
    if 'username' not in session:
        return "Log in first"

@app.route("/")
def home():
    return render_template("home.html", customcss='home.css')
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        if request.form.get('username') and request.form.get('password'):
            username = request.form.get('username')
            password = request.form.get('password')
            result = cr.execute("SELECT username FROM users WHERE username = ?", (username, )).fetchone()
            if result:
                return "You are already registered"
            else:    
                create_account(username, password)
            db.commit()
            return redirect(url_for('login'))
        else:
            return "Please Type valid username and password"
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('profile'))
    if request.method == "GET":
        return render_template('login.html', customcss='login.css')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'os7n' and password != 'os7n_skill_issue':
            return "Sorry you didn't type the right password for 'os7n' which is 'os7n_skill_issue'"
        query = cr.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        if query:
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return f"Incorrect username or password"

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    result = cr.execute("SELECT skill FROM skills WHERE username = ?", (session['username'], )).fetchall()
    return render_template('profile.html', skills=result)


@app.route('/robots.txt')
def robots():
    return send_file('robots.txt')

@app.route('/skills', methods = ['GET', 'POST'])
def skills():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('skills.html')

    if request.form.get('skill'):
        skill = request.form.get('skill')
        print(skill)
        result = cr.execute("SELECT skill FROM skills WHERE skill = ?", (skill, )).fetchone()
        if result:
            return "You already added this skill."
        else:
            cr.execute("INSERT INTO skills (username, skill) VALUES (?, ?)" ,  (session['username'], skill))
            db.commit()
            return "Your skill is added!"


@app.route('/skill-issue')
def skill_issue():
    return render_template('skill-issue.html')
@app.route('/admin')
def admin():
    if session['username'] != 'os7n':
        return "Sorry, you are not os7n so you can't access this page\nPlease login with os7n account"
    else:
        return render_template('admin.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

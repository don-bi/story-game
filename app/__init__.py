from flask import Flask,render_template,session,request
import secrets
from db import *

app = Flask(__name__)

app.secret_key = secrets.token_bytes(32)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('discover.html') # page with all the stories
    return render_template('index.html') # welcome page, has login button

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return render_template('index.html')

@app.route('/discover', methods=["POST"])
def discover(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if ('login' in request.form): #based on submit button name="login" to check if it's login or signup
            correct_credentials = check_credentials(username, password)
            #sends user back to login page with an error if user credentials are wrong
            #sends them to discover page otherwise
            if correct_credentials: 
                session['username'] = username
                return render_template('discover.html')
            else:
                return render_template('login.html', error = True)
        else: #for signups
            no_user_exists = check_user_not_exists(username)
            if no_user_exists: #signs up and logs in the user
                create_new_user(username, password)
                session['username'] = username
                return render_template('discover.html')
            else: #error because user already exists
                return render_template('signup.html', error = True)
    
@app.route('/add')
def add():
    return render_template('add.html')
    
@app.route('/profile')
def profile():
    return render_template('profile.html', username = session['username'])
    
@app.route('/story')
def story():
    return render_template('story.html')
    
if __name__ == '__main__':
    app.debug = True
    app.run()
from flask import Flask,render_template,session,request
import secrets

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

@app.route('/discover')
def discover(): 
    if request.method == 'POST':
        return render_template('discover.html')
    
@app.route('/add')
def add():
    return render_template('add.html')
    
@app.route('/profile')
def profile():
    return render_template('profile.html', username = session['username'])
    
@app.route('story.html')
def story():
    return render_template('story.html')
    
if __name__ == '__main__':
    app.debug = True
    app.run()
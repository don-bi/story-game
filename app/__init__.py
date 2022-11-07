from flask import Flask,render_template,session,request
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_bytes(32)

@app.route('/', methods=['POST'])
def home():
    if 'username' in session:
        return render_template('discover.html',) # page with all the stories
    return render_template('index.html',) # welcome page, has login button

@app.route('/') 
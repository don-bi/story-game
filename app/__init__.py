from flask import Flask,render_template,session,request
import secrets
from db import *

app = Flask(__name__)

app.secret_key = secrets.token_bytes(32)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('discover.html', stories = get_stories()) # page with all the stories
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
    if 'addition' in request.form:
        title = request.form['title']
        first_part = request.form['first_part']
        creator = session['username']
        create_story(creator, title, first_part)
    return render_template('discover.html', stories = get_stories())

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/profile', methods=['GET','POST'])
def profile():
    if request.method == 'POST':
        if 'username' in request.form: #makes sure that it's a login or signup assigning
            username = request.form['username']
            password = request.form['password']
        print(request.form)
        if 'login' in request.form: #based on submit button name="login" to check if it's login or signup
            db_table_inits() #makes tables if they don't exist
            correct_credentials = check_credentials(username, password)
            #sends user back to login page with an error if user credentials are wrong
            #sends them to discover page otherwise
            if correct_credentials:
                session['username'] = username
            else:
                return render_template('login.html', error = 'login')

        elif 'signup' in request.form: #for signups
            db_table_inits() #makes tables if they don't exist
            no_user_exists = check_user_not_exists(username)
            if no_user_exists: #signs up and logs in the user
                if password == request.form['confirmation']:
                    create_new_user(username, password)
                    session['username'] = username
                else:
                    #error because confirmation not same as password
                    return render_template('signup.html', error = 'confirmation')
            else:
                #error because user already exists
                return render_template('signup.html', error = 'signup')

    username = session['username']
    created_stories = get_created_stories(username)
    contributed_stories = get_contributed_stories(username)
    print(contributed_stories)
    return render_template('profile.html',
                           created_stories = created_stories, contributed_stories = contributed_stories, username = username)

@app.route('/story', methods=["POST"])
def story():
    story_id = list(request.form)[0][0] #gets id from name="{{story[0]}}", turns into list becuase request.form is dictonary
    story_title = get_story_title(story_id)
    if len(request.form) > 1: #request.form will only have more than one element when contribution request
        story_id = list(request.form)[-1][0]
        contribution = request.form['contribution']
        add_to_story(session['username'], story_id, contribution)

    story_info = get_story_info(story_id)
    contributor_list = get_contributor_list(story_id)
    newest_contribution = story_info[-1][2]
    #print(newest_contribution) #testing
    return render_template('story.html', story_id = story_id, story_title = story_title,
    story_info = story_info, contributor_list = contributor_list,
    username = session['username'], newest_contribution = newest_contribution)

if __name__ == '__main__':
    app.debug = True
    app.run()

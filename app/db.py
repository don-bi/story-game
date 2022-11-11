import sqlite3, random as rand

DB_FILE = "data.db"

db = None

def db_connect():
    global db 
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def db_close():
    db.commit()
    db.close()
    
def db_table_inits(): #creates stories and user tables if they don't exist
    c = db_connect()
    c.execute("CREATE TABLE IF NOT EXISTS stories (id int, title text, creator text)")
    c.execute("CREATE TABLE IF NOT EXISTS users (username text, password text)")
    db_close()
    
#for signing up
def check_user_not_exists(username): #checks if user doesn't exist, returns True if they don't exist
    c = db_connect()
    c.execute('SELECT username FROM users WHERE username=?',username)
    user = c.fetchone()
    db_close()
    print(user)
    print(username)
    if user:
        return False
    return True

#for signing up
def create_new_user(username, password): #creates new user
    c = db_connect()
    c.execute('INSERT INTO users VALUES (?,?)',(username, password))
    c.execute("SELECT * from users")
    print(len(c.fetchall()))
    db_close()


#for logging in
def check_credentials(username, password): #checks if there exists username and password in db, returns True if there is
    c = db_connect()
    c.execute('SELECT username,password FROM users WHERE username=? AND password=?',(username, password))
    user = c.fetchone()
    db_close()
    if user:
        return True
    return False

''' Testing functions
 
db_table_inits()
create_new_user("troll","troll123")
c = db_connect()
c.execute("select * from users")
print(c.fetchall())
db_close()

print(check_user_not_exists("troll))
print(check_credentials("troll","troll123"))
'''

def create_story(creator, title, first_part):
    c = db_connect()
    c.execute("SELECT * FROM stories")
    story_id = len(c.fetchall()) #the id of the new story

    c.execute('INSERT INTO stories VALUES (?, ?, ?)',(story_id,title,creator)) #stores a new story in the database
    c.execute('CREATE TABLE story_? (story_part int, story text, contributor text)',story_id) #creates a new table for the story
    c.execute('INSERT INTO story_? VALUES (0, ?, ?)',(story_id,first_part,creator)) #inserts creator's addition to the story's table
    db_close()

def add_to_story(contributor, story_id, story_addition):
    c = db_connect()
    c.execute('SELECT * from story_{story_id}')
    story_part = len(c.fetchall())
    #adds new addition
    c.execute('INSERT INTO story_{story_id} VALUES ({story_part}, "{story_addition}", "{contributor}")')
    db_close()

'''
db_table_inits()
#create_story("troll", "trolltitle", "hello I am troll")
add_to_story("trollno2", 0, "hello there I am troll 2")
c = db_connect()
c.execute("SELECT * FROM story_0")
print(c.fetchall())
db_close()
'''

def get_stories():
    c = db_connect()
    c.execute('SELECT * FROM stories')
    stories = c.fetchall()
    rand.shuffle(stories)
    return stories

def get_story_info(story_id):
    c = db_connect()
    c.execute(f'SELECT * FROM story_{story_id}')
    story_info = c.fetchall()
    return story_info

def get_contributor_list(story_id):
    c = db_connect()
    c.execute(f'SELECT contributor FROM story_{story_id}')
    contributor_list = c.fetchall()
    return contributor_list
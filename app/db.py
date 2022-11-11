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
    c.execute("CREATE TABLE IF NOT EXISTS story_info (id int, story_part int, story text, contributor text)")
    c.execute("CREATE TABLE IF NOT EXISTS users (username text, password text)")
    db_close()
    
#for signing up
def check_user_not_exists(username): #checks if user doesn't exist, returns True if they don't exist
    c = db_connect()
    c.execute('SELECT username FROM users WHERE username=?',(username,))
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
    c.execute('INSERT INTO story_info VALUES (?, 0, ?, ?)',(story_id,first_part,creator)) #inserts creator's addition to story_info table
    db_close()

def add_to_story(contributor, story_id, story_addition):
    c = db_connect()
    c.execute('SELECT * FROM story_info WHERE id=?',story_id)
    story_part = len(c.fetchall())
    #adds new addition to story_info
    c.execute('INSERT INTO story_info VALUES (?, ?, ?, ?)',(story_id,story_part,story_addition,contributor))
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

def get_stories(): #randomly gets stories (for formatting cards in discover.html)
    c = db_connect()
    c.execute('SELECT * FROM stories')
    stories = c.fetchall()
    rand.shuffle(stories)
    db_close()
    return stories

def get_story_info(story_id): #gets list of each part of a story(tuple)
    c = db_connect()
    c.execute('SELECT * FROM story_info WHERE id=?',story_id)
    story_info = c.fetchall()
    db_close()
    return story_info

def get_contributor_list(story_id): #gets list of contributors(tuples) 
    c = db_connect()
    c.execute('SELECT contributor FROM story_info WHERE id=?',story_id)
    contributor_list = c.fetchall()
    db_close()
    return contributor_list

def get_created_stories(username): #returns the stories that a user has created (for profile)
    c = db_connect()
    c.execute('SELECT * FROM stories WHERE creator=?',(username,))
    created_stories = c.fetchall()
    db_close()
    print(f'created_stories:{created_stories}')
    return created_stories
    
def get_contributed_stories(username): #returns the stories a user has contributed to (for profile)
    c = db_connect()
    c.execute('SELECT id FROM story_info WHERE contributor=?',(username,))
    contributed_id = c.fetchall() #gets a list of all the ids that user has contributed to
    contributed_stories = []
    for story_id in contributed_id: #goes through every story the user has contributed and makes a list of tuples
        c.execute('SELECT * FROM stories WHERE id=? AND creator!=?',(story_id[0],username))
        contributed_story = c.fetchone()
        if contributed_story != None: #checks to make sure there is at least one story
            contributed_stories.append(contributed_story)
    db_close()
    print(f'contributed_stories:{contributed_stories}') #testing
    return contributed_stories
        
        
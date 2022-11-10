import sqlite3

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
    c.execute("CREATE TABLE IF NOT EXISTS stories (id int, part int, creator text, story text, contributor text)")
    c.execute("CREATE TABLE IF NOT EXISTS users (username text, password text)")
    db_close()
    
#for signing up
def check_user_not_exists(username): #checks if user doesn't exist, returns True if they don't exist
    c = db_connect()
    c.execute(f'SELECT username FROM users WHERE username="{username}"')
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
    c.execute(f'INSERT INTO users VALUES ("{username}","{password}")')
    db_close()


#for logging in
def check_credentials(username, password): #checks if there exists username and password in db, returns True if there is
    c = db_connect()
    c.execute(f'SELECT username,password FROM users WHERE username="{username}" AND password="{password}"')
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
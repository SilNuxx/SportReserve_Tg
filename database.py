import sqlite3 as sq

# Initialize database

with sq.connect("database.db") as db:
	cur = db.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS 
		users(
			username TEXT, 
			user_id INT PRIMARY KEY,
			reservations_id INT NULL,
			administrator BOOL,
			FOREIGN KEY(reservations_id) REFERENCES resservations(reservations_id))""")
	cur.execute("""CREATE TABLE IF NOT EXISTS 
		gyms(
			gym_id INTEGER PRIMARY KEY AUTOINCREMENT,
			gym_name TEXT, 
			count_reservations INT, 
			reservations_id INT NULL,
			FOREIGN KEY(reservations_id) REFERENCES resservations(reservations_id))""")
	cur.execute("""CREATE TABLE IF NOT EXISTS 
		reservations(
			reservations_id INTEGER PRIMARY KEY AUTOINCREMENT, 
			user_id INT, 
			gym_id INT, 
			date_start DATE, 
			date_end DATE,
			FOREIGN KEY(user_id) REFERENCES users(user_id),
			FOREIGN KEY(gym_id) REFERENCES gyms(gym_id))""")

# Add user in database

def add_user(user):
	with sq.connect("database.db") as db:
		cur = db.cursor()
		try:
			cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)", user)
		except sq.IntegrityError:
			return False
	return True

def add_gym(gym):
	with sq.connect("database.db") as db:
		cur = db.cursor()
		
		try:
			cur.execute("INSERT INTO gyms VALUES(?, ?, ?, ?)", gym)
			return True
		except:
			return False

# Get all admins from the database

def get_admins():
	with sq.connect("database.db") as db:
		cur = db.cursor()
		cur.execute("SELECT user_id FROM users WHERE administrator = True")
		return cur.fetchall()

# Get all users from the database

def get_all_users():
	with sq.connect("database.db") as db:
		cur = db.cursor()
		cur.execute("SELECT * FROM users")
		return cur.fetchall()

# Get all gyms from the database

def get_all_gyms():
	with sq.connect("database.db") as db:
		cur = db.cursor()
		cur.execute("SELECT * FROM gyms")
		return cur.fetchall()
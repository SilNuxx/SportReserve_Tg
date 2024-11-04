import sqlite3 as sq

with sq.connect("database.db") as db:
	db.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, user_id INT PRIMARY KEY, date_registration DATE)")
	db.commit

def add_user(user):
	with sq.connect("database.db") as db:
		db.execute("INSERT INTO users VALUES(?, ?, ?)", user)
		db.commit()
	return True
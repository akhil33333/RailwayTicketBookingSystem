import sqlite3

con = sqlite3.connect("database.db")
print("Database created successfully")
con.execute("CREATE TABLE users (uid INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, email TEXT, "
            "phone TEXT, "
            "address TEXT, "
            "city TEXT, state TEXT, zipcode TEXT )")
con.execute("CREATE TABLE tickets (tid INTEGER PRIMARY KEY AUTOINCREMENT, from_place text, to_place text, persons text)")
print("Connection Created Successfully")
con.close()

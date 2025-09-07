import sqlite3, os

db_path = os.path.abspath("pswmgrv2.db")
print("Opening DB at:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# list tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# dump accounts if it exists
try:
    cursor.execute("SELECT * FROM accounts;")
    rows = cursor.fetchall()
    print("Rows:", rows)
except Exception as e:
    print("Error:", e)

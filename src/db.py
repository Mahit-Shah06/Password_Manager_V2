import sqlite3
from tkinter import messagebox as mb

class DBfunc():
    def __init__(self, db_name = "pswmgrv2.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def initialize_tables(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                upid INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                hased_password TEXT UNIQUE NOT NULL,
                salt TEXT NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                upid INTEGER PRIMARY KEY,
                site TEXT NOT NULL,
                username_email TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)

        self.conn.commit()
        self.conn.close()

    def retrieve_account(self, username):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT upid, hashed_password FROM accounts WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result

    def enter_account(self, upid, username, hashed_password, salt):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("INSERT INTO accounts (upid, username, master_password_hash, salt) VALUES (?, ?)", (upid, username, hashed_password, salt))
            self.conn.commit()
            mb.showinfo(f"Account for '{username}' created successfully.")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            mb.showerror(f"Error: Account already exists for '{username}'.")
            return None
        finally:
            self.conn.close()

    def add_password(self, upid, website, username_email, encrypted_password, notes=None):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
        """INSERT INTO passwords (upid, site, username_email, encrypted_password, notes) VALUES (?, ?, ?, ?, ?)""", (upid, website, username_email, encrypted_password, notes)
        )
        self.conn.commit()
        self.conn.close()
        mb.showinfo("Password entry added successfully.")

    def retrieve_password(self, upid):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT site, username_email, encrypted_password, notes FROM passwords WHERE upid = ?", (upid,))
        entries = self.cursor.fetchall()
        self.conn.close()
        return entries
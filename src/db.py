import sqlite3
from tkinter import messagebox as mb
import os

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
                uuid TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                hashed_password BLOB UNIQUE NOT NULL,
                salt BLOB NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                uuid TEXT PRIMARY KEY,
                site TEXT NOT NULL,
                username_email TEXT NOT NULL,
                encrypted_password BLOB NOT NULL,
                notes TEXT,
                FOREIGN KEY (uuid) REFERENCES accounts (uuid)
            );
        """)
        self.conn.commit()
        self.conn.close()

    def retrieve_account(self, username):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT uuid, hashed_password, salt FROM accounts WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        self.conn.close()
        return result

    def enter_account(self, uuid, username, hashed_password:bytes, salt:bytes):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("INSERT INTO accounts (uuid, username, hashed_password, salt) VALUES (?, ?, ?, ?)", (uuid, username, hashed_password, salt))
            self.conn.commit()
            return True, None
        except Exception as e:
            return False, e
        finally:
            self.conn.close()

    def add_password(self, uuid, website, username_email, encrypted_password:bytes, notes=None):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
            "INSERT INTO passwords (uuid, site, username_email, encrypted_password, notes) VALUES (?, ?, ?, ?, ?)", (uuid, website, username_email, encrypted_password, notes)
           )
            self.conn.commit()
            return True, None

        except Exception as e:
            return False, e
        finally:
            self.conn.close() 

    def retrieve_passwords(self, uuid):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "SELECT site, username_email, encrypted_password, notes FROM passwords WHERE user_uuid = ?",
            (uuid,)
        )
        entries = self.cursor.fetchall()
        self.conn.close()
        return entries 
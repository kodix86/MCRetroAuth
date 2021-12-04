import requests
from flask import Flask, request
from flask_bcrypt import Bcrypt
import sqlite3


class Server:
    def __init__(self, name: str):
        self.name = name
        self.core = Flask(name)
        self.b_crypt = Bcrypt(self.core)
        self.running = True
        self.file = sqlite3.connect("shared/userDB")
        self.db = self.file.cursor()

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT,
            userUUID TEXT,
            clientToken TEXT,
            accessToken TEXT
        )
        """)
        self.file.commit()

    def close_server(self):
        self.db.close()

#!/usr/bin/false

import requests
from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import sqlite3


# ! Children of this class need to supply an auth and identity function
class Server:
    def __init__(self, name: str):
        self.name = name
        self.core = Flask(name)
        self.core.config['SECRET_KEY'] = 'super-secret'  # REPLACE ME!
        self.b_crypt = Bcrypt(self.core)
        self.jwt = JWTManager(self.core)
        self.running = True
        self.file = sqlite3.connect("shared/userDB")
        self.db = self.file.cursor()

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            userUUID TEXT UNIQUE,
            clientToken TEXT,
            accessToken TEXT
        )
        """)
        self.file.commit()

    def close_server(self):
        self.db.close()

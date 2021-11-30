#!/usr/bin/false
from flask import Flask
from flask_bcrypt import Bcrypt

from server import Server


class Solo(Server):
    def register(self, username: str, password: str):
        reg_command = 'INSERT INTO USERS (username, password) VALUES(?, ?)'
        hashed_pass = self.b_crypt.generate_password_hash(password).decode('utf-8')

        data = [  # This structure is how we pass arguments to an sql command.
            username, hashed_pass
        ]

        print("Adding user with name \"" + username + "\" and password hash of \"" + hashed_pass + "\"")

        self.db.execute(reg_command, data)

        return 0

    def server_handle(self):
        @self.core.route('/authenticate', methods=["POST"])
        def handle_auth():
            ...

        return 0

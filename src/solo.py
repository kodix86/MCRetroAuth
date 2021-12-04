#!/usr/bin/false
from flask import Flask
from flask_bcrypt import Bcrypt
from uuid import uuid4

from server import Server


class Solo(Server):
    def register(self, username: str, password: str):
        reg_command = 'SELECT * FROM users WHERE username = ? LIMIT 1'

        data = [
            username
        ]

        self.db.execute(reg_command, data)
        result = self.db.fetchall()

        if not result:
            reg_command = 'INSERT INTO users (username, password, userUUID) VALUES(?, ?, ?)'
            hashed_pass = self.b_crypt.generate_password_hash(password).decode('utf-8')
            new_uuid = uuid4()

            data = [
                username, hashed_pass, str(new_uuid)
            ]

            print("Adding user with name \"" + username + "\" and password hash of \"" + hashed_pass + "\"")
            print("New player was also assigned the following uuid: " + str(new_uuid))

            self.db.execute(reg_command, data)
            self.file.commit()

            return 0

        else:
            print("User \"" + username + "\" already exists...")
            return 1

    def login(self, username: str, password: str):
        reg_command = 'SELECT * FROM users WHERE username = ?'

        data = [
            username
        ]

        self.db.execute(reg_command, data)
        result = self.db.fetchall()

        if result:
            pw_correct = self.b_crypt.check_password_hash(result[0][1], password)
            print(result[0])
            print("Password is correct?: " + str(pw_correct))

            return not pw_correct
        else:
            print("User does not exist!")
            return 1

    def server_handle(self):
        @self.core.route('/authenticate', methods=["POST"])
        def handle_auth():
            ...

        return 0

#!/usr/bin/false

from uuid import uuid4
from os.path import exists

from server import Server
from exit import ExitStatus


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
            new_uuid = str(uuid4())

            data = [
                username, hashed_pass, new_uuid
            ]

            print("Adding user with name \"" + username + "\" and password hash of \"" + hashed_pass + "\"")
            print("New player was also assigned the following uuid: " + new_uuid)

            self.db.execute(reg_command, data)
            self.file.commit()

            return ExitStatus.success

        else:
            print("User \"" + username + "\" already exists...")
            return ExitStatus.invalid_username

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

            if pw_correct:
                return ExitStatus.success
            else:
                return ExitStatus.auth_failure

        else:
            print("User does not exist!")
            return ExitStatus.invalid_username

    def server_handle(self):
        @self.core.route('/')
        def handle_base():
            if exists("shared/page.html"):
                file = open("shared/page.html", "r")
                content = file.read()
                file.close()

                return content
            else:
                return "Simple MC Auth Server"

        @self.core.route('/authenticate', methods=["POST"])
        def handle_authenticate():
            return "0"

        @self.core.route('/refresh', methods=["POST"])
        def handle_refresh():
            ...

        @self.core.route('/validate', methods=["POST"])
        def handle_validate():
            ...

        @self.core.route('/signout', methods=["POST"])
        def handle_signout():
            ...

        @self.core.route('/validate', methods=["POST"])
        def handle_invalidate():
            ...

        @self.core.route('/', methods=["POST"])
        def handle_legacy_authenticate():
            ...

        @self.core.route('/session', methods=["POST"])
        def handle_legacy_session():
            ...

        if exists("shared/key.pub") and exists("shared/key.prv"):
            self.core.run(ssl_context=('shared/key.crt', 'shared/key.prv'), port=5000)  # Start hosting the server!
            return ExitStatus.success
        else:
            self.core.run(ssl_context='adhoc', port=5000)
            return ExitStatus.missing_encryption_keys

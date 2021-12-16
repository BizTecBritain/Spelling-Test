__all__ = ['FlaskServer']
__version__ = '3.3.5'
__author__ = 'Alexander Bisland'

import json
import pickle
import random
import sqlite3
import string
from datetime import datetime, timedelta
from captcha.image import ImageCaptcha
from flask import Flask, send_file, Response, make_response, render_template, redirect, url_for, request
from flask_classful import FlaskView, route
from data_management.database import Database
from communications.session_management import SessionManager
from communications.security import hash_password, uuid_generator, login_check, email_check, username_check,\
    chars_only, lettersnumbers_only
from gtts import gTTS
import os
from data_management.email_server import EmailServer
from urllib.parse import unquote


class FlaskServer(FlaskView):
    route_base = '/'
    local_storage = "local_storage/"
    session_manager = SessionManager()
    email_server = EmailServer(local_storage+"server.ini")
    debug = False
    main_app = None
    logins = []
    ip_address = "localhost"
    port = 5000
    captchas = {}

    @classmethod
    def create_tables(cls) -> None:
        """
        Description: Function that creates the tables in the database if they dont already exist
        :return: void
        """
        database_manager = Database(cls.local_storage + "server.db")
        if cls.debug:
            print("Creating USERS table")
        with open(cls.local_storage + "sql_commands/create_users.txt", "r") as f:
            database_manager.create_table("USERS", f.readlines()[0].strip())
        if cls.debug:
            print("Creating LEADERBOARD table")
        with open(cls.local_storage + "sql_commands/create_leaderboard.txt", "r") as f:
            database_manager.create_table("LEADERBOARD", f.readlines()[0].strip())
        if cls.debug:
            print("Creating WORDLIST table")
        with open(cls.local_storage + "sql_commands/create_wordlist.txt", "r") as f:
            database_manager.create_table("WORDLIST", f.readlines()[0].strip())
        if cls.debug:
            print("Finished creating tables")

    @classmethod
    def download_files(cls) -> None:
        """
        Description: Function to download all the audio files from the web
        :return: void
        """
        database_manager = Database(cls.local_storage + "server.db")
        for file_name, word in database_manager.select("WORDLIST", "file_name, word"):
            if not os.path.exists(cls.local_storage + "audio/" + file_name):
                if cls.debug:
                    print("Downloading " + word + " to " + file_name)
                download = gTTS(word, lang="en", tld="com")
                download.save(cls.local_storage + "audio/" + file_name)
                if cls.debug:
                    print("Finished downloading " + word + " to " + file_name)
            elif cls.debug:
                print(file_name + " already exists")

    @classmethod
    def logout_all(cls) -> None:
        """
        Description: Function to log out all users
        :return: void
        """
        if cls.debug:
            print("Logging everyone out")
        database_manager = Database(cls.local_storage + "server.db")
        database_manager.submit_sql("""UPDATE USERS
                                        SET logged_in=?""", ("false",))
        if cls.debug:
            print("Finished logging everyone out")

    @route('/get_leaderboard/<string:datatype>/<string:difficulty>')
    def get_leaderboard(self, datatype: str, difficulty: str) -> str:
        """
        Description: Route to get the leadboard based on difficulty
        :param datatype: the type of leaderboard to return
        :param difficulty: the file of the database to access
        :return: str - json.dumps of the leaderboard
        """
        database_manager = Database(self.local_storage + "server.db")
        if datatype == "scores":
            if difficulty == "easy":
                return json.dumps(database_manager.select("LEADERBOARD", "*", where="category=\'easy\'",
                                                          order_by="score DESC, time DESC", limit="10"))
            if difficulty == "medium":
                return json.dumps(database_manager.select("LEADERBOARD", "*", where="category=\'medium\'",
                                                          order_by="score DESC, time DESC", limit="10"))
            if difficulty == "hard":
                return json.dumps(database_manager.select("LEADERBOARD", "*", where="category=\'hard\'",
                                                          order_by="score DESC, time DESC", limit="10"))
        if datatype == "words":
            words = []
            if difficulty == "easy":
                words = database_manager.select("WORDLIST", "word, correct, answered",
                                                where="category=\'easy\' AND answered>0")
            if difficulty == "medium":
                words = database_manager.select("WORDLIST", "word, correct, answered",
                                                where="category=\'medium\' AND answered>0")
            if difficulty == "hard":
                words = database_manager.select("WORDLIST", "word, correct, answered",
                                                where="category=\'hard\' AND answered>0")
            if difficulty in ["easy", "medium", "hard"]:
                order_words = {}
                for word in words:
                    order_words[word] = int(word[1]) / int(word[2]) * 100
                order_words = sorted(order_words.items(), key=lambda x: int(x[1]), reverse=True)[:10]
                return json.dumps(order_words)
        return ""

    @route('/get_leaderboard', methods=["GET", "POST"])
    def get_leaderboard_get_post(self) -> str:
        """
        Description: Route to get the leadboard based on difficulty for get/post request
        :return: str - json.dumps of the leaderboard
        """
        if request.method == 'POST':
            try:
                difficulty = request.form['difficulty']
                return self.get_leaderboard(difficulty)
            except KeyError:
                return ""
        else:
            try:
                difficulty = request.args.get('difficulty')
                return self.get_leaderboard(difficulty)
            except KeyError:
                return ""

    @route('/login/<string:username>/<string:password>')
    def login_short(self, username: str, password: str) -> str:
        """
        Description: Route to login user
        :param username: the username of the user to log in
        :param password: the password of the user to log in
        :return: str - new session_id
        """
        return self.login(username, password, "0")

    @route('/login/<string:username>/<string:password>/<string:logout>')
    def login(self, username: str, password: str, logout: str) -> str:
        """
        Description: Route to login user
        :param username: the username of the user to log in
        :param password: the password of the user to log in
        :param logout: whether to logout other users
        :return: str - new session_id
        """
        username = unquote(username)
        password = unquote(password)
        if username_check(username) < 0:
            return "-4"
        database_manager = Database(self.local_storage + "server.db")
        real_pass = database_manager.select("USERS", "password, verified, logged_in, verify_address",
                                            where="username=\'{}\'".format(username))
        if len(real_pass) == 1:
            hashed_pass = hash_password(password, real_pass[0][3])
            if real_pass[0][0] == hashed_pass and real_pass[0][2] == "false" and real_pass[0][1] == "true":
                database_manager.update("USERS", "logged_in=\"true\"", "username=\'{}\'".format(username))
                return self.session_manager.new_session(username)
        if len(real_pass) != 1:
            return "-4"
        hashed_pass = hash_password(password, real_pass[0][3])
        if real_pass[0][0] != hashed_pass:
            return "-4"
        if real_pass[0][1] == "false":
            return "-9"
        if real_pass[0][2] == "true" and real_pass[0][0] == hashed_pass and logout == "1":
            session_id = self.session_manager.get_session_id_from_user(username)
            database_manager.update("USERS", "logged_in=\"false\"", "username=\'{}\'".format(username))
            if session_id != "":
                self.logout(session_id)
        if real_pass[0][2] == "true":
            return "-5"
        return "-3"

    @route('/login', methods=["GET", "POST"])
    def login_get_post(self) -> str:
        """
        Description: Route to login user
        :return: str - new session_id
        """
        if request.method == 'POST':
            try:
                username = request.form['username']
                password = request.form['password']
                return self.login(username, password)
            except KeyError:
                return ""
        else:
            try:
                username = request.args.get('username')
                password = request.args.get('password')
                return self.login(username, password)
            except KeyError:
                return ""

    @route('/logout/<string:session_id>')
    def logout(self, session_id: str) -> str:
        """
        Description: Route to logout user
        :param session_id: the session_id of the user to logout
        :return: str - Null string
        """
        database_manager = Database(self.local_storage + "server.db")
        try:
            username = self.session_manager.get_user(session_id)
        except KeyError:
            return "-6"
        self.session_manager.remove_session(session_id)
        database_manager.update("USERS", "logged_in=\"false\"", "username=\'{}\'".format(username))
        return "-6"

    @route('/logout', methods=["GET", "POST"])
    def logout_get_post(self) -> str:
        """
        Description: Route to logout user
        :return: str - Null string
        """
        if request.method == 'POST':
            try:
                session_id = request.form['session_id']
                return self.logout(session_id)
            except KeyError:
                return ""
        else:
            try:
                session_id = request.args.get('session_id')
                return self.logout(session_id)
            except KeyError:
                return ""

    @route('/reset_password/<string:username>/<string:email>')
    def reset_password(self, username: str, email: str) -> str:
        """
        Description: Route to reset password
        :param username: the username of the account to reset
        :param email: the email of the account to reset
        :return: Null String
        """
        username = unquote(username)
        email = unquote(email)
        if username_check(username) < 0:
            return "1"
        if len(self.logins) != 0:
            time = datetime.utcnow()
            while self.logins[0] < (time - timedelta(minutes=1)):
                del self.logins[0]
        if len(self.logins) < 300:
            database = Database(self.local_storage + "server.db")
            real_email = database.select("USERS", "email, reset_address", where="username=\"{0}\"".format(username))
            if len(real_email) == 1:
                reset = real_email[0][1]
                real_email = real_email[0][0]
                if email.lower().strip() == real_email.lower().strip():
                    url = "https://{0}:{1}/reset/{2}".format(self.ip_address, self.port, reset)
                    self.email_server.send_mail("biztecbritain@gmail.com", email, "Reset your password",
                                                """Welcome to <b>SQUID GAMES</b> Spelling Test, {0}<br>
                                                Please navigate to <a href="{1}">{1}</a> to reset your password<br>
                                                Thank you!""".format(username, url))
                return "1"
            if len(real_email) == 0:
                return "1"
            else:
                return "-3"
        return "-8"

    @route('/reset_password', methods=["GET", "POST"])
    def reset_password_get_post(self) -> str:
        """
        Description: Route to reset password
        :return: Null String
        """
        if request.method == 'POST':
            try:
                username = request.form['username']
                email = request.form['email']
                return self.reset_password(username, email)
            except KeyError:
                return ""
        else:
            try:
                username = request.args.get('username')
                email = request.args.get('email')
                return self.reset_password(username, email)
            except KeyError:
                return ""

    @route('/register_user/<string:username>/<string:password>/<string:email>/<string:captcha_uuid>/<string:captcha>')
    def register_user(self, username: str, password: str, email: str, captcha_uuid: str, captcha: str) -> str:
        """
        Description: Route to register user
        :param username: the username of the account to register
        :param password: the password of the account to register
        :param email: the email of the account to register
        :param captcha_uuid: The uuid of the captcha
        :param captcha: The captcha
        :return: Null String
        """
        username = unquote(username)
        password = unquote(password)
        email = unquote(email)
        captcha = captcha.replace(" ", "")
        if len(self.captchas.keys()) != 0:
            time = datetime.utcnow()
            for captcha_time in list(self.captchas.keys()):
                if captcha_time < (time - timedelta(minutes=1)):
                    del self.captchas[captcha_time]
        captcha_list = list(self.captchas.values())
        found = -1
        for index, captcha_element in enumerate(captcha_list):
            if captcha_element[0] == captcha_uuid:
                found = index
                break
        if found == -1:
            return "-22"
        if captcha_list[found][1].lower() != captcha.lower():
            return "-22"
        login_verify = login_check(username, password)
        email_verify = email_check(email)
        if login_verify < 0:
            return str(login_verify)
        if email_verify < 0:
            return str(email_verify)
        password = hash_password(password, username)
        if len(self.logins) != 0:
            time = datetime.utcnow()
            while self.logins[0] < (time - timedelta(minutes=1)):
                del self.logins[0]
        if len(self.logins) < 300:
            database_manager = Database(self.local_storage + "server.db")
            salt = uuid_generator(32)
            try:
                database_manager.insert("USERS", [username, hash_password(password, salt), email, "false",
                                                  "false", salt, uuid_generator(32)])
                url = "https://{0}:{1}/verify/{2}".format(self.ip_address, self.port, salt)
                self.email_server.send_mail("biztecbritain@gmail.com", email, "Verify your email address",
                                            """Welcome to <b>SQUID GAMES</b> Spelling Test, {0}<br>
                                            Please navigate to <a href="{1}">{1}</a> to finish your account setup<br>
                                            Thank you for signing up!""".format(username, url))
                return "1"
            except sqlite3.IntegrityError as e:
                if "username" in str(e):
                    return "-10"
                elif "email" in str(e):
                    return "-11"
                else:
                    return "-3"
        else:
            return "-8"

    @route('/register_user', methods=["GET", "POST"])
    def register_user_get_post(self) -> str:
        """
        Description: Route to register user
        :return: Null String
        """
        if request.method == 'POST':
            try:
                username = request.form['username']
                password = request.form['password']
                email = request.form['email']
                captcha_uuid = request.form['captcha_uuid']
                captcha = request.form['captcha']
                return self.register_user(username, password, email, captcha_uuid, captcha)
            except KeyError:
                return ""
        else:
            try:
                username = request.args.get('username')
                password = request.args.get('password')
                email = request.args.get('email')
                captcha_uuid = request.args.get('captcha_uuid')
                captcha = request.args.get('captcha')
                return self.register_user(username, password, email, captcha_uuid, captcha)
            except KeyError:
                return ""

    @route('/get_audio/<string:difficulty>/<string:session_id>')
    def get_audio(self, difficulty: str, session_id: str) -> Response:
        """
        Description: Route to download the audio
        :param difficulty: the difficulty of the wordlist
        :param session_id: the session_id of the user
        :return: Response - the requested file and new session_id in the header
        """
        status, new_session_id = self.session_manager.validate_session(session_id, 30)
        if status == 1:
            if not chars_only(difficulty) or difficulty not in ["easy", "medium", "hard"]:
                response = make_response()
                response.headers['session_id'] = new_session_id
                response.headers['error'] = -7
                return response
            database_manager = Database(self.local_storage + "server.db")
            if self.session_manager.sessions[new_session_id][1] is None:
                wordlist = database_manager.select("WORDLIST", "word, definition",
                                                   where="category=\"{0}\"".format(difficulty))
                definitions = {element[0]: element[1] for element in wordlist}
                wordlist = [element[0] for element in wordlist]
                random.shuffle(wordlist)
                wordlist = wordlist[:10]
                definitions = [definitions[element] for element in wordlist]
                self.session_manager.new_game(new_session_id, wordlist, definitions, difficulty, self.local_storage)
            elif self.session_manager.sessions[new_session_id][1].difficulty != difficulty:
                response = make_response()
                response.headers['session_id'] = new_session_id
                response.headers['error'] = -7
                response.headers['definition'] = ""
                return response
            word, definition = self.session_manager.sessions[new_session_id][1].next_word()
            filename = database_manager.select("WORDLIST", "file_name", where="word=\"{0}\"".format(word))[0][0]
            response = make_response(send_file('..\\' + self.local_storage.replace("/", "\\") + 'audio\\' + filename))
            response.headers['session_id'] = new_session_id
            response.headers['error'] = 0
            response.headers['definition'] = definition
            return response
        else:
            response = make_response()
            response.headers['session_id'] = new_session_id
            response.headers['error'] = status
            response.headers['definition'] = ""
            self.logout(session_id)
            return response

    @route('/get_audio', methods=["GET", "POST"])
    def get_audio_get_post(self) -> Response:
        """
        Description: Route to download the audio
        :return: Response - the requested file and new session_id in the header
        """
        if request.method == 'POST':
            try:
                difficulty = request.form['difficulty']
                session_id = request.form['session_id']
                return self.get_audio(difficulty, session_id)
            except KeyError:
                return make_response("")
        else:
            try:
                difficulty = request.args.get('difficulty')
                session_id = request.args.get('session_id')
                return self.get_audio(difficulty, session_id)
            except KeyError:
                return make_response("")

    @route('/submit_answer/<string:session_id>/<string:answer>')
    def submit_answer(self, session_id: str, answer: str) -> Response:
        """
        Description: Constructor sets up attributes including objects
        :param session_id: the session_id to submit the answer to
        :param answer: the answer that is submitted
        :return: Response - if the question was correct and new session_id in the header
        """
        answer = unquote(answer).replace(" ", "")
        answer = ''.join(e for e in answer if e.isalpha())
        status, new_session_id = self.session_manager.validate_session(session_id, 30)
        if status == 1:
            correct, word = self.session_manager.sessions[new_session_id][1].check(answer)
            self.session_manager.sessions[new_session_id][1].end()
            if correct:
                response = make_response("1", 200)
            else:
                response = make_response("0", 200)
            delete_game = False
            if self.session_manager.sessions[new_session_id][1].get_finished():
                time = self.session_manager.sessions[new_session_id][1].difference()
                response.headers['time'] = time
                database_manager = Database(self.local_storage + "server.db")
                username = self.session_manager.sessions[new_session_id][0].get_user()
                score = self.session_manager.sessions[new_session_id][1].get_score()
                avg_time = str(round(1000 * time / self.session_manager.sessions[new_session_id][1].get_total_q()))
                now = datetime.now()
                date_time = now.strftime("%d/%m/%Y")
                difficulty = self.session_manager.sessions[new_session_id][1].difficulty
                database_manager.insert("LEADERBOARD", [username, score, avg_time, date_time, difficulty])
                delete_game = True
            else:
                response.headers['time'] = "not finished"
            response.headers['score'] = self.session_manager.sessions[new_session_id][1].get_score()
            response.headers['correct'] = self.session_manager.sessions[new_session_id][1].get_correct()
            response.headers['session_id'] = new_session_id
            response.headers['error'] = 0
            response.headers['prev_word'] = word.lower()
            if delete_game:
                self.session_manager.sessions[new_session_id][1] = None
            return response
        else:
            response = make_response()
            response.headers['session_id'] = new_session_id
            response.headers['error'] = status
            self.logout(session_id)
            return response

    @route('/submit_answer', methods=["GET", "POST"])
    def submit_answer_get_post(self) -> Response:
        """
        Description: Constructor sets up attributes including objects
        :return: Response - if the question was correct and new session_id in the header
        """
        if request.method == 'POST':
            try:
                session_id = request.form['session_id']
                answer = request.form['answer']
                return self.submit_answer(session_id, answer)
            except KeyError:
                return make_response("")
        else:
            try:
                session_id = request.args.get('session_id')
                answer = request.args.get('answer')
                return self.submit_answer(session_id, answer)
            except KeyError:
                return make_response("")

    @route('/end_game/<string:session_id>')
    def end_game(self, session_id: str) -> str:
        """
        Description: Constructor sets up attributes including objects
        :param session_id: the session_id to submit the answer to
        :return: str - new session_id
        """
        status, new_session_id = self.session_manager.validate_session(session_id, 30)
        if status == 1:
            self.session_manager.sessions[new_session_id][1] = None
        else:
            self.logout(session_id)
        return new_session_id

    @route('/submit_answer', methods=["GET", "POST"])
    def end_game_get_post(self) -> str:
        """
        Description: Constructor sets up attributes including objects
        :return: str - new session_id
        """
        if request.method == 'POST':
            try:
                session_id = request.form['session_id']
                return self.end_game(session_id)
            except KeyError:
                return ""
        else:
            try:
                session_id = request.args.get('session_id')
                return self.end_game(session_id)
            except KeyError:
                return ""

    @route('/establish_connection')
    def establish_connection(self) -> str:
        """
        Description: Route to verify that the server is running
        :return: str - Null string
        """
        return "1"

    @route('/establish_connection/<string:session_id>')
    def establish_connection_session_id(self, session_id: str) -> str:
        """
        Description: Route to verify that the server is running
        :param session_id: the session id of the previous session
        :return: str - Logged in verification
        """
        resp, new_session_id = self.session_manager.validate_session(session_id)
        if resp == 1:
            return new_session_id
        else:
            return "1"

    @route('/verify/<string:verify_id>')
    def verify(self, verify_id: str) -> str:  # TODO create webpages
        """
        Description: Route to display the webpage to verify email
        :param verify_id: the verify id of the username
        :return: Null String
        """
        if not lettersnumbers_only(verify_id):
            return "Invalid id"
        database_manager = Database(self.local_storage + "server.db")
        resp = database_manager.select("USERS", "username", where="verify_address=\"{0}\"".format(verify_id))
        if len(resp) == 1:
            database_manager.update("USERS", "verified=\"true\"", "username=\"{0}\"".format(resp[0][0]))
            return "Verified"
        return "Invalid id"

    @route('/reset/<string:reset_id>')
    def reset(self, reset_id: str) -> str:
        """
        Description: Route to display the page to reset the password
        :param reset_id: the reset id of the username
        :return: Null String
        """
        if not lettersnumbers_only(reset_id):
            return "Invalid id"
        database_manager = Database(self.local_storage + "server.db")
        resp = database_manager.select("USERS", "username", where="reset_address=\"{0}\"".format(reset_id))
        if len(resp) == 1:
            return render_template("html/reset password.html")
        return "Invalid id"

    @route('/reset/<string:reset_id>/<string:new_pass>')
    def actual_reset(self, reset_id: str, new_pass: str) -> Response:
        """
        Description: Route to actually reset the password
        :param reset_id: the reset id of the username
        :param new_pass: the new password for user
        :return: Response - redirect to correct finish page
        """
        new_pass = unquote(new_pass)
        if not lettersnumbers_only(reset_id):
            return redirect(url_for('FlaskServer:wrong_reset'))
        database_manager = Database(self.local_storage + "server.db")
        resp = database_manager.select("USERS", "username, verify_address",
                                       where="reset_address=\"{0}\"".format(reset_id))
        if len(resp) == 1:
            database_manager.update("USERS", "reset_address=\"{0}\"".format(uuid_generator(32)),
                                    "username=\"{0}\"".format(resp[0][0]))
            if login_check(resp[0][0], new_pass) > 0:
                password = hash_password(new_pass, resp[0][0])
            else:
                return redirect(url_for('FlaskServer:wrong_reset_password'))
            password = hash_password(password, resp[0][1])
            database_manager.update("USERS", "password=\"{0}\"".format(password),
                                    "username=\"{0}\"".format(resp[0][0]))
            return redirect(url_for('FlaskServer:done_reset'))
        return redirect(url_for('FlaskServer:wrong_reset'))

    @route('/reset_complete')
    def done_reset(self) -> str:
        """
        Description: Route to show success of reset password
        :return: Null String
        """
        return "Done"

    @route('/reset_invalid')
    def wrong_reset(self) -> str:
        """
        Description: Route to show failure of reset password
        :return: Null String
        """
        return "Invalid id"

    @route('/reset_password_invalid')
    def wrong_reset_password(self) -> str:
        """
        Description: Route to show failure of reset password
        :return: Null String
        """
        return "Invalid Password"

    @route('/restart/<string:password>')
    def restart(self, password: str) -> Response:
        """
        Description: Route for admins to remotely restart the server
        :return: Response - Null string
        """
        password = hash_password(password)
        if password == '5c544166cf46c4de255e39d09413499e0c954f8edb2233b6d9dfcc172401413d':
            self.main_app.reset()
            return make_response("200", 200)
        return make_response("401", 401)

    @route('/stop/<string:password>')
    def stop(self, password: str) -> Response:
        """
        Description: Route for admins to remotely stop the server
        :return: Response - Null string
        """
        password = hash_password(password)
        if password == '5c544166cf46c4de255e39d09413499e0c954f8edb2233b6d9dfcc172401413d':
            self.main_app.clean_exit()
            return make_response("200", 200)
        return make_response("401", 401)

    @route('request_captcha/<string:ratio>')
    def request_captcha(self, ratio: str) -> Response:
        """
        Description: Route to get a Captcha image
        :param ratio: the ratio to resize the image
        :return: Response - the serialised image and headers
        """
        if len(self.captchas.keys()) != 0:
            time = datetime.utcnow()
            for captcha in list(self.captchas.keys()):
                if captcha < (time - timedelta(minutes=1)):
                    del self.captchas[captcha]
        if len(self.captchas.keys()) < 300:
            ratio = float(ratio)
            uuid = uuid_generator(8)
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            time = datetime.utcnow()
            self.captchas[time] = [uuid, random_string, time]
            image_captcha = ImageCaptcha(width=int(250 * ratio), height=int(125 * ratio))
            image_generated = image_captcha.generate(random_string)
            resp = pickle.dumps(image_generated)
            response = make_response(str(resp))
            response.headers['uuid'] = uuid
            return response
        return make_response("-8")

    @route("/download_zip")
    def download_zip(self) -> Response:
        return send_file("spelling_test.zip")

    @route("/download_storage")
    def download_storage(self) -> Response:
        return send_file("spelling_test.zip")

    @route("/download")
    def download(self) -> Response:
        return send_file("../Spelling Test Installer.exe", as_attachment=True)


if __name__ == "__main__":
    app = Flask(__name__)
    FlaskServer.local_storage = "../local_storage/"
    FlaskServer.create_tables()
    FlaskServer.logout_all()
    FlaskServer.download_files()
    FlaskServer.register(app)
    app.run(host='localhost')

__all__ = ['SessionManager', 'ClientSessionManagement', 'Session']
__version__ = '2.3.1'
__author__ = 'Alexander Bisland'

from .security import uuid_generator
from data_management.game import Game
from data_management.config import Config
from datetime import datetime, timedelta
from typing import Tuple, List


class SessionManager:
    def __init__(self) -> None:
        """
        Description: Constructor sets up attributes
        :return: void
        """
        self.sessions = {}
        self.errors = {-1: "Invalid Session ID",
                       -2: "Session timed out",
                       -3: "Unknown Server Error",
                       -4: "Incorrect password",
                       -5: "Already logged in",
                       -6: "Logged out",
                       -7: "Invalid difficulty",
                       -8: "Too many requests! Try again later!",
                       -9: "Not verified",
                       -10: "Username already exists",
                       -11: "Email already in use",
                       -12: "The length of the password must be greater than 6",
                       -13: "The length of the password must be less than 15",
                       -14: "The length of the username must be less than 8",
                       -15: "The length of the username must be greater than 4",
                       -16: "The password must contain one number",
                       -17: "The password must contain one uppercase letter",
                       -18: "The password must contain one lowercase letter",
                       -19: "The password must contain at least 1 symbol",
                       -20: "Invalid Email",
                       -21: "Invalid username or password",
                       -22: "Invalid captcha",
                       -23: "Invalid Parameters"}

    def new_session(self, user_id: str) -> str:
        """
        Description: Creates a new session object, stores it and reurns the uuid
        :param user_id: the id of the user requesting the session
        :return: str - the sessions uuid
        """
        session = Session(user_id)
        self.sessions[session.uuid] = [session, None]
        return session.uuid

    def validate_session(self, session_id: str, timeout: int = 5) -> Tuple[int, str]:
        """
        Description: Checks if a session is still valid and returns a new session_id
        :param session_id: the id of the session to validate
        :param timeout: the timeout for the session in minutes
        :return: tuple[int, str] - (status, new_session_id)
        """
        if session_id in self.sessions.keys():
            if self.sessions[session_id][0].timeout(timeout):
                self.sessions[session_id][0].new_session_id()
                uuid = self.sessions[session_id][0].uuid
                self.sessions[uuid] = self.sessions.pop(session_id)
                return 1, uuid
            return -2, self.errors[-2]
        return -1, self.errors[-1]

    def get_user(self, session_id: str) -> str:
        """
        Description: Gets the user_id from a session_id
        :param session_id: the id of the session
        :return: str - the user_id
        """
        return self.sessions[session_id][0].get_user()

    def new_game(self, session_id: str, wordlist: List[str], category: str, local_storage: str) -> None:
        """
        Description: Creates a new game object for a session
        :param session_id: the id of the session
        :param wordlist: the list of words for the game
        :param category: the difficulty of the wordlist
        :param local_storage: th path to local storage
        :return: void
        """
        self.sessions[session_id][1] = Game(wordlist, category, local_storage)

    def remove_session(self, session_id: str) -> None:
        """
        Description: Removes a session from the current sessions (eg if a user logs out)
        :param session_id: the session id of the session to delete
        :return: void
        """
        del self.sessions[session_id]

    def get_session_id_from_user(self, user: str) -> str:
        """
        Description: Gets the session_id from the username
        :param user: the username
        :return: str - the session_id
        """
        for value in self.sessions.values():
            if value[0].get_user() == user:
                return value[0].uuid
        return ""


class ClientSessionManagement:
    def __init__(self) -> None:
        """
        Description: Constructor sets up attributes including objects
        :return: void
        """
        self._config_manager = Config()
        self._config_manager.load("local_storage/client.ini")
        self.__session_id = None
        self.error = False
        self.errors = {-1: "Invalid Session ID",
                       -2: "Session timed out",
                       -3: "Unknown Internal Server Error",
                       -4: "Incorrect password",
                       -5: "Already logged in",
                       -6: "Logged out",
                       -7: "Invalid difficulty",
                       -8: "Too many requests! Try again later!",
                       -9: "Not verified",
                       -10: "Username already exists",
                       -11: "Email already in use",
                       -12: "The length of the password must be greater than 6",
                       -13: "The length of the password must be less than 15",
                       -14: "The length of the username must be less than 8",
                       -15: "The length of the username must be greater than 4",
                       -16: "The password must contain one number",
                       -17: "The password must contain one uppercase letter",
                       -18: "The password must contain one lowercase letter",
                       -19: "The password must contain at least 1 symbol",
                       -20: "Invalid Email",
                       -21: "invalid username or password",
                       -22: "Invalid captcha",
                       -23: "Invalid Parameters"}

    def update(self, session_id: str) -> int:
        """
        Description: Updates your session_id
        :param session_id: new session_id
        :return: int - status
        """
        self.__session_id = session_id
        if session_id is None:
            self.error = True
            return 0
        else:
            self.error = False
            self._config_manager.append_tag("USERINFO", 'session_id', str(session_id))
            return 1

    def get_session_id(self) -> str:
        """
        Description: gets the current session_id
        :return: str - the session_id
        """
        return self.__session_id


class Session:
    def __init__(self, user_id: str) -> None:
        """
        Description: Constructor sets up attributes
        :param user_id: the user_id of the owner of the session
        :return: void
        """
        self.__starttime = datetime.utcnow()
        self.__timeout = timedelta(minutes=5)
        self.__user_id = user_id
        self.uuid = uuid_generator()

    def new_session_id(self) -> None:
        """
        Description: Generates a new session_id
        :return: void
        """
        self.uuid = uuid_generator()

    def get_user(self) -> str:
        """
        Description: Gets the user_id of the owner of the session
        :return: str - the user_id of the owner of the session
        """
        return self.__user_id

    def timeout(self, new_timeout: int = 5) -> bool:
        """
        Description: Fuction to check if the session has timed out
        :param new_timeout: the new timeout in minutes
        :return: bool - if the session is still valid
        """
        newtime = datetime.utcnow()
        if self.__timeout != -1:
            if (self.__starttime + self.__timeout) < newtime:
                self.__timeout = timedelta(minutes=new_timeout)
                self.__starttime = newtime
                return False
            self.__timeout = timedelta(minutes=new_timeout)
            self.__starttime = newtime
            return True
        else:
            self.__timeout = timedelta(minutes=new_timeout)
            self.__starttime = newtime
            return True

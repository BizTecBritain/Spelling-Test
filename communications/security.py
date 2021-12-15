__all__ = ['hash_password', 'uuid_generator', 'login_check', 'email_check', 'username_check', 'password_check',
           'chars_only', 'hex_only', 'lettersnumbers_only', 'make_chars_only']
__version__ = '1.3.1'
__author__ = 'Daniel Hart'

import string
import random
import hashlib
import re


def hash_password(password: str, salt: str = "salt", iterations: int = 900000) -> str:
    """
    Description: Hashes a given password for security
    :param password: the password to hash
    :param salt: the salt to use
    :param iterations: the amount of iterations (at least 100,000)
    :return: str - the hashed password
    """
    password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations).hex()
    return password


def uuid_generator(size: int = 16, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase) -> str:
    """
    Description: Generates a random, unique string of spicified length
    :param size: [Optional] the length of the random string
    :param chars: [Optional] the characters to include
    :return: str - the random string
    """
    return ''.join(random.choice(chars) for _ in range(size))


def login_check(username: str, password: str) -> int:
    """
    Description: Function to verify if a username and password are valid
    :param username: the username to check
    :param password: the password to check
    :return: int - error code or 1 if success
    """
    username_verif = username_check(username)
    if username_verif < 0:
        return username_verif

    password_verif = password_check(password)
    return password_verif


def username_check(username: str) -> int:
    """
    Description: Function to check if a username complies to the standard
    :param username: the username to check
    :return: int - error code or 1 if success
    """
    username_sym = string.ascii_letters + string.digits + '._-'

    if len(username) > 8:
        return -14
    if len(username) < 4:
        return -15
    if any(char not in username_sym for char in username):
        return -21
    return 1


def password_check(password: str) -> int:
    """
    Description: Function to check if a password complies to the standard
    :param password: the password to check
    :return: int - error code or 1 if success
    """
    special_sym = '$@#%?!£*)(,./~{}:|;_-'
    password_sym = string.ascii_letters + string.digits + special_sym

    if len(password) < 6:
        return -12
    if len(password) > 15:
        return -13
    if not any(char.isdigit() for char in password):
        return -16
    if not any(char.isupper() for char in password):
        return -17
    if not any(char.islower() for char in password):
        return -18
    if not any(char in special_sym for char in password):
        return -19
    if any(char not in password_sym for char in password):
        return -21
    return 1


def email_check(user_email: str) -> int:
    """
    Description: Function to verify the email
    :param user_email: the email to check
    :return: int - error code or 1 if success
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(pattern, user_email):
        return 1
    return -20


def chars_only(word: str) -> bool:
    """
    Description: Function to return whether or not a string contains only letters
    :param word: the word to check
    :return: bool - whether or not a string contains only letters
    """
    if any(char not in string.ascii_letters for char in word):
        return False
    return True


def hex_only(word: str) -> bool:
    """
    Description: Function to return whether or not a string contains only hex digits (for a  hash)
    :param word: the word to check
    :return: bool - whether or not a string contains only hex digits
    """
    if any(char not in string.hexdigits for char in word):
        return False
    return True


def lettersnumbers_only(word: str) -> bool:
    """
    Description: Function to return whether or not a string contains only letters or numbers
    :param word: the word to check
    :return: bool - whether or not a string contains only letters or numbers
    """
    if any(char not in string.ascii_letters+string.digits for char in word):
        return False
    return True


def make_chars_only(sentence: str) -> str:
    """
    Description: Function to make a sentence letters only
    :param sentence: the sentence to convert
    :return: str - the new sentence
    """
    allowed = string.ascii_letters+string.digits+" ?,;."
    return "".join(e for e in sentence if e in allowed)

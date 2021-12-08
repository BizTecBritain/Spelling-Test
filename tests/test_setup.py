from data_management.database import Database
import os
from communications.security import uuid_generator, hash_password
import random
from PyDictionary import PyDictionary

try:
    os.remove('local_storage/server.db')
except FileNotFoundError:
    pass
database_manager = Database('local_storage/server.db')

with open("local_storage/sql_commands/create_users.txt", "r") as f:
    database_manager.create_table("USERS", f.readlines()[0].strip())
with open("local_storage/sql_commands/create_leaderboard.txt", "r") as f:
    database_manager.create_table("LEADERBOARD", f.readlines()[0].strip())
with open("local_storage/sql_commands/create_wordlist.txt", "r") as f:
    database_manager.create_table("WORDLIST", f.readlines()[0].strip())

uuid_1 = uuid_generator(32)
uuid_2 = uuid_generator(32)
uuid_3 = uuid_generator(32)
database_manager.insert("USERS", ["username", hash_password(hash_password("password", "username"), uuid_1),
                                  "biztecbritain@gmail.com", "true", "true", uuid_1, uuid_generator(32)])
database_manager.insert("USERS", ["username2", hash_password(hash_password("password2", "username2"), uuid_2),
                                  "email2@gmail.com", "false", "true", uuid_2, uuid_generator(32)])
database_manager.insert("USERS", ["username3", hash_password(hash_password("password3", "username3"), uuid_3),
                                  "email3@gmail.com", "true", "false", uuid_3, uuid_generator(32)])

with open("local_storage/wordlists/easy.txt") as f:
    easy = f.readlines()
    random.shuffle(easy)
with open("local_storage/wordlists/medium.txt") as f:
    medium = f.readlines()
    random.shuffle(medium)
with open("local_storage/wordlists/hard.txt") as f:
    hard = f.readlines()
    random.shuffle(hard)

dictionary = PyDictionary()

for i in range(30):
    easy_t = easy[i].strip()
    easy_d_tmp = dictionary.meaning(easy_t)
    try:
        easy_d = ", ".join(easy_d_tmp[list(easy_d_tmp.keys())[0]]).replace(easy_t, "?")
    except AttributeError:
        easy_d = ""
    med_t = medium[i].strip()
    med_d_tmp = dictionary.meaning(med_t)
    try:
        med_d = ", ".join(med_d_tmp[list(med_d_tmp.keys())[0]]).replace(med_t, "?")
    except AttributeError:
        med_d = ""
    hard_t = hard[i].strip()
    hard_d_tmp = dictionary.meaning(hard_t)
    try:
        hard_d = ", ".join(hard_d_tmp[list(hard_d_tmp.keys())[0]]).replace(hard_t, "?")
    except AttributeError:
        hard_d = ""
    database_manager.insert("WORDLIST", [uuid_generator()+".mp3", "easy", easy_t, easy_d, 0, 0])
    database_manager.insert("WORDLIST", [uuid_generator()+".mp3", "medium", med_t, med_d, 0, 0])
    database_manager.insert("WORDLIST", [uuid_generator()+".mp3", "hard", hard_t, hard_d, 0, 0])

print(database_manager.select("USERS", "*"))
print(database_manager.select("LEADERBOARD", "*"))
print(database_manager.select("WORDLIST", "*"))

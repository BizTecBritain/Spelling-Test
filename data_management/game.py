__all__ = ['Game']
__version__ = '1.2.1'
__author__ = 'Alexander Bisland'

from datetime import datetime
from typing import List, Tuple
from data_management import Database


class Game:
    def __init__(self, wordlist: List[str], definitions: List[str], difficulty: str, local_storage: str) -> None:
        """
        Description: Constructor sets up attributes
        :param wordlist: the list of words for the game
        :param difficulty: the difficulty of the game
        :param definitions: the list of definitions for the words
        :param local_storage: the path for local storage
        :return: void
        """
        self.__start = datetime.utcnow()
        self.__prev_time = datetime.utcnow()
        self.__end = None
        self.__wordlist = wordlist
        self.__definitions = definitions
        self.__index = 0
        self.__score = 0
        self.__correct = 0
        self.difficulty = difficulty
        self.__finished = False
        self.local_storage = local_storage

    def end(self) -> None:
        """
        Description: Fuction that is run when the game is over to stop the timer
        :return: void
        """
        if self.__end is None and self.__index == len(self.__wordlist):
            self.__end = datetime.utcnow()
            self.__finished = True
        elif self.__end is not None:
            raise RuntimeError("The timer has already been stopped")

    def difference(self) -> int:
        """
        Description: Function that returns the time taken to play the game
        :return: int - the time taken to play the game
        """
        if self.__end is not None:
            return (self.__end - self.__start).total_seconds()
        raise RuntimeError("The timer has not ended yet")

    def next_word(self) -> Tuple[str, str]:
        """
        Description: Function that returns the next word in the list
        :return: Tuple[str, str] - the next word in the list and its definition
        """
        if not self.__finished:
            word = self.__wordlist[self.__index]
            definition = self.__definitions[self.__index]
            self.__index += 1
            return word, definition
        return "", ""

    def check(self, answer: str) -> Tuple[bool, str]:
        """
        Description: Function used to verify if the user input was correct
        :param answer: the users answer
        :return: Tuple[bool, str] - boolean to show if it was correct or not and the word
        """
        bonus = 0
        if (datetime.utcnow() - self.__prev_time).total_seconds() < 5:
            bonus = 5
        self.__prev_time = datetime.utcnow()
        word = ""
        if not self.__finished:
            word = self.__wordlist[self.__index-1]
            database = Database(self.local_storage + "server.db")
            prev_answered = int(database.select("WORDLIST", "answered", where="word=\"{0}\"".format(word))[0][0])
            database.update("WORDLIST", "answered=\"{0}\"".format(prev_answered+1), "word=\"{0}\"".format(word))
            if word.lower() == answer.lower():
                prev_correct = int(database.select("WORDLIST", "correct", where="word=\"{0}\"".format(word))[0][0])
                database.update("WORDLIST", "correct=\"{0}\"".format(prev_correct + 1), "word=\"{0}\"".format(word))
                print(database.select("WORDLIST", "*"))
                self.__score += 5 + bonus
                self.__correct += 1
                return True, word
        return False, word

    def get_score(self) -> int:
        """
        Description: Function to return the current score
        :return: int - the current score
        """
        return self.__score

    def get_correct(self) -> int:
        """
        Description: Function to return the current number of correct questions
        :return: int - the current number of correct questions
        """
        return self.__correct

    def get_finished(self) -> bool:
        """
        Description: Function used to test if the game is finished
        :return: bool - boolean showing if the game is finished
        """
        return self.__finished

    def get_total_q(self) -> int:
        """
        Description: Function to get the total number of questions
        :return: void
        """
        return len(self.__wordlist)

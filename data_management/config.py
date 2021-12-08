from __future__ import annotations

__all__ = ['Config']
__version__ = '1.2.7'
__author__ = 'Alexander Bisland'

from configparser import ConfigParser, SectionProxy
from typing import List


class Config:
    def __init__(self) -> None:
        """
        Description: Constructor sets up attributes including objects
        :return: void
        """
        self.config_object = ConfigParser()
        self.loaded = False
        self.file = ""

    class Decorator:
        @staticmethod
        def file_decorator(fnc):
            def inner(objecta, *args, file=""):
                if file != "":
                    objecta.file = file
                    objecta.loaded = False
                return fnc(objecta, *args)
            return inner

    def load(self, file: str) -> None:
        """
        Description: Function to load a config file (.ini) for later use
        :param file: The file to load
        :return: void
        """
        self.config_object.read(file)
        self.loaded = True
        self.file = file

    @Decorator.file_decorator
    def overwrite(self, section: str, dictionary: dict[str:str]) -> None:
        """
        Description: Function to (over)write a config file (.ini)
        :param section: the section of the file to (over)write
        :param dictionary: the dictionary to overwrite with
        :return: void
        """
        if self.file != "":
            self.config_object[section] = dictionary
            with open(self.file, 'w') as file:
                self.config_object.write(file)

    @Decorator.file_decorator
    def append_section(self, section: str, dictionary: dict[str:str]) -> None:
        """
        Description: Function that allows you to append a dictionary to a section of the file
        :param section: the section of the file to append to
        :param dictionary: the dictionary to overwrite with in the format {tag:value}
        :return: void
        """
        if not self.loaded:
            self.load(self.file)
        self.config_object[section] = dictionary
        with open(self.file, 'w') as file:
            self.config_object.write(file)

    @Decorator.file_decorator
    def append_sections(self, sections: List[str], list_of_dictionaries: List[dict[str:str]]) -> None:
        """
        Description: Function that allows you to append multiple dictionaries to multiple sections of the file
        :param sections: the list of sections of the file to append to
        :param list_of_dictionaries: the list of dictionaries to overwrite with
        :return: void
        """
        for i in range(len(sections)):
            self.append_section(sections[i], list_of_dictionaries[i])

    @Decorator.file_decorator
    def append_tag(self, section: str, tag: str, string: str) -> None:
        """
        Description: Function that allows you to append a tag to a section of the file
        :param section: the section of the file to append to
        :param tag: the tag of the section to append to
        :param string: the string to add to that tag
        :return: void
        """
        if not self.loaded:
            self.load(self.file)
        self.config_object[section][tag] = string
        with open(self.file, 'w') as file:
            self.config_object.write(file)

    @Decorator.file_decorator
    def append_tags(self, section: str, tags: List[str], strings: List[str]) -> None:
        """
        Description: Function that allows you to append multiple tags to a section of the file
        See: Config.append_section()
        :param section: the section of the file to append to
        :param tags: a list of the tags of the section to append to
        :param strings: a list of the strings to add to the tags
        :return: void
        """
        for i in range(len(tags)):
            self.append_tag(section, tags[i], strings[i])

    @Decorator.file_decorator
    def read_section_object(self, section: str) -> SectionProxy:
        """
        Description: Function to get a whole config section in the form of a SectionProxy object
        :param section: the section to read from
        :return: configparser.SectionProxy - the object to access the section
        """
        if not self.loaded:
            self.load(self.file)
        return self.config_object[section]

    @Decorator.file_decorator
    def read_tag(self, section: str, tag: str) -> str:
        """
        Description: Function that gets the value of a specified tag in a section
        :param section: the section to read from
        :param tag: the tag to read
        :return: str - the tag that has been read
        """
        if not self.loaded:
            self.load(self.file)
        return self.config_object[section][tag]


if __name__ == "__main__":
    a = Config()
    a.overwrite("USERINFO", {'admin': 'Chankey Pathak',
                             'password': 'tutswiki',
                             'loginid': 'chankeypathak'}, file="testconfig.ini")
    a.append_section("SERVERCONFIG", {'host': 'tutswiki.com'})
    a.append_tag("SERVERCONFIG", 'ipaddr', '8.8.8.8')
    a.append_tags("SERVERCONFIG", ['port1', 'host'], ['5000', '8080'])
    print(a.read_section_object("USERINFO"))
    print(a.read_tag("USERINFO", "admin"))
    print(a.read_tag("TOKEN", "admin"))

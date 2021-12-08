from __future__ import annotations

__all__ = ['DataChannel']
__version__ = '1.0.0'
__author__ = 'Alexander Bisland'

import os

import requests
from .security import uuid_generator
import urllib3
from typing import Tuple

urllib3.disable_warnings()


class DataChannel:
    def __init__(self, ip_address, port):
        """
        Description: Constructor sets up attributes
        :return: void
        """
        self.ip_address = ip_address
        self.port = str(port)

    def establish_connection(self, session_id: str = None) -> str:
        """
        Description: Establishes a connection and gains a session id
        :param session_id: [Optional] The old session_id if there is one
        :return: int - status of the server
        """
        error = False
        value = "1"
        try:
            if session_id is not None:
                resp = requests.get("https://"+self.ip_address+":"+self.port+"/establish_connection/"+session_id,
                                    verify=False)
            else:
                resp = requests.get("https://"+self.ip_address+":"+self.port+"/establish_connection",
                                    verify=False)
            if resp.status_code != 200:
                error = True
            if resp.text != "1":
                value = resp.text
        except requests.ConnectionError:
            try:
                requests.get("https://google.com")
                error = True
            except requests.ConnectionError:
                raise ConnectionError("Can\'t connect to internet! Check your connection!")
        if error:
            raise ConnectionError("Can\'t connect to server! Try again later!")
        return value

    def download_file(self, address: str, *, folder: str = 'local_storage/word_audio/', file: str = None,
                      params: dict[str:str] = None) -> Tuple[str, dict[str:str]]:
        """
        Description: Downloads a file from website
        :param address: the address of the website to request eg "login" for https://ip_address:port/login
        :param folder: [Optional] the folder to write to
        :param file: [Optional] the file to write to
        :param params: [Optional] the parameters to send with the request
        :return: str - filename
        """
        if file is None:
            file = folder + uuid_generator() + '.mp3'
        resp = requests.get("https://" + self.ip_address + ":" + self.port + "/" + address, params=params,
                            verify=False)
        if resp.status_code == 200:
            with open(file, 'wb') as f:
                f.write(resp.content)
            return os.path.abspath(file), resp.headers

    def get_json(self, address: str, params: dict[str:str] = None) -> dict[str:str]:
        """
        Description: gets json response from website
        See: get_json_headers
        :param address: the address of the website to request eg "login" for https://ip_address:port/login
        :param params: [Optional] the parameters to send with the request
        :return: dict[str:str] - json response as a dictionary
        """
        resp = requests.get("https://" + self.ip_address + ":" + self.port + "/" + address, params=params,
                            verify=False)
        if resp.status_code == 200:
            return resp.json()

    def get_text(self, address: str, params: dict[str:str] = None) -> str:
        """
        Description: gets text response from website
        See: get_text_headers
        :param address: the address of the website to request eg "login" for https://ip_address:port/login
        :param params: [Optional] the parameters to send with the request
        :return: str - text response
        """
        resp = requests.get("https://" + self.ip_address + ":" + self.port + "/" + address, params=params,
                            verify=False)
        if resp.status_code == 200:
            return resp.text

    def get_json_headers(self, address: str, params: dict[str:str] = None) -> Tuple[dict[str:str], dict[str:str]]:
        """
        Description: gets json response from website and the headers
        See: get_json
        :param address: the address of the website to request eg "login" for https://ip_address:port/login
        :param params: [Optional] the parameters to send with the request
        :return: dict[str:str] - json response as a dictionary
        """
        resp = requests.get("https://" + self.ip_address + ":" + self.port + "/" + address, params=params,
                            verify=False)
        if resp.status_code == 200:
            return resp.json(), resp.headers

    def get_text_headers(self, address: str, params: dict[str:str] = None) -> Tuple[str, dict[str:str]]:
        """
        Description: gets text response from website and the headers
        See: get_text
        :param address: the address of the website to request eg "login" for https://ip_address:port/login
        :param params: [Optional] the parameters to send with the request
        :return: str - text response
        """
        resp = requests.get("https://" + self.ip_address + ":" + self.port + "/" + address, params=params,
                            verify=False)
        if resp.status_code == 200:
            return resp.text, resp.headers

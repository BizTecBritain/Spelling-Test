__all__ = ['Server']
__version__ = '1.0.3'
__author__ = 'Alexander Bisland'

import os

from .flask_app import FlaskServer
from flask import Flask, request


class Server:
    def __init__(self, main_app) -> None:
        """
        Description: Constructor sets up attributes including objects
        :param main_app: the object of the main app
        :return: void
        """
        self.ip_address = '0.0.0.0'
        self.port = 5000
        self.app = main_app

    def listen(self, ip_address: str = '0.0.0.0', port: int = 5000, debug: bool = __debug__) -> None:
        """
        Description: Function that starts the server
        :param ip_address: the ip address to start the server on
        :param port: the port to start the server on
        :param debug: whether to turn on debug mode or not
        :return: void
        """
        self.ip_address = ip_address
        self.port = port
        template_dir = os.path.abspath("local_storage")
        app = Flask(__name__, template_folder=template_dir, static_folder=template_dir)
        FlaskServer.local_storage = "local_storage/"
        FlaskServer.main_app = self.app
        FlaskServer.debug = debug
        FlaskServer.ip_address = ip_address
        FlaskServer.port = port
        FlaskServer.create_tables()
        FlaskServer.logout_all()
        FlaskServer.download_files()
        FlaskServer.register(app, base_route="/")
        app.run(host=ip_address, port=port, ssl_context=('local_storage/cert.pem', 'local_storage/key.pem'))

    @staticmethod
    def close() -> str:
        """
        Description: Function used to shut down the server
        :return: str - Null string
        """
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        shutdown_func()
        return "Shutting down..."

    def reset(self) -> None:
        """
        Description: Function to restart the server
        :return: void
        """
        self.close()
        self.listen(self.ip_address, self.port)

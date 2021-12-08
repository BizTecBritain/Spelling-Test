__all__ = ['Application']
__version__ = '1.0.3'
__author__ = 'Alexander Bisland'

from data_management.config import Config
from server import Server


class Application:
    def __init__(self) -> None:
        """
        Description: Costructor sets up attributes including objects
        :return: void
        """
        self.ip_address = None
        self.port = None
        self.reconfigure()
        self.server = Server(self)

    def reconfigure(self) -> None:
        """
        Description: Function used to configure settings for the server
        :return: void
        """
        config_object = Config()
        config_object.load("local_storage/server.ini")
        self.ip_address = config_object.read_tag("SERVERCONFIG", "ipaddr")
        self.port = int(config_object.read_tag("SERVERCONFIG", "port"))

    def run(self, debug: bool = False) -> None:
        """
        Description: Function to start the server
        :param debug: whether to turn on debug mode or not
        :return: void
        """
        try:
            self.server.listen(self.ip_address, self.port, debug)
        except KeyboardInterrupt:
            reset = input("Restart Server? (y/n): ")
            if reset.lower() == 'y':
                self.reset()
            else:
                self.clean_exit()
                exit()

    def clean_exit(self) -> None:
        """
        Description: Function to Stop the server
        :return: void
        """
        self.server.close()

    def reset(self) -> None:
        """
        Description: Function to reset the server
        :return: void
        """
        self.clean_exit()
        self.reconfigure()
        self.run()


if __name__ == "__main__":
    app = Application()
    app.run(False)

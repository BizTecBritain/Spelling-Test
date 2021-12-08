__all__ = ['Application']
__version__ = '1.0.3'
__author__ = 'Alexander Bisland'

from client import PageManager, ask_yes_no, show_error
from data_management.config import Config


class Application:
    def __init__(self) -> None:
        """
        Description: Constructor sets up attributes including objects
        :return: void
        """
        self.ip_address = None
        self.port = None
        self.old_session_id = None
        self.reconfigure()
        self.page_manager = PageManager()

    def reconfigure(self) -> None:
        """
        Description: Function used to configure settings for the game
        :return: void
        """
        config_object = Config()
        config_object.load("local_storage/client.ini")
        self.ip_address = config_object.read_tag("SERVERCONFIG", "ipaddr")
        self.port = int(config_object.read_tag("SERVERCONFIG", "port"))
        self.old_session_id = config_object.read_tag("USERINFO", "session_id")

    def run(self, debug: bool = False) -> None:
        """
        Description: Function to start the game
        :param debug: whether to turn on debug mode or not
        :return: void
        """
        try:
            self.page_manager.start(self.ip_address, self.port, self.old_session_id, debug)
        except KeyboardInterrupt:
            if ask_yes_no("Restart", "Restart Server?"):
                self.reset()
            else:
                self.clean_exit()
                exit()

    def clean_exit(self) -> None:
        """
        Description: Function to Stop the server
        :return: void
        """
        self.page_manager.stop()

    def reset(self) -> None:
        """
        Description: Function to reset the server
        :return: void
        """
        self.clean_exit()
        self.reconfigure()
        self.run()


if __name__ == "__main__":
    try:
        app = Application()
        app.run()
    except Exception as e:
        show_error(e)
        exit()

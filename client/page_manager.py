__all__ = ['PageManager']
__version__ = '2.0.1'
__author__ = 'Daniel Hart'

import os
import client.pages
from communications.data_channel import DataChannel
from communications.session_management import ClientSessionManagement
from data_management.audio_player import AudioPlayer


class PageManager:
    def __init__(self) -> None:
        """
        Description: Constructor sets up attributes and objects
        :return: void
        """
        self.data_channel = None
        self.logged_in = False
        self.session_manager = ClientSessionManagement()
        for file in os.listdir("local_storage/word_audio"):
            os.remove("local_storage/word_audio/"+file)
        self.audio_manager = AudioPlayer()
        self.difficulty_chosen = ""
        self.time = None
        self.score = None
        self.correct = None

    def start(self, ip_address, port, old_session_id, debug=False) -> None:
        """
        Description: Function to start the PageManager and open the first page
        :param ip_address: the ip address of the server to connect to
        :param port: the port of the server to connect to
        :param old_session_id: the session_isof the previous login to attempt to reconnect
        :param debug: whether to turn on debug mode or not
        :return: void
        """
        self.data_channel = DataChannel(ip_address, port)
        resp = self.data_channel.establish_connection(old_session_id)
        if resp != "1":
            self.session_manager.update(resp)
            self.logged_in = True
        self.audio_manager.start("local_storage/client_audio/main_menu_music.mp3")
        client.pages.MenuPage(self).mainloop()

    def stop(self) -> None:
        """
        Description: [Placeholder Function]
        :return: void
        """
        pass

    class Decorator:
        @staticmethod
        def destroy_prev(fnc):
            """
            Description: Wrapper function to destroy the previous page
            :param fnc: the function that has the wrapper arround it
            :return: fnc - the response of the function
            """
            def inner(objecta, prevpage=None):
                if prevpage is not None:
                    prevpage.destroy()
                return fnc(objecta)
            return inner

    @Decorator.destroy_prev
    def end_page(self):
        self.audio_manager.start("local_storage/client_audio/main_menu_music.mp3")
        client.pages.EndPage(self).mainloop()

    @Decorator.destroy_prev
    def leaderboard_page(self):
        client.pages.LeaderboardPage(self).mainloop()

    @Decorator.destroy_prev
    def login_page(self):
        client.pages.LoginPage(self).mainloop()

    @Decorator.destroy_prev
    def menu_page(self):
        client.pages.MenuPage(self).mainloop()

    @Decorator.destroy_prev
    def registration_page(self):
        client.pages.RegistrationPage(self).mainloop()

    @Decorator.destroy_prev
    def spelling_test_page(self):
        self.audio_manager.stop()
        client.pages.SpellingTestPage(self).mainloop()

    @Decorator.destroy_prev
    def difficulty_page(self):
        client.pages.DifficultyPage(self).mainloop()

    @Decorator.destroy_prev
    def forgot_password(self):
        client.pages.ForgotPasswordPage(self).mainloop()

    @Decorator.destroy_prev
    def too_many_requests_page(self):
        client.pages.TooManyRequestsPage(self).mainloop()

    @Decorator.destroy_prev
    def forgot_verify_page(self):
        client.pages.ForgotVerifyPage(self).mainloop()

    @Decorator.destroy_prev
    def registration_verify_page(self):
        client.pages.RegistrationVerifyPage(self).mainloop()


if __name__ == "__main__":
    a = PageManager()
    a.start('127.0.0.1', 5000, "")

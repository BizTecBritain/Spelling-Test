__all__ = ['MenuPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label, Button
from .my_tk_widgets import PhotoImage
from PIL import ImageTk, Image


class MenuPage(Base):
    def __init__(self, page_manager):
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Menu", 1920, 1080, page_manager)  # details for the window

        if not self.page_manager.logged_in:  # if the user isn't logged in
            self.login_button_photo = PhotoImage(file=r"local_storage/images/login_main.png",
                                                 ratio=self.ratio)  # opens the image to be used
            self.login_button = Button(self, text="", image=self.login_button_photo, bg='#E4D6B6',
                                       command=self.login)  # details for button
            self.login_button.place(x=self.ratio*500, y=self.ratio*325)  # places the button

            self.register_button_photo = PhotoImage(file=r"local_storage/images/register_main.png",
                                                    ratio=self.ratio)  # opens the image to be used
            self.register_button = Button(self, text="", image=self.register_button_photo, bg='#E4D6B6',
                                          command=self.register_redirect)  # details for button
            self.register_button.place(x=self.ratio*791, y=self.ratio*325)  # places the button
        else:  # if the user is logged in
            self.start_button_photo = PhotoImage(file=r"local_storage/images/take_a_test.png",
                                                 ratio=self.ratio)  # opens the image to be used
            self.start_button = Button(self, text="", image=self.start_button_photo, bg='#E4D6B6',
                                       command=self.choose_difficulty)  # details for button
            self.start_button.place(x=self.ratio*501, y=self.ratio*286)  # places the button

            self.logout_button_photo = PhotoImage(file=r"local_storage/images/log_out.png",
                                                  ratio=self.ratio)  # opens the image to be used
            self.logout_button = Button(self, text="", image=self.logout_button_photo, bg='#E4D6B6',
                                        command=self.logout)  # details for button
            # self.logout_button.place(x=self.ratio*650, y=self.ratio*750)
            self.logout_button.place(x=self.ratio*1250, y=self.ratio*20)

        self.image_open_background = Image.open("local_storage/images/menu_background.gif")  # opens the image
        self.image_open_background = self.image_open_background.resize((self.winfo_screenwidth(),
                                                                        self.winfo_screenheight()), Image.ANTIALIAS)
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=self.ratio*-2, y=self.ratio*-2)  # positions the image in the background
        self.bg.lower()  # makes sure the background is at the back and not covering anything

        self.leaderboard_button_photo = PhotoImage(file=r"local_storage/images/leaderboard_main.png",
                                                   ratio=self.ratio)  # opens the image to be used
        self.leaderboard_button = Button(self, text="", image=self.leaderboard_button_photo, bg='#E4D6B6',
                                         command=self.leaderboard)  # details for button
        self.leaderboard_button.place(x=self.ratio*500, y=self.ratio*450)  # places the button

        self.quit_button_photo = PhotoImage(file=r"local_storage/images/quit.png",
                                            ratio=self.ratio)  # opens the image to be used
        self.quit_button = Button(self, text="", image=self.quit_button_photo, bg='#E4D6B6',
                                  command=self.destroy)  # details for button
        self.quit_button.place(x=self.ratio*500, y=self.ratio*600)  # places the button

    def login(self) -> None:
        """
        Description: Function to return to the login page
        :return: void
        """
        self.page_manager.login_page(self)  # opens the login page and closes menu

    def register_redirect(self) -> None:
        """
        Description: Function to return to the registration page
        :return: void
        """
        self.page_manager.registration_page(self)  # opens the register page and closes menu

    def choose_difficulty(self) -> None:
        """
        Description: Function to return to the difficulty page
        :return: void
        """
        self.page_manager.difficulty_page(self)  # opens the test page and closes menu

    def leaderboard(self) -> None:
        """
        Description: Function to return to the leaderboard page
        :return: void
        """
        self.page_manager.leaderboard_page(self)  # opens the leaderboard and closes menu

    def logout(self) -> None:
        """
        Description: Function to logout user
        :return: void
        """
        session_id = self.page_manager.session_manager.get_session_id()
        self.page_manager.data_channel.get_text("logout/{0}".format(session_id))
        self.page_manager.logged_in = False
        self.page_manager.menu_page(self)

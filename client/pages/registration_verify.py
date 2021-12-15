__all__ = ['RegistrationVerifyPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label
from .my_tk_widgets import PhotoImage, ClickButton
from PIL import ImageTk, Image


class RegistrationVerifyPage(Base):
    def __init__(self, page_manager) -> None:
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Verify Registration", 1920, 1080, page_manager)

        self.image_open_background = Image.open("local_storage/images/background.gif")  # opens the image
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=self.ratio*-200, y=self.ratio*-100)  # positions the image in the background

        self.squid_games_label_photo = PhotoImage(file=r"local_storage/images/squid_games.png", ratio=self.ratio)
        self.squid_games_label = Label(self, text="", image=self.squid_games_label_photo, bg='#E4D6B6')  # label details
        self.squid_games_label.place(x=self.ratio*250, y=self.ratio*20)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = ClickButton(self, image=self.exit_button_photo, bg='#E4D6B6', activebackground="#E4D6B6",
                                       command=self.menu, op_file="local_storage/images/exit_highlight.png",
                                       ratio=self.ratio)  # closes the registration and opens menu
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.verify_label = Label(self, text='Please check your emails to verify your registration.\nIf it is not in '
                                             'your inbox, check the junk folder.',
                                  font=('Courier', str(int(24*self.ratio))), bg='#E4D6B6')
        self.verify_label.place(x=self.ratio*275, y=self.ratio*400)  # places the label

        self.protocol("WM_DELETE_WINDOW", self.menu)

    def menu(self):  # function for when exit is pressed
        self.page_manager.audio_manager.click()
        self.page_manager.menu_page(self)  # opens the menu page

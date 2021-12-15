__all__ = ['CreditsPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label
from .my_tk_widgets import PhotoImage, ClickButton
from PIL import ImageTk, Image
from client.page_manager import PageManager


class CreditsPage(Base):
    def __init__(self, page_manager: PageManager = None):
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Well Done!", 1920, 1080, page_manager)

        self.image_open_background = Image.open("local_storage/images/background.gif")  # opens the image
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=self.ratio * -200, y=self.ratio * -100)  # positions the image in the background

        self.squid_games_label_photo = PhotoImage(file=r"local_storage/images/squid_games.png", ratio=self.ratio)
        self.squid_games_label = Label(self, text="", image=self.squid_games_label_photo, bg='#E4D6B6')  # label details
        self.squid_games_label.place(x=self.ratio * 250, y=self.ratio * 20)  # places the label

        self.credits_title_label_photo = PhotoImage(file=r"local_storage/images/credits.png",
                                                    ratio=self.ratio)  # opens the image
        self.credits_title_label = Label(self, text="", image=self.credits_title_label_photo, bg='#E4D6B6')  # details
        self.credits_title_label.place(x=self.ratio * 550, y=self.ratio * 200)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = ClickButton(self, text="", image=self.exit_button_photo, bg='#E4D6B6',
                                       activebackground='#E4D6B6', command=self.settings, ratio=self.ratio,
                                       op_file="local_storage/images/exit_highlight.png")
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.credits_label = Label(self, text='Squid Games - Created By Alexander Bisland, Daniel Hart, '
                                              'Finley Wallace - Wright and Edward Hopper\n'
                                              '\n'  # newline (blank)
                                              '\n'  # newline (blank)
                                              'Server - Alexander Bisland\n'
                                              '\n'  # newline (blank)
                                              'Login and Register - Daniel Hart\n'
                                              '\n'  # newline (blank)
                                              'GUI - Finley Wallace - Wright\n'
                                              '\n'  # newline (blank)
                                              'Utility Functions - Edward Hopper\n'
                                              '\n'  # newline (blank)
                                              '\n'  # newline (blank)
                                              '\n'  # newline (blank)
                                              'Thank You For Taking Our Spelling Test!',
                                   font=('Courier', str(int(18 * self.ratio)), 'bold'), bg='#E4D6B6')
        self.credits_label.place(x=self.ratio * 80, y=self.ratio * 320)  # places label

        self.protocol("WM_DELETE_WINDOW", self.settings)

    def settings(self) -> None:
        """
        Description: Function to return to the settings page
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.settings_page(self)  # opens the menu page

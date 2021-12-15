__all__ = ['ForgotPasswordPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label, Button, Entry
from .my_tk_widgets import PhotoImage, ClickButton
from PIL import ImageTk, Image
from client.error_manager import show_error
from urllib.parse import quote


class ForgotPasswordPage(Base):
    def __init__(self, page_manager):
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Forgot Password", 500, 500, page_manager)

        self.image_open_background = Image.open("local_storage/images/background.gif")  # opens the image
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=self.ratio * -200, y=self.ratio * -100)  # positions the image in the background

        self.squid_games_label_photo = PhotoImage(file=r"local_storage/images/squid_games.png", ratio=self.ratio)
        self.squid_games_label = Label(self, text="", image=self.squid_games_label_photo, bg='#E4D6B6')  # label details
        self.squid_games_label.place(x=self.ratio * 250, y=self.ratio * 20)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = ClickButton(self, text="", image=self.exit_button_photo, bg='#E4D6B6',
                                       activebackground="#E4D6B6", op_file="local_storage/images/exit_highlight.png",
                                       command=self.login, ratio=self.ratio)  # closes the registration and opens menu
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.forgot_password_label_photo = PhotoImage(file=r"local_storage/images/forgot_password.png",
                                                      ratio=self.ratio)  # opens the image
        self.forgot_password_label = Label(self, text="", image=self.forgot_password_label_photo, bg='#E4D6B6')
        self.forgot_password_label.place(x=self.ratio * 450, y=self.ratio * 220)  # places the label

        self.info_label = Label(self, text='Enter Your Info Below To Retrieve Your Password',
                                font=('Courier', str(int(16 * self.ratio))), bg='#E4D6B6')  # details
        self.info_label.place(x=self.ratio * 485, y=self.ratio * 350)  # places label

        self.username_label = Label(self, text='Username', font=('Courier', str(int(16 * self.ratio))), bg='#E4D6B6')
        self.username_label.place(x=self.ratio * 600, y=self.ratio * 400)  # places label

        self.username_entry = Entry(self, width=30, font=(None, str(int(10 * self.ratio))))  # details
        self.username_entry.place(x=self.ratio * 720, y=self.ratio * 403)  # places entry box

        self.email_label = Label(self, text='Email', font=('Courier', str(int(16 * self.ratio))), bg='#E4D6B6')
        self.email_label.place(x=self.ratio * 600, y=self.ratio * 430)  # places label

        self.email_entry = Entry(self, width=30, font=(None, str(int(10 * self.ratio))))  # details
        self.email_entry.place(x=self.ratio * 720, y=self.ratio * 433)  # places entry box

        self.submit_button = Button(self, text='Reset my Password', font=('Courier', str(int(13 * self.ratio))),
                                    command=self.submit_info)  # details
        self.submit_button.place(x=self.ratio * 700, y=self.ratio * 480)

        self.protocol("WM_DELETE_WINDOW", self.login)

    def login(self) -> None:
        """
        Description: Function for when exit is pressed
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.login_page(self)  # opens the menu page

    def submit_info(self) -> None:
        """
        Description: Function for when submit is pressed
        :return: void
        """
        self.page_manager.audio_manager.click()
        username = quote(self.username_entry.get(), safe="")
        email = quote(self.email_entry.get(), safe="")
        resp = self.page_manager.data_channel.get_text("reset_password/{0}/{1}".format(username, email))
        if int(resp) == -8:
            self.page_manager.too_many_requests_page(self)
        elif int(resp) < 0:
            show_error(self.page_manager.session_manager.errors[int(resp)])
        else:
            self.page_manager.forgot_verify_page(self)

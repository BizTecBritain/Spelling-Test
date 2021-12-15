__all__ = ['LoginPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

import tkinter.messagebox

from .tk_base import Base
from tkinter import Label, Entry, Button
from .my_tk_widgets import PhotoImage, ClickButton
from client.error_manager import show_error, ask_yes_no
from communications.security import hash_password, login_check
from PIL import ImageTk, Image
import webbrowser
from urllib.parse import quote


class LoginPage(Base):  # TODO add 2fa
    def __init__(self, page_manager) -> None:
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Login", 1920, 1080, page_manager)

        self.image_open_background = Image.open("local_storage/images/background.gif")  # opens the image
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=self.ratio * -200, y=self.ratio * -100)  # positions the image in the background

        self.squid_games_label_photo = PhotoImage(file=r"local_storage/images/squid_games.png",
                                                  ratio=self.ratio)  # opens image to be used
        self.squid_games_label = Label(self, text="", image=self.squid_games_label_photo, bg='#E4D6B6')  # label details
        self.squid_games_label.place(x=self.ratio * 250, y=self.ratio * 20)  # places the image

        self.sign_in_label_photo = PhotoImage(file=r"local_storage/images/sign_in_login.png",
                                              ratio=self.ratio)  # opens the image to be used
        self.sign_in_label = Label(self, text="", image=self.sign_in_label_photo, bg='#E4D6B6')  # label details
        self.sign_in_label.place(x=self.ratio * 430, y=self.ratio * 250)  # places the image

        self.label_username = Label(self, text='Username', bg='#E4D6B6',
                                    font=('Courier', str(int(16 * self.ratio))))  # label details
        self.label_username.place(x=self.ratio * 410, y=self.ratio * 337)  # places the label

        self.entry_username = Entry(self, width=20, font=(None, str(int(10 * self.ratio))))  # details for entry box
        self.entry_username.place(x=self.ratio * 530, y=self.ratio * 340)  # places the entry box

        self.label_password = Label(self, text='Password', bg='#E4D6B6',
                                    font=('Courier', str(int(16 * self.ratio))))
        self.label_password.place(x=self.ratio * 410, y=self.ratio * 380)

        self.entry_password = Entry(self, show='*', width=20, font=(None, str(int(10 * self.ratio))))
        self.entry_password.place(x=self.ratio * 530, y=self.ratio * 383)

        self.forgot_password_button = Button(self, text='Forgot Password', command=self.reset_password,
                                             font=(None, str(int(11 * self.ratio))))
        self.forgot_password_button.place(x=self.ratio * 410, y=self.ratio * 430)  # places the button

        self.login_button = Button(self, text='Login', width=12, command=self.login,
                                   font=(None, str(int(11 * self.ratio))))  # details for login button
        self.login_button.place(x=self.ratio * 560, y=self.ratio * 430)  # places the button

        def open_url():  # what to do when the privacy policy is clicked
            self.page_manager.audio_manager.click()
            webbrowser.open_new_tab(url)  # opens the url

        url = "https://www.freeprivacypolicy.com/live/4330e9cd-6747-4d1f-bd9c-70b4960b3c61"  # url to open
        self.label_privacy_policy = Label(self, text="Privacy Policy", cursor="hand2", bg='#E4D6B6',
                                          font=('Courier', str(int(16 * self.ratio)), 'underline'))
        self.label_privacy_policy.place(x=self.ratio * 440, y=self.ratio * 470)  # places label
        self.label_privacy_policy.bind("<Button-1>", lambda e: open_url())  # makes the label clickable

        self.new_user_label_photo = PhotoImage(file=r"local_storage/images/new_user_login.png", ratio=self.ratio)
        self.new_user_label = Label(self, text="", image=self.new_user_label_photo, bg='#E4D6B6')
        self.new_user_label.place(x=self.ratio * 800, y=self.ratio * 260)

        self.new_user_register_button_photo = PhotoImage(file=r"local_storage/images/register_login_page.png",
                                                         ratio=self.ratio)  # opens the image to be used
        self.new_user_register_button = ClickButton(self, image=self.new_user_register_button_photo, ratio=self.ratio,
                                                    bg='#E4D6B6', activebackground='#E4D6B6',
                                                    command=self.register_redirect,
                                                    op_file=r"local_storage/images/register_login_page_highlight.png")
        self.new_user_register_button.place(x=self.ratio * 795, y=self.ratio * 375)  # places the button

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png",
                                            ratio=self.ratio)  # opens the image to be used
        self.exit_button = ClickButton(self, text="", image=self.exit_button_photo, bg='#E4D6B6',
                                       activebackground="#E4D6B6", op_file="local_storage/images/exit_highlight.png",
                                       command=self.on_closing, ratio=self.ratio)  # closes the login and opens menu
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.bind("<Return>", lambda event: self.login())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def login(self) -> None:
        """
        Description: Function to log the user in
        :return: void
        """
        self.page_manager.audio_manager.click()
        username, password = self.entry_username.get(), self.entry_password.get()
        if len(username) == 0 or len(password) == 0:
            tkinter.messagebox.showerror("Invalid Credentials", "Please enter some details!")
            return
        login_check_val = login_check(username, password)
        if login_check_val < 0:
            tkinter.messagebox.showerror("Invalid Credentials", "The password you entered is incorrect!")
            return
        password = hash_password(password, username)
        username = quote(username, safe="")
        session_id = self.page_manager.data_channel.get_text("login/{0}/{1}/0".format(username, password))
        if session_id[1:].isnumeric() and session_id[0] == "-":
            if int(session_id) < 0:
                if int(session_id) == -5:
                    resp = ask_yes_no("Already logged in", "You have a session elsewhere! Do you want to log it out?")
                    if resp:
                        session_id = self.page_manager.data_channel.get_text("login/{0}/{1}/1".format(username,
                                                                                                      password))
                        self.login()
                    else:
                        return
                else:
                    show_error(SystemError(self.page_manager.session_manager.errors[int(session_id)]))
                    self.entry_password.delete(0, 'end')
                    return
        self.page_manager.session_manager.update(session_id)
        self.page_manager.logged_in = True
        self.on_closing()

    def register_redirect(self) -> None:
        """
        Description: Function to return to the registration page
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.registration_page(self)  # opens the registration page

    def reset_password(self) -> None:
        """
        Description: Function to return to forgot password page
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.forgot_password(self)

    def on_closing(self) -> None:
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.menu_page(self)  # opens the menu page

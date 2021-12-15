__all__ = ['RegistrationPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

import pickle
import tkinter
from .tk_base import Base
from tkinter import Label, Entry
from .my_tk_widgets import PhotoImage, ClickButton
from PIL import ImageTk, Image
import webbrowser
from client.error_manager import show_error
from urllib.parse import quote


class RegistrationPage(Base):
    def __init__(self, page_manager):
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Register", 1920, 1080, page_manager)

        self.image_open_background = Image.open("local_storage/images/background.gif")  # opens the image
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=self.ratio * -200, y=self.ratio * -100)  # positions the image in the background

        self.squid_games_label_photo = PhotoImage(file=r"local_storage/images/squid_games.png",
                                                  ratio=self.ratio)  # opens the image
        self.squid_games_label = Label(self, text="", image=self.squid_games_label_photo, bg='#E4D6B6')  # label details
        self.squid_games_label.place(x=self.ratio * 250, y=self.ratio * 20)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = ClickButton(self, text="", image=self.exit_button_photo, bg='#E4D6B6', ratio=self.ratio,
                                       activebackground="#E4D6B6", command=self.on_closing,
                                       op_file="local_storage/images/exit_highlight.png", pagemanager=self.page_manager)
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.register_register_label_photo = PhotoImage(file=r"local_storage/images/register_register_page.png",
                                                        ratio=self.ratio)
        self.register_register_label = Label(self, text="", image=self.register_register_label_photo, bg='#E4D6B6')
        self.register_register_label.place(x=self.ratio * 600, y=self.ratio * 260)

        self.register_desc_label = Label(self, text='   Register to play your \n spelling test now',
                                         font=('courier', str(int(16 * self.ratio))), bg='#E4D6B6')
        self.register_desc_label.place(x=self.ratio * 593, y=self.ratio * 330)  # places the label

        self.email_ask_label = Label(self, text='Email', font=('courier', str(int(16 * self.ratio))),
                                     bg='#E4D6B6')  # label details
        self.email_ask_label.place(x=self.ratio * 610, y=self.ratio * 400)  # places the label

        self.email_ask_entry = Entry(self, width=30, font=(None, str(int(10 * self.ratio))))  # details for entry box
        self.email_ask_entry.place(x=self.ratio * 695, y=self.ratio * 402)  # places the entry box

        self.username_ask_label = Label(self, text='Username', font=('courier', str(int(16 * self.ratio))),
                                        bg='#E4D6B6')
        self.username_ask_label.place(x=self.ratio * 615, y=self.ratio * 440)

        self.username_ask_entry = Entry(self, width=23, font=(None, str(int(10 * self.ratio))))
        self.username_ask_entry.place(x=self.ratio * 735, y=self.ratio * 442)

        self.password_ask_label = Label(self, text='Password', font=('courier', str(int(16 * self.ratio))),
                                        bg='#E4D6B6')
        self.password_ask_label.place(x=self.ratio * 615, y=self.ratio * 480)

        self.password_ask_entry = Entry(self, width=23, show='*', font=(None, str(int(10 * self.ratio))))
        self.password_ask_entry.place(x=self.ratio * 735, y=self.ratio * 482)

        self.captcha_ask_label = Label(self, text='Captcha', font=('courier', str(int(16 * self.ratio))), bg='#E4D6B6')
        self.captcha_ask_label.place(x=self.ratio * 620, y=self.ratio * 520)

        self.captcha_ask_entry = Entry(self, width=23, font=(None, str(int(10 * self.ratio))))
        self.captcha_ask_entry.place(x=self.ratio * 730, y=self.ratio * 522)

        self.register_confirm = tkinter.Button(self, text='Confirm Registration',
                                               command=self.register_func)  # details for button
        self.register_confirm.place(x=self.ratio * 690, y=self.ratio * 560)  # places the button

        def open_url():  # what to do when the privacy policy is clicked
            self.page_manager.audio_manager.click()
            webbrowser.open_new_tab(url)  # opens the url

        url = "https://www.freeprivacypolicy.com/live/4330e9cd-6747-4d1f-bd9c-70b4960b3c61"  # url to open
        self.label_privacy_policy = Label(self, text="Privacy Policy", cursor="hand2", bg='#E4D6B6',
                                          font=('Courier', str(int(16 * self.ratio)), 'underline'))
        self.label_privacy_policy.place(x=self.ratio * 675, y=self.ratio * 590)  # places label
        self.label_privacy_policy.bind("<Button-1>", lambda e: open_url())  # makes the label clickable

        self.__verify_label = Label(self, font=('Courier', str(int(16 * self.ratio))))
        self.__image_label = Label(self, font=('Courier', str(int(16 * self.ratio))))

        self.__createImage()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def register_func(self) -> None:
        """
        Description: Function to register the user
        :return: void
        """
        self.page_manager.audio_manager.click()
        username, password = self.username_ask_entry.get(), self.password_ask_entry.get()
        email = self.email_ask_entry.get()
        if username != "" and password != "" and email != "":
            username = quote(username, safe="")
            password = quote(password, safe="")
            email = quote(email, safe="")
            the_captcha = quote(self.captcha_ask_entry.get().lower(), safe="")
            address = "register_user/{0}/{1}/{2}/{3}/{4}".format(username, password, email, self.cap_uuid,
                                                                 the_captcha)
            resp = int(self.page_manager.data_channel.get_text(address))
            if resp > 0:
                self.page_manager.registration_verify_page(self)
            elif resp == -8:
                self.page_manager.too_many_requests_page(self)
            else:
                show_error(SystemError(self.page_manager.session_manager.errors[resp]))

    def on_closing(self) -> None:
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.menu_page(self)  # opens the menu page

    def __createImage(self, flag: int = 0) -> None:
        """
        Description: Function to generate a captcha image
        :param flag: flag to set if it is not the first time that the function is called
        :return: void
        """
        if flag == 1:
            self.page_manager.audio_manager.click()
            self.__verify_label.place_forget()
        self.captcha_ask_entry.delete(0, tkinter.END)
        resp, headers = self.page_manager.data_channel.get_text_headers("request_captcha/"+str(self.ratio))
        if resp == "-8":
            self.page_manager.too_many_requests_page(self)
        elif resp[1:].isnumeric() and resp[0] == "-":
            show_error(SystemError(self.page_manager.session_manager.errors[int(resp)]))
        else:
            self.__image_generated = pickle.loads(eval(resp))
            self.cap_uuid = headers["uuid"]
            self.__image_display = ImageTk.PhotoImage(Image.open(self.__image_generated), master=self)
            self.__image_label.place_forget()
            self.__image_label = Label(self, image=self.__image_display)
            self.__image_label.place(x=self.ratio * 630, y=self.ratio * 650)
            self.__image_label.bind("<Button-1>", lambda event: self.__createImage(1))


if __name__ == "__main__":
    RegistrationPage(None).mainloop()

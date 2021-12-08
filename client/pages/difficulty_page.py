__all__ = ['DifficultyPage']
__version__ = '1.2.1'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label, messagebox
from .my_tk_widgets import PhotoImage, Button
from PIL import ImageTk, Image


class DifficultyPage(Base):
    def __init__(self, page_manager) -> None:
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Choose Difficulty", 1920, 1080, page_manager)

        self.image_open_background = Image.open("local_storage/images/background.gif")  # opens the image
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=self.ratio*-200, y=self.ratio*-100)  # positions the image in the background

        self.squid_games_label_photo = PhotoImage(file=r"local_storage/images/squid_games.png",
                                                  ratio=self.ratio)  # opens the image
        self.squid_games_label = Label(self, text="", image=self.squid_games_label_photo, bg='#E4D6B6')  # label details
        self.squid_games_label.place(x=self.ratio*250, y=self.ratio*20)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = Button(self, text="", image=self.exit_button_photo, bg='#E4D6B6', activebackground="#E4D6B6",
                                  command=self.menu)  # closes the registration and opens menu
        self.exit_button.place(x=self.ratio*1344, y=self.ratio*781)  # places the button

        self.choose_difficulty_label_photo = PhotoImage(file=r"local_storage/images/choose_difficulty.png",
                                                        ratio=self.ratio)  # opens the image
        self.choose_difficulty_label = Label(self, text="", image=self.choose_difficulty_label_photo, bg='#E4D6B6')
        self.choose_difficulty_label.place(x=self.ratio*500, y=self.ratio*220)  # places the label

        self.easy_button_photo = PhotoImage(file=r"local_storage/images/easy.png", ratio=self.ratio)  # opens the image
        self.easy_button = Button(self, text="", image=self.easy_button_photo, activebackground='#E4D6B6', bg='#E4D6B6',
                                  command=self.easy)  # details
        self.easy_button.place(x=self.ratio*200, y=self.ratio*300)  # places the label

        self.medium_button_photo = PhotoImage(file=r"local_storage/images/medium.png",
                                              ratio=self.ratio)  # opens the image
        self.medium_button = Button(self, text="", image=self.medium_button_photo, activebackground='#E4D6B6',
                                    bg='#E4D6B6', command=self.medium)  # details
        self.medium_button.place(x=self.ratio*200, y=self.ratio*400)  # places the label

        self.hard_button_photo = PhotoImage(file=r"local_storage/images/hard.png", ratio=self.ratio)  # opens the image
        self.hard_button = Button(self, text="", image=self.hard_button_photo, activebackground='#E4D6B6', bg='#E4D6B6',
                                  command=self.hard)  # details
        self.hard_button.place(x=self.ratio*200, y=self.ratio*500)  # places the label

        self.go_to_test_button_photo = PhotoImage(file=r"local_storage/images/go_to_test.png",
                                                  ratio=self.ratio)  # opens the image
        self.go_to_test_button = Button(self, text="", image=self.go_to_test_button_photo, activebackground='#E4D6B6',
                                        bg='#E4D6B6', command=self.take_test)  # details
        self.go_to_test_button.place(x=self.ratio*800, y=self.ratio*400)  # places the label

        self.protocol("WM_DELETE_WINDOW", self.menu)

    def menu(self) -> None:
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.menu_page(self)  # opens the menu page

    def take_test(self) -> None:
        """
        Description: Function to start the test
        :return: void
        """
        if self.page_manager.difficulty_chosen == "":  # if the variable has no value
            messagebox.showinfo(title='No Difficulty Chosen',  # shows a box to tell the user theres no difficultly
                                message="You haven't chosen a difficulty, please try again.")
        else:  # if the variable has something in it
            self.page_manager.spelling_test_page(self)  # opens the test page

    def easy(self) -> None:
        """
        Description: Function to highlight the easy button when pressed
        :return: void
        """
        img_easy = PhotoImage(file="local_storage/images/easy_highlight.png", ratio=self.ratio)
        img_medium = PhotoImage(file="local_storage/images/medium.png", ratio=self.ratio)
        img_hard = PhotoImage(file="local_storage/images/hard.png", ratio=self.ratio)
        self.easy_button.configure(image=img_easy)
        self.easy_button.image = img_easy
        self.medium_button.configure(image=img_medium)
        self.medium_button.image = img_medium
        self.hard_button.configure(image=img_hard)
        self.hard_button.image = img_hard
        self.page_manager.difficulty_chosen = "easy"  # sets the variable to easy

    def medium(self) -> None:
        """
        Description: Function to highlight the medium button when pressed
        :return: void
        """
        img_easy = PhotoImage(file="local_storage/images/easy.png", ratio=self.ratio)
        img_medium = PhotoImage(file="local_storage/images/medium_highlight.png", ratio=self.ratio)
        img_hard = PhotoImage(file="local_storage/images/hard.png", ratio=self.ratio)
        self.easy_button.configure(image=img_easy)
        self.easy_button.image = img_easy
        self.medium_button.configure(image=img_medium)
        self.medium_button.image = img_medium
        self.hard_button.configure(image=img_hard)
        self.hard_button.image = img_hard
        self.page_manager.difficulty_chosen = "medium"  # sets the variable to medium

    def hard(self) -> None:
        """
        Description: Function to highlight the hard button when pressed
        :return: void
        """
        img_easy = PhotoImage(file="local_storage/images/easy.png", ratio=self.ratio)
        img_medium = PhotoImage(file="local_storage/images/medium.png", ratio=self.ratio)
        img_hard = PhotoImage(file="local_storage/images/hard_highlight.png", ratio=self.ratio)
        self.easy_button.configure(image=img_easy)
        self.easy_button.image = img_easy
        self.medium_button.configure(image=img_medium)
        self.medium_button.image = img_medium
        self.hard_button.configure(image=img_hard)
        self.hard_button.image = img_hard
        self.page_manager.difficulty_chosen = "hard"  # sets the variable to hard

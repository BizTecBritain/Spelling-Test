__all__ = ['SpellingTestPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label, messagebox, Entry
from .my_tk_widgets import PhotoImage, Button, ClickButton
from PIL import ImageTk, Image
from client.error_manager import show_error
from urllib.parse import quote


class SpellingTestPage(Base):
    def __init__(self, page_manager):
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Test", 1920, 1080, page_manager)

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
        self.exit_button = Button(self, text="", image=self.exit_button_photo, bg='#E4D6B6', activebackground="#E4D6B6",
                                  command=self.menu)  # closes the registration and opens menu
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.test_title_label_photo = PhotoImage(file=r"local_storage/images/test_title.png",
                                                 ratio=self.ratio)  # opens the image
        self.test_title_label = Label(self, text="", image=self.test_title_label_photo, bg='#E4D6B6')  # label details
        self.test_title_label.place(x=self.ratio * 600, y=self.ratio * 200)  # places the label

        self.type_here_label = Label(self, text='Type Your Answer Here', font=('Courier', str(int(16 * self.ratio))),
                                     bg='#E4D6B6')  # detail
        self.type_here_label.place(x=self.ratio * 250, y=self.ratio * 350)  # places the label

        self.word_text = Entry(self, width=40, font=(None, str(int(16 * self.ratio))))  # details for the textbox
        self.word_text.place(x=self.ratio * 550, y=self.ratio * 350)  # places the textbox

        self.audio_button_photo = PhotoImage(file=r"local_storage/images/audio.png",
                                             ratio=self.ratio)  # opens the image
        self.audio_button = ClickButton(self, text="", image=self.audio_button_photo, bg='#E4D6B6',
                                        activebackground='#E4D6B6', command=self.speak_word, ratio=self.ratio,
                                        op_file=r"local_storage/images/audio_highlight.png")  # label details
        self.audio_button.place(x=self.ratio * 920, y=self.ratio * 320)  # places the label

        self.next_word_button_photo = PhotoImage(file=r"local_storage/images/next_word.png",
                                                 ratio=self.ratio)  # opens the image
        self.next_word_button = ClickButton(self, text="", image=self.next_word_button_photo, bg='#E4D6B6',
                                            activebackground='#E4D6B6', command=self.next_word, ratio=self.ratio,
                                            op_file=r"local_storage/images/next_word_highlight.png")  # label details
        self.next_word_button.place(x=self.ratio * 250, y=self.ratio * 450)  # places the label

        self.bind("<Return>", lambda event: self.next_word())
        self.protocol("WM_DELETE_WINDOW", self.menu)

        self.file = None
        self.words_completed = 0
        self.next_word()

    def menu(self) -> None:
        """
        Description: Function to return to the menu
        :return: void
        """
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):  # asks if they are sure they want to quit
            self.page_manager.menu_page(self)  # opens the menu page

    def speak_word(self) -> None:
        """
        Description: Function that speaks the audio
        :return: void
        """
        self.page_manager.audio_manager.start(self.file)

    def next_word(self) -> None:
        """
        Description: Function to move on to the next word
        :return: void
        """
        if self.words_completed != 0:
            word = self.word_text.get()
            if len(word) != 0:
                self.word_text.delete(0, 'end')
                session_id = self.page_manager.session_manager.get_session_id()
                word = quote(word, safe="")
                _, headers = self.page_manager.data_channel.get_text_headers(
                    "submit_answer/{0}/{1}".format(session_id, word))
                if int(headers["error"]) == 0:
                    self.page_manager.session_manager.update(headers["session_id"])
                else:
                    if int(headers['error']) == -2:
                        self.page_manager.logged_in = False
                    show_error(SystemError(self.page_manager.session_manager.errors[int(headers["error"])]))
                    self.page_manager.menu_page(self)
                if self.words_completed == 10:
                    self.page_manager.time = headers["time"]
                    self.page_manager.score = headers["score"]
                    self.page_manager.correct = headers["correct"]
                    self.page_manager.end_page(self)
                    return
                if self.words_completed == 9:
                    self.next_word_button_photo = PhotoImage(file=r"local_storage/images/submit.png",
                                                             ratio=self.ratio)  # opens the image
                    self.next_word_button.configure(image=self.next_word_button_photo)
                    self.next_word_button.op_file = "local_storage/images/submit_highlight.png"
                    self.next_word_button.image = self.next_word_button_photo
                    self.next_word_button.place_forget()
                    self.next_word_button.place(x=self.ratio * 230, y=self.ratio * 430)
        difficulty = self.page_manager.difficulty_chosen
        session_id = self.page_manager.session_manager.get_session_id()
        file, headers = self.page_manager.data_channel.download_file("get_audio/{0}/{1}".format(difficulty, session_id))
        if int(headers["error"]) == 0:
            self.page_manager.session_manager.update(headers["session_id"])
            self.file = file
            self.speak_word()
        else:
            if int(headers['error']) == -2:
                self.page_manager.logged_in = False
            show_error(SystemError(self.page_manager.session_manager.errors[int(headers["error"])]))
            self.page_manager.menu_page(self)
        self.words_completed += 1

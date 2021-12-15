__all__ = ['EndPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label
from .my_tk_widgets import PhotoImage, ClickButton
from PIL import ImageTk, Image
from client.page_manager import PageManager


class EndPage(Base):
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

        self.game_over_label_photo = PhotoImage(file=r"local_storage/images/game_over.png",
                                                ratio=self.ratio)  # opens the image
        self.game_over_label = Label(self, text="", image=self.game_over_label_photo, bg='#E4D6B6')  # details
        self.game_over_label.place(x=self.ratio * 500, y=self.ratio * 20)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = ClickButton(self, text="", image=self.exit_button_photo, bg='#E4D6B6', command=self.menu,
                                       activebackground='#E4D6B6', op_file="local_storage/images/exit_highlight.png",
                                       ratio=self.ratio)  # closes the leaderboard and opens menu
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.time_taken_label = Label(self, text='Time Taken:', font=('Courier', str(int(16 * self.ratio))),
                                      bg='#E4D6B6')  # label details
        self.time_taken_label.place(x=self.ratio * 200, y=self.ratio * 200)  # places the label

        self.time_taken_text = Label(self, font=('Courier', str(int(20 * self.ratio))), bg='#E4D6B6',
                                     text=self.page_manager.time + "s")  # details for the textbox
        self.time_taken_text.place(x=self.ratio * 350, y=self.ratio * 201)  # places the textbox
        self.time_taken_text.config(state='disabled')  # disables textbox to prevent editing

        self.words_spelt_correctly_label = Label(self, text='Words Spelt Correctly:',
                                                 font=('Courier', str(int(16 * self.ratio))), bg='#E4D6B6')
        self.words_spelt_correctly_label.place(x=self.ratio * 200, y=self.ratio * 250)

        self.words_spelt_correctly_text = Label(self, font=('Courier', str(int(20 * self.ratio))), bg='#E4D6B6',
                                                text=self.page_manager.correct)
        self.words_spelt_correctly_text.place(x=self.ratio * 490, y=self.ratio * 250)
        self.words_spelt_correctly_text.config(state='disabled')  # disables textbox to prevent editing

        self.words_spelt_incorrectly_label = Label(self, text='Total Score (with bonuses):',
                                                   font=('Courier', str(int(16 * self.ratio))), bg='#E4D6B6')
        self.words_spelt_incorrectly_label.place(x=self.ratio * 200, y=self.ratio * 300)

        self.words_spelt_incorrectly_text = Label(self, font=('Courier', str(int(20 * self.ratio))), bg='#E4D6B6',
                                                  text=self.page_manager.score + "points")
        self.words_spelt_incorrectly_text.place(x=self.ratio * 520, y=self.ratio * 300)
        self.words_spelt_incorrectly_text.config(state='disabled')  # disables textbox to prevent editing

        self.placement_label = Label(self, text='Have A Look At Where You Placed',
                                     font=('Courier', str(int(16 * self.ratio))), bg='#E4D6B6')
        self.placement_label.place(x=self.ratio * 200, y=self.ratio * 400)

        self.leaderboard_button_photo = PhotoImage(file=r"local_storage/images/leaderboard_end_screen.png",
                                                   ratio=self.ratio)  # opens the image to be used
        self.leaderboard_button = ClickButton(self, text="", image=self.leaderboard_button_photo, bg='#E4D6B6',
                                              activebackground='#E4D6B6', command=self.leaderboard, ratio=self.ratio,
                                              op_file="local_storage/images/leaderboard_end_screen_highlight.png")
        self.leaderboard_button.place(x=self.ratio * 202, y=self.ratio * 450)  # places the button

        self.squid_photo = PhotoImage(file=r"local_storage/images/squid_image.png", ratio=self.ratio)  # opens the image
        self.squid = Label(self, text="", image=self.squid_photo, bg='#E4D6B6')  # details
        self.squid.place(x=self.ratio * 900, y=self.ratio * 200)  # places the label

        self.word = Label(self, text='', width=16, anchor="center",
                          font=('Courier', str(int(20 * self.ratio))), bg='#E4D6B6')
        self.word.place(x=self.ratio * 245, y=self.ratio * 600)

        self.correct_word = Label(self, text='', width=16, anchor="center",
                                  font=('Courier', str(int(20 * self.ratio))), bg='#E4D6B6')
        self.correct_word.place(x=self.ratio * 245, y=self.ratio * 630)

        self.left_arrow_image = PhotoImage(file=r"local_storage/images/left_arrow.png", ratio=self.ratio * 0.1)
        self.left_arrow = ClickButton(self, image=self.left_arrow_image, bg='#E4D6B6', command=self.prev_word,
                                      op_file="local_storage/images/left_arrow_highlight.png", ratio=self.ratio * 0.1)
        self.left_arrow.place(x=self.ratio * 200, y=self.ratio * 600)

        self.right_arrow_image = PhotoImage(file=r"local_storage/images/right_arrow.png", ratio=self.ratio * 0.1)
        self.right_arrow = ClickButton(self, image=self.right_arrow_image, bg='#E4D6B6', command=self.next_word,
                                       op_file="local_storage/images/right_arrow_highlight.png", ratio=self.ratio * 0.1)
        self.right_arrow.place(x=self.ratio * 500, y=self.ratio * 600)

        self.protocol("WM_DELETE_WINDOW", self.menu)
        self.index = 0
        self.update_text()

    def menu(self) -> None:
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.menu_page(self)  # opens the menu page

    def leaderboard(self) -> None:
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.leaderboard_page(self)  # opens the leaderboard page

    def next_word(self) -> None:
        """
        Description: Function to show the next word
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.index += 1
        if self.index == 10:
            self.index = 0
        self.update_text()

    def prev_word(self) -> None:
        """
        Description: Function to show the next word
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.index -= 1
        if self.index == -1:
            self.index = 9
        self.update_text()

    def update_text(self) -> None:
        """
        Description: Function to update the words
        :return: void
        """
        new_words = self.page_manager.words_list[self.index]
        self.word.configure(text=new_words[0])
        self.correct_word.configure(text=new_words[1])
        if new_words[0] == new_words[1]:
            self.word.configure(fg="green")
            self.correct_word.configure(fg="green")
        else:
            self.word.configure(fg="red")
            self.correct_word.configure(fg="red")


if __name__ == "__main__":
    EndPage().mainloop()

__all__ = ['EndPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label
from .my_tk_widgets import PhotoImage, Button
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
        self.bg.place(x=self.ratio*-200, y=self.ratio*-100)  # positions the image in the background

        self.game_over_label_photo = PhotoImage(file=r"local_storage/images/game_over.png",
                                                ratio=self.ratio)  # opens the image
        self.game_over_label = Label(self, text="", image=self.game_over_label_photo, bg='#E4D6B6')  # details
        self.game_over_label.place(x=self.ratio*500, y=self.ratio*20)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = Button(self, text="", image=self.exit_button_photo, bg='#E4D6B6', activebackground='#E4D6B6',
                                  command=self.menu)  # closes the leaderboard and opens menu
        self.exit_button.place(x=self.ratio*1344, y=self.ratio*781)  # places the button

        self.time_taken_label = Label(self, text='Time Taken:', font=('Courier', str(int(16*self.ratio))),
                                      bg='#E4D6B6')  # label details
        self.time_taken_label.place(x=self.ratio*200, y=self.ratio*200)  # places the label

        self.time_taken_text = Label(self, font=('Courier', str(int(20*self.ratio))), bg='#E4D6B6',
                                     text=self.page_manager.time+"s")  # details for the textbox
        self.time_taken_text.place(x=self.ratio*350, y=self.ratio*201)  # places the textbox
        self.time_taken_text.config(state='disabled')  # disables textbox to prevent editing

        self.words_spelt_correctly_label = Label(self, text='Words Spelt Correctly:',
                                                 font=('Courier', str(int(16*self.ratio))), bg='#E4D6B6')
        self.words_spelt_correctly_label.place(x=self.ratio*200, y=self.ratio*250)

        self.words_spelt_correctly_text = Label(self, font=('Courier', str(int(20*self.ratio))), bg='#E4D6B6',
                                                text=self.page_manager.correct)
        self.words_spelt_correctly_text.place(x=self.ratio*490, y=self.ratio*250)
        self.words_spelt_correctly_text.config(state='disabled')  # disables textbox to prevent editing

        self.words_spelt_incorrectly_label = Label(self, text='Total Score (with bonuses):',
                                                   font=('Courier', str(int(16*self.ratio))), bg='#E4D6B6')
        self.words_spelt_incorrectly_label.place(x=self.ratio*200, y=self.ratio*300)

        self.words_spelt_incorrectly_text = Label(self, font=('Courier', str(int(20*self.ratio))), bg='#E4D6B6',
                                                  text=self.page_manager.score+"points")
        self.words_spelt_incorrectly_text.place(x=self.ratio*520, y=self.ratio*300)
        self.words_spelt_incorrectly_text.config(state='disabled')  # disables textbox to prevent editing

        self.placement_label = Label(self, text='Have A Look At Where You Placed',
                                     font=('Courier', str(int(16*self.ratio))), bg='#E4D6B6')
        self.placement_label.place(x=self.ratio*200, y=self.ratio*400)

        self.leaderboard_button_photo = PhotoImage(file=r"local_storage/images/leaderboard_end_screen.png",
                                                   ratio=self.ratio)  # opens the image to be used
        self.leaderboard_button = Button(self, text="", image=self.leaderboard_button_photo, bg='#E4D6B6',
                                         activebackground='#E4D6B6', command=self.leaderboard)  # details for button
        self.leaderboard_button.place(x=self.ratio*202, y=self.ratio*450)  # places the button

        self.squid_photo = PhotoImage(file=r"local_storage/images/squid_image.png", ratio=self.ratio)  # opens the image
        self.squid = Label(self, text="", image=self.squid_photo, bg='#E4D6B6')  # details
        self.squid.place(x=self.ratio*900, y=self.ratio*200)  # places the label

        self.protocol("WM_DELETE_WINDOW", self.menu)

    def menu(self):
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.menu_page(self)  # opens the menu page

    def leaderboard(self):
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.leaderboard_page(self)  # opens the leaderboard page


if __name__ == "__main__":
    EndPage().mainloop()

# MAKE SURE TO RE-ENABLE TEXTBOXES BEFORE YOU INSERT THE INFO (use self.textbox_name.config(state='normal')
# THEN DISABLE AGAIN AFTER INSERT TO PREVENT EDITING

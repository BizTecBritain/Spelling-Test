__all__ = ['LeaderboardPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

import json
from .tk_base import Base
from tkinter import Label, Text, StringVar, OptionMenu
from .my_tk_widgets import PhotoImage, ClickButton
from PIL import ImageTk, Image


class LeaderboardPage(Base):
    def __init__(self, page_manager):
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Leaderboard", 1920, 1080, page_manager)

        self.image_open_background = Image.open("local_storage/images/background.gif")  # opens the image
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=-200, y=self.ratio * -100)  # positions the image in the background

        self.squid_games_label_photo = PhotoImage(file=r"local_storage/images/squid_games.png",
                                                  ratio=self.ratio)  # opens the image
        self.squid_games_label = Label(self, text="", image=self.squid_games_label_photo, bg='#E4D6B6')  # label details
        self.squid_games_label.place(x=self.ratio * 250, y=self.ratio * 20)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = ClickButton(self, text="", image=self.exit_button_photo, bg='#E4D6B6',
                                       activebackground="#E4D6B6", op_file="local_storage/images/exit_highlight.png",
                                       command=self.menu, ratio=self.ratio)  # closes the leaderboard and opens menu
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.leaderboard_label_photo = PhotoImage(file=r"local_storage/images/leaderboard.png",
                                                  ratio=self.ratio)  # opens the image
        self.leaderboard_label = Label(self, text="", image=self.leaderboard_label_photo, bg='#E4D6B6')  # details
        self.leaderboard_label.place(x=self.ratio * 550, y=self.ratio * 230)  # places the leaderboard title

        self.first_place_textbox = Text(self, width=18, height=1,
                                        font=(None, str(int(25 * self.ratio))))  # details for the first textbox
        self.first_place_textbox.place(x=self.ratio * 400, y=self.ratio * 350)  # places the first textbox
        self.first_place_textbox.configure(state='disabled')  # sets the state to disabled to prevent editing

        self.first_place_label_photo = PhotoImage(file=r"local_storage/images/first.png",
                                                  ratio=self.ratio)  # opens the picture for first
        self.first_place_label = Label(self, text="", image=self.first_place_label_photo, bg='#E4D6B6')  # details
        self.first_place_label.place(x=self.ratio * 250, y=self.ratio * 350)  # places the first label

        self.second_place_textbox = Text(self, width=18, height=1,
                                         font=(None, str(int(25 * self.ratio))))  # details for the second textbox
        self.second_place_textbox.place(x=self.ratio * 400, y=self.ratio * 450)  # places the second textbox
        self.second_place_textbox.configure(state='disabled')  # sets the state to disabled to prevent editing

        self.second_place_label_photo = PhotoImage(file=r"local_storage/images/second.png",
                                                   ratio=self.ratio)  # opens the picture for second
        self.second_place_label = Label(self, text="", image=self.second_place_label_photo, bg='#E4D6B6')  # details
        self.second_place_label.place(x=self.ratio * 250, y=self.ratio * 450)  # places the second label

        self.third_place_textbox = Text(self, width=18, height=1,
                                        font=(None, str(int(25 * self.ratio))))  # details for the third textbox
        self.third_place_textbox.place(x=self.ratio * 400, y=self.ratio * 550)  # places the third textbox
        self.third_place_textbox.configure(state='disabled')  # sets the state to disabled to prevent editing

        self.third_place_label_photo = PhotoImage(file=r"local_storage/images/third.png",
                                                  ratio=self.ratio)  # opens the picture for third
        self.third_place_label = Label(self, text="", image=self.third_place_label_photo, bg='#E4D6B6')  # details
        self.third_place_label.place(x=self.ratio * 250, y=self.ratio * 550)  # places the third label

        self.fourth_place_textbox = Text(self, width=18, height=1,
                                         font=(None, str(int(25 * self.ratio))))
        self.fourth_place_textbox.place(x=self.ratio * 400, y=self.ratio * 650)
        self.fourth_place_textbox.configure(state='disabled')

        self.fourth_place_label_photo = PhotoImage(file=r"local_storage/images/fourth.png",
                                                   ratio=self.ratio)
        self.fourth_place_label = Label(self, text="", image=self.fourth_place_label_photo, bg='#E4D6B6')
        self.fourth_place_label.place(x=self.ratio * 250, y=self.ratio * 650)

        self.fifth_place_textbox = Text(self, width=18, height=1,
                                        font=(None, str(int(25 * self.ratio))))
        self.fifth_place_textbox.place(x=self.ratio * 400, y=self.ratio * 750)
        self.fifth_place_textbox.configure(state='disabled')

        self.fifth_place_label_photo = PhotoImage(file=r"local_storage/images/fifth.png", ratio=self.ratio)
        self.fifth_place_label = Label(self, text="", image=self.fifth_place_label_photo, bg='#E4D6B6')
        self.fifth_place_label.place(x=self.ratio * 250, y=self.ratio * 750)

        self.sixth_place_textbox = Text(self, width=18, height=1,
                                        font=(None, str(int(25 * self.ratio))))
        self.sixth_place_textbox.place(x=self.ratio * 950, y=self.ratio * 350)
        self.sixth_place_textbox.configure(state='disabled')

        self.sixth_place_label_photo = PhotoImage(file=r"local_storage/images/sixth.png", ratio=self.ratio)
        self.sixth_place_label = Label(self, text="", image=self.sixth_place_label_photo, bg='#E4D6B6')
        self.sixth_place_label.place(x=self.ratio * 800, y=self.ratio * 350)

        self.seventh_place_textbox = Text(self, width=18, height=1,
                                          font=(None, str(int(25 * self.ratio))))
        self.seventh_place_textbox.place(x=self.ratio * 950, y=self.ratio * 450)
        self.seventh_place_textbox.configure(state='disabled')

        self.seventh_place_label_photo = PhotoImage(file=r"local_storage/images/seventh.png", ratio=self.ratio)
        self.seventh_place_label = Label(self, text="", image=self.seventh_place_label_photo, bg='#E4D6B6')
        self.seventh_place_label.place(x=self.ratio * 800, y=self.ratio * 450)

        self.eighth_place_textbox = Text(self, width=18, height=1, font=(None, str(int(25 * self.ratio))))
        self.eighth_place_textbox.place(x=self.ratio * 950, y=self.ratio * 550)
        self.eighth_place_textbox.configure(state='disabled')

        self.eighth_place_label_photo = PhotoImage(file=r"local_storage/images/eighth.png", ratio=self.ratio)
        self.eighth_place_label = Label(self, text="", image=self.eighth_place_label_photo, bg='#E4D6B6')
        self.eighth_place_label.place(x=self.ratio * 800, y=self.ratio * 550)

        self.ninth_place_textbox = Text(self, width=18, height=1, font=(None, str(int(25 * self.ratio))))
        self.ninth_place_textbox.place(x=self.ratio * 950, y=self.ratio * 650)
        self.ninth_place_textbox.configure(state='disabled')

        self.ninth_place_label_photo = PhotoImage(file=r"local_storage/images/ninth.png", ratio=self.ratio)
        self.ninth_place_label = Label(self, text="", image=self.ninth_place_label_photo, bg='#E4D6B6')
        self.ninth_place_label.place(x=self.ratio * 800, y=self.ratio * 650)

        self.tenth_place_textbox = Text(self, width=18, height=1, font=(None, str(int(25 * self.ratio))))
        self.tenth_place_textbox.place(x=self.ratio * 950, y=self.ratio * 750)
        self.tenth_place_textbox.configure(state='disabled')

        self.tenth_place_label_photo = PhotoImage(file=r"local_storage/images/tenth.png", ratio=self.ratio)
        self.tenth_place_label = Label(self, text="", image=self.tenth_place_label_photo, bg='#E4D6B6')
        self.tenth_place_label.place(x=self.ratio * 800, y=self.ratio * 750)

        self.options = ['Easy', 'Medium', 'Hard']  # options for drop down
        self.clicked = StringVar()  # variable for the value chosen
        self.clicked.set('Easy')  # default setting
        self.clicked.trace("w", lambda *args: self.refresh())
        self.drop_down = OptionMenu(self, self.clicked, *self.options)  # details
        self.drop_down.place(x=self.ratio * 50, y=self.ratio * 60)  # places the drop down

        self.options_data = ['Scores', 'Words']  # options for drop down
        self.clicked_data = StringVar()  # variable for the value chosen
        self.clicked_data.set('Scores')  # default setting
        self.clicked_data.trace("w", lambda *args: self.refresh())
        self.drop_down_data = OptionMenu(self, self.clicked_data, *self.options_data)  # details
        self.drop_down_data.place(x=self.ratio * 1400, y=self.ratio * 60)  # places the drop down

        self.difficulty_label = Label(self, text='Difficulty', font=('Courier', '16'), bg='#E4D6B6')  # label details
        self.difficulty_label.place(x=self.ratio * 20, y=self.ratio * 20)  # places the label

        self.datatype_label = Label(self, text='Datatype', font=('Courier', '16'), bg='#E4D6B6')  # label details
        self.datatype_label.place(x=self.ratio * 1380, y=self.ratio * 20)  # places the label

        self.refresh_button_photo = PhotoImage(file=r"local_storage/images/refresh.png", ratio=self.ratio*0.75)
        self.refresh_button = ClickButton(self, text="", image=self.refresh_button_photo, bg='#E4D6B6',
                                          command=self.refresh_click, activebackground='#E4D6B6', ratio=self.ratio*0.75,
                                          op_file="local_storage/images/refresh_highlight.png")
        self.refresh_button.place(x=self.ratio*5, y=self.ratio*760)  # places button

        self.refresh()
        self.protocol("WM_DELETE_WINDOW", self.menu)

    def menu(self):
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.menu_page(self)  # opens the menu page

    def refresh_click(self) -> None:
        """
        Description: Function to refresh leaderboard
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.refresh()

    def refresh(self) -> None:
        """
        Description: Function to refresh leaderboard
        :return: void
        """
        score_boxes = [self.first_place_textbox,
                       self.second_place_textbox,
                       self.third_place_textbox,
                       self.fourth_place_textbox,
                       self.fifth_place_textbox,
                       self.sixth_place_textbox,
                       self.seventh_place_textbox,
                       self.eighth_place_textbox,
                       self.ninth_place_textbox,
                       self.tenth_place_textbox]
        for score_box in score_boxes:
            score_box.configure(state='normal')
            score_box.delete("1.0", 'end')
            score_box.configure(state='disabled')
        resp = self.page_manager.data_channel.get_text("get_leaderboard/{0}/{1}".format(self.clicked_data.get().lower(),
                                                                                        self.clicked.get().lower()))
        if len(resp) == 0:
            raise SystemError(self.page_manager.session_manager.errors[-3])
        resp_dict = json.loads(resp)
        if self.clicked_data.get().lower() == "scores":
            for index, person in enumerate(resp_dict):
                score_boxes[index].configure(state='normal')
                score_boxes[index].insert("1.0", "{0} {1}p {2}s".format(person[1], person[2], str(int(person[3])/1000)))
                score_boxes[index].configure(state='disabled')
        elif self.clicked_data.get().lower() == "words":
            for index, word in enumerate(resp_dict):
                score_boxes[index].configure(state='normal')
                score_boxes[index].insert("1.0", "{0} {1}%".format(word[0][0],
                                                                   int((int(word[0][1])/int(word[0][2]))*100)))
                score_boxes[index].configure(state='disabled')
        self.update()
        self.update_idletasks()

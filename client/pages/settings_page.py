__all__ = ['SettingsPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label
from .my_tk_widgets import PhotoImage, Button
from PIL import ImageTk, Image
from client.page_manager import PageManager
from customtkinter import CTkSlider


class SettingsPage(Base):
    def __init__(self, page_manager: PageManager = None):
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Settings", 1920, 1080, page_manager)

        music_volume_set = 100  # default sound setting
        game_audio_volume_set = 100  # default sound setting

        self.image_open_background = Image.open("local_storage/images/background.gif")  # opens the image
        self.image_background = ImageTk.PhotoImage(self.image_open_background)
        self.bg = Label(image=self.image_background)  # sets the image to a label
        self.bg.image = self.image_background  # makes the background the image
        self.bg.place(x=self.ratio * -200, y=self.ratio * -100)  # positions the image in the background

        self.squid_games_label_photo = PhotoImage(file=r"local_storage/images/squid_games.png", ratio=self.ratio)
        self.squid_games_label = Label(self, text="", image=self.squid_games_label_photo, bg='#E4D6B6')  # label details
        self.squid_games_label.place(x=self.ratio * 250, y=self.ratio * 20)  # places the label

        self.settings_label_photo = PhotoImage(file=r"local_storage/images/settings_label.png",
                                               ratio=self.ratio)  # opens the image
        self.settings_label = Label(self, text="", image=self.settings_label_photo, bg='#E4D6B6')  # details
        self.settings_label.place(x=self.ratio * 600, y=self.ratio * 170)  # places the label

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = Button(self, text="", image=self.exit_button_photo, bg='#E4D6B6', activebackground='#E4D6B6',
                                  command=self.menu)  # closes the leaderboard and opens menu
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.volume_slider_label = Label(self, text="Music Volume", font=("Courier", 16),
                                         bg='#E4D6B6')  # details for label
        self.volume_slider_label.place(x=self.ratio * 100, y=self.ratio * 300)  # places label

        def main_volume_change(value):  # PUT CODE TO CHANGE VOLUME HERE
            """
            Description: Function for the main volume slider is used
            :return: void
            """
            main_volume = value/10  # divides by 10 because pygame sets the volume between 1 and 10
            print(main_volume)

        def game_volume_change(value):  # PUT CODE TO CHANGE GAME VOLUME HERE
            """
            Description: Function for when the game audio slider is used
            :return: void
            """
            game_volume = value/10  # divides by 10 becasue pygame sets the volume between 1 and 10
            print(game_volume)

        self.volume_main_slider = CTkSlider(master=self, width=1025, height=17, border_width=5, from_=0, to=100,
                                            bg_color='#E4D6B6', command=main_volume_change)  # details
        self.volume_main_slider.place(x=self.ratio * 270, y=self.ratio * 305)  # places
        self.volume_main_slider.set(music_volume_set)  # sets the slider to its default

        self.game_audio_slider_label = Label(self, text="Game Audio", font=("Courier", 16), bg='#E4D6B6')  # details
        self.game_audio_slider_label.place(x=self.ratio * 100, y=self.ratio * 400)  # [places

        self.game_audio_slider = CTkSlider(master=self, width=1025, height=17, border_width=5, from_=20, to=100,
                                           bg_color='#E4D6B6', command=game_volume_change)  # details
        self.game_audio_slider.place(x=self.ratio * 270, y=self.ratio * 405)  # places
        self.volume_main_slider.set(game_audio_volume_set)  # sets the slider to its default

        self.test_button_photo = PhotoImage(file=r"local_storage/images/test_sound.png", ratio=self.ratio)  # image
        self.test_button = Button(self, text="", image=self.test_button_photo, bg='#E4D6B6', activebackground='#E4D6B6',
                                  command=self.test_sound)  # details
        self.test_button.place(x=self.ratio * 279, y=self.ratio * 520)  # places the button

        self.unmute_button_photo = PhotoImage(file=r"local_storage/images/unmute.png", ratio=self.ratio)
        self.unmute_button = Button(self, text="", image=self.unmute_button_photo, bg='#E4D6B6',
                                    activebackground='#E4D6B6', command=self.mute_sound)
        self.unmute_button.place(x=self.ratio * 260, y=self.ratio * 590)  # places the button

        self.mute_button_photo = PhotoImage(file=r"local_storage/images/mute.png", ratio=self.ratio)
        self.mute_button = Button(self, text="", image=self.mute_button_photo, bg='#E4D6B6', activebackground='#E4D6B6',
                                  command=self.unmute_sound)  # closes the leaderboard and opens menu
        self.mute_button.place(x=self.ratio * 260, y=self.ratio * 590)  # places the button

        self.apply_button_photo = PhotoImage(file=r"local_storage/images/apply.png", ratio=self.ratio)  # opens image
        self.apply_button = Button(self, text="", image=self.apply_button_photo, bg='#E4D6B6',
                                   activebackground='#E4D6B6', command=self.apply)  # details
        self.apply_button.place(x=self.ratio * 2, y=self.ratio * 781)  # places the button

        self.protocol("WM_DELETE_WINDOW", self.menu)

    def menu(self):
        """
        Description: Function to return to the menu
        :return: void
        """
        self.page_manager.menu_page(self)  # opens the menu page

    def test_sound(self):
        """
        Description: Function to test sound is working
        :return: void
        """
        pass

    def mute_sound(self):
        """
        Description: Function for when mute is pressed
        :return: void
        """
        self.mute_button.lift(self.unmute_button)  # shows the unmute button

    def unmute_sound(self):
        """
        Description: Function for when unmute is pressed
        :return: void
        """
        self.unmute_button.lift(self.mute_button)  # shows the mute button

    def apply(self):
        """
        Description: Function for when apply is pressed, applys chosen settings
        :return: void
        """
        pass

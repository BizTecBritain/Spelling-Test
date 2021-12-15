__all__ = ['SettingsPage']
__version__ = '1.0.0'
__author__ = 'Finley Wallace - Wright'

from .tk_base import Base
from tkinter import Label, Checkbutton, IntVar
from .my_tk_widgets import PhotoImage, Button, Slider, ClickButton
from PIL import ImageTk, Image
from client.page_manager import PageManager
from data_management.config import Config
from client.error_manager import ask_yes_no


class SettingsPage(Base):
    def __init__(self, page_manager: PageManager = None):
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Settings", 1920, 1080, page_manager)

        self.config_parser = Config()
        self.config_parser.load("local_storage/client.ini")
        self.music_volume_set = float(self.config_parser.read_tag("USERINFO", "music_volume"))  # default sound setting
        self.game_audio_volume_set = float(self.config_parser.read_tag("USERINFO", "game_volume"))
        temp_click = int(self.config_parser.read_tag("USERINFO", "click"))
        self.temp_music = 0
        self.temp_game = 20
        self.music_mute = False
        self.game_mute = False
        self.applied = None

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

        self.mute_button_photo = PhotoImage(file=r"local_storage/images/mute.png", ratio=self.ratio)
        self.med_audio_photo = PhotoImage(file=r"local_storage/images/audio_med.png", ratio=self.ratio)
        self.mute_button_music = Button(self, text="", image=self.mute_button_photo, bg='#E4D6B6',
                                        activebackground='#E4D6B6', command=self.unmute_sound)
        self.mute_button_music.place(x=self.ratio * 1080, y=self.ratio * 265)  # places the button

        self.unmute_button_photo = PhotoImage(file=r"local_storage/images/audio.png", ratio=self.ratio)
        self.unmute_button_music = Button(self, text="", image=self.unmute_button_photo, bg='#E4D6B6',
                                          activebackground='#E4D6B6', command=self.mute_sound)
        self.unmute_button_music.place(x=self.ratio * 1080, y=self.ratio * 265)  # places the button

        self.lower_button_photo = PhotoImage(file=r"local_storage/images/audio_low.png", ratio=self.ratio)
        self.mute_button_game = Button(self, text="", image=self.lower_button_photo, bg='#E4D6B6',
                                       activebackground='#E4D6B6', command=self.unmute_game)
        self.mute_button_game.place(x=self.ratio * 1080, y=self.ratio * 365)  # places the button

        self.unmute_button_game = Button(self, text="", image=self.unmute_button_photo, bg='#E4D6B6',
                                         activebackground='#E4D6B6', command=self.lower_game)
        self.unmute_button_game.place(x=self.ratio * 1080, y=self.ratio * 365)  # places the button

        self.exit_button_photo = PhotoImage(file=r"local_storage/images/exit.png", ratio=self.ratio)  # opens the image
        self.exit_button = Button(self, text="", image=self.exit_button_photo, bg='#E4D6B6', activebackground='#E4D6B6',
                                  command=self.menu)  # closes the leaderboard and opens menu
        self.exit_button.place(x=self.ratio * 1344, y=self.ratio * 781)  # places the button

        self.volume_slider_label = Label(self, text="Music Volume: " + str(self.music_volume_set * 100),
                                         font=("Courier", str(int(16 * self.ratio))), bg='#E4D6B6')  # details for label
        self.volume_slider_label.place(x=self.ratio * 100, y=self.ratio * 300)  # places label

        self.click_audio_var = IntVar()
        self.click_audio_var.set(temp_click)
        self.click_audio_var.trace_add("write", lambda *args: click_change())
        self.click_audio = Checkbutton(self, text="Click audio", font=("Courier", str(int(16 * self.ratio))),
                                       variable=self.click_audio_var, bg='#E4D6B6', activebackground='#E4D6B6')
        self.click_audio.place(x=self.ratio * 100, y=self.ratio * 500)

        def click_change() -> None:
            """
            Description: Function to trace when the checkbutton is pressed
            :return: void
            """
            if self.click_audio_var.get():
                self.page_manager.audio_manager.click()
            self.applied = False

        def main_volume_change(value: float) -> None:
            """
            Description: Function for the main volume slider is used
            :param value: the new value of the slider
            :return: void
            """
            self.music_volume_set = int(value * 10) / 1000
            self.volume_slider_label.config(text="Music Volume: %d" % round(value, 0))
            if self.music_mute:
                self.unmute_button_music.lift(self.mute_button_music)
                self.music_mute = False
            if value == 0:
                self.unmute_button_music.configure(image=self.mute_button_photo)
            elif value < 33:
                self.unmute_button_music.configure(image=self.lower_button_photo)
            elif value < 66:
                self.unmute_button_music.configure(image=self.med_audio_photo)
            else:
                self.unmute_button_music.configure(image=self.unmute_button_photo)
            self.applied = False

        def game_volume_change(value: float) -> None:
            """
            Description: Function for when the game audio slider is used
            :param value: the new value of the slider
            :return: void
            """
            self.game_audio_volume_set = int(value * 10) / 1000
            self.game_audio_slider_label.config(text="Game Audio: %d" % round(value, 0))
            if self.game_mute:
                self.unmute_button_game.lift(self.mute_button_game)
                self.game_mute = False
            if value < 47.0:
                self.unmute_button_game.configure(image=self.lower_button_photo)
            elif value < 73.0:
                self.unmute_button_game.configure(image=self.med_audio_photo)
            else:
                self.unmute_button_game.configure(image=self.unmute_button_photo)
            self.applied = False

        self.volume_main_slider = Slider(master=self, width=720, height=20, border_width=5, to=100,
                                         ratio=self.ratio, command=main_volume_change)  # details
        self.volume_main_slider.place(x=self.ratio * 350, y=self.ratio * 305)  # places
        self.volume_main_slider.set(self.music_volume_set * 100)  # sets the slider to its default

        self.game_audio_slider_label = Label(self, text="Game Audio: " + str(self.game_audio_volume_set * 100),
                                             font=("Courier", str(int(16 * self.ratio))), bg='#E4D6B6')  # details
        self.game_audio_slider_label.place(x=self.ratio * 100, y=self.ratio * 400)

        self.game_audio_slider = Slider(master=self, width=720, height=20, border_width=5, from_=20, to=100,
                                        ratio=self.ratio, command=game_volume_change)  # details
        self.game_audio_slider.place(x=self.ratio * 350, y=self.ratio * 405)  # places
        self.game_audio_slider.set(self.game_audio_volume_set * 100)  # sets the slider to its default

        self.test_button_photo = PhotoImage(file=r"local_storage/images/test_sound.png", ratio=self.ratio*0.65)  # image
        self.test_button_music = ClickButton(self, text="", image=self.test_button_photo, command=self.test_sound_music,
                                             activebackground='#E4D6B6', bg='#E4D6B6', ratio=self.ratio*0.65,
                                             op_file="local_storage/images/test_sound_highlight.png")  # details
        self.test_button_music.place(x=self.ratio * 1180, y=self.ratio * 280)  # places the button

        self.test_button_game = ClickButton(self, text="", image=self.test_button_photo, command=self.test_sound_game,
                                            activebackground='#E4D6B6', bg='#E4D6B6', ratio=self.ratio*0.65,
                                            op_file="local_storage/images/test_sound_highlight.png")  # details
        self.test_button_game.place(x=self.ratio * 1180, y=self.ratio * 380)  # places the button

        self.apply_button_photo = PhotoImage(file=r"local_storage/images/apply.png", ratio=self.ratio)
        self.apply_button = ClickButton(self, text="", image=self.apply_button_photo, bg='#E4D6B6', ratio=self.ratio,
                                        activebackground='#E4D6B6', command=self.apply,
                                        op_file="local_storage/images/apply_highlight.png")  # details
        self.apply_button.place(x=self.ratio * 2, y=self.ratio * 781)  # places the button

        self.credits_button_photo = PhotoImage(file=r"local_storage/images/credits_button.png", ratio=self.ratio*1.5)
        self.credits_button = ClickButton(self, text="", image=self.credits_button_photo, bg='#E4D6B6',
                                          activebackground='#E4D6B6', command=self.credits, ratio=self.ratio*1.5,
                                          op_file="local_storage/images/credits_button_highlight.png")  # details

        self.credits_button.place(x=self.ratio * 520, y=self.ratio * 600)  # places the button

        self.applied = True
        self.playing = 0
        self.check_event()
        self.protocol("WM_DELETE_WINDOW", self.menu)

    def credits(self) -> None:
        """
        Description: Function for when the credits button is pressed
        :return: void
        """
        self.page_manager.audio_manager.click()
        self.page_manager.credits_page(self)  # opens the credits page

    def menu(self) -> None:
        """
        Description: Function to return to the menu
        :return: void
        """
        if not self.applied:
            if ask_yes_no("Apply Settings", "Do you want to apply the settings?"):
                self.apply()
        self.page_manager.audio_manager.start("local_storage/client_audio/main_menu_music.mp3", -1, True)
        self.page_manager.menu_page(self)  # opens the menu page

    def test_sound_music(self) -> None:
        """
        Description: Function to test sound is working
        :return: void
        """
        self.apply()
        self.page_manager.audio_manager.stop()
        if self.playing != 1:
            self.page_manager.audio_manager.start("local_storage/client_audio/main_menu_music.mp3", 0, True)
            self.playing = 1
        else:
            self.playing = 0

    def test_sound_game(self) -> None:
        """
        Description: Function to test sound is working
        :return: void
        """
        self.apply()
        self.page_manager.audio_manager.stop()
        if self.playing != 2:
            self.page_manager.audio_manager.start("local_storage/client_audio/test_audio.mp3")
            self.playing = 2
        else:
            self.playing = 0

    def mute_sound(self) -> None:
        """
        Description: Function for when mute is pressed
        :return: void
        """
        self.mute_button_music.lift(self.unmute_button_music)  # shows the unmute button
        self.temp_music = self.music_volume_set * 100
        self.volume_main_slider.set(0)
        self.music_mute = True

    def unmute_sound(self) -> None:
        """
        Description: Function for when unmute is pressed
        :return: void
        """
        self.music_mute = False
        self.unmute_button_music.lift(self.mute_button_music)  # shows the mute button
        self.volume_main_slider.set(self.temp_music)

    def lower_game(self) -> None:
        """
        Description: Function for when mute is pressed
        :return: void
        """
        self.mute_button_game.lift(self.unmute_button_game)  # shows the unmute button
        self.temp_game = self.game_audio_volume_set * 100
        self.game_audio_slider.set(20)
        self.game_mute = True

    def unmute_game(self) -> None:
        """
        Description: Function for when unmute is pressed
        :return: void
        """
        self.game_mute = False
        self.unmute_button_game.lift(self.mute_button_game)  # shows the mute button
        self.game_audio_slider.set(self.temp_game)

    def apply(self) -> None:
        """
        Description: Function for when apply is pressed, applys chosen settings
        :return: void
        """
        self.page_manager.audio_manager.music_volume = self.music_volume_set
        self.config_parser.append_tag("USERINFO", "music_volume", str(self.music_volume_set))
        self.page_manager.audio_manager.game_volume = self.game_audio_volume_set
        self.config_parser.append_tag("USERINFO", "game_volume", str(self.game_audio_volume_set))
        self.page_manager.audio_manager.click_play = self.click_audio_var.get()
        self.config_parser.append_tag("USERINFO", "click", str(self.click_audio_var.get()))
        self.applied = True

    def check_event(self) -> None:
        """
        Description: Fuction that recursively checks if the music has stopped
        :return: void
        """
        for event in self.page_manager.audio_manager.get_events():
            if event.type == self.page_manager.audio_manager.MUSIC_END:
                self.playing = 0
        self.after(100, self.check_event)

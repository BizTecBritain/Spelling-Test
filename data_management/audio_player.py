__all__ = ['AudioPlayer']
__version__ = '1.2.1'
__author__ = 'Alexander Bisland'

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class AudioPlayer:
    def __init__(self) -> None:
        """
        Description: Constructor sets up attributes and objects
        :return: void
        """
        pygame.mixer.pre_init(frequency=44100)
        pygame.init()
        pygame.mixer.init(frequency=44100)
        self.paused = False
        self.music_volume = 100  # TODO Change
        self.game_volume = 100
        self.click_play = True
        self.MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

    def start(self, file: str, loops: int = 0, music: bool = False) -> None:
        """
        Description: Function to start a new peice of music
        :param file: the name of the file to play
        :param loops: the number of times to play
        :param music: if the audio is a music file or audio file
        :return: void
        """
        pygame.mixer.music.stop()
        pygame.mixer.init()
        if music:
            pygame.mixer.music.set_volume(self.music_volume)
        else:
            pygame.mixer.music.set_volume(self.game_volume)
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loops)
        self.paused = False

    def pause(self) -> None:
        """
        Description: Function to pause/unpause the music
        :return: void
        """
        if pygame.mixer.music.get_busy():
            if self.paused:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            self.paused = not self.paused

    @staticmethod
    def stop() -> None:
        """
        Description: Function to stop a channel from playing and delete it
        :return: void
        """
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    @staticmethod
    def fade() -> None:
        """
        Description: Function to stop a channel from playing and delete it
        :return: void
        """
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(200)

    def click(self) -> None:
        """
        Description: Function to play mouse click sound
        :return: void
        """
        if self.click_play:
            pygame.mixer.Sound("local_storage/client_audio/MouseClick.wav").play()

    @staticmethod
    def get_events() -> pygame.event:
        """
        Description: Function to get the events from pygame
        :return: pygame.event - the events
        """
        return pygame.event.get()

    def __del__(self) -> None:
        """
        Description: Destructor of class cleans up pygame.mixer object
        :return:
        """
        pygame.mixer.quit()

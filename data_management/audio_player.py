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
        pygame.mixer.init()
        self.paused = False

    def start(self, file: str, loops: int = 0) -> None:
        """
        Description: Function to start a new peice of music
        :param file: the name of the file to play
        :param loops: the number of times to play
        :return: void
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
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
    def click() -> None:
        """
        Description: Function to play mouse click sound
        :return: void
        """
        pygame.mixer.Sound("local_storage/clieent_audio/MouseClick.wav").play()

    def __del__(self) -> None:
        """
        Description: Destructor of class cleans up pygame.mixer object
        :return:
        """
        pygame.mixer.quit()

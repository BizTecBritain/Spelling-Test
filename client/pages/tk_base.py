from tkinter import Tk
from client.page_manager import PageManager


class Base(Tk):
    ratios = {1536: 1, 1280: 5 / 6}

    def __init__(self, title: str, width: int, height: int, page_manager: PageManager = None) -> None:
        """
        Description: Constructor sets up attributes
        :param title: the title of the window
        :param width: the width of the window
        :param height: the height of the window
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__()
        self.page_manager = page_manager
        self.title(title)
        self.geometry(str(width) + "x" + str(height))
        self.attributes("-fullscreen", True)
        self.resizable(False, False)
        try:
            self.ratio = Base.ratios[self.winfo_screenwidth()]
        except KeyError:
            self.ratio = 1
        self.focus_force()

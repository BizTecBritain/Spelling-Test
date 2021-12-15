__all__ = ['show_error', 'ask_yes_no']
__version__ = '1.1.5'
__author__ = 'Edward Hopper'

from tkinter import Tk, messagebox


def show_error(error: Exception, withdraw: bool = False) -> None:
    """
    Description: Function to show a messagebox when an error occurs
    :param error: the error that has occured
    :param withdraw: whether to show the window or not
    :return: void
    """
    if withdraw:
        Tk().withdraw()
    messagebox.showerror(type(error).__name__, str(error))


def ask_yes_no(title: str, question: str, withdraw: bool = False) -> bool:
    """
    Description: Function to show a messagebox to ask the user a yes no question
    :param title: the title of the messagebox window
    :param question: the question to ask
    :param withdraw: whether to show the window or not
    :return: bool - True for a yes response, False for a no
    """
    if withdraw:
        Tk().withdraw()
    return messagebox.askyesno(title, question)

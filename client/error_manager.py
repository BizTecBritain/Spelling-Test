from tkinter import Tk, messagebox


def show_error(error: Exception, withdraw: bool = False):
    if withdraw:
        Tk().withdraw()
    messagebox.showerror(type(error).__name__, str(error))


def ask_yes_no(title: str, question: str, withdraw: bool = False):
    if withdraw:
        Tk().withdraw()
    return messagebox.askyesno(title, question)

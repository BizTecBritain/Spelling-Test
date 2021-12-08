__all__ = ['PhotoImage', 'Button', 'ClickButton']
__version__ = '3.0.2'
__author__ = 'Alexander Bisland'

import tkinter
from PIL import ImageTk, Image


class PhotoImage(ImageTk.PhotoImage):
    def __init__(self, *args, **kwargs) -> None:
        """
        Description: Constructor resizes image and then calls super()
        :param args: the arguments for ImageTk.PhotoImage.__init__()
        :param kwargs: the keyword arguments for ImageTk.PhotoImage.__init__()
        :return: void
        """
        try:
            ratio = kwargs.pop('ratio')
        except KeyError:
            ratio = None
        try:
            image = Image.open(kwargs.pop('file'))
        except KeyError:
            try:
                image = kwargs.pop("image")
            except KeyError:
                return
        if ratio is not None:
            width, height = image.size
            image = image.resize((int(width*ratio), int(height*ratio)), Image.ANTIALIAS)
        super(PhotoImage, self).__init__(image, *args, **kwargs)


class Button(tkinter.Label):
    def __init__(self, *args, **kwargs) -> None:
        """
        Description: Constructor resizes image and then calls super()
        :param args: the arguments for tkinter.Label.__init__()
        :param kwargs: the keyword arguments for tkinter.Label.__init__()
        :return: void
        """
        command = kwargs.pop('command')
        super(Button, self).__init__(*args, **kwargs)
        self.bind("<Button-1>", lambda event: command())


class ClickButton(tkinter.Label):
    def __init__(self, *args, **kwargs) -> None:
        """
        Description: Constructor resizes image and then calls super()
        :param args: the arguments for tkinter.Label.__init__()
        :param kwargs: the keyword arguments for tkinter.Label.__init__()
        :return: void
        """
        self.command = kwargs.pop('command')
        self.op_file = kwargs.pop('op_file')
        self.ratio = kwargs.pop('ratio')
        self.image = kwargs['image']
        self.img = None
        super(ClickButton, self).__init__(*args, **kwargs)
        self.bind("<ButtonPress-1>", lambda event: self.OnMouseDown())
        self.bind("<ButtonRelease-1>", lambda event: self.OnMouseUp())

    def OnMouseDown(self) -> None:
        """
        Description: Function that is run while the mouse is down on the button
        :return: void
        """
        self.img = PhotoImage(file=self.op_file, ratio=self.ratio)
        self.configure(image=self.img)

    def OnMouseUp(self) -> None:
        """
        Description: Function that is run while the mouse is released from the button
        :return: void
        """
        self.configure(image=self.image)
        self.command()

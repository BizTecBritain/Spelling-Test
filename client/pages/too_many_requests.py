from .tk_base import Base


class TooManyRequestsPage(Base):
    def __init__(self, page_manager) -> None:
        """
        Description: Constructor makes all of the tkinter widgets
        :param page_manager: the PageManager object
        :return: void
        """
        super().__init__("Too Many Requests", 1920, 1080, page_manager)
        self.page_manager.menu_page(self)

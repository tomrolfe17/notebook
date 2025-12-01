import tkinter as tk
import sys

from apple_menu import AppleMenu
from file_menu import FileMenu
from edit_menu import EditMenu




class Menu(tk.Menu):
    """A menu for a notebook window."""


    def __init__(self, parent: tk.Toplevel):
        self.notebook = parent

        super().__init__(parent)

        self._configure_menus()
    

    def _configure_menus(self) -> None:
        """Internal function. Configure the menu."""
   
        # Application menu, we can attach this one straight away
        # as it comes first after the apple icon menu.
        apple_menu = AppleMenu(self)
        self.add_cascade(menu=apple_menu)

        # If any more menus are required then we can define them
        # here but not necessarily attach then straight away so we
        # get the right order.

        # File menu
        self.file_menu = FileMenu(self)
        self.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = EditMenu(self)
        self.add_cascade(label="Edit", menu=self.edit_menu)     
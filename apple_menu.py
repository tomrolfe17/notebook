import tkinter as tk
from tkinter import messagebox



class AppleMenu(tk.Menu):
    """
    The apple or application menu. 
    
    The only addition is the About Notebook command which opens a new
    toplevel.
    
    """

    def __init__(self, parent: tk.Menu):
        self.notebook_menu = parent

        super().__init__(parent, name="apple")

        self.add_command(label="About Notebook", command=self._open_about)
        self.add_separator()


    def _open_about(self) -> None:
        """
        Internal function.
        
        Open the about dialog.
        
        """
        messagebox.showinfo(message="Notebook", detail="Version 1.0\n", 
            icon="info", parent=self.notebook_menu.notebook)     
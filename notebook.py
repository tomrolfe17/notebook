import tkinter as tk
from tkinter import ttk

from menu import Menu
from text_area import TextArea




class Notebook(tk.Toplevel):
    """
    A notebook window for editing text documents. 
    
    It contains a menu, line bar, text area and status bar.
    
    The menu contains typical commands for managing the contents of the 
    text editor. The index bar provides line number labels which auto
    update during editing of the text editor. The text editor allows for
    editing text documents. The status bar provides updates on the
    content of the text editor including the type of file open and the
    position of the cursor in the text editor.

    """

    def __init__(self, parent: tk.Tk, name: str, xpos: float, ypos: float):
        self.manager = parent
        self.name = name
        self.width = 600
        self.height = 400

        super().__init__(parent)
        self.title(name)
        self.minsize(self.width, self.height)
        self.geometry(f"+{xpos}+{ypos}")
        self.protocol("WM_DELETE_WINDOW", 
            lambda: self.manager.close_notebook(name))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._configure_widgets()


    def _configure_widgets(self) -> None:
        """
        Internal function.
        
        Configure the widgets for the notebook.
        
        """

        self.menu = Menu(self)
        self.configure(menu=self.menu)

        self.text_area = TextArea(self)
        self.text_area.grid(row=0, column=0, sticky="nsew")

        vscroll = ttk.Scrollbar(self, orient="vertical",
            command=self.text_area.yview)
        vscroll.grid(row=0, column=1, sticky="ns")
        self.text_area.configure(yscrollcommand=vscroll.set)

        # Lastly we request that the text area gets the focus on opening
        # from the window manager
        self.text_area.focus()    
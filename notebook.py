import tkinter as tk
from tkinter import ttk

from menu import Menu
from text_area import TextArea
from status_bar import StatusBar




class Notebook(tk.Toplevel):
    """A Notebook window for editing text documents."""


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

        self._configure_traces()


    def _configure_widgets(self) -> None:
        """Internal function. Configure the widgets for the notebook."""

        self.menu = Menu(self)
        self.configure(menu=self.menu)

        self.text_area = TextArea(self)
        self.text_area.grid(row=0, column=0, sticky="nsew")

        sep_right = ttk.Separator(self, orient="vertical")
        sep_right.grid(row=0, column=1, sticky="ns")

        vscroll = ttk.Scrollbar(self, orient="vertical",
            command=self.text_area.yview)
        vscroll.grid(row=0, column=2, sticky="ns")
        self.text_area.configure(yscrollcommand=vscroll.set)

        sep_bottom = ttk.Separator(self, orient="horizontal")
        sep_bottom.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=2, column=0, columnspan=3, sticky="ew")

        # Lastly we request that the Text Area gets the focus on opening
        # from the window manager.
        self.text_area.focus()


    def _configure_traces(self) -> None:
        """Internal function. Configure the traces between widgets."""

        # Configure the traces to the Text Area variables tracking the
        # content changes so that the Status Bar variables can be 
        # updated.
        self.text_area.chars.trace_add("write", 
            lambda *args: self.status_bar.update_chars(
                self.text_area.chars.get()))
        self.text_area.lines.trace_add("write",
            lambda *args: self.status_bar.update_lines(
                self.text_area.lines.get()))
        self.text_area.cursor.trace_add("write",
            lambda *args: self.status_bar.update_cursor(
                self.text_area.cursor.get()))

        # Trace for the filetype variable
        self.menu.file_menu.filetype.trace_add("write",
            lambda *args: self.status_bar.update_filetype(
                self.menu.file_menu.filetype.get()))  
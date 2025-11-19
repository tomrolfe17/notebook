import tkinter as tk
from tkinter import ttk




class StatusBar(ttk.Frame):
    """A Status Bar providing updates on Text Area content."""


    def __init__(self, parent: tk.Toplevel):
        self.notebook = parent
        self.filetype = tk.StringVar(value="")
        self.chars = tk.StringVar(value="Chars 0")
        self.lines = tk.StringVar(value="Lines 1")
        self.cursor = tk.StringVar(value="Ln 1, Col 1, Pos 1")

        super().__init__(parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,1,2,3,4), weight=1)

        self._configure_widgets()


    def _configure_widgets(self) -> None:
        """Internal function. Configure the widgets for the Status Bar"""

        # Create the labels for the document type, current line, total 
        # lines and chars
        lbl_filetype = ttk.Label(self, textvariable=self.filetype)
        lbl_chars = ttk.Label(self, textvariable=self.chars)
        lbl_lines = ttk.Label(self, textvariable=self.lines)
        lbl_curpos = ttk.Label(self, textvariable=self.cursor)

        # Grid the labels
        lbl_filetype.grid(row=0, column=0, columnspan=2)
        lbl_chars.grid(row=0, column=2)
        lbl_lines.grid(row=0, column=3)
        lbl_curpos.grid(row=0, column=4)

    
    def update_filetype(self, filetype: str) -> None:
        """Update the filetype label."""
        self.filetype.set(filetype)


    def update_chars(self, count: int) -> None:
        """Update the character count label."""
        self.chars.set(f"Chars {count}")


    def update_lines(self, count: int) -> None:
        """Update the line count label."""
        self.lines.set(f"Lines {count}")


    def update_cursor(self, cursor: str) -> None:
        """Update the cursor position label."""
        self.cursor.set(cursor)
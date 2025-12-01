import tkinter as tk
from typing import Literal




class EditMenu(tk.Menu):
    """An Edit menu to attach to the main window menu."""


    def __init__(self, parent):
        self.notebookmenu = parent
        self.notebook = parent.notebook
        self.text_area = parent.notebook.text_area

        super().__init__(parent, name="edit")

        self._configure_menus()


    def _configure_menus(self) -> None:
        """Internal function. Configure the Edit menu."""

        # Undo and Redo commands
        self.add_command(label="Undo", accelerator="Cmd+Z", command=self.undo)
        self.add_command(label="Redo", accelerator="Shift+Cmd+Z", 
            command=self.redo)
        self.add_separator()

        # Cut, Copy, Paste and Delete commands. All of these default to
        # the current line if no selection has been made.
        self.add_command(label="Cut", accelerator="Cmd+X", command=self.cut)
        self.add_command(label="Copy", accelerator="Cmd+C", command=self.copy)
        self.add_command(label="Paste", accelerator="Cmd+V", command=self.paste)
        self.add_command(label="Delete", command=self.delete)
        self.add_separator()

        # Select all the text
        self.add_command(label="Select All", accelerator="Cmd+A",
            command=self.selectall)
        self.add_separator()

        # Tranform menu items. Includes an uppercase, lowercase and
        # capitalize transformation commands.
        transform_menu = tk.Menu(self)
        transform_menu.add_command(label="Make Uppercase", 
            command=lambda: self._configure_case("upper"))
        transform_menu.add_command(label="Make Lowercase", 
            command=lambda: self._configure_case("lower"))
        transform_menu.add_command(label="Capitalize", 
            command=lambda: self._configure_case("capitalize"))
        self.add_cascade(label="Transformation", menu=transform_menu)


    def undo(self) -> None:
        """Undo last modification to the text area."""
        try:
            self.text_area.edit_undo()
            self.text_area.event_generate("<<Undo>>")
        except tk.TclError:
            pass


    def redo(self) -> None:
        """Redo last modification to the text area."""
        try:
            self.text_area.edit_redo()
            self.text_area.event_generate("<<Redo>>")
        except tk.TclError:
            pass

    
    def cut(self) -> None:
        """
        Cut selected text to clipboard and remove from place in text.

        Clears the current clipboard content and appends the new
        selection. If no selection is made the current line is used by
        default.
        
        """
        # Clear the cliboard
        self.clipboard_clear()
        
        # Get the text widget indices range for the selection
        selection = self.text_area.tag_ranges(tk.SEL)

        # Use the selection if available or default to current line
        if selection:
            # Append the selection to the clipboard
            self.clipboard_append(self.text_area.selection_get())

            # Delete the selected text from the text widget
            self.text_area.delete(selection[0], selection[1])
        else:
            # Get the indices of the insertion cursor
            indice = self.text_area.index(tk.INSERT)

            # Split the insertion cursor indices to get the line number
            line = indice.split('.')[0]

            # Append the line to clipboard
            self.clipboard_append(self.text_area.get(f"{line}.0", f"{line}.end"))

            # Delete the selected text from the text widget
            self.text_area.delete(f"{line}.0", f"{line}.end")


    def copy(self) -> None:
        """
        Copy selected text to clipboard.
        
        Clears the current clipboard content and appends the new 
        selection. If no selection is made the current line is used by
        default.
        
        """
        # Clear the clipboard
        self.clipboard_clear()

        # Get the text widget indices range for the selection
        selection = self.text_area.tag_ranges(tk.SEL)

        if selection:
            # Append the selection to the clipboard
            self.clipboard_append(self.text_area.selection_get())
        else:
            # Get the indices of the insertion cursor
            indice = self.text_area.index(tk.INSERT)

            # Split the insertion cursor indices to get the line number
            line = indice.split('.')[0]

            # Append the line to clipboard
            self.clipboard_append(self.text_area.get(f"{line}.0", f"{line}.end"))

    
    def paste(self) -> None:
        """Paste the contents of the clipboard to the text area."""
        
        clipboard_text = self.clipboard_get()
        if not self.clipboard_get() == "":
            cursor_index = self.text_area.index(tk.INSERT)
            self.text_area.insert(cursor_index, clipboard_text)


    def delete(self) -> None:
        """
        Delete the current selection.
        
        If nothing is selected, default to the current line.
        
        """

        # Get the text widget indices range for the selection
        selection = self.text_area.tag_ranges(tk.SEL)

        if selection:
            # Delete the selection from the text area
            self.text_area.delete(selection[0], selection[1])

        else:
            # Get the indices of the insertion cursor
            indice = self.text_area.index(tk.INSERT)

            # Split the insertion cursor indices to get the line number
            line = indice.split('.')[0]

            # Delete the current line from the text area
            self.text_area.delete(f"{line}.0", f"{line}.end")


    def selectall(self) -> None:
        """Updates the selection in the text area to all the contents."""
        self.text_area.tag_add("sel", "1.0", "end")

        
    def _configure_case(self, type: Literal["upper", "lower", "capitalize"]) -> None:
        """
        Configure the case of the current selection to TYPE.
        
        If nothing is selected, defaults to the current line.
        
        """
        # Get the text widget indices range for the selection
        selection = self.text_area.tag_ranges(tk.SEL)

        if not selection:

            # Get the indices of the insertion cursor
            indice = self.text_area.index(tk.INSERT)

            # Split the insertion cursor indices to get the line number
            line = indice.split('.')[0]

            # Configure the selection as the current line
            selection = (f"{line}.0", f"{line}.end")

        # Get the selection text
        text = self.text_area.get(selection[0], selection[1])

        # Replace the selection with text formatted as TYPE
        if type == "upper":
            self.text_area.replace(selection[0], selection[1], text.upper())
        elif type == "lower":
            self.text_area.replace(selection[0], selection[1], text.lower())
        elif type == "capitalize":
            self.text_area.replace(selection[0], selection[1], text.capitalize())
        else:
            pass
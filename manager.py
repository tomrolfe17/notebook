import tkinter as tk
from tkinter import messagebox

from notebook import Notebook




class Manager(tk.Tk):
    """
    The main class for the notebook application.
    
    This class manages the opening and closing of notebook windows and 
    where they are positioned on screen. This application does not
    support tabbed windows as it was not deemed necessary for the type
    of text editing that this application was intended for.

    When the last toplevel window is closed, the main loop of Tk will be
    destroyed.
    
    """


    def __init__(self):
        self.xpos = 30                         # x position windows are opened
        self.ypos = 30                         # y position windows are opened
        self.xoffset = 0                       # x offset for new notebooks
        self.yoffset = 0                       # y offset for new notebooks
        self.notebooks = {}                    # track the open toplevels
        self.notebook_count = 1                # default notebook name number

        super().__init__()
        self.platform = self.tk.call("tk", "windowingsystem")
        self.withdraw()                        # withdraw the default window
        
        self.open_notebook()                   # open first notebook on start


    def _update_offset(self) -> None:
        """
        Internal function. 
        
        Update the window offset values to ensure a new window is 
        positioned with an appropriate offset to the other open windows.

        """
        self.xoffset += 30
        self.yoffset += 30


    def _update_window_position(self) -> None:
        """
        Internal function.
        
        Update the window x and y positions on screen.
        
        """
        self._update_offset()
        self.xpos += self.xoffset
        self.ypos += self.yoffset


    def open_notebook(self, name: str = None) -> Notebook:
        """
        Open a new text editor window.

        Name is for the title of the new window. By default it is 
        'BookX' where 'X' is based on the number of windows open or have
        been opened since the application started. 
        
        If the window is opened from the file menu using the Open... 
        command then name will be the name of the file with extension. 
        If the file trying to be opened is already open an error message 
        is displayed.
        
        """
        # Check if name is parsed, default name created from tracked
        # window count variable.
        if not name:
            name = f"Book{self.notebook_count}"
        
        # Create the new window and record the instance
        new_notebook = Notebook(self, name, self.xpos, self.ypos)
        self.notebooks[name] = new_notebook

        # Update the window position attributes for the next window.
        self._update_window_position()

        # update the window count for default window name numbering
        self.notebook_count += 1

        return new_notebook


    def update_notebook(self, old_name: str, new_name: str) -> None:
        """
        Update a windows stored name. 
        
        This is used when a new document is saved or an existing
        document is saved with a new name. 
        
        """

        self.notebooks[new_name] = self.notebooks.pop(old_name)    


    def close_notebook(self, name: str) -> None:
        """
        Closes and removes window NAME from tracked windows.
        
        Prompts the user to save if the window contains unsaved data by
        asking to open to file dialog.

        """
        # Pop the selected window, we can't reverse the closing process
        # now, only choose whether to save any unsaved changes.
        selected_notebook = self.notebooks.pop(name)

        # We need to check that there are no unsaved changes to the
        # window the user is attempting to close. To do this we query
        # the modified attribute of the text widget.
        if selected_notebook.text_area.edit_modified() == True:
            confirm_close = messagebox.askyesno(
                message="Window contains unsaved changes, save before closing?",
                icon="warning",
                default="yes",
                parent=selected_notebook)

            if confirm_close == True:
                selected_notebook.notebook_menu.file_menu.file_save()

        selected_notebook.destroy()
        
        if len(self.notebooks) == 0:
            self.destroy()


    def close_all_notebook(self) -> None:
        """
        Closes all open notebooks.
        
        Prompts the user to save each window if the window contains 
        unsaved data by asking to open to file dialog.

        """
        for notebook in self.notebooks:
            self.close_notebook(notebook.notebook_name)
import tkinter as tk
from tkinter import filedialog
from pathlib import Path




class FileMenu(tk.Menu):
    """
    A File menu to attach to the main window menu.
    
    This menu contains the typical commands associated with an 
    application that manages documents including new, open, save and 
    save as.
    
    """


    def __init__(self, parent: tk.Menu):
        self.menu = parent
        self.notebook = parent.notebook
        self.manager = parent.notebook.manager
        self.filepath: Path | None = None

        super().__init__(parent)             

        # configure the menubar
        self._configure_menu()
    

    def _configure_menu(self) -> None:
        """Configure the file menu commands i.e. New, Open..."""

        # This command creates a new blank window.
        self.add_command(label="New Book", accelerator="Command+N", 
            command=self.manager.open_notebook)
        self.add_separator()

        # Open an existing text based document into the editor.
        self.add_command(label="Open...", accelerator="Command+O", 
            command=self.file_open)

        self.add_separator()

        # Save commands.
        self.add_command(label="Save", accelerator="Command+S", 
            command=self.file_save)

        self.add_command(label="Save As...", accelerator="Shift+Command+S",
            command=self.file_save_as)

        self.add_separator()

        # Option to rename a file.
        self.add_command(label="Rename...", command=self.file_rename)

        self.add_separator()

        # Close commands for notebook windows.
        self.add_command(label="Close Window", accelerator="Shift+Command+W",
            command=lambda: 
                self.manager.close_notebook(self.notebook.title()))

        self.add_command(label="Close All",
            command=lambda: self.manager.close_all_notebook)


    def file_open(self) -> None:
        """Create a new window with the content of the selected file."""
        
        new_filepath = filedialog.askopenfilename(defaultextension=".txt",
            filetypes=(("txt files","*.txt"),("All files","*.*")),
            parent=self.notebook)

        # Check a file was selected from the dialog
        if not new_filepath == "":

            # Create a new path object
            new_filepath = Path(new_filepath)

            # Create a new window with the name filename
            new_notebook = self.manager.open_notebook(new_filepath.name)

            # Insert the file contents to the text widget.
            with open(file=new_filepath, mode="r") as f:
                new_notebook.text_area.insert("1.0", f.read())

            # Set the modified status of the text area to False
            new_notebook.textarea.edit_modified(False)

            # Save the new filepath
            new_notebook.menu.file_menu.filepath = new_filepath

    
    def file_save(self) -> None:
        """Save the open file if it has a path. Otherwise invoke save
        as."""

        if not self.filepath:
            self.file_save_as()
        else:
            with open(file=self.filepath, mode="w") as f:
                f.write(self.notebook.text_area.get("1.0", "end"))

    
    def file_save_as(self) -> None:
        """Prompt the user to select a file location and filename using 
        the native dialog windows and write the file."""

        # Prompt the user to select a directory and provide a filename,
        # then return the path.
        new_filepath = filedialog.asksaveasfilename(defaultextension=".txt",
            filetypes=(("txt files", "*.txt"),("all files", "*.*")),
            initialfile=self.notebook.title(),
            parent=self.notebook)

        # Check a file was selected
        if not new_filepath == "":

            # Create a new path object
            new_filepath = Path(new_filepath)

            # Create a new window with the name filename
            new_notebook = self.manager.open_notebook(new_filepath.name)

            # Write the file contents to the new file
            with open(file=new_filepath, mode="w") as f:
                f.write(self.notebook.text_area.get("1.0", "end"))

            # Insert the file contents to the new window
            new_notebook.text_area.insert("1.0", 
                self.notebook.text_area.get("1.0", "end"))

            # Save the new filepath
            new_notebook.menu.file_menu.filepath = new_filepath

    
    def file_rename(self) -> None:
        """Prompt the user to specify a new filepath to overwrite the
        existing filepath."""

        # Need to check that the file has an existing Path object. If
        # not we call the file_save_as method.
        if self.filepath == None:
            self.file_save_as()

        else:

            # Prompt the user to select a directory and provide a filename,
            # then return the path.
            new_filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                filetypes=(("txt files", "*.txt"),("all files", "*.*")),
                initialfile=self.notebook.title(),
                parent=self.notebook)

            # Check a file was selected
            if not new_filepath == "":

                # Rename the file in the filesystem and also update the
                # stored filepath attribute.
                self.filepath = self.filepath.replace(new_filepath)

                # Update the window title
                self.notebook.title(self.filepath.name)
import tkinter as tk




class TextArea(tk.Text):
    """The Text Area is a custom tk Text widget for a notebook window."""


    def __init__(self, parent):
        self.chars = tk.IntVar(value=0)
        self.lines = tk.IntVar(value=1)
        self.cursor = tk.StringVar(value="Ln 1, Col 1, Pos 1")
        self.words = tk.IntVar(value=0)

        super().__init__(
            parent,
            bd=3,
            highlightthickness=0,
            tabstyle="wordprocessor",
            wrap="word",
            undo=True,
            maxundo=100
        )
        self.tabspace = 8       # default used in the Text widget

        self._configure_bindings()

    
    def _configure_bindings(self) -> None:
        """Internal function. Configure the additional bindings."""

        # The FocusIn event is the most reliable way of updating the
        # char and word counts as well as the cursor position when a new
        # file is opened and the content is inserted into the text
        # widget.
        self.bind("<FocusIn>", lambda _ : self._call_updates("FocusIn"), "+")

        # The ButtonPress and ButtonRelease events are important for the
        # cursor position for instance when the user is performing a
        # selection. 
        self.bind("<ButtonPress>", 
            lambda _ : self._call_updates("ButtonPress"), "+")
        self.bind("<ButtonRelease>", 
            lambda _ : self._call_updates("ButtonRelease"), "+")
        
        # The KeyPress event obviously impacts the char and word counts
        # as well as the cursor position. We also track the KeyRelease
        # event too.
        self.bind("<KeyPress>", lambda _ : self._call_updates("KeyPress"), "+")
        self.bind("<KeyRelease>", lambda _ : self._call_updates("KeyPress"), "+")

        # The Cut and Paste events also impact the char and word counts
        # as well as the cursor position.
        self.bind("<<Cut>>", lambda _ : self._call_updates("Cut"), "+")
        self.bind("<<Paste>>", lambda _ : self._call_updates("Paste"), "+")

        # The Undo and Redo events also impact the char and word counts
        # as well as the cursor position.
        self.bind("<<Undo>>", lambda _ : self._call_updates("Undo"), "+")
        self.bind("<<Redo>>", lambda _ : self._call_updates("Redo"), "+")


    def _call_updates(self, event: str) -> None:
        """Internal function. Call the relevant update function."""

        # The cursor needs to be updated on any additional event which 
        # has been binded to.
        self._update_cursor()

        # The ButtonPress and ButtonRelease events do not require calls
        # to update the char, line or word counts.
        if not (event == "ButtonPress" or event == "ButtonRelease"):
            self._update_char_count()
            self._update_line_count()
            self._update_word_count()


    def _update_cursor(self, *args) -> None:
        """Internal function. Updates the cursor position attribute."""

        # Get the insertion cursor index in the text widget
        cursor_index = self.index(tk.INSERT)

        # Set the new line number
        line = cursor_index.split('.')[0]

        # Get the column index. We need to retrieve the text on the 
        # current line so we can check for things like tabs.
        text = self.get(f"{line}.0", cursor_index)

        col = 1
        for c in text:
            if c == '\n':
                break
            elif c == '\t':
                col += self.tabspace
            else:
                col += 1

        # Get the position index (number of characters up to this point).
        pos = self.count("1.0", cursor_index, "chars")
        if pos == None:
            pos = 1
        else:
            pos = pos[0] + 1
        
        self.cursor.set(f"Ln {line}, Col {col}, Pos {pos}")


    def _update_char_count(self, *args) -> None:
        """Internal function. Updates the character count."""

        chars = self.count("1.0", "end-1c", "chars")
        if chars == None:
            self.chars.set(0)
        else:
            self.chars.set(chars[0])
        

    def _update_line_count(self, *args) -> None:
        """Internal function. Update the line count."""

        lines = self.count("1.0", "end", "lines")

        if lines == None:
            self.lines.set(0)
        else:
            self.lines.set(lines[0])


    def _update_word_count(self, *args) -> None:
        """Internal function. Updates the word count."""

        words = 0
        text = self.get("1.0", "end")
        word_length = 0
        for char in text:
            if char == ' ' or char == '\t':
                if word_length > 0:
                    words += 1
                    word_length = 0
            else:
                word_length += 1
        self.words.set(words)
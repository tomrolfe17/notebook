import tkinter as tk




class TextArea(tk.Text):
    """
    A Notebook window widget.
    
    The Text Area is a custom tk Text widget for a notebook window. 
    
    It maintains a series of attributes related to its contents including
    the cursor position and number of lines which are subsequently used
    by other areas of the window such as the Line Bar and Status Bar. 
    
    """


    def __init__(self, parent):

        super().__init__(
            parent,
            bd=3,
            highlightthickness=0,
            tabstyle="wordprocessor",
            wrap="word",
            undo=True,
            maxundo=100
        )
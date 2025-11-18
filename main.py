import sys

from manager import Manager




def main() -> None:
    """Entry point of the notebook application."""

    # Create an instance of the notebook application manager. By default
    # this opens a new blank notebook.
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()
"""
This is the client script, setting up the user interface for connecting to the server, down/uploading patterns and running them.
"""

from tkinter import *  # pyright: ignore[reportWildcardImportFromLibrary]
from tkinter.ttk import *  # pyright: ignore[reportWildcardImportFromLibrary]

from ttkthemes import ThemedStyle

from colours import *


class Window(Tk):
  """
  The client window.
  """
  def __init__(self, width: int = 1280, height: int = 720):
    super().__init__("Conwayland")
    self.geometry(f"{width}x{height}")

    self.style = ThemedStyle(self, theme="arc")
    
    self.label_hello = Label(self, text="Hello, world!")
    self.button_quit = Button(self, text="Quit", command=self.quit)
    print("All has been set!")

def main():
  root = Window()
  root.mainloop()

if __name__ == "__main__":
  main()

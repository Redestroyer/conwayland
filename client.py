"""
This is the client script, setting up the user interface for connecting to the server, down/uploading patterns and running them.
"""

from tkinter import *  # pyright: ignore[reportWildcardImportFromLibrary]
from tkinter.ttk import *  # pyright: ignore[reportWildcardImportFromLibrary]

#from ttkthemes import ThemedStyle, ThemedTk
from colours import *
from widgets import pack_all


class Window(Tk):
  """
  The client window.
  """
  def __init__(self, width: int = 640, height: int = 360):
    super().__init__("Conwayland")
    x, y = self.winfo_screenwidth() - width, self.winfo_screenheight() - height
    x >>= 1
    y >>= 1
    self.geometry(f"{width}x{height}+{x}+{y}")
    self.resizable(False, False)
    self.attributes("-alpha", 0.8) # type: ignore

    self.style = Style(self)
    self.style.theme_create("Conwayland", "default", {
      "TLabel": {
        "configure": {
          "foreground": SLATE700,
          "background": SLATE200
        }
      }
    })
    
    self.label_hello = Label(self, text="Hello, world!")
    self.button_quit = Button(self, text="Quit", command=self.quit)
    pack_all(self.label_hello, self.button_quit)

def main():
  root = Window()
  root.mainloop()

if __name__ == "__main__":
  main()

"""
This is the client script, setting up the user interface for connecting to the server, down/uploading patterns and running them.
"""

from tkinter import *  # pyright: ignore[reportWildcardImportFromLibrary]
from tkinter.ttk import *  # pyright: ignore[reportWildcardImportFromLibrary]

#from ttkthemes import ThemedStyle, ThemedTk
from board_widget import BoardWidget
from colours import *
from conway import ConwayBoard


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
    self.attributes("-alpha", 0.9) # type: ignore

    self.style = Style(self)
    self.style.theme_create("Conwayland", "default", {
      "TLabel": {
        "configure": {
          "foreground": SLATE700,
          "background": SLATE200
        }
      },
      
      "TBoardWidget": {
        "configure": {
          "background": SLATE900,
          "foreground": SLATE100
        }
      }
    })
    self.style.theme_use("Conwayland")
    
    self.board = BoardWidget(self, board=ConwayBoard(16, 16), style="TBoardWidget")
    self.button_quit = Button(self, text="Quit", command=self.quit)
    self.board.pack()
    self.button_quit.pack()

def main():
  root = Window()
  root.mainloop()

if __name__ == "__main__":
  main()

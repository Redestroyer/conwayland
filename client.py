"""
This is the client script, setting up the user interface for connecting to the server, down/uploading patterns and running them.
"""

from tkinter import *  # pyright: ignore[reportWildcardImportFromLibrary]
from tkinter.ttk import *  # pyright: ignore[reportWildcardImportFromLibrary]

from board_widget import BoardWidget
from colours import *
from conway import ConwayBoard
from widgets import pack_all


class Window(Tk):
  """
  The client window.
  """
  class ControlButtons(Frame):
    """
    Frame containing buttons to control the board.
    """
    def __init__(self, master: Misc, *, board: BoardWidget):
      super().__init__(
        master
      )
      self.wipeout_button = Button(
        self,
        text="Clear",
        command=board.wipeout
      )
      self.tick_button = Button(
        self,
        text="Step",
        command=board.run_tick
      )
      pack_all(self.wipeout_button, self.tick_button)

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
    self.control = Window.ControlButtons(self, board=self.board)
    self.button_quit = Button(self, text="Quit", command=self.quit)
    self.board.pack(side="left")
    self.control.pack(side="right")
    self.button_quit.pack()

def main():
  root = Window()
  root.mainloop()

if __name__ == "__main__":
  main()

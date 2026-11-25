from tkinter import Misc
from tkinter.ttk import Button, Frame

from board_widget import BoardWidget
from conway import ConwayBoard


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
    self.wipeout_button.pack()
    self.tick_button.pack()

class ConwayWidget(Frame):
  """
  Frame containing the board and controls.
  """
  def __init__(self, master, *, board: ConwayBoard | None = None):
    super().__init__(master)

    self._board = board or ConwayBoard(16, 16)
    self.board = BoardWidget(self, board=self._board, style="TBoardWidget")
    self.control = ControlButtons(self, board=self.board)
    self.board.pack(side="left")
    self.control.pack(side="right")
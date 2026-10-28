from tkinter import Misc
from tkinter.ttk import Frame, Label, LabelFrame

from conway import ConwayBoard


class BoardWidget(LabelFrame):
  """
  A widget to display the Conway board. Allows quickening and killing cells.
  """
  __slots__ = "board", "grid", "height", "width"

  def __init__(self, master: Misc, *, board: ConwayBoard, style: str = "TBoardWidget") -> None:
    super().__init__(
      master,
      text="Board",
      width=board.width*10,
      height=board.height*10,
      #style=style
    ) # type: ignore
    self.board = board
    self.width = board.width
    self.height = board.height
    self.update_grid()
  
  def update_grid(self):
    self.grid = [
      (Cell(self, self.board.cell_state(x, y)), x, y)
      for x in range(self.board.width)
      for y in range(self.board.height)
    ]
    for c, x, y in self.grid:
      c.grid(columnspan=self.width,column=x, rowspan=self.height,row=y)

class Cell(Frame):
  def __init__(self, master: Misc, state: bool) -> None:
    super().__init__(master, width=10, height=10)
    self.alive = state
    self.label = Label(self, text=("A" if state else "D"))

from tkinter import Event, Misc
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
      Cell(self, board=self.board, x=x, y=y)
      for x in range(self.board.width)
      for y in range(self.board.height)
    ]
    self.bind_class("Cell", "<Button>", self._binding_toggle_cell) # type: ignore
    for c in self.grid:
      c.bind("<Button>", self._binding_toggle_cell) # type: ignore
      c.grid(
        column=c.x,
        row=c.y
      )
  
  def toggle_cell(self, x: int, y: int):
    self.board.toggle_cell(x, y)
  def _binding_toggle_cell(self, event: "Event[Cell]"):
    x, y = event.widget.position
    print(f"Updating cell ({x}, {y})")
    self.toggle_cell(x, y)
    self.update_grid()
  def run_tick(self):
    self.board.tick()

class Cell(Frame):
  def __init__(self, master: Misc, *, board: ConwayBoard, x: int, y: int) -> None:
    super().__init__(master, width=10, height=10)
    self.x = x
    self.y = y
    self.alive = board.cell_state(x, y)
    self.label = Label(
      self,
      text=("A" if self.alive else "D"),
      font=("Helvetica", 5)
    )
    self.label.pack(expand=True, fill="both")

  @property
  def position(self) -> tuple[int, int]:
    return self.x, self.y

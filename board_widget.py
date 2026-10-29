from collections.abc import Callable
from tkinter import Misc
from tkinter.ttk import Button, Frame, LabelFrame
from typing import Any, Self

from conway import ConwayBoard


class BoardWidget(LabelFrame):
  """
  A widget to display the Conway board. Allows quickening and killing cells.
  """
  __slots__ = "board", "grid", "height", "width"

  def __init__(self, master: Misc, *, board: ConwayBoard, style: str = "TBoardWidget") -> None:
    super().__init__(
      master,
      class_="TBoardWidget",
      text="Board",
      width=board.width*20,
      height=board.height*20,
      #style=style
    ) # type: ignore
    self.board = board
    self.width = board.width
    self.height = board.height
    self.load_grid()
  
  def load_grid(self):
    self.grid = [
      Cell(self, alive=self.cell_state(x, y), x=x, y=y, command=self._binding_toggle_cell)
      for x in range(self.board.width)
      for y in range(self.board.height)
    ]
    for c in self.grid:
      c.grid(
        row=c.x,
        column=c.y,
      )
  def update_grid(self):
    for c in self.grid:
      c.alive = self.cell_state(c.x, c.y)
  
  def cell_state(self, x: int, y: int) -> bool:
    return self.board.cell_state(x, y)
  
  def wipeout(self):
    result = self.board.wipeout()
    self.update_grid()
    return result
  def toggle_cell(self, x: int, y: int):
    result = self.board.toggle_cell(x, y)
    self.update_grid()
    return result
  def _binding_toggle_cell(self, cell: "Cell"):
    x, y = cell.position
    cell.alive = self.toggle_cell(x, y)
  
  def run_tick(self):
    self.board.tick()
    self.update_grid()

class Cell(Frame):
  def __init__(self, master: Misc, *, alive: bool, x: int, y: int, command: Callable[[Self], Any]) -> None:
    super().__init__(
      master,
      class_="TCell",
      width=20,
      height=20
    )
    self.x = x
    self.y = y
    self._alive = alive
    self.label = Button(
      self,
      text=self.life_text,
      command=lambda : command(self)
    )
    self.label.pack(expand=True, fill="both")

  @property
  def position(self) -> tuple[int, int]:
    return self.x, self.y
  
  @property
  def alive(self) -> bool:
    return self._alive
  @alive.setter
  def alive(self, value: bool):
    if self._alive == value:
      return
    self._alive = value
    self.label.configure(
      text=self.life_text
    )
  @property
  def life_text(self) -> str:
    return "A" if self.alive else "D"
  
  def __repr__(self) -> str:
    return f"Cell({self.x}, {self.y}, {"Alive" if self.alive else "Dead"})"

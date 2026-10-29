from typing import Literal

from bitarray import bitarray
from bitarray.util import ba2hex


def _validate_dimensions(width: int, height: int):
  if width < 1 or height < 1:
    raise ValueError("Dimensions must be positive and non-zero!")

class _Board:
  """
  This class holds an individual board instance of the board.
  """
  __slots__ = "_board", "_height", "_width"
  def __init__(self, width: int, height: int, initial: bitarray | None = None):
    _validate_dimensions(width, height)
    self._width = width
    self._height = height
    self._board = initial or bitarray(width*height)

  @property
  def width(self) -> int:
    return self._width
  @property
  def height(self) -> int:
    return self._height
  @property
  def current_state(self) -> bitarray:
    return self._board

  def cell_state(self, x: int, y: int) -> Literal[0, 1]:
    if x < 0 or x >= self._width or y < 0 or y >= self._height:
      return 0
    # Accessing a single element of a bitarray always returns either 0 or 1.
    return self._board[x + y*self._height]; # type: ignore
  def wipeout(self):
    self._board[:] = False
  def kill_cell(self, x: int, y: int):
    if x < 0 or x >= self._width or y < 0 or y >= self._height:
      return
    self._board[x + y*self._height] = 0
  def quicken_cell(self, x: int, y: int):
    if x < 0 or x >= self._width or y < 0 or y >= self._height:
      return
    self._board[x + y*self._height] = 1
  def toggle_cell(self, x: int, y: int):
    if x < 0 or x >= self._width or y < 0 or y >= self._height:
      return None
    self._board.invert(x + y*self._height)
    return self.cell_state(x, y)
  def live_neighbours(self, x: int, y: int) -> int:
    offsets = [-1, 0, 1]
    return sum(
      self.cell_state(x+dx, y+dy)
      for dx in offsets
      for dy in offsets
      if dx != 0 or dy != 0
    )
  
  def __repr__(self) -> str:
    return f"Board(0x{ba2hex(self._board)})"

class ConwayBoard:
  """
  This class holds the board and runs the steps.
  """
  __slots__ = "_alter", "_height", "_pool", "_read", "_width", "_write"
  def __init__(self, width: int, height: int):
    _validate_dimensions(width, height)
    self._width = width
    self._height = height
    self._read = _Board(width, height)
    self._write = _Board(width, height)

  @property
  def width(self) -> int:
    return self._width
  @property
  def height(self) -> int:
    return self._height
  @property
  def current_state(self) -> bitarray:
    return self._read.current_state.copy()
  
  def cell_state(self, x: int, y: int) -> bool:
    return self._read.cell_state(x, y) == 1
  
  def wipeout(self):
    return self._read.wipeout()
  def toggle_cell(self, x: int, y: int):
    return self._read.toggle_cell(x, y) == 1

  def tick(self):
    """
    Runs through the state.
    """
    
    for x, y in (
      (x, y)
      for x in range(self._width)
      for y in range(self._height)
    ):
      count = self._read.live_neighbours(x, y)
      alive = self._read.cell_state(x, y) == 1
      if count == 3 or (alive and count in (2, 3)):
        self._write.quicken_cell(x, y)
      else:
        self._write.kill_cell(x, y)
      
    #print(f"Previous board: {self._read!r}\nNext board: {self._write!r}")
    self._read, self._write = self._write, self._read

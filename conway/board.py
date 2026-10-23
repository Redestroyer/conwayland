from multiprocessing import Pool
from typing import Literal

from bitarray import bitarray


def _validate_dimensions(width: int, height: int):
  if width < 1 or height < 1:
    raise ValueError("Dimensions must be positive and non-zero!")

class _Board:
  """
  This class holds an individual board instance of the board.
  """
  __slots__ = "_board", "_height", "_width"
  def __init__(self, width: int, height: int):
    _validate_dimensions(width, height)
    self._width = width
    self._height = height
    self._board = bitarray(width*height)

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
  def live_neighbours(self, x: int, y: int) -> int:
    offsets = [-1, 0, 1]
    return sum(
      self.cell_state(dx, dy)
      for dx in offsets
      for dy in offsets
      if dx != 0 or dy != 0
    )

class ConwayBoard:
  """
  This class holds the board and runs the steps.
  """
  __slots__ = "_alter", "_board1", "_board2", "_height", "_pool", "_width"
  def __init__(self, width: int, height: int):
    _validate_dimensions(width, height)
    self._width = width
    self._height = height
    self._board1 = _Board(width, height)
    self._board2 = _Board(width, height)
    self._alter: bool = False

  @property
  def width(self) -> int:
    return self._width
  @property
  def height(self) -> int:
    return self._height
  @property
  def current_state(self) -> bitarray:
    return self._read_write_pair()[0].current_state.copy()

  def _read_write_pair(self) -> tuple[_Board, _Board]:
    """
    First is read, second is write.
    """
    return (self._board2, self._board1) if self._alter else (self._board1, self._board2)

  def tick(self):
    """
    Runs through the state.
    """
    read, write = self._read_write_pair()
    with Pool(16) as pool:
      def run(pos: tuple[int, int]):
        count = read.live_neighbours(*pos)
        alive = read.cell_state(*pos) == 1
        # Either a new cell is born amongst three, one already existing lives amongst two or three others or dies.
        (write.quicken_cell if count == 3 or (alive and 2 <= count <= 3) else write.kill_cell)(*pos)
      
      pool.map(run, (
        (x, y)
        for x in range(self._width)
        for y in range(self._height)
      ))
    self._alter = not self._alter


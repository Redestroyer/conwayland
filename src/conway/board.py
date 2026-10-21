from bitarray import bitarray


class ConwayBoard:
    __slots__ = "_alter", "_board1", "_board2", "_height", "_width";
    """
    This class holds the board and runs the steps.
    """
    def __init__(self, width: int, height: int):
        if width < 1 or height < 1:
            raise ValueError("Dimensions must be positive and non-zero!");
        self._width = width;
        self._height = height;
        self._board1 = bitarray(width*height);
        self._board2 = bitarray(width*height);
        self._alter: bool = False;
    
    @property
    def width(self) -> int:
        return self._width
    @property
    def height(self) -> int:
        return self._height
    @property
    def current_state(self) -> bitarray:
        return self._read_write_pair()[0].copy();

    def _read_write_pair(self) -> tuple[bitarray, bitarray]:
        """
        First is read, second is write.
        """
        return (self._board2, self._board1) if self._alter else (self._board1, self._board2)

    def tick(self):
        """
        Runs through the state.
        """
        read, write = self._read_write_pair();

class _Board:
    """
    This class holds an individual board instance of the board.
    """
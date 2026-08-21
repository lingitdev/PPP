from config import GRID_WIDTH, GRID_HEIGHT
from core.cell import Cell

class Grid:
    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT):
        self.width = width
        self.height = height
        
        self.cells: list[list[Cell]] = [
            [Cell(x, y) for y in range(height)]
            for x in range(width)
        ]

    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell | None:
        if self.is_valid_position(x, y):
            return self.cells[x][y]
        return None

    def clear_all(self) -> None:
        for col in self.cells:
            for cell in col:
                cell.reset_color()
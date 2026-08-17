from config import COLOR_DEFAULT_CELL

class Cell:
    def __init__(self, grid_x: int = 0, grid_y: int = 0):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.default_color = COLOR_DEFAULT_CELL
        self.current_color = self.default_color

    def set_color(self, new_color: tuple[int, int, int]) -> None:
        self.current_color = new_color

    def reset_color(self) -> None:
        self.current_color = self.default_color
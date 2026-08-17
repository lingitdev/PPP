import pygame
from config import CELL_SIZE, MAX_ZOOM, MIN_ZOOM

class Camera:
    def __init__(self):
        self.zoom_level:float = 1.0
        self.offset_x:float = 0.0
        self.offset_y:float = 0.0

    def pan(self, dx: float, dy: float) -> None:
        self.offset_x += dx
        self.offset_y += dy

    def screen_to_grid(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        current_cell_size = CELL_SIZE * self.zoom_level
        grid_x = int((screen_x - self.offset_x) // current_cell_size)
        grid_y = int((screen_y - self.offset_y) // current_cell_size)
        return grid_x, grid_y

    def zoom(self, factor: float, mouse_pos: tuple[int, int]) -> None:
        mouse_x, mouse_y = mouse_pos
        
        old_zoom = self.zoom_level
        new_zoom = max(MIN_ZOOM, min(MAX_ZOOM, old_zoom * factor))

        if old_zoom == new_zoom:
            return

        self.offset_x = mouse_x - (mouse_x - self.offset_x) * (new_zoom / old_zoom)
        self.offset_y = mouse_y - (mouse_y - self.offset_y) * (new_zoom / old_zoom)
        
        self.zoom_level = new_zoom
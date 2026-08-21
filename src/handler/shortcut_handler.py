import pygame
from config import COLOR_PALETTE
from core.grid import Grid


class ShortcutHandler:
    def __init__(self):
        self.active_color = COLOR_PALETTE[pygame.K_F1]

    def handle_keydown(self, event: pygame.event.Event, grid: Grid, grid_x: int, grid_y: int) -> None:
        if event.key in COLOR_PALETTE:
            self.active_color = COLOR_PALETTE[event.key]

        elif event.key == pygame.K_DELETE:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_SHIFT:
                grid.clear_all()
            else:
                target_cell = grid.get_cell(grid_x, grid_y)
                if target_cell:
                    target_cell.reset_color()
import pygame

from config import COLOR_PALETTE
from core.grid import Grid


class ShortcutHandler:
    def __init__(self):
        self.active_color = COLOR_PALETTE[pygame.K_F1]

    def handle_keydown(self, event: pygame.event.Event, grid: Grid, grid_x: int, grid_y: int) -> str | None:

        mods = pygame.key.get_mods()

        if mods & pygame.KMOD_CTRL:

            if event.key == pygame.K_s:
                if mods & pygame.KMOD_SHIFT:
                    return "SAVE_AS"

                return "SAVE"

            if event.key == pygame.K_w:
                return "BACK_TO_PROJECTS"

            if event.key == pygame.K_q:
                return "EXIT_APPLICATION"

            if event.key == pygame.K_n:
                return "NEW_PROJECT"

        if event.key == pygame.K_ESCAPE:
            return "BACK"

        if event.key in COLOR_PALETTE:
            self.active_color = COLOR_PALETTE[event.key]
            return None

        if event.key == pygame.K_DELETE:
            if mods & pygame.KMOD_SHIFT:
                grid.clear_all()

            else:
                target_cell = grid.get_cell(grid_x, grid_y)

                if target_cell:
                    target_cell.reset_color()

            return None

        return None
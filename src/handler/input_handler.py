import pygame
from core.grid import Grid
from core.camera import Camera
from handler.shortcut_handler import ShortcutHandler


class InputHandler:
    def __init__(self):
        self.shortcut_handler = ShortcutHandler()
        self.is_panning = False
        self.last_mouse_pos = (0, 0)

    def process_events(self, grid: Grid, camera: Camera) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        grid_x, grid_y = camera.screen_to_grid(mouse_pos[0], mouse_pos[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    camera.zoom(1.15, mouse_pos)
                elif event.y < 0:
                    camera.zoom(0.85, mouse_pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.is_panning = True
                    self.last_mouse_pos = mouse_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.is_panning = False

            elif event.type == pygame.MOUSEMOTION:
                if self.is_panning:
                    dx = mouse_pos[0] - self.last_mouse_pos[0]
                    dy = mouse_pos[1] - self.last_mouse_pos[1]
                    camera.pan(dx, dy)
                    self.last_mouse_pos = mouse_pos

            elif event.type == pygame.KEYDOWN:
                self.shortcut_handler.handle_keydown(event, grid, grid_x, grid_y)

        self._handle_continuous_input(grid, camera, mouse_pos, grid_x, grid_y)
        return True

    def _handle_continuous_input(
        self, grid: Grid, camera: Camera, mouse_pos: tuple[int, int], grid_x: int, grid_y: int
    ) -> None:
        mouse_buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and mouse_buttons[0]:
            if not self.is_panning:
                self.is_panning = True
                self.last_mouse_pos = mouse_pos
            else:
                dx = mouse_pos[0] - self.last_mouse_pos[0]
                dy = mouse_pos[1] - self.last_mouse_pos[1]
                camera.pan(dx, dy)
                self.last_mouse_pos = mouse_pos
        else:
            if not mouse_buttons[1]:
                self.is_panning = False

            if mouse_buttons[0] and not keys[pygame.K_SPACE]:
                cell = grid.get_cell(grid_x, grid_y)
                if cell:
                    cell.set_color(self.shortcut_handler.active_color)

            elif mouse_buttons[2]:
                cell = grid.get_cell(grid_x, grid_y)
                if cell:
                    cell.reset_color()
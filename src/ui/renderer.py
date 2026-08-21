import pygame
from config import COLOR_BACKGROUND, COLOR_GRID_LINE, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from core.grid import Grid
from core.camera import Camera


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def render(self, grid: Grid, camera: Camera, active_color: tuple[int, int, int]) -> None:
        self.screen.fill(COLOR_BACKGROUND)

        scaled_cell_size = CELL_SIZE * camera.zoom_level

        start_x = max(0, int((-camera.offset_x) // scaled_cell_size))
        end_x = min(grid.width, int((SCREEN_WIDTH - camera.offset_x) // scaled_cell_size) + 1)
        start_y = max(0, int((-camera.offset_y) // scaled_cell_size))
        end_y = min(grid.height, int((SCREEN_HEIGHT - camera.offset_y) // scaled_cell_size) + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                cell = grid.cells[x][y]
                draw_x = camera.offset_x + (x * scaled_cell_size)
                draw_y = camera.offset_y + (y * scaled_cell_size)

                pygame.draw.rect(
                    self.screen,
                    cell.current_color,
                    (draw_x, draw_y, scaled_cell_size, scaled_cell_size)
                )

                if camera.zoom_level > 0.3:
                    pygame.draw.rect(
                        self.screen,
                        COLOR_GRID_LINE,
                        (draw_x, draw_y, scaled_cell_size, scaled_cell_size),
                        1
                    )

        matrix_rect = (
            camera.offset_x,
            camera.offset_y,
            grid.width * scaled_cell_size,
            grid.height * scaled_cell_size
        )
        pygame.draw.rect(self.screen, (255, 255, 255), matrix_rect, 2)

        pygame.draw.rect(self.screen, active_color, (SCREEN_WIDTH - 45, 15, 30, 30))
        pygame.draw.rect(self.screen, (255, 255, 255), (SCREEN_WIDTH - 45, 15, 30, 30), 2)
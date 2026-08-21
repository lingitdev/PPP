import sys
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.grid import Grid
from core.camera import Camera
from ui.renderer import Renderer
from handler.input_handler import InputHandler


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Paint - PPP")
    clock = pygame.time.Clock()

    grid = Grid()
    camera = Camera()
    renderer = Renderer(screen)
    input_handler = InputHandler()

    running = True
    while running:
        running = input_handler.process_events(grid, camera)
        
        active_color = input_handler.shortcut_handler.active_color
        renderer.render(grid, camera, active_color)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
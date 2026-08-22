import sys
import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_WELCOME,
    STATE_DRAWING,
)

from core.grid import Grid
from core.camera import Camera
from core.project import Project

from ui.renderer import Renderer
from ui.welcome_screen import WelcomeScreen

from handler.input_handler import InputHandler


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption("Pixel Paint - PPP")

    clock = pygame.time.Clock()

    current_state = STATE_WELCOME
    running = True

    grid = Grid()
    camera = Camera()

    renderer = Renderer(screen)
    welcome_screen = WelcomeScreen(screen)
    input_handler = InputHandler()

    current_project: Project | None = None

    while running:
        if current_state == STATE_WELCOME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    continue

                action = welcome_screen.handle_event(event)

                if action == STATE_DRAWING:
                    current_project = welcome_screen.selected_project

                    if current_project is not None:
                        grid = Grid()
                        camera = Camera()
                        current_state = STATE_DRAWING

                elif action == "NEW_PROJECT":
                    current_project = Project.create(
                        "Untitled Project"
                    )

                    grid = Grid()
                    camera = Camera()

                    welcome_screen.refresh_projects()
                    current_state = STATE_DRAWING

                elif action == "EXIT_APPLICATION":
                    running = False

                elif action == "SETTINGS":
                    pass

            welcome_screen.render()

        elif current_state == STATE_DRAWING:
            action = input_handler.process_events(
                grid,
                camera,
            )

            if action == "EXIT_APPLICATION":
                if current_project is not None:
                    if current_project.modified:
                        current_project.save()

                running = False

            elif action == "SAVE":
                if current_project is not None:
                    current_project.save()

            elif action == "SAVE_AS":
                pass

            elif action == "BACK_TO_PROJECTS":
                if current_project is not None:
                    if current_project.modified:
                        current_project.save()

                current_project = None
                welcome_screen.refresh_projects()
                current_state = STATE_WELCOME

            elif action == "NEW_PROJECT":
                current_project = Project.create(
                    "Untitled Project"
                )

                grid = Grid()
                camera = Camera()

            elif action == "BACK":
                if current_project is not None:
                    if current_project.modified:
                        current_project.save()

                current_project = None
                welcome_screen.refresh_projects()
                current_state = STATE_WELCOME

            active_color = (
                input_handler
                .shortcut_handler
                .active_color
            )

            renderer.render(
                grid,
                camera,
                active_color,
            )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
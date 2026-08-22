import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_BACKGROUND,
    STATE_DRAWING,
)

from core.project import Project


class WelcomeScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.font_title = pygame.font.Font(None, 48)
        self.font_button = pygame.font.Font(None, 28)
        self.font_project = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 22)
        self.selected_project = None

        self.panel_width = int(SCREEN_WIDTH * 0.23)

        self.panel_rect = pygame.Rect(
            0,
            0,
            self.panel_width,
            SCREEN_HEIGHT,
        )

        self.content_rect = pygame.Rect(
            self.panel_width,
            0,
            SCREEN_WIDTH - self.panel_width,
            SCREEN_HEIGHT,
        )

        self.buttons = []

        button_x = 20
        button_y = 130
        button_width = self.panel_width - 40
        button_height = 50
        button_gap = 12

        definitions = [
            ("New Project", "NEW_PROJECT"),
            ("Settings", "SETTINGS"),
            ("Exit", "EXIT_APPLICATION"),
        ]

        for text, action in definitions:
            rect = pygame.Rect(
                button_x,
                button_y,
                button_width,
                button_height,
            )

            self.buttons.append(
                {
                    "rect": rect,
                    "text": text,
                    "action": action,
                }
            )

            button_y += button_height + button_gap

        self.projects = []
        self.project_rects = []

        self.refresh_projects()

    def refresh_projects(self) -> None:
        self.projects = Project.list_projects()

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        mouse_pos = event.pos

        if event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(mouse_pos):
                    return button["action"]

            for index, rect in enumerate(self.project_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_project = self.projects[index]
                    return STATE_DRAWING

        if event.button == 3:
            for index, rect in enumerate(self.project_rects):
                if rect.collidepoint(mouse_pos):
                    project = self.projects[index]
                    print(
                        f"Context menu requested: {project.name}"
                    )
                    return None

        return None

    def render(self) -> None:
        self.screen.fill(COLOR_BACKGROUND)

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(
            self.screen,
            (28, 28, 32),
            self.panel_rect,
        )

        title = self.font_title.render(
            "PPP",
            True,
            (255, 255, 255),
        )

        title_rect = title.get_rect(
            center=(self.panel_width // 2, 55)
        )

        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render(
            "Pixel Paint",
            True,
            (140, 140, 145),
        )

        subtitle_rect = subtitle.get_rect(
            center=(self.panel_width // 2, 82)
        )

        self.screen.blit(subtitle, subtitle_rect)

        for button in self.buttons:
            rect = button["rect"]
            hovered = rect.collidepoint(mouse_pos)

            if button["action"] == "EXIT_APPLICATION":
                normal = (95, 40, 40)
                hover = (140, 55, 55)
            else:
                normal = (45, 45, 52)
                hover = (65, 65, 75)

            color = hover if hovered else normal

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=8,
            )

            text = self.font_button.render(
                button["text"],
                True,
                (235, 235, 235),
            )

            text_rect = text.get_rect(
                midleft=(
                    rect.left + 18,
                    rect.centery,
                )
            )

            self.screen.blit(text, text_rect)

        title = self.font_title.render(
            "Projects",
            True,
            (255, 255, 255),
        )

        self.screen.blit(
            title,
            (
                self.panel_width + 40,
                40,
            ),
        )

        self.project_rects.clear()

        x = self.panel_width + 40
        y = 110

        card_width = self.content_rect.width - 80
        card_height = 70
        gap = 12

        if not self.projects:
            empty_text = self.font_small.render(
                "No projects yet.",
                True,
                (130, 130, 135),
            )

            self.screen.blit(
                empty_text,
                (x, y),
            )

        for project in self.projects:
            rect = pygame.Rect(
                x,
                y,
                card_width,
                card_height,
            )

            self.project_rects.append(rect)

            hovered = rect.collidepoint(mouse_pos)

            color = (
                (55, 55, 65)
                if hovered
                else (40, 40, 48)
            )

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=8,
            )

            name = self.font_project.render(
                project.name,
                True,
                (240, 240, 240),
            )

            name_rect = name.get_rect(
                midleft=(
                    rect.left + 20,
                    rect.centery,
                )
            )

            self.screen.blit(name, name_rect)

            y += card_height + gap
import sys
import pygame

# --- 1. AYARLAR & SABİTLER ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_WIDTH = 100
GRID_HEIGHT = 100
CELL_SIZE = 24

MIN_ZOOM = 0.4
MAX_ZOOM = 5.0

COLOR_BACKGROUND = (30, 30, 35)
COLOR_GRID_LINE = (50, 50, 60)
COLOR_DEFAULT_CELL = (220, 220, 220)

COLOR_PALETTE = {
    pygame.K_F1:  (0, 0, 0),        # F1: Siyah
    pygame.K_F2:  (255, 255, 255),  # F2: Beyaz
    pygame.K_F3:  (239, 68, 68),    # F3: Kırmızı
    pygame.K_F4:  (34, 197, 94),    # F4: Yeşil
    pygame.K_F5:  (59, 130, 246),   # F5: Mavi
    pygame.K_F6:  (234, 179, 8),    # F6: Sarı
    pygame.K_F7:  (168, 85, 247),   # F7: Mor
    pygame.K_F8:  (236, 72, 153),   # F8: Pembe
    pygame.K_F9:  (249, 115, 22),   # F9: Turuncu
    pygame.K_F10: (6, 182, 212),    # F10: Turkuaz
}


# --- 2. MODEL SINIFLARI ---
class Cell:
    def __init__(self, grid_x: int, grid_y: int):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.default_color = COLOR_DEFAULT_CELL
        self.current_color = COLOR_DEFAULT_CELL

    def set_color(self, new_color: tuple[int, int, int]) -> None:
        self.current_color = new_color

    def reset_color(self) -> None:
        self.current_color = self.default_color


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


class Camera:
    def __init__(self):
        self.zoom_level: float = 1.0
        self.offset_x: float = (SCREEN_WIDTH - (GRID_WIDTH * CELL_SIZE)) / 2
        self.offset_y: float = (SCREEN_HEIGHT - (GRID_HEIGHT * CELL_SIZE)) / 2

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


# --- 3. UYGULAMA VE EVENT LOOP ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Paint - Prototip")
    clock = pygame.time.Clock()

    grid = Grid()
    camera = Camera()
    active_color = COLOR_PALETTE[pygame.K_F1]
    is_panning = False
    last_mouse_pos = (0, 0)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        grid_x, grid_y = camera.screen_to_grid(mouse_pos[0], mouse_pos[1])

        # --- OLAY İŞLEME (EVENT LOOP) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Fare Tekerleği -> Zoom
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    camera.zoom(1.15, mouse_pos)
                elif event.y < 0:
                    camera.zoom(0.85, mouse_pos)

            # Fare Tuşuna Basılma
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # Orta Tuş -> Pan Başlat
                    is_panning = True
                    last_mouse_pos = mouse_pos

            # Fare Tuşunu Bırakma
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    is_panning = False

            # Fare Hareketi
            elif event.type == pygame.MOUSEMOTION:
                if is_panning:
                    dx = mouse_pos[0] - last_mouse_pos[0]
                    dy = mouse_pos[1] - last_mouse_pos[1]
                    camera.pan(dx, dy)
                    last_mouse_pos = mouse_pos

            # Klavye Kısayolları
            elif event.type == pygame.KEYDOWN:
                # F1 - F10 Renk Seçimi
                if event.key in COLOR_PALETTE:
                    active_color = COLOR_PALETTE[event.key]

                # DEL / SHIFT + DEL
                elif event.key == pygame.K_DELETE:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_SHIFT:
                        grid.clear_all()
                    else:
                        target_cell = grid.get_cell(grid_x, grid_y)
                        if target_cell:
                            target_cell.reset_color()

        # --- FARE İLE SÜREKLİ ÇİZİM / SİLME ---
        mouse_buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        # Space + Sol Tık ile Pan
        if keys[pygame.K_SPACE] and mouse_buttons[0]:
            if not is_panning:
                is_panning = True
                last_mouse_pos = mouse_pos
            else:
                dx = mouse_pos[0] - last_mouse_pos[0]
                dy = mouse_pos[1] - last_mouse_pos[1]
                camera.pan(dx, dy)
                last_mouse_pos = mouse_pos
        else:
            if not pygame.mouse.get_pressed()[1]:  # Orta tuş basılı değilse
                is_panning = False

            # Sol Tık -> Boya (Space basılı değilken)
            if mouse_buttons[0] and not keys[pygame.K_SPACE]:
                cell = grid.get_cell(grid_x, grid_y)
                if cell:
                    cell.set_color(active_color)

            # Sağ Tık -> Hücreyi Sıfırla
            elif mouse_buttons[2]:
                cell = grid.get_cell(grid_x, grid_y)
                if cell:
                    cell.reset_color()

        # --- ÇİZİM MOTORU (RENDERER) ---
        screen.fill(COLOR_BACKGROUND)

        scaled_cell_size = CELL_SIZE * camera.zoom_level

        # Frustum Culling: Sadece ekranda görünen hücrelerin sınırlarını hesapla
        start_x = max(0, int((-camera.offset_x) // scaled_cell_size))
        end_x = min(GRID_WIDTH, int((SCREEN_WIDTH - camera.offset_x) // scaled_cell_size) + 1)
        start_y = max(0, int((-camera.offset_y) // scaled_cell_size))
        end_y = min(GRID_HEIGHT, int((SCREEN_HEIGHT - camera.offset_y) // scaled_cell_size) + 1)

        # Hücreleri Çiz
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                cell = grid.cells[x][y]
                draw_x = camera.offset_x + (x * scaled_cell_size)
                draw_y = camera.offset_y + (y * scaled_cell_size)

                # Hücre Dolgusu
                pygame.draw.rect(
                    screen,
                    cell.current_color,
                    (draw_x, draw_y, scaled_cell_size, scaled_cell_size)
                )

                # Izgara Çizgisi
                if camera.zoom_level > 0.3:
                    pygame.draw.rect(
                        screen,
                        COLOR_GRID_LINE,
                        (draw_x, draw_y, scaled_cell_size, scaled_cell_size),
                        1
                    )

        # Matris Dış Sınır Çerçevesi
        matrix_rect = (
            camera.offset_x,
            camera.offset_y,
            GRID_WIDTH * scaled_cell_size,
            GRID_HEIGHT * scaled_cell_size
        )
        pygame.draw.rect(screen, (255, 255, 255), matrix_rect, 2)

        # Sağ üst köşede seçili fırça rengi kutusu
        pygame.draw.rect(screen, active_color, (SCREEN_WIDTH - 45, 15, 30, 30))
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH - 45, 15, 30, 30), 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
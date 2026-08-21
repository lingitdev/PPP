import pygame

# SCREEN INF
SCREEN_HEIGHT: int = 720
SCREEN_WIDTH: int = 1280

# GRID INF
MAX_GRID: int = 150
GRID_HEIGHT: int = 100
GRID_WIDTH: int = 100

#CELL INF
CELL_SIZE:int = 24

#ZOOM INF
MAX_ZOOM:float = 5.0
MIN_ZOOM:float = 0.4

# --- UI COLOR(S)
COLOR_BACKGROUND = (30, 30, 35)      
COLOR_GRID_LINE  = (50, 50, 60)       
COLOR_DEFAULT_CELL = (220, 220, 220)  

# --- COLOR SELECTIONS AND SHORTCUTS DICT
COLOR_PALETTE = {
    pygame.K_F1:  (0, 0, 0),        # F1: BLACK
    pygame.K_F2:  (255, 255, 255),  # F2: WHITE
    pygame.K_F3:  (239, 68, 68),    # F3: RED
    pygame.K_F4:  (34, 197, 94),    # F4: GREEN
    pygame.K_F5:  (59, 130, 246),   # F5: BLUE
    pygame.K_F6:  (234, 179, 8),    # F6: YELLOW
    pygame.K_F7:  (168, 85, 247),   # F7: PURPLE
    pygame.K_F8:  (236, 72, 153),   # F8: PINK
    pygame.K_F9:  (249, 115, 22),   # F9: ORANGE
    pygame.K_F10: (6, 182, 212),    # F10: TURQUOISE 
}

# DEFAULT COLOR
DEFAULT_ACTIVE_COLOR = COLOR_PALETTE[pygame.K_F1]

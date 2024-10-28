from constants import *
import pygame


def create_walls():
    # standard_wall_width
    sww = 10
    return [
        # Outer walls - Main structure
        pygame.Rect(100, 50, 1070, sww),  # Top wall
        pygame.Rect(100, 550, 1070, sww),  # Bottom wall
        pygame.Rect(100, 50, sww, 510),  # Left wall
        pygame.Rect(1160, 50, sww, 510),  # Right wall

        # Vertical room dividers (left to right)
        pygame.Rect(350, 50, sww, 200),  # V1 upper
        pygame.Rect(600, 50, sww, 200),  # V2 upper
        pygame.Rect(550, 300, sww, 260),  # V2 lower
        pygame.Rect(850, 50, sww, 200),  # V3 upper
        pygame.Rect(900, 300, sww, 260),  # V3 lower

        # Horizontal room dividers
        pygame.Rect(100, 250, 150, sww),
        pygame.Rect(300, 250, 180, sww),
        pygame.Rect(530, 250, 180, sww),
        pygame.Rect(760, 250, 250, sww),

        # Bedroom doors
        pygame.Rect(550, 450, 50, sww),
        pygame.Rect(630, 450, 50, sww),
        pygame.Rect(710, 450, 50, sww),
        pygame.Rect(790, 450, 50, sww),
        pygame.Rect(870, 450, 30, sww),

        # Bedroom walls
        pygame.Rect(760, 250, 250, sww),
    ]


def create_furniture():
    from entities.furniture import Furniture

    return [
        # Living Room (bottom left - larger entertainment area)
        Furniture(pygame.Rect(130, 380, 180, 40), BEIGE, "large couch"),
        Furniture(pygame.Rect(130, 440, 60, 60), BEIGE, "armchair 1"),
        Furniture(pygame.Rect(250, 440, 60, 60), BEIGE, "armchair 2"),

        # Main Bedroom (top left - master suite)
        Furniture(pygame.Rect(130, 80, 160, 100), GRAY, "king bed"),
        Furniture(pygame.Rect(130, 200, 60, 40), BEIGE, "dresser"),
        Furniture(pygame.Rect(290, 80, 40, 40), BEIGE, "nightstand"),

        # Dining Room (top middle - formal dining)
        Furniture(pygame.Rect(400, 100, 160, 100), BEIGE, "dining table"),
        Furniture(pygame.Rect(400, 80, 40, 40), GRAY, "china cabinet"),

        # Kitchen (top right - modern kitchen)
        Furniture(pygame.Rect(640, 80, 180, 40), GRAY, "counter"),
        Furniture(pygame.Rect(640, 160, 80, 80), BEIGE, "kitchen table"),
        Furniture(pygame.Rect(750, 160, 80, 40), GRAY, "island"),

        # Study (bottom middle - work space)
        Furniture(pygame.Rect(400, 320, 100, 60), GRAY, "desk"),
        Furniture(pygame.Rect(400, 450, 60, 80), BEIGE, "bookshelf 1"),

        # Library (bottom right - reading room)
        Furniture(pygame.Rect(1000, 380, 60, 150), BEIGE, "tall bookshelf 2"),

        # Guest Bedroom (top far right)
        Furniture(pygame.Rect(900, 80, 120, 80), GRAY, "queen bed"),
        Furniture(pygame.Rect(1040, 80, 40, 40), BEIGE, "guest nightstand"),

        # Windows
        Furniture(pygame.Rect(1140, 100, 20, 60), LIGHT_BLUE, "window 1"),
        Furniture(pygame.Rect(1140, 300, 20, 60), LIGHT_BLUE, "window 2"),
        Furniture(pygame.Rect(1140, 500, 20, 60), LIGHT_BLUE, "window 3"),
        Furniture(pygame.Rect(100, 100, 20, 60), LIGHT_BLUE, "window 4"),
        Furniture(pygame.Rect(100, 300, 20, 60), LIGHT_BLUE, "window 5"),
    ]
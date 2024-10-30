from constants import *
import pygame


def create_walls():
    # standard_wall_width
    sww = 10
    return [
        # Outer walls - Main structure
        pygame.Rect(100, 50, 970, sww),  # Top wall
        pygame.Rect(100, 550, 970, sww),  # Bottom wall
        pygame.Rect(100, 50, sww, 510),  # Left wall
        pygame.Rect(1060, 50, sww, 510),  # Right wall

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
        pygame.Rect(810, 450, sww, 100),
        pygame.Rect(730, 450, sww, 100),
        pygame.Rect(650, 450, sww, 100),

        # Bathroom walls
        #pygame.Rect(500, 300, sww, 260),
    ]


def create_furniture():
    from entities.furniture import Furniture

    return [
        # Living Room (bottom left - larger entertainment area)
        Furniture(pygame.Rect(130, 380, 180, 40), BEIGE, "large couch"),
        Furniture(pygame.Rect(130, 440, 60, 60), BEIGE, "armchair 1"),
        Furniture(pygame.Rect(250, 440, 60, 60), BEIGE, "armchair 2"),

        # TV room
        Furniture(pygame.Rect(110, 180, 15, 60), GRAY, "Tv"),
        Furniture(pygame.Rect(180, 190, 30, 60), BROWN, "Sofa 1"),
        Furniture(pygame.Rect(180, 170, 30, 30), BROWN, "Sofa 2"),
        #Furniture(pygame.Rect(290, 80, 40, 40), BEIGE, "nightstand"),

        # Dining Room (top middle - formal dining)
        Furniture(pygame.Rect(400, 100, 160, 100), BEIGE, "dining table"),
        Furniture(pygame.Rect(400, 80, 40, 40), GRAY, "china cabinet"),

        # Kitchen (top right - modern kitchen)
        Furniture(pygame.Rect(610, 60, 240, 30), GRAY, "counter"),
        Furniture(pygame.Rect(630, 140, 80, 80), BEIGE, "kitchen table"),
        Furniture(pygame.Rect(770, 210, 80, 40), GRAY, "Large fridge"),

        # Study (bottom middle - work space)
        #Furniture(pygame.Rect(400, 320, 100, 60), GRAY, "desk"),
        #Furniture(pygame.Rect(400, 450, 60, 80), BEIGE, "bookshelf 1"),

        # Library (bottom right - reading room)
        Furniture(pygame.Rect(985, 300, 75, 30), BEIGE, "tall bookshelf 1"),
        Furniture(pygame.Rect(985, 360, 75, 30), BEIGE, "tall bookshelf 2"),
        Furniture(pygame.Rect(985, 420, 75, 30), BEIGE, "tall bookshelf 3"),

        # Bedroom furniture (Middle bottom)
        Furniture(pygame.Rect(580, 490, 40, 60), GRAY, "bed 1"),
        Furniture(pygame.Rect(620, 530, 20, 20), BEIGE, "nightstand 1"),

        Furniture(pygame.Rect(670, 490, 40, 60), GRAY, "bed 2"),
        Furniture(pygame.Rect(710, 530, 20, 20), BEIGE, "nightstand 2"),

        Furniture(pygame.Rect(750, 490, 40, 60), GRAY, "bed 3"),
        Furniture(pygame.Rect(790, 530, 20, 20), BEIGE, "nightstand 3"),

        Furniture(pygame.Rect(840, 490, 40, 60), GRAY, "bed 4"),
        Furniture(pygame.Rect(880, 530, 20, 20), BEIGE, "nightstand 4"),

        # Windows
        Furniture(pygame.Rect(1060, 100, 10, 60), LIGHT_BLUE, "window 1"),
        Furniture(pygame.Rect(1060, 450, 10, 60), LIGHT_BLUE, "window 2"),
        Furniture(pygame.Rect(100, 100, 10, 60), LIGHT_BLUE, "window 3"),
        Furniture(pygame.Rect(100, 300, 10, 60), LIGHT_BLUE, "window 4"),
        Furniture(pygame.Rect(500, 50, 60, 10), LIGHT_BLUE, "window 5"),
        Furniture(pygame.Rect(700, 50, 60, 10), LIGHT_BLUE, "window 6"),
        Furniture(pygame.Rect(300, 550, 60, 10), LIGHT_BLUE, "window 7"),
        Furniture(pygame.Rect(925, 550, 60, 10), LIGHT_BLUE, "window 8"),
    ]
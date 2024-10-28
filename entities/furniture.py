import pygame
import random
from constants import *

class Furniture:
    def __init__(self, rect, color, name):
        self.rect = rect
        self.color = color
        self.name = name
        self.approach_points = self.calculate_approach_points()

    def calculate_approach_points(self):
        points = []
        offset = 60  # Increased from 50 to keep NPC further away

        # Add points at a greater distance
        points.append((self.rect.centerx, self.rect.bottom + offset))
        points.append((self.rect.centerx, self.rect.top - offset))
        points.append((self.rect.left - offset, self.rect.centery))
        points.append((self.rect.right + offset, self.rect.centery))

        return points

    def get_random_approach_point(self):
        # Adjust the valid area to keep points further from walls
        valid_points = [p for p in self.approach_points
                       if 240 < p[0] < 540 and  # Narrowed from 220-560
                       140 < p[1] < 440]        # Narrowed from 120-460
        return random.choice(valid_points) if valid_points else (self.rect.centerx, self.rect.bottom + 70)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
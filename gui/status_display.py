# gui/status_display.py
import pygame
from typing import List, Tuple
from constants import *


class StatusBar:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.border_rect = pygame.Rect(x - 2, y - 2, width + 4, height + 4)

    def draw(self, surface: pygame.Surface, value: float, color: Tuple[int, int, int]):
        # Draw border
        pygame.draw.rect(surface, BLACK, self.border_rect, 2)

        # Draw background
        pygame.draw.rect(surface, (200, 200, 200), self.rect)

        # Draw filled portion
        fill_width = int((value / 100) * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(surface, color, fill_rect)


class NPCStatusDisplay:
    def __init__(self):
        self.bar_width = 150
        self.bar_height = 15
        self.padding = 5
        self.section_height = 130  # Height for each NPC's status section

        # Colors for different status bars
        self.colors = {
            'health': (255, 0, 0),  # Red
            'hunger': (0, 255, 0),  # Green
            'stamina': (0, 191, 255)  # Deep Sky Blue
        }

        # Initialize font
        self.font = pygame.font.SysFont('Arial', 12)

    def draw(self, surface: pygame.Surface, npcs: List['NPC']):
        start_x = WINDOW_WIDTH - self.bar_width - 20  # 20 pixels from right edge

        for i, npc in enumerate(npcs):
            if npc.dead:
                continue

            start_y = 20 + (i * self.section_height)

            # Draw NPC name and role
            name_text = self.font.render(f"{npc.name} ({npc.role})", True, BLACK)
            surface.blit(name_text, (start_x, start_y))

            # Draw status bars
            statuses = [
                ('Health', npc.health, self.colors['health']),
                ('Hunger', npc.hunger, self.colors['hunger']),
                ('Stamina', npc.stamina, self.colors['stamina'])
            ]

            for j, (label, value, color) in enumerate(statuses):
                # Draw label
                y_pos = start_y + 20 + (j * (self.bar_height + self.padding * 2))
                label_text = self.font.render(f"{label}: {int(value)}", True, BLACK)
                surface.blit(label_text, (start_x, y_pos))

                # Draw status bar
                bar = StatusBar(
                    start_x + 70,  # Offset for label
                    y_pos,
                    self.bar_width - 70,  # Reduce width to account for label
                    self.bar_height
                )
                bar.draw(surface, value, color)
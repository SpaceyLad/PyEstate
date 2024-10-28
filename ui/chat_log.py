import pygame
from constants import *

class ChatLog:
    def __init__(self):
        self.messages = []
        self.max_messages = 5
        self.background = pygame.Rect(10, WINDOW_HEIGHT - 150, 300, 140)  # Updated width
        self.font = pygame.font.SysFont('Arial', 10)  # Smaller font size
        self.last_message = None  # Track last message to prevent duplicates

    def add_message(self, message):
        # Only add if it's not the same as the last message
        if message != self.last_message:
            self.messages.append(message)
            if len(self.messages) > self.max_messages:
                self.messages.pop(0)
            self.last_message = message

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.background)
        pygame.draw.rect(surface, BLACK, self.background, 2)
        for i, message in enumerate(self.messages):
            text_surface = self.font.render(message, True, BLACK)
            surface.blit(text_surface, (20, WINDOW_HEIGHT - 140 + (i * 25)))

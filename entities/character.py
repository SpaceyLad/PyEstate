import pygame
import time
from constants import *
from entities.furniture import Furniture


class Character:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = color
        self.speed = PLAYER_SPEED
        self.current_message = ""
        self.message_time = 0

    def move(self, dx, dy, walls, furniture):
        # Try moving in both directions first
        original_x = self.rect.x
        original_y = self.rect.y
        collided = False

        # Try full movement first
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Check for collisions
        for obstacle in walls + furniture:
            obstacle_rect = obstacle.rect if isinstance(obstacle, Furniture) else obstacle
            if self.rect.colliderect(obstacle_rect):
                collided = True
                break

        if collided:
            # Reset position
            self.rect.x = original_x
            self.rect.y = original_y

            # Try moving horizontally only
            self.rect.x += dx * self.speed
            horizontal_collision = False
            for obstacle in walls + furniture:
                obstacle_rect = obstacle.rect if isinstance(obstacle, Furniture) else obstacle
                if self.rect.colliderect(obstacle_rect):
                    horizontal_collision = True
                    self.rect.x = original_x
                    break

            # Try moving vertically only
            self.rect.y += dy * self.speed
            vertical_collision = False
            for obstacle in walls + furniture:
                obstacle_rect = obstacle.rect if isinstance(obstacle, Furniture) else obstacle
                if self.rect.colliderect(obstacle_rect):
                    vertical_collision = True
                    self.rect.y = original_y
                    break

            # If both directions are blocked, try sliding at reduced speed
            if horizontal_collision and vertical_collision and (abs(dx) > 0 and abs(dy) > 0):
                # Try sliding horizontally at reduced speed
                slide_speed = self.speed * 0.7  # Reduce sliding speed
                self.rect.x += dx * slide_speed
                for obstacle in walls + furniture:
                    obstacle_rect = obstacle.rect if isinstance(obstacle, Furniture) else obstacle
                    if self.rect.colliderect(obstacle_rect):
                        self.rect.x = original_x
                        break

                # Try sliding vertically at reduced speed
                self.rect.y += dy * slide_speed
                for obstacle in walls + furniture:
                    obstacle_rect = obstacle.rect if isinstance(obstacle, Furniture) else obstacle
                    if self.rect.colliderect(obstacle_rect):
                        self.rect.y = original_y
                        break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.current_message and time.time() - self.message_time < CHAT_DURATION:
            self.draw_message(surface)

    def say(self, message):
        self.current_message = message
        self.message_time = time.time()

    def draw_message(self, surface):
        font = pygame.font.SysFont('Arial', FONT_SIZE)
        message_surface = font.render(self.current_message, True, BLACK)
        message_rect = message_surface.get_rect()
        message_rect.midbottom = (self.rect.centerx, self.rect.top - 5)

        padding = 5
        background_rect = message_rect.inflate(padding * 2, padding * 2)
        background_rect.midbottom = (self.rect.centerx, self.rect.top - 5)
        pygame.draw.rect(surface, WHITE, background_rect)
        pygame.draw.rect(surface, BLACK, background_rect, 1)

        surface.blit(message_surface, message_rect)
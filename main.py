import pygame
import sys
import time
from constants import *
from entities.character import Character
from entities.npc import NPC
from entities.furniture import Furniture
from ui.chat_log import ChatLog
from entities.npc_data import NPCData


def main():
    pygame.init()
    pygame.font.init()

    # Set up display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PyEstate")
    clock = pygame.time.Clock()

    # Create walls
    # standard_wall_width
    sww = 10
    walls = [
        # Outer walls - Main structure
        pygame.Rect(100, 50, 1070, sww),  # Top wall
        pygame.Rect(100, 550, 1070, sww),  # Bottom wall
        pygame.Rect(100, 50, sww, 510),  # Left wall
        pygame.Rect(1160, 50, sww, 510),  # Right wall

        # Vertical room dividers (left to right)
        pygame.Rect(350, 50, sww, 200),  # V1 upper
        # pygame.Rect(350, 300, sww, 260),  # V1 lower
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

    # Expanded furniture layout
    furniture = [
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
        # Furniture(pygame.Rect(890, 320, 120, 40), BEIGE, "reading couch"),
        # Furniture(pygame.Rect(890, 380, 60, 150), BEIGE, "tall bookshelf"),
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

    chat_log = ChatLog()

    # Create NPCs using the preset data
    npc_data = NPCData.create_preset_npcs()
    npcs = [
        NPC(300, 200, npc_data["butler"]),
        NPC(400, 300, npc_data["maid"]),
        NPC(500, 200, npc_data["gardener"]),
        NPC(350, 270, npc_data["chef"])
    ]

    for npc in npcs:
        npc.chat_log = chat_log
        npc.set_patrol_points(furniture, walls)

    # Create game objects
    player = Character(400, 300, RED)
    # Game state variables
    last_position_print = time.time()
    input_text = ""
    input_active = False
    font = pygame.font.SysFont('Arial', FONT_SIZE)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text:
                    player.say(input_text)
                    chat_log.add_message(f"You: {input_text}")
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_t and not input_active:
                    input_active = True
                elif event.key == pygame.K_ESCAPE:
                    input_active = False
                    input_text = ""
                elif input_active and event.unicode.isprintable():
                    input_text += event.unicode

        # Handle player movement (only if not typing)
        if not input_active:
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            player.move(dx, dy, walls, furniture)

        # Update NPC
        for npc in npcs:
            npc.update(walls, furniture)
            # Add NPC messages to chat log when they speak
            if npc.current_message and time.time() - npc.message_time < 0.1:
                print(npc.current_message)
                chat_log.add_message(f"{npc.current_message}")

        # Print positions every second (debug)
        current_time = time.time()
        if current_time - last_position_print >= 5.0:
            print(f"Player position: ({player.rect.x}, {player.rect.y})")
            for npc in npcs:
                print(f"{npc.role} position: ({npc.rect.x}, {npc.rect.y})")
            last_position_print = current_time

        # Drawing
        screen.fill(WHITE)

        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, BROWN, wall)

        # Draw furniture
        for item in furniture:
            item.draw(screen)

        # Draw characters
        player.draw(screen)
        for npc in npcs:
            npc.draw(screen)

        # Draw chat log
        chat_log.draw(screen)

        # Draw input box if active
        if input_active:
            input_box = pygame.Rect(10, WINDOW_HEIGHT - 30, 200, 25)
            pygame.draw.rect(screen, WHITE, input_box)
            pygame.draw.rect(screen, BLACK, input_box, 2)
            text_surface = font.render(input_text, True, BLACK)
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

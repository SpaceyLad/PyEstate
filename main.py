import pygame
import sys
import time
from constants import *
from entities.character import Character
from entities.npc import NPC, NavigationMesh
from ui.chat_log import ChatLog
from entities.npc_data import NPCData
from utils.layout_config import create_walls, create_furniture

walls = create_walls()
furniture = create_furniture()
nav_mesh = NavigationMesh(walls, furniture)


def main():
    pygame.init()
    pygame.font.init()

    # Set up display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PyEstate")
    clock = pygame.time.Clock()

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
        npc.set_navigation_mesh(nav_mesh)

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

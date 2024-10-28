import random
import time
import math
from constants import *
from entities.character import Character
from utils.pathfinding import PathFinder
from entities.npc_data import NPCData
from typing import List, Tuple, Dict, Set
import pygame
import heapq


class NavigationMesh:
    def __init__(self, walls: List[pygame.Rect], furniture: List['Furniture'], cell_size: int = 40):
        self.cell_size = cell_size
        self.walkable_cells: Set[Tuple[int, int]] = set()
        self.path_cache: Dict[Tuple[Tuple[int, int], Tuple[int, int]], List[Tuple[int, int]]] = {}
        self.create_navigation_mesh(walls, furniture)

    def create_navigation_mesh(self, walls: List[pygame.Rect], furniture: List['Furniture']) -> None:
        """Create a grid of walkable cells"""
        # Convert coordinates to grid cells
        min_x, max_x = 100, 1160  # From wall coordinates
        min_y, max_y = 50, 550

        # Create initial grid
        for x in range(min_x, max_x, self.cell_size):
            for y in range(min_y, max_y, self.cell_size):
                cell = pygame.Rect(x, y, self.cell_size, self.cell_size)
                is_walkable = True

                # Check collision with walls and furniture
                for wall in walls:
                    if cell.colliderect(wall):
                        is_walkable = False
                        break

                if is_walkable:
                    for item in furniture:
                        if cell.colliderect(item.rect):
                            is_walkable = False
                            break

                if is_walkable:
                    self.walkable_cells.add((x // self.cell_size, y // self.cell_size))

    def get_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get path between two points, using cache if available"""
        # Convert to grid coordinates
        start_cell = (start[0] // self.cell_size, start[1] // self.cell_size)
        end_cell = (end[0] // self.cell_size, end[1] // self.cell_size)

        # Check cache
        cache_key = (start_cell, end_cell)
        if cache_key in self.path_cache:
            return self.path_cache[cache_key]

        # A* pathfinding
        path = self._find_path(start_cell, end_cell)

        # Cache the result
        self.path_cache[cache_key] = path
        return path

    def _find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """A* pathfinding with optimizations"""
        if start == end:
            return [start]

        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == end:
                break

            # Only check orthogonal movements (no diagonals)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_cell = (current[0] + dx, current[1] + dy)

                if next_cell not in self.walkable_cells:
                    continue

                new_cost = cost_so_far[current] + 1

                if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                    cost_so_far[next_cell] = new_cost
                    priority = new_cost + self._heuristic(next_cell, end)
                    heapq.heappush(frontier, (priority, next_cell))
                    came_from[next_cell] = current

        # Reconstruct path
        current = end
        path = []
        while current is not None:
            # Convert back to world coordinates
            world_coords = (current[0] * self.cell_size + self.cell_size // 2,
                            current[1] * self.cell_size + self.cell_size // 2)
            path.append(world_coords)
            current = came_from.get(current)

        return list(reversed(path))

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


class NPC(Character):
    def __init__(self, x, y, npc_data: NPCData):
        color = self.get_role_color(npc_data.role)  # Different colors for different roles
        super().__init__(x, y, color)
        self.name = npc_data.name
        self.age = npc_data.age
        self.role = npc_data.role
        self.chat_messages = npc_data.chat_messages

        # Initialize other NPC attributes
        self.speed = NPC_SPEED
        self.last_chat_time = time.time()
        self.current_patrol_index = 0
        self.patrol_points = []
        self.target_x = x
        self.target_y = y
        self.waiting_time = 0
        self.wait_duration = 2.0
        self.current_path = None
        self.current_path_index = 0
        self.pathfinder = None
        self.furniture = None
        self.last_movement_time = time.time()
        self.stuck_timeout = 1.0
        self.respawn_timeout = 5.0
        self.is_unsticking = False
        self.unstick_path = None
        self.last_position = (x, y)
        self.original_target = None
        self.last_unstick_attempt = time.time()
        self.unstick_attempts = 0
        self.max_unstick_attempts = 2
        self.stuck_start_time = None
        self.initial_x = x
        self.initial_y = y

    def set_navigation_mesh(self, nav_mesh):
        self.nav_mesh = nav_mesh

    def update_path(self, target_pos):
        start_pos = (self.rect.centerx, self.rect.centery)
        self.current_path = self.nav_mesh.get_path(start_pos, target_pos)

    def get_role_color(self, role):
        """Return different colors for different NPC roles"""
        color_map = {
            "Butler": (0, 0, 255),  # Blue
            "Maid": (255, 192, 203),  # Pink
            "Gardener": (0, 255, 0),  # Green
            "Chef": (255, 0, 0)  # Red
        }
        return color_map.get(role, (0, 0, 255))  # Default to blue if role not found

    def say(self, message):
        """Override say method to include NPC name"""
        self.current_message = f"{self.name} ({self.role}): {message}"
        self.message_time = time.time()

    def respawn(self):
        print("NPC respawning...")
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.current_path = None
        self.current_path_index = 0
        self.is_unsticking = False
        self.unstick_path = None
        self.original_target = None
        self.unstick_attempts = 0
        self.stuck_start_time = None
        self.last_movement_time = time.time()
        self.last_position = (self.initial_x, self.initial_y)
        self.say("Whoops, got stuck! Starting over...")

    def try_unstick(self):
        print(f"Attempting to unstick NPC (attempt {self.unstick_attempts + 1})...")

        # Store original target if this is the first unstick attempt
        if not self.is_unsticking:
            self.original_target = (self.target_x, self.target_y)
            self.unstick_attempts = 0

        # Increase radius based on number of attempts
        base_radius = 40
        radius_increase = self.unstick_attempts * 20  # Increase radius by 20 pixels per attempt
        min_distance = base_radius + radius_increase
        max_distance = min_distance + 40

        # Generate a point in an expanding circle
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(min_distance, max_distance)

        # Calculate new unstick target
        unstick_x = self.rect.centerx + math.cos(angle) * distance
        unstick_y = self.rect.centery + math.sin(angle) * distance

        # Keep the point within the house bounds
        unstick_x = max(240, min(540, unstick_x))
        unstick_y = max(140, min(440, unstick_y))

        # Find a path to this temporary point
        self.unstick_path = self.pathfinder.find_path(
            (self.rect.centerx, self.rect.centery),
            (unstick_x, unstick_y)
        )

        if self.unstick_path:
            self.is_unsticking = True
            self.last_unstick_attempt = time.time()
            self.unstick_attempts += 1
            print(f"Found unstick path to ({unstick_x}, {unstick_y})")
            return True
        return False

    def try_return_to_original(self):
        if not self.original_target:
            return False

        return_path = self.pathfinder.find_path(
            (self.rect.centerx, self.rect.centery),
            self.original_target
        )

        if return_path:
            print("Found path back to original target!")
            self.current_path = return_path
            self.current_path_index = 0
            self.is_unsticking = False
            self.unstick_path = None
            self.original_target = None
            self.unstick_attempts = 0
            return True
        return False

    def update(self, walls, furniture):
        current_time = time.time()

        # Chat updates
        if current_time - self.last_chat_time > NPC_CHAT_INTERVAL:
            self.say(random.choice(self.chat_messages))
            self.last_chat_time = current_time

        # If we're waiting at a point, don't do stuck detection
        if self.waiting_time > 0:
            if current_time - self.waiting_time > self.wait_duration:
                self.waiting_time = 0
                self.current_patrol_index = (self.current_patrol_index + 1) % len(self.furniture)
                self.current_path = None
            return

        # Get current path
        current_path = self.unstick_path if self.is_unsticking else self.current_path

        # Only do stuck detection if we have a path and are trying to move
        if current_path and self.current_path_index < len(current_path):
            current_pos = (self.rect.x, self.rect.y)
            distance_moved = math.sqrt(
                (current_pos[0] - self.last_position[0]) ** 2 +
                (current_pos[1] - self.last_position[1]) ** 2
            )

            if distance_moved < 1:  # If we haven't moved significantly
                # Start tracking stuck time if we haven't already
                if self.stuck_start_time is None:
                    self.stuck_start_time = current_time

                # Check if we've been stuck long enough to respawn
                if current_time - self.stuck_start_time > self.respawn_timeout:
                    self.respawn()
                    return
                # Normal unstick behavior if we haven't reached respawn timeout
                elif current_time - self.last_movement_time > self.stuck_timeout:
                    if self.is_unsticking and current_time - self.last_unstick_attempt > self.stuck_timeout:
                        if self.unstick_attempts < self.max_unstick_attempts:
                            self.try_unstick()
                        else:
                            print("Too many unstick attempts, finding new patrol target...")
                            self.is_unsticking = False
                            self.unstick_path = None
                            self.original_target = None
                            self.unstick_attempts = 0
                            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.furniture)
                            self.find_new_path()
                    elif not self.is_unsticking:
                        self.try_unstick()
            else:
                # Reset stuck tracking if we've moved
                self.stuck_start_time = None
                self.last_movement_time = current_time
                if self.is_unsticking and current_time - self.last_unstick_attempt > 0.5:
                    self.try_return_to_original()

            self.last_position = current_pos

        # Use unstick path if we're unsticking, otherwise use normal path
        current_path = self.unstick_path if self.is_unsticking else self.current_path

        # If no path or reached end of path, find new path
        if not current_path or self.current_path_index >= len(current_path):
            if self.is_unsticking:
                # If we've finished the unstick path, try to return to original target
                if self.try_return_to_original():
                    current_path = self.current_path
                else:
                    # If we can't return to original target, try unsticking again
                    if not self.try_unstick():
                        return
                    current_path = self.unstick_path
            else:
                if not self.find_new_path():
                    return
                current_path = self.current_path

        # Ensure we have a valid path
        if not current_path:
            return

        # Move towards target
        target = current_path[self.current_path_index]
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.speed:
            self.current_path_index += 1
            if self.current_path_index >= len(current_path):
                if self.is_unsticking:
                    # Try to return to original target
                    self.try_return_to_original()
                else:
                    self.waiting_time = current_time
        else:
            dx = dx / distance
            dy = dy / distance
            self.move(dx, dy, walls, furniture)



    def draw(self, surface):
        super().draw(surface)
        # Draw pathfinding debug lines
        current_path = self.unstick_path if self.is_unsticking else self.current_path

        if current_path and len(current_path) > self.current_path_index:
            start_pos = (self.rect.centerx, self.rect.centery)
            path_color = RED if self.is_unsticking else BLUE  # Red for unstick path

            # Draw line from NPC to next point
            pygame.draw.line(surface, path_color, start_pos, current_path[self.current_path_index], 2)

            # Draw remaining path
            for i in range(self.current_path_index, len(current_path) - 1):
                pygame.draw.line(surface, path_color, current_path[i], current_path[i + 1], 2)

            # Draw original target if we're unsticking
            if self.original_target and self.is_unsticking:
                pygame.draw.circle(surface, GREEN, (int(self.original_target[0]), int(self.original_target[1])), 5)


    def set_patrol_points(self, furniture, walls):
        self.furniture = furniture
        self.pathfinder = PathFinder(walls, furniture)

    def find_new_path(self):
        if random.random() < RANDOM_MOVE_CHANCE:
            self.target_x = random.randint(220, 560)
            self.target_y = random.randint(120, 460)
        else:
            current_furniture = self.furniture[self.current_patrol_index]
            target = current_furniture.get_random_approach_point()
            self.target_x, self.target_y = target

        # Use NPC center for both start and end positions
        start_pos = (self.rect.centerx, self.rect.centery)
        end_pos = (self.target_x, self.target_y)

        path = self.pathfinder.find_path(start_pos, end_pos)

        if path:
            # Store the path without any offset adjustments
            self.current_path = path
            self.current_path_index = 0
        return path is not None
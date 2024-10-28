import pygame
from heapq import heappush, heappop
from constants import *

class Node:
    def __init__(self, x, y, cost, parent=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class PathFinder:
    def __init__(self, walls, furniture):
        self.grid_size = GRID_SIZE
        self.walls = walls
        self.furniture = furniture
        self.grid_width = WINDOW_WIDTH // self.grid_size
        self.grid_height = WINDOW_HEIGHT // self.grid_size

    def is_valid(self, x, y):
        if x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height:
            return False

        pixel_x = x * self.grid_size
        pixel_y = y * self.grid_size
        rect = pygame.Rect(pixel_x, pixel_y, self.grid_size, self.grid_size)

        for wall in self.walls:
            if rect.colliderect(wall):
                return False

        for item in self.furniture:
            if rect.colliderect(item.rect):
                return False

        return True

    def get_neighbors(self, node):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            new_x = node.x + dx
            new_y = node.y + dy
            if self.is_valid(new_x, new_y):
                cost = 1.4 if dx != 0 and dy != 0 else 1
                neighbors.append(Node(new_x, new_y, node.cost + cost, node))
        return neighbors

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start_pos, end_pos):
        start = (int(start_pos[0] // self.grid_size), int(start_pos[1] // self.grid_size))
        end = (int(end_pos[0] // self.grid_size), int(end_pos[1] // self.grid_size))

        if not self.is_valid(start[0], start[1]) or not self.is_valid(end[0], end[1]):
            return None

        open_set = []
        closed_set = set()

        start_node = Node(start[0], start[1], 0)
        start_node.f = self.heuristic(start, end)

        heappush(open_set, (start_node.f, start_node))

        while open_set:
            current_f, current_node = heappop(open_set)

            if (current_node.x, current_node.y) == end:
                path = []
                while current_node:
                    path.append((current_node.x * self.grid_size + self.grid_size // 2,
                               current_node.y * self.grid_size + self.grid_size // 2))
                    current_node = current_node.parent
                return path[::-1]

            closed_set.add((current_node.x, current_node.y))

            for neighbor in self.get_neighbors(current_node):
                if (neighbor.x, neighbor.y) in closed_set:
                    continue

                neighbor.f = neighbor.cost + self.heuristic((neighbor.x, neighbor.y), end)

                if not any(node.x == neighbor.x and node.y == neighbor.y for _, node in open_set):
                    heappush(open_set, (neighbor.f, neighbor))

        return None
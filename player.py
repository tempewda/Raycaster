# player.py

import pygame
import math

class Player:
    def __init__(self, x, y, dir_x=-1, dir_y=0, plane_x=0, plane_y=0.66, move_speed=4.0, rot_speed=0.1):
        # Initialize player position and viewing direction
        self.pos_x = x
        self.pos_y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.plane_x = plane_x
        self.plane_y = plane_y
        self.move_speed = move_speed
        self.rot_speed = rot_speed

    def update_position(self, delta_time, game_map):
        """Update player position based on key presses and delta time."""
        move_speed = self.move_speed * delta_time  # Adjusted for frame rate
        rot_speed = self.rot_speed * delta_time

        keys = pygame.key.get_pressed()

        # Move forward
        if keys[pygame.K_w]:
            next_x = self.pos_x + self.dir_x * move_speed
            next_y = self.pos_y + self.dir_y * move_speed
            if not game_map.is_wall(int(next_x), int(self.pos_y)):
                self.pos_x = next_x
            if not game_map.is_wall(int(self.pos_x), int(next_y)):
                self.pos_y = next_y

        # Move backward
        if keys[pygame.K_s]:
            next_x = self.pos_x - self.dir_x * move_speed
            next_y = self.pos_y - self.dir_y * move_speed
            if not game_map.is_wall(int(next_x), int(self.pos_y)):
                self.pos_x = next_x
            if not game_map.is_wall(int(self.pos_x), int(next_y)):
                self.pos_y = next_y

        # Strafe left
        if keys[pygame.K_a]:
            next_x = self.pos_x - self.dir_y * move_speed
            next_y = self.pos_y + self.dir_x * move_speed
            if not game_map.is_wall(int(next_x), int(self.pos_y)):
                self.pos_x = next_x
            if not game_map.is_wall(int(self.pos_x), int(next_y)):
                self.pos_y = next_y

        # Strafe right
        if keys[pygame.K_d]:
            next_x = self.pos_x + self.dir_y * move_speed
            next_y = self.pos_y - self.dir_x * move_speed
            if not game_map.is_wall(int(next_x), int(self.pos_y)):
                self.pos_x = next_x
            if not game_map.is_wall(int(self.pos_x), int(next_y)):
                self.pos_y = next_y


    def update_direction(self, dx):
        """Update player's direction based on mouse movement (dx)."""
        # Rotate the direction vector
        old_dir_x = self.dir_x
        self.dir_x = self.dir_x * math.cos(-dx) - self.dir_y * math.sin(-dx)
        self.dir_y = old_dir_x * math.sin(-dx) + self.dir_y * math.cos(-dx)

        # Rotate the camera plane
        old_plane_x = self.plane_x
        self.plane_x = self.plane_x * math.cos(-dx) - self.plane_y * math.sin(-dx)
        self.plane_y = old_plane_x * math.sin(-dx) + self.plane_y * math.cos(-dx)
    
    def handle_mouse_rotation(self, sensitivity=0.005):
        """Adjust player's direction based on mouse movement for rotation."""
        dx, dy = pygame.mouse.get_rel()
        self.update_direction(dx * sensitivity)

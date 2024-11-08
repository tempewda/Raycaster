import math
import pygame

class Raycaster:
    def __init__(self, screen, screen_width, screen_height, world_map, colors):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_map = world_map
        self.colors = colors

    def cast_ray(self, player):
        for x in range(self.screen_width):
            # Calculate ray position and direction
            cameraX = 2 * x / self.screen_width - 1
            rayDirX = player.dir_x + player.plane_x * cameraX
            rayDirY = player.dir_y + player.plane_y * cameraX

            # Map position
            mapX, mapY = int(player.pos_x), int(player.pos_y)

            # Length of ray from one side to next in x or y
            deltaDistX = abs(1 / rayDirX) if rayDirX != 0 else float('inf')
            deltaDistY = abs(1 / rayDirY) if rayDirY != 0 else float('inf')

            # Calculate step and initial sideDist
            if rayDirX < 0:
                stepX = -1
                sideDistX = (player.pos_x - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1.0 - player.pos_x) * deltaDistX
            if rayDirY < 0:
                stepY = -1
                sideDistY = (player.pos_y - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1.0 - player.pos_y) * deltaDistY

            # Perform DDA (Digital Differential Analysis)
            hit, side = 0, 0
            while hit == 0:
                # Jump to the next map square, either in x or y direction
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1
                # Check if the ray has hit a wall
                if self.world_map.is_wall(x = mapX, y = mapY) > 0:
                    hit = 1

            # Calculate distance projected on camera direction
            perpWallDist = (sideDistX - deltaDistX) if side == 0 else (sideDistY - deltaDistY)

            # Calculate height of line to draw on screen
            lineHeight = int(self.screen_height / perpWallDist)

            # Calculate lowest and highest pixel to fill in the current stripe
            drawStart = -lineHeight // 2 + self.screen_height // 2
            drawEnd = lineHeight // 2 + self.screen_height // 2
            drawStart = max(0, drawStart)
            drawEnd = min(self.screen_height - 1, drawEnd)

            # Choose wall color and adjust color based on side
            color = self.colors.get(self.world_map.get_cell(mapX, mapY), (255, 255, 0))
            if side == 1:
                color = tuple(c // 2 for c in color)  # Darken color for y-side walls

            # Draw the vertical line on screen
            pygame.draw.line(self.screen, color, (x, drawStart), (x, drawEnd))

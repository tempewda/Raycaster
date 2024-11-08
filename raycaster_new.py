import math
import pygame

class Raycaster:
    def __init__(self, screen, screen_width, screen_height, world_map, texture_manager):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_map = world_map
        self.texture_manager = texture_manager

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
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1
                if self.world_map.is_wall(mapX, mapY) > 0:
                    hit = 1

            # Calculate distance projected on camera direction
            perpWallDist = (sideDistX - deltaDistX) if side == 0 else (sideDistY - deltaDistY)
            lineHeight = int(self.screen_height / perpWallDist)
            drawStart = max(0, -lineHeight // 2 + self.screen_height // 2)
            drawEnd = min(self.screen_height - 1, lineHeight // 2 + self.screen_height // 2)

            # Determine texture and texture coordinates
            wall_type = self.world_map.get_cell(mapX, mapY)
            texture = self.texture_manager.get_texture(wall_type)

            # Calculate texture x-coordinate
            wallX = (player.pos_y + perpWallDist * rayDirY) if side == 0 else (player.pos_x + perpWallDist * rayDirX)
            wallX -= math.floor(wallX)
            texX = int(wallX * texture.get_width())
            if (side == 0 and rayDirX > 0) or (side == 1 and rayDirY < 0):
                texX = texture.get_width() - texX - 1

            # Draw each pixel in the column
            for y in range(drawStart, drawEnd):
                # Calculate corresponding y-coordinate on the texture
                texY = int(((y - drawStart) * texture.get_height()) / lineHeight)
                color = texture.get_at((texX, texY))
                if side == 1:
                    color = tuple(c // 2 for c in color)  # Darken the color for y-side walls
                self.screen.set_at((x, y), color)

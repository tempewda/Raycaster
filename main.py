import pygame
import math
import time

# Constants
screenWidth = 640
screenHeight = 480
mapWidth = 24
mapHeight = 24

# World map layout
worldMap = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Colors for walls
colors = {
    1: (255, 0, 0),    # Red
    2: (0, 255, 0),    # Green
    3: (0, 0, 255),    # Blue
    4: (255, 255, 255),# White
    5: (255, 255, 0),  # Yellow (default)
}

def main():
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Raycaster")

    # Initial player position and direction
    posX, posY = 22, 12
    dirX, dirY = -1, 0
    planeX, planeY = 0, 0.66

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Raycasting
        for x in range(screenWidth):
            cameraX = 2 * x / screenWidth - 1
            rayDirX = dirX + planeX * cameraX
            rayDirY = dirY + planeY * cameraX

            mapX, mapY = int(posX), int(posY)

            deltaDistX = abs(1 / rayDirX) if rayDirX != 0 else float('inf')
            deltaDistY = abs(1 / rayDirY) if rayDirY != 0 else float('inf')

            stepX = -1 if rayDirX < 0 else 1
            stepY = -1 if rayDirY < 0 else 1
            sideDistX = (posX - mapX) * deltaDistX if rayDirX < 0 else (mapX + 1.0 - posX) * deltaDistX
            sideDistY = (posY - mapY) * deltaDistY if rayDirY < 0 else (mapY + 1.0 - posY) * deltaDistY

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
                if worldMap[mapX][mapY] > 0: hit = 1

            perpWallDist = (sideDistX - deltaDistX) if side == 0 else (sideDistY - deltaDistY)
            lineHeight = int(screenHeight / perpWallDist)
            drawStart, drawEnd = -lineHeight // 2 + screenHeight // 2, lineHeight // 2 + screenHeight // 2
            drawStart, drawEnd = max(0, drawStart), min(screenHeight - 1, drawEnd)

            color = colors.get(worldMap[mapX][mapY], (255, 255, 0))
            if side == 1:
                color = tuple(c // 2 for c in color)

            pygame.draw.line(screen, color, (x, drawStart), (x, drawEnd))

        pygame.display.flip()
        
        # Player movement and rotation
        frameTime = clock.tick(60) / 1000.0
        moveSpeed, rotSpeed = frameTime * 5.0, frameTime * 3.0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if worldMap[int(posX + dirX * moveSpeed)][int(posY)] == 0: posX += dirX * moveSpeed
            if worldMap[int(posX)][int(posY + dirY * moveSpeed)] == 0: posY += dirY * moveSpeed
        if keys[pygame.K_DOWN]:
            if worldMap[int(posX - dirX * moveSpeed)][int(posY)] == 0: posX -= dirX * moveSpeed
            if worldMap[int(posX)][int(posY - dirY * moveSpeed)] == 0: posY -= dirY * moveSpeed
        if keys[pygame.K_RIGHT]:
            oldDirX = dirX
            dirX = dirX * math.cos(-rotSpeed) - dirY * math.sin(-rotSpeed)
            dirY = oldDirX * math.sin(-rotSpeed) + dirY * math.cos(-rotSpeed)
            oldPlaneX = planeX
            planeX = planeX * math.cos(-rotSpeed) - planeY * math.sin(-rotSpeed)
            planeY = oldPlaneX * math.sin(-rotSpeed) + planeY * math.cos(-rotSpeed)
        if keys[pygame.K_LEFT]:
            oldDirX = dirX
            dirX = dirX * math.cos(rotSpeed) - dirY * math.sin(rotSpeed)
            dirY = oldDirX * math.sin(rotSpeed) + dirY * math.cos(rotSpeed)
            oldPlaneX = planeX
            planeX = planeX * math.cos(rotSpeed) - planeY * math.sin(rotSpeed)
            planeY = oldPlaneX * math.sin(rotSpeed) + planeY * math.cos(rotSpeed)

    pygame.quit()

if __name__ == "__main__":
    main()

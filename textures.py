import pygame
import os

class TextureManager:
    def __init__(self, pics_folder="pics"):
        self.pics_folder = pics_folder
        self.textures = {}

    def load_textures(self):
        """Load textures from the 'pics' folder based on wall types."""
        # Map each wall type to a texture file name based on Lode Vandevenne's tutorial
        texture_files = {
            1: "wood.png", 
            2: "colorstone.png", 
            3: "redbrick.png", 
            4: "purplestone.png", 
            5: "eagle.png"  
        }
        
        # Load and resize each texture to 64x64 and store it in the textures dictionary
        for wall_type, file_name in texture_files.items():
            path = os.path.join(self.pics_folder, file_name)
            try:
                texture = pygame.image.load(path).convert()
                # Resize the texture to 64x64
                texture = pygame.transform.scale(texture, (64, 64))
                self.textures[wall_type] = texture
            except pygame.error as e:
                print(f"Error loading texture '{file_name}': {e}")

    def get_texture(self, wall_type):
        """Retrieve a texture based on wall type."""
        return self.textures.get(wall_type, None)  # Return None if texture not found

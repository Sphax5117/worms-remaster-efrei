import pygame
import csv
import os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, solid=False):
        """Create a tile with an image. Mark it as solid if needed."""
        super().__init__()
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((32, 32))  # Corrected size to 32x32
            self.image.fill((255, 0, 0))       # Red fallback for missing tiles

        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = solid  # Boolean to check collision

    def draw(self, surface):
        """Draw the tile on the surface."""
        surface.blit(self.image, self.rect.topleft)

class TileMap:
    def __init__(self, filename, tile_size=32):
        self.tile_size = tile_size
        self.tiles = pygame.sprite.Group()
        self.solid_tiles = pygame.sprite.Group()
        self.map_w, self.map_h = 0, 0
        self.start_x, self.start_y = 100, 100
        self.TILE_ASSETS = {
            '0': (None, False),
            '1': (os.path.join('assets', 'gameon', 'nature_env', 'tile27.png'), True),
            '2': (os.path.join('assets', 'gameon', 'nature_env', 'tile42.png'), False),
            'S': (None, False),
        }
        self.load_tiles(filename)

    def load_tiles(self, filename):
        """Load tiles from a CSV file and create tile objects."""
        map_data = self.read_csv(filename)
        self.map_w = len(map_data[0]) * self.tile_size if map_data else 0
        self.map_h = len(map_data) * self.tile_size

        for row in map_data:
            for tile_x, tile_id in enumerate(row):
                x = tile_x * self.tile_size
                y = row.index(tile_id) * self.tile_size

                if tile_id == 'S':
                    self.start_x = x
                    self.start_y = y
                elif tile_id in self.TILE_ASSETS:
                    image_path, is_solid = self.TILE_ASSETS[tile_id]
                    if image_path:
                        tile = Tile(image_path, x, y, is_solid)
                        self.tiles.add(tile)
                        if is_solid:
                            self.solid_tiles.add(tile)
                    elif tile_id == '0':
                        pass

    def read_csv(self, filename):
        """Load CSV file and return its contents as a list."""
        # Get the directory of the current script (tilemap.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the CSV file, assuming it's in a "maps" subdirectory
        csv_path = os.path.join(script_dir, 'maps', filename) # Assumes map.csv is in a folder named maps

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        with open(csv_path, 'r') as data:
            reader = csv.reader(data)
            return list(reader)

    def draw_map(self, surface):
        """Draw all tiles onto the given surface."""
        self.tiles.draw(surface)






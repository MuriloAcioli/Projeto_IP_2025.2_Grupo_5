import pygame as pg
# Configuração do tamanho do quadrado (Tile)
TILE_SIZE = 48 

# --- 2. Classe Obstáculo ---
class Obstaculo(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((15, 80, 15)) 
        pg.draw.rect(self.image, (0,0,0), (0,0,TILE_SIZE,TILE_SIZE), 2)
        self.rect = self.image.get_rect(topleft=(x, y))

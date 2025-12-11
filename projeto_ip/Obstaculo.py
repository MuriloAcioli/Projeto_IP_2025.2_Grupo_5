import pygame as pg
# Configuração do tamanho do quadrado (Tile)
TILE_SIZE = 48 

# O seu mapa desenhado com caracteres

# --- 2. Classe Obstáculo (Parede/Árvore) ---
class Obstaculo(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Aqui você carregaria a imagem da árvore: pg.image.load("assets/arvore.png")
        # Vou usar um quadrado verde escuro por enquanto
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((15, 80, 15)) # Verde Escuro
        # Opcional: Desenhar uma borda para parecer um bloco
        pg.draw.rect(self.image, (0,0,0), (0,0,TILE_SIZE,TILE_SIZE), 2)
        self.rect = self.image.get_rect(topleft=(x, y))
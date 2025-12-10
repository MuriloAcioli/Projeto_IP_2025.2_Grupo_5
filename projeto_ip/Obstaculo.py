import pygame as pg
from coletaveis import Pokebola
# Configuração do tamanho do quadrado (Tile)
TILE_SIZE = 32 

# O seu mapa desenhado com caracteres
MAPA_JOGO = [
    "TTTTTTTTTTTTTTTTTTTT",
    "T..................T",
    "T..P....BB.........T",
    "T.......TT.........T",
    "T.......TT...B.....T",
    "T..................T",
    "TTTTTTTTTTTTTTTTTTTT"
]

# Classe para paredes/árvores
class Obstaculo(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Aqui você carregaria a imagem da árvore: pg.image.load('arvore.png')
        # Vou usar um quadrado verde escuro por enquanto
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 100, 0)) 
        
        self.rect = self.image.get_rect(topleft=(x, y))
        


#
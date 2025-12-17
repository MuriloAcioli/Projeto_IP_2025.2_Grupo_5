import pygame as pg
import os 
import random

DIRETORIO_BASE = os.path.dirname(__file__)  # Caminho do diretório atual

# Configuração do tamanho do quadrado (Tile)
TILE_SIZE = 48 

# --- 2. Classe Obstáculo ---
class Obstaculo(pg.sprite.Sprite):
    def __init__(self, x, y, tamanho = (48,48)):
        super().__init__()
        
        # 1. Caminho Relativo (apenas a pasta e nome)
        caminho_relativo = "assets/obstaculos/arbusto.png" 
        
        # 2. Caminho Absoluto (Cola o diretório do script + caminho relativo)
        # Use vírgulas no join, é mais seguro que barras manuais
        caminho_completo = os.path.join(DIRETORIO_BASE, "assets", "obstaculos", "arbusto.png")

        try:
            # 3. Carrega usando o CAMINHO COMPLETO calculado acima
            imagem_carregada = pg.image.load(caminho_completo).convert_alpha()
            
            # Recorte (se necessário)
            random_int = random.randint(0, 1) 
            rect_certo = pg.Rect(0, random_int*64, 64, 64) 
            imagem_cortada = imagem_carregada.subsurface(rect_certo)
            
            # Escala
            self.image = pg.transform.scale(imagem_cortada, tamanho)
            
        except Exception as e:
            print(f"ERRO: Não achei a imagem em: {caminho_completo}")
            print(f"Detalhe do erro: {e}")
            
            # Cria um quadrado verde feio para o jogo não fechar
            self.image = pg.Surface(tamanho)
            self.image.fill((15, 80, 15)) 
            pg.draw.rect(self.image, (0,0,0), (0,0,tamanho[0],tamanho[1]), 2)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()
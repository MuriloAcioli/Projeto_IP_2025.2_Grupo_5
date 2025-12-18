import pygame as pg
import os

DIRETORIO_BASE = os.path.dirname(__file__)  # Caminho do diretório atual

class Mato(pg.sprite.Sprite):
    def __init__(self, x, y, imagem_path= r"assets\backgrounds\tileset.png", cor_padrao=(255, 255, 0), tamanho=(48, 48)):
        super().__init__()
        if imagem_path:
            # Tenta carregar, se der erro cria um quadrado (fallback)
            try:
                 # Carrega a imagem original (o tileset completo)
                imagem_path = os.path.join(DIRETORIO_BASE, imagem_path)
                imagem_bruta = pg.image.load(imagem_path).convert_alpha()
                
                # 1. Definir qual pedaço do tileset queremos pegar
                rect_certo = pg.Rect(64*1, 64*2, 64, 64)

                # 2. Criar uma sub-imagem (cortar apenas o quadrado do tileset)
                imagem_cortada = imagem_bruta.subsurface(rect_certo)

                # 3. Agora sim, escalar esse pedaço cortado para o tamanho desejado
                self.image = pg.transform.scale(imagem_cortada, tamanho)
                
            except FileNotFoundError:
                print(f"Erro: Imagem {imagem_path} não achada. Usando quadrado.")
                self.image = pg.Surface(tamanho) # Usa o tamanho definido
                self.image.fill(cor_padrao)
        else:
            self.image = pg.Surface(tamanho) # Usa o tamanho definido
            self.image.fill(cor_padrao)
            
        self.rect = self.image.get_rect(topleft=(x, y))

import pygame as pg
import os

DIRETORIO_BASE = os.path.dirname(__file__)  # Caminho do diretório atual

class Coletavel(pg.sprite.Sprite):
    def __init__(self, x, y, imagem_path=None, cor_padrao=(255, 255, 0), tamanho=(24, 24)):
        super().__init__()
        
        if imagem_path:
            # Tenta carregar, se der erro cria um quadrado (fallback)
            try:
                # Carrega a imagem original
                imagem_path = os.path.join(DIRETORIO_BASE, imagem_path)

                imagem_bruta = pg.image.load(imagem_path).convert_alpha()

                self.image = pg.transform.scale(imagem_bruta, tamanho)
                
            except FileNotFoundError:
                print(f"Erro: Imagem {imagem_path} não achada. Usando quadrado.")
                self.image = pg.Surface(tamanho) # Usa o tamanho definido
                self.image.fill(cor_padrao)
        else:
            self.image = pg.Surface(tamanho) # Usa o tamanho definido
            self.image.fill(cor_padrao)
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()
        self.nome_item = "item_desconhecido"
        self.quantidade = 1

    def coletar(self, player):
        print(f"-> Player pegou: {self.nome_item}")
        
        if self.nome_item in player.inventario:
            player.inventario[self.nome_item] += self.quantidade
        else:
            player.inventario[self.nome_item] = self.quantidade
            
        self.kill()

class Pokebola(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/coletaveis/pokeloot_.png", cor_padrao=(200, 0, 0))
        self.nome_item = "Pokebola"
        
    def coletar(self, player):
        super().coletar(player)

class GreatBall(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/coletaveis/pokeloot_.png", cor_padrao=(0, 0, 200))
        self.nome_item = "Grande Bola"
        
    def coletar(self, player):
        super().coletar(player)

class Ultraball(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/coletaveis/pokeloot_.png", cor_padrao=(0, 0, 200))
        self.nome_item = "Ultra Bola"
        
    def coletar(self, player):
        super().coletar(player)

class Pocao(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/coletaveis/pokeloot_.png", cor_padrao=(0, 0, 200))
        self.nome_item = "Poção de Vida"

class Insignia(Coletavel):
    def __init__(self, x, y):
        # Por enquanto usa um sprite temporário (cor dourada)
        super().__init__(x, y, "assets/coletaveis/pokeloot_.png", cor_padrao=(255, 215, 0))
        self.nome_item = "Insígnia do Professor"
        
    def coletar(self, player):
        super().coletar(player)
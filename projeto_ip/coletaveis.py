import pygame as pg
import os

DIRETORIO_BASE = os.path.dirname(__file__)  # Caminho do diretório atual

class Coletavel(pg.sprite.Sprite):
    # ALTERAÇÃO 1: Adicionei o argumento 'tamanho' com um valor padrão (32, 32)
    def __init__(self, x, y, imagem_path=None, cor_padrao=(255, 255, 0), tamanho=(32, 32)):
        super().__init__()
        
        if imagem_path:
            # Tenta carregar, se der erro cria um quadrado (fallback)
            try:
                # Carrega a imagem original
                imagem_path = os.path.join(DIRETORIO_BASE, imagem_path)

                imagem_bruta = pg.image.load(imagem_path).convert_alpha()
                
                # ALTERAÇÃO 2: Aqui nós forçamos a imagem a ficar do tamanho padrão
                self.image = pg.transform.scale(imagem_bruta, tamanho)
                
            except FileNotFoundError:
                print(f"Erro: Imagem {imagem_path} não achada. Usando quadrado.")
                self.image = pg.Surface(tamanho) # Usa o tamanho definido
                self.image.fill(cor_padrao)
        else:
            self.image = pg.Surface(tamanho) # Usa o tamanho definido
            self.image.fill(cor_padrao)
            
        self.rect = self.image.get_rect(topleft=(x, y))
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
        # Se quiser que a pokebola seja um pouco maior, você pode passar o tamanho aqui
        # Exemplo: tamanho=(40, 40). Se não passar nada, usa o padrão (32, 32) da mãe.
        super().__init__(x, y, "assets/coletaveis/pokebola2.png", cor_padrao=(200, 0, 0))
        self.nome_item = "Pokebola"
        
    def coletar(self, player):
        # pg.mixer.Sound("assets/sons/pegar.wav").play()
        super().coletar(player)

class GreatBall(Coletavel):
    def __init__(self, x, y):
        # Se quiser que a pokebola seja um pouco maior, você pode passar o tamanho aqui
        # Exemplo: tamanho=(40, 40). Se não passar nada, usa o padrão (32, 32) da mãe.
        super().__init__(x, y, "assets/coletaveis/greatball.png", cor_padrao=(0, 0, 200))
        self.nome_item = "Grande Bola"
        
    def coletar(self, player):
        # pg.mixer.Sound("assets/sons/pegar.wav").play()
        super().coletar(player)

class Pocao(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/coletaveis/pocao.png", cor_padrao=(0, 0, 200))
        self.nome_item = "Pocao de Vida"
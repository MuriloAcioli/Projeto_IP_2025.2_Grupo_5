import pygame as pg

class Pokemon(pg.sprite.Sprite):
    def __init__(self, vida=100, ataque=10, defesa=5, velocidade=5):
        super().__init__()
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.velocidade = velocidade



class Pikachu(Pokemon):
    def __init__(self):
        super().__init__(vida=120, ataque=15, defesa=8)
        self.nome = "Pikachu"
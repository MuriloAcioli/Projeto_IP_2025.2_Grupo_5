import pygame as pg
import os
from pokedex import POKEDEX
from ataques import GOLPES_DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
#       CLASSES DO SISTEMA
# =============================================================================

class Golpe:
    def __init__(self, nome, poder, tipo, precisao=100):
        self.nome = nome
        self.poder = poder
        self.tipo = tipo
        self.precisao = precisao

class Pokemon:
    def __init__(self, id_dex, nome, nivel, tipo, base_stats, sprite_path, sprite_back_path, golpes=[]):
        self.id = id_dex
        self.nome = nome
        self.nivel = nivel
        self.tipo = tipo
        
        # Stats Base
        self.base_hp, self.base_atk, self.base_def, self.base_spd = base_stats
        
        # Sistema de XP
        self.xp_atual = 0
        self.xp_prox_nivel = self.nivel * 25
        
        self.golpes = golpes 

        # Tamanho base do SPRITE base

        self.TAMANHO_SPRITE = (280, 280) 
        
        # Carregando os sprites
        
        # 1. Frente (Inimigo usa esse)
        full_path = os.path.join(BASE_DIR, sprite_path)
        try:
            self.image = pg.image.load(full_path).convert_alpha()
            # Escala a imagem
            self.image = pg.transform.scale(self.image, self.TAMANHO_SPRITE)
        except Exception:
            # Fallback se não achar imagem
            self.image = pg.Surface((200, 200))
            self.image.fill((100, 100, 100))

        # 2. Costas (Jogador usa esse)
        full_back_path = os.path.join(BASE_DIR, sprite_back_path)
        try:
            self.back_image = pg.image.load(full_back_path).convert_alpha()
            # Escala a imagem de costas também
            self.back_image = pg.transform.scale(self.back_image, self.TAMANHO_SPRITE)
        except Exception:
            # Se não achar a de costas, usa a de frente (já escalada)
            self.back_image = self.image 

        # Calcula Stats Iniciais
        self.calcular_stats()
        self.hp_atual = self.hp_max

    def calcular_stats(self):
        """Recalcula status baseado no nível""" # Ele vai recalcular sempre que upa de nível e/ou é criado basicamente
        self.hp_max = int(((self.base_hp + 50) * self.nivel) / 50) + 10
        self.atk = int((self.base_atk * self.nivel) / 50) + 5
        self.defense = int((self.base_def * self.nivel) / 50) + 5
        self.speed = int((self.base_spd * self.nivel) / 50) + 5

    def receber_dano(self, dano): 
        self.hp_atual -= dano
        if self.hp_atual < 0: self.hp_atual = 0
        
    def esta_vivo(self):
        return self.hp_atual > 0

    # Lógica para upar o nível
    def ganhar_xp(self, quantidade):
        self.xp_atual += quantidade
        subiu = False
        while self.xp_atual >= self.xp_prox_nivel:
            self.xp_atual -= self.xp_prox_nivel
            self.subir_nivel()
            subiu = True
        return subiu

    def subir_nivel(self):
        self.nivel += 1
        self.xp_prox_nivel = self.nivel * 50
        
        # Recalcula e cura o aumento de HP
        antigo_hp = self.hp_max
        self.calcular_stats()
        self.hp_atual += (self.hp_max - antigo_hp)

# =============================================================================
#  Função de instanciação dos pokemons
# =============================================================================

def criar_pokemon(nome_especie, nivel):
    if nome_especie not in POKEDEX:
        return None

    data = POKEDEX[nome_especie]
    
    lista_golpes_objs = []
    for nome_golpe in data['golpes']:
        if nome_golpe in GOLPES_DB:
            g = GOLPES_DB[nome_golpe]
            lista_golpes_objs.append(Golpe(nome_golpe, g["poder"], g["tipo"], g["precisao"]))
    
    novo_pkmn = Pokemon( # Para entender melhor, leia o arquivo pokedex.py, basicamente, ele acessa os dados do pokemon, usando a chave nome_especie, e usa os dados base da espécie, que é tudo menos o nível, que é momentâneo.
        id_dex=data['id'],
        nome=nome_especie,
        nivel=nivel,
        tipo=data['tipo'],
        base_stats=data['stats'],
        sprite_path=data['sprite'],
        sprite_back_path=data['sprite_back'], 
        golpes=lista_golpes_objs,
    )
    
    return novo_pkmn
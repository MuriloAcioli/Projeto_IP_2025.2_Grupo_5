import pygame as pg
import os

# Define o diretório base para carregar sprites corretamente (evita erro de caminho)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# 1. BANCO DE DADOS (DB)
# Aqui ficam as constantes e configurações de balanceamento.
# =============================================================================

# --- GOLPES ---
GOLPES_DB = {
    "Investida": {"poder": 40, "tipo": "Normal", "precisao": 100},
    "Brasas":    {"poder": 40, "tipo": "Fogo",   "precisao": 100},
    "Chicote":   {"poder": 45, "tipo": "Grama",  "precisao": 100},
    "Bolhas":    {"poder": 40, "tipo": "Agua",   "precisao": 100},
    "Arranhao":  {"poder": 40, "tipo": "Normal", "precisao": 100},
}

# --- POKÉDEX ---
# Estrutura: ID, Tipo, (HP, Atk, Def, Spd), Sprite, [Golpes Iniciais]
POKEDEX = {
    "Charmander": {
        "id": 4, 
        "tipo": "Fogo", 
        "stats": (39, 52, 43, 65),
        "sprite": "assets/pokemons/charmander.png",
        "sprite_back": "assets/pokemons/charmander_back.png",
        "golpes": ["Brasas", "Investida"]
    },
    "Squirtle": {
        "id": 7, 
        "tipo": "Agua", 
        "stats": (44, 48, 65, 43),
        "sprite": "assets/pokemons/squirtle.png",
        "sprite_back": "assets/pokemons/squirtle_back.png",
        "golpes": ["Bolhas", "Investida"]
    },
    "Bulbasaur": {
        "id": 1, 
        "tipo": "Grama", 
        "stats": (45, 49, 49, 45),
        "sprite": "assets/pokemons/bulbasaur.png",
        "sprite_back": "assets/pokemons/bulbasaur_back.png",
        "golpes": ["Chicote", "Investida"]
    }
}

# =============================================================================
# 2. CLASSES DO SISTEMA
# =============================================================================

class Golpe:
    def __init__(self, nome, poder, tipo, precisao=100):
        self.nome = nome
        self.poder = poder
        self.tipo = tipo
        self.precisao = precisao

class Pokemon:
    def __init__(self, id_dex, nome, nivel, tipo, base_stats, sprite_path,sprite_back_path, golpes=[]):
        self.id = id_dex
        self.nome = nome
        self.nivel = nivel
        self.tipo = tipo
        
        # Desempacota os Stats Base
        self.base_hp, self.base_atk, self.base_def, self.base_spd = base_stats
        
        # --- CÁLCULO DE STATS REAIS (Nível) ---
        self.hp_max = int(((self.base_hp + 50) * self.nivel) / 50) + 10
        self.hp_atual = self.hp_max
        self.atk = int((self.base_atk * self.nivel) / 50) + 5
        self.defense = int((self.base_def * self.nivel) / 50) + 5
        self.speed = int((self.base_spd * self.nivel) / 50) + 5
        
        # Lista de golpes (Objetos da classe Golpe)
        self.golpes = golpes 
        
        # --- CARREGAMENTO DE SPRITE (Seguro) ---
        full_path = os.path.join(BASE_DIR, sprite_path)
        
        try:
            self.image = pg.image.load(full_path).convert_alpha()
            self.image = pg.transform.scale(self.image, (200, 200))
        except Exception as e:
            # Se der erro (arquivo não existe), cria um quadrado colorido
            self.image = pg.Surface((200, 200))
            if self.tipo == "Fogo": 
                self.image.fill((200, 50, 0))
            elif self.tipo == "Agua": 
                self.image.fill((0, 50, 200))
            elif self.tipo == "Grama": 
                self.image.fill((0, 200, 50))
            else: 
                self.image.fill((100, 100, 100))
        full_back_path = os.path.join(BASE_DIR, sprite_back_path)
        self.back_image = pg.image.load(full_back_path).convert_alpha()
        #checar exceções
    def receber_dano(self, dano):
        self.hp_atual -= dano
        if self.hp_atual < 0: 
            self.hp_atual = 0
        
    def esta_vivo(self):
        return self.hp_atual > 0

# =============================================================================
# 3. FÁBRICA (FACTORY)
# =============================================================================

def criar_pokemon(nome_especie, nivel):
    """Cria uma instância de Pokemon montando os dados da Pokedex + Golpes"""
    
    # Verifica se existe na "base de dados"
    if nome_especie not in POKEDEX:
        print(f"ERRO: Pokémon {nome_especie} não existe na POKEDEX.")
        return None

    data = POKEDEX[nome_especie]
    
    # 1. Transforma nomes de golpes em Objetos Golpe reais
    lista_golpes_objs = []
    for nome_golpe in data['golpes']:
        if nome_golpe in GOLPES_DB:
            dados_g = GOLPES_DB[nome_golpe]
            novo_golpe = Golpe(nome_golpe, dados_g["poder"], dados_g["tipo"], dados_g["precisao"])
            lista_golpes_objs.append(novo_golpe)
    
    # 2. Instancia o Pokémon
    novo_pkmn = Pokemon(
        id_dex=data['id'],
        nome=nome_especie,
        nivel=nivel,
        tipo=data['tipo'],
        base_stats=data['stats'],
        sprite_path=data['sprite'],
        sprite_back_path=data['sprite_back'],
        golpes=lista_golpes_objs
    )
    
    return novo_pkmn
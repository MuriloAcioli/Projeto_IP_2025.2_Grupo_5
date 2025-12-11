import pygame as pg
from player import Player
from camera import Camera
from coletaveis import Pokebola, GreatBall, Pocao
from inventario import MenuInventario
# --- IMPORTANDO A BATALHA ---
from batalha import BatalhaPokemon, Pokemon, Golpe 
import os

DIRETORIO_BASE = os.path.dirname(__file__)

# --- Configurações Globais ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48 
FPS = 60

# --- ESTADOS DO JOGO ---
ESTADO_MAPA = 0
ESTADO_BATALHA = 1
estado_atual = ESTADO_MAPA 

# --- 1. DEFINIÇÃO DO MAPA ---
MAPA_MATRIZ = [
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', 'P', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'G', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'M', 'T', 'T', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', 'P', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'G', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
]

# --- 2. Classe Obstáculo ---
class Obstaculo(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((15, 80, 15)) 
        pg.draw.rect(self.image, (0,0,0), (0,0,TILE_SIZE,TILE_SIZE), 2)
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Função Carregar Mapa ---
def carregar_mapa(mapa, grupo_obs, grupo_col):
    pos_player = (100, 100)
    
    for row_index, row in enumerate(mapa):
        for col_index, letra in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            if letra == 'T':
                grupo_obs.add(Obstaculo(x, y))
            elif letra == 'B':
                grupo_col.add(Pokebola(x, y))
            elif letra == 'G':
                grupo_col.add(GreatBall(x, y))
            elif letra == 'H':
                grupo_col.add(Pocao(x, y))
            elif letra == 'P':
                pos_player = (x, y)
                
    largura_total = len(mapa[0]) * TILE_SIZE
    altura_total = len(mapa) * TILE_SIZE
    return largura_total, altura_total, pos_player

# --- INICIALIZAÇÃO PYGAME ---
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("PokeCIn - Batalha Integrada")
clock = pg.time.Clock()

# Grupos
grupo_obstaculos = pg.sprite.Group()
grupo_coletaveis = pg.sprite.Group()

# Carregando Mapa
map_w, map_h, player_pos = carregar_mapa(MAPA_MATRIZ, grupo_obstaculos, grupo_coletaveis)

# Player
try:
    path_down = os.path.join(DIRETORIO_BASE, "assets/mc/mc_down.png")
    path_left = os.path.join(DIRETORIO_BASE, "assets/mc/mc_left.png")
    path_up = os.path.join(DIRETORIO_BASE, "assets/mc/mc_up.png")
    path_right = os.path.join(DIRETORIO_BASE, "assets/mc/mc_right.png")
    protagonista = Player(player_pos[0], player_pos[1], path_down, path_left, path_up, path_right)
    player_group = pg.sprite.GroupSingle(protagonista)
except FileNotFoundError:
    print("ERRO: Imagens do player não encontradas.")
    print(f"Verifique se as imagens estão na pasta: {os.path.join(DIRETORIO_BASE, 'assets/mc/')}")
    exit()

menu_inv = MenuInventario()
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, map_w, map_h)

# Fundo do Mapa
fundo_grama = pg.Surface((map_w, map_h))
fundo_grama.fill((34, 139, 34)) 

# --- SETUP DA BATALHA (Dados de Teste) ---
# Criando golpes
golpe_investida = Golpe("Investida", 40, "Normal")
golpe_chamas = Golpe("Brasas", 40, "Fogo")

# Criando Pokémons
meu_poke_base = Pokemon("Charizard", 10, "Fogo", 100, 25, 20, 30, [golpe_chamas])
inimigo_poke_base = Pokemon("Bulbasaur", 8, "Grama", 80, 20, 20, 25, [golpe_investida])

batalha_atual = None

# --- LOOP PRINCIPAL ---
running = True
while running:
    # --- 1. EVENTOS ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        # --- EVENTOS: NO MAPA ---
        if estado_atual == ESTADO_MAPA:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    menu_inv.alternar() 
                
                # [TESTE] Pressione 'B' para iniciar batalha
                if event.key == pg.K_b:
                    estado_atual = ESTADO_BATALHA
                    inimigo_poke_base.hp_atual = inimigo_poke_base.hp_max 
                    batalha_atual = BatalhaPokemon(meu_poke_base, inimigo_poke_base, protagonista.inventario)

        # --- EVENTOS: NA BATALHA ---
        elif estado_atual == ESTADO_BATALHA:
            if event.type == pg.KEYDOWN:
                # 1 = Lutar
                if event.key == pg.K_1:
                    batalha_atual.turno_lutar(0)
                
                # 2 = Item
                elif event.key == pg.K_2:
                    batalha_atual.turno_usar_item("Poção")
                
                # 3 = Fugir
                elif event.key == pg.K_3:
                    if batalha_atual.turno_fugir():
                        estado_atual = ESTADO_MAPA

            if batalha_atual and batalha_atual.battle_over:
                pg.time.delay(1000)
                estado_atual = ESTADO_MAPA

    # --- 2. ATUALIZAÇÃO ---
    if estado_atual == ESTADO_MAPA:
        antigo_rect = protagonista.rect.copy()
        player_group.update()
        
        if pg.sprite.spritecollide(protagonista, grupo_obstaculos, False):
            protagonista.rect = antigo_rect

        camera.update(protagonista.rect)

        hits = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False)
        for item in hits:
            item.coletar(protagonista)

    # --- 3. DESENHO ---
    if estado_atual == ESTADO_MAPA:
        screen.fill((0,0,0)) 
        screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))
        
        for parede in grupo_obstaculos:
            screen.blit(parede.image, camera.apply(parede.rect))

        for item in grupo_coletaveis:
            screen.blit(item.image, camera.apply(item.rect))

        for sprite in player_group:
            screen.blit(sprite.image, camera.apply(sprite.rect))
            
        menu_inv.desenhar(screen, protagonista.inventario)
        
        # Dica na tela
        font_debug = pg.font.SysFont(None, 24)
        debug_text = font_debug.render("Aperte 'B' para Batalhar", True, (255, 255, 255))
        screen.blit(debug_text, (10, 10))

    elif estado_atual == ESTADO_BATALHA:
        if batalha_atual:
            batalha_atual.desenhar(screen)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
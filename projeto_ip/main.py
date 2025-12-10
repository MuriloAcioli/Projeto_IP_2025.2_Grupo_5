import pygame as pg
from player import Player
from camera import Camera
from coletaveis import Pokebola, GreatBall, Pocao
from inventario import MenuInventario
import os

DIRETORIO_BASE = os.path.dirname(__file__)  # Caminho do diretório atual
# --- Configurações Globais ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48 # Tamanho de cada quadrado do mapa (64x64)
FPS = 60

# --- 1. DEFINIÇÃO DO MAPA (Visualize sua fase aqui!) ---
# P = Player (Onde começa)
# T = Tree/Tronco (Obstáculo)
# B = Pokebola
# G = GreatBall
# H = Health Potion (Poção)
# . = Grama (Chão livre)

MAPA_TEXTO = [
    "TTTTTTTTTTTTTTTTTTTTTTTTT",
    "T...........T...........T",
    "T..P........T...B.......T",
    "T...........T...........T",
    "TTTTTT......T...........T",
    "T...........TTTTTT..G...T",
    "T...B...................T",
    "T...........H...........T",
    "T.......TTTMTTMM........T",
    "T...........T...........T",
    "T...........T...........T",
    "T..P........T...B.......T",
    "T...........T...........T",
    "TTTTTT......T...........T",
    "T...........TTTTTT..G...T",
    "T...B...................T",
    "T...........H...........T",
    "T.......TTTTTTTT........T",
    "T...........T...........T",
    "TTTTTTTTTTTTTTTTTTTTTTTTT",

    # aumentar complexidade dos tilesets
    
]

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

# --- Função para Ler o Mapa ---
def carregar_mapa(mapa, grupo_obs, grupo_col):
    pos_player = (100, 100) # Valor padrão caso não tenha 'P'
    
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
            
                
    # Retorna o tamanho total do mapa e a posição inicial do player
    largura_total = len(mapa[0]) * TILE_SIZE
    altura_total = len(mapa) * TILE_SIZE
    return largura_total, altura_total, pos_player

# --- INICIALIZAÇÃO ---
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("PokeCIn - Fim do Mangue Vermelho")
clock = pg.time.Clock()

# Grupos
grupo_obstaculos = pg.sprite.Group()
grupo_coletaveis = pg.sprite.Group()

# 3. Carregando o Mapa
map_w, map_h, player_pos = carregar_mapa(MAPA_TEXTO, grupo_obstaculos, grupo_coletaveis)

# 4. Player (Usando a posição que veio do mapa 'P')
try:
    path_down = os.path.join(DIRETORIO_BASE, "assets/mc/mc_down.png")
    path_left = os.path.join(DIRETORIO_BASE, "assets/mc/mc_left.png")
    path_up = os.path.join(DIRETORIO_BASE, "assets/mc/mc_up.png")
    path_right = os.path.join(DIRETORIO_BASE, "assets/mc/mc_right.png")
    protagonista = Player(player_pos[0], player_pos[1], 
                          path_down, 
                          path_left, 
                          path_up, 
                          path_right)
    
    player_group = pg.sprite.GroupSingle(protagonista)
except FileNotFoundError:
    print("ERRO: Imagens do player não encontradas.")
    exit()

# Inventário
menu_inv = MenuInventario()

# 5. Câmera (Com o tamanho calculado do mapa)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, map_w, map_h)

# Fundo Básico (Chão de grama para preencher os espaços '.')
fundo_grama = pg.Surface((map_w, map_h))
fundo_grama.fill((34, 139, 34)) # Verde Grama

running = True
while running:
    # --- EVENTOS ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                menu_inv.alternar() 

    # --- ATUALIZAÇÃO ---
    
    # Salva a posição antiga antes de mover (para colisão)
    antigo_rect = protagonista.rect.copy()
    
    player_group.update()
    
    # Colisão com Árvores/Paredes
    # Se bater, volta para a posição antiga
    if pg.sprite.spritecollide(protagonista, grupo_obstaculos, False):
        protagonista.rect = antigo_rect

    # Atualiza câmera
    camera.update(protagonista.rect)

    # Coletar Itens
    hits = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False)
    for item in hits:
        item.coletar(protagonista)

    # --- DESENHO ---
    screen.fill((0,0,0)) 

    # 1. Desenha o Fundo (Grama)
    screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))

    # 2. Desenha as Árvores (Obstáculos)
    for parede in grupo_obstaculos:
        screen.blit(parede.image, camera.apply(parede.rect))

    # 3. Desenha os Coletáveis
    for item in grupo_coletaveis:
        screen.blit(item.image, camera.apply(item.rect))

    # 4. Desenha o Player
    for sprite in player_group:
        screen.blit(sprite.image, camera.apply(sprite.rect))
        
    # 5. Interface (Inventário) - Sempre por último e sem câmera
    menu_inv.desenhar(screen, protagonista.inventario)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()


"""

"""
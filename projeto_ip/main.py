import pygame as pg
import random
import os
# --- Imports ---
from player import Player
from camera import Camera
from coletaveis import Pokebola, GreatBall, Pocao
from inventario import MenuInventario
from Obstaculo import Obstaculo
import os # Importante para garantir caminhos de arquivo
import random
from mato import Mato
# IMPORTANTE: Importamos a função de criar agora!
from pokemon import Pokemon, criar_pokemon 
from batalha import BatalhaPokemon
# 1. NOVO IMPORT: Importa as funções de intro
from intro import definir_piso, exibir_intro, cena_professor, animacao_transicao

# --- Configurações Gerais ---
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48 
FPS = 60

# --- MAPA ---
MAPA_MATRIZ = [
     ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', 'P', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', 'T', 'T', 'T', 'T', 'T', '.', 'M', 'M', 'M', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'G', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', 'B', '.', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', 'B', '.', '.', '.', 'T', 'T', 'T', 'M', 'T', 'T', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', 'G', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'M', 'T', 'T', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', 'P', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', 'P', '.', '.', '.', '.', '.', 'M', '.', '.', 'T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'G', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
     ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']
]


# --- Função para Ler o Mapa ---
def carregar_mapa(mapa, grupo_obs, grupo_col, grupo_mato):
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
            elif letra == 'M':
                grupo_mato.add(Mato(x, y)) 
            elif letra == 'P':
                pos_player = (x, y)
                
    largura_total = len(mapa[0]) * TILE_SIZE
    altura_total = len(mapa) * TILE_SIZE
    return largura_total, altura_total, pos_player


# =============================================================================
# --- SETUP INICIAL ---
# =============================================================================
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("PokeCIn - Fim do Mangue Vermelho")
clock = pg.time.Clock() # A variável clock precisa existir antes de chamar as funções de intro

# Inicializa Grupos
grupo_obstaculos = pg.sprite.Group()
grupo_coletaveis = pg.sprite.Group()
grupo_mato = pg.sprite.Group()

# 3. Carregando o Mapa
map_w, map_h, player_pos = carregar_mapa(MAPA_MATRIZ, grupo_obstaculos, grupo_coletaveis,grupo_mato)
# Carrega Mapa
map_w, map_h, player_pos = carregar_mapa(MAPA_MATRIZ, grupo_obstaculos, grupo_coletaveis, grupo_mato)

# Inicializa Player
try:
    protagonista = Player(player_pos[0], player_pos[1], os.path.join(DIRETORIO_BASE, "assets/mc/mc_down.png"), os.path.join(DIRETORIO_BASE, "assets/mc/mc_left.png"), os.path.join(DIRETORIO_BASE, "assets/mc/mc_up.png"), os.path.join(DIRETORIO_BASE, "assets/mc/mc_right.png"))
    player_group = pg.sprite.GroupSingle(protagonista)
except FileNotFoundError: 
    print("ERRO: Imagens do player não encontradas.")
    exit()

# Inicializa Sistemas
menu_inv = MenuInventario()
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, map_w, map_h)

# Caminho para a imagem que você mandou (salve ela na pasta assets!)
caminho_img_tileset = os.path.join(DIRETORIO_BASE, "assets/backgrounds/tileset.png")

# Gera o chão texturizado (Chama a função importada)
fundo_grama = definir_piso(map_w, map_h, caminho_img_tileset)

# --- EQUIPE INICIAL ---
charmander = criar_pokemon("Charmander", 5)
squirtle = criar_pokemon("Squirtle", 5)
equipe_jogador = [charmander, squirtle] 

# =============================================================================
# --- FLUXO PRINCIPAL DO JOGO ---
# =============================================================================
# 3. Chamadas de função atualizadas
jogo_ativo = exibir_intro(screen, clock) 
nome_jogador = "Player"

# Roda a cena do professor se passou da intro
if jogo_ativo:
    jogo_ativo, nome_escolhido = cena_professor(screen, clock) # 3. Chamadas de função atualizadas
    if nome_escolhido:
        nome_jogador = nome_escolhido
        print(f"Bem-vindo ao mangue, {nome_jogador}!") 
        
        # Toca a musica do mapa se tudo der certo
        if jogo_ativo:
            try: 
                pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3"))
                pg.mixer.music.set_volume(0.2)
                pg.mixer.music.play(-1, fade_ms=2000)
            except: pass

# --- LOOP DO JOGO ---
estado_jogo = "MUNDO"
sistema_batalha = None
running = jogo_ativo 

while running:
    # --- MODO MUNDO (Exploração) ---
    if estado_jogo == "MUNDO":
        # 1. Eventos
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e: 
                    menu_inv.alternar() 

        # 2. Updates (Movimento e Física)
        antigo_rect = protagonista.rect.copy()
        player_group.update()
        
        # 3. Checagem de Batalha (Lógica do Mato)
        if protagonista.direction.magnitude() > 0:
            if pg.sprite.spritecollide(protagonista, grupo_mato, False):
                if random.random() < 0.015: 
                    # Animação (Chama a função importada)
                    animacao_transicao(screen)
                    estado_jogo = "BATALHA"
                    
                    # Cria Inimigo
                    inimigo_pokemon = criar_pokemon("Bulbasaur", random.randint(3, 5))
                    
                    # === PREPARAÇÃO DO INVENTÁRIO (Segurança contra Crash) ===
                    inv_batalha = {'Pocao': 5, 'Pokebola': 5}
                    try:
                        if hasattr(menu_inv, 'itens'): 
                            inv_batalha = menu_inv.itens
                        elif hasattr(protagonista, 'inventario') and hasattr(protagonista.inventario, 'itens'):
                            inv_batalha = protagonista.inventario.itens
                    except: 
                        pass

                    # Inicia Batalha
                    try:
                        sistema_batalha = BatalhaPokemon(equipe_jogador, inimigo_pokemon, inv_batalha)
                    except Exception as e:
                        print(f"ERRO AO INICIAR BATALHA: {e}")
                        estado_jogo = "MUNDO"

        # 4. Colisões e Câmera
        # Se bater na parede, volta para a posição antiga
        if pg.sprite.spritecollide(protagonista, grupo_obstaculos, False):
            protagonista.rect = antigo_rect
        
        # Atualiza a câmera para seguir o player
        camera.update(protagonista.rect)
        
        # Coleta itens
        hits = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False)
        for item in hits:
            item.coletar(protagonista)

        # 5. Desenho (Draw)
        screen.fill((0,0,0)) 
        screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))

        for item in grupo_mato: 
            screen.blit(item.image, camera.apply(item.rect))
        for parede in grupo_obstaculos: 
            screen.blit(parede.image, camera.apply(parede.rect))
        for item in grupo_coletaveis: 
            screen.blit(item.image, camera.apply(item.rect))
        for sprite in player_group: 
            screen.blit(sprite.image, camera.apply(sprite.rect))
        
        menu_inv.desenhar(screen, protagonista.inventario)

    # --- MODO BATALHA ---
    elif estado_jogo == "BATALHA":
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                running = False
            
            # Input da Batalha
            if event.type == pg.KEYDOWN:
                if sistema_batalha and sistema_batalha.battle_over:
                    if event.key == pg.K_SPACE:
                        if sistema_batalha.vencedor == "INIMIGO":
                            print("GAME OVER")
                            running = False
                        else:
                            estado_jogo = "MUNDO"
                            try: 
                                pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3"))
                                pg.mixer.music.play(-1)
                            except: 
                                pass
                else:
                    if sistema_batalha: 
                        sistema_batalha.processar_input(event)

        if sistema_batalha: 
            sistema_batalha.desenhar(screen)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
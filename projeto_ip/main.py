import pygame as pg
import random
import os

# --- Módulos do Jogo ---
from player import Player
from camera import Camera
from coletaveis import Pokebola, GreatBall, Pocao
from inventario import MenuInventario
from Obstaculo import Obstaculo
from mato import Mato
from pokemon import Pokemon, criar_pokemon 
from batalha import BatalhaPokemon
from npc import NPC

# --- Módulo de Intro ---
from intro import definir_piso, exibir_intro, cena_professor, animacao_transicao

# =============================================================================
# CONFIGURAÇÕES GERAIS
# =============================================================================
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48 
FPS = 60

# =============================================================================
# DADOS DO MAPA
# =============================================================================
MAPA_MATRIZ = [
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'N', '.', 'T'],
    ['T', '.', 'P', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', 'M', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', 'M', 'M', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'G', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'B', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'M', 'T', 'T', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'G', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', 'T', 'T', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', 'T', 'T', '.', '.', 'M', 'T', 'T', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', ',', 'T'], # NPC AQUI (N)
    ['T', '.', '.', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', 'M', '.', '.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'G', '.', '.', '.', 'T'],
    ['T', '.', '.', 'M', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', 'M', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
    
]

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def carregar_mapa(mapa, grupo_obs, grupo_col, grupo_mato, grupo_npcs):
    """Lê a matriz do mapa e instancia os objetos nas posições corretas."""
    pos_player = (100, 100)
    path_professor = os.path.join(DIRETORIO_BASE, "assets/professor/professor_massa.png") 
    
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
            elif letra == 'N':
                # Cria NPC
                try:
                    npc = NPC(x, y, path_professor, "Está pronto para derrotar o Mangue Vermelho?")
                    grupo_npcs.add(npc)
                    grupo_obs.add(npc) # Player colide com NPC
                except Exception as e:
                    print(f"Erro ao criar NPC: {e}")
                
    largura_total = len(mapa[0]) * TILE_SIZE
    altura_total = len(mapa) * TILE_SIZE
    
    return largura_total, altura_total, pos_player


# =============================================================================
# SETUP INICIAL DO JOGO
# =============================================================================
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("PokeCIn - Fim do Mangue Vermelho")
clock = pg.time.Clock()

# --- Grupos de Sprites ---
grupo_obstaculos = pg.sprite.Group()
grupo_coletaveis = pg.sprite.Group()
grupo_mato = pg.sprite.Group()
grupo_npcs = pg.sprite.Group()

# --- Carregamento do Mundo ---
map_w, map_h, player_pos = carregar_mapa(MAPA_MATRIZ, grupo_obstaculos, grupo_coletaveis, grupo_mato, grupo_npcs)

# --- Inicialização do Player ---
try:
    path_down = os.path.join(DIRETORIO_BASE, "assets/mc/mc_down.png")
    path_left = os.path.join(DIRETORIO_BASE, "assets/mc/mc_left.png")
    path_up = os.path.join(DIRETORIO_BASE, "assets/mc/mc_up.png")
    path_right = os.path.join(DIRETORIO_BASE, "assets/mc/mc_right.png")
    
    protagonista = Player(player_pos[0], player_pos[1], path_down, path_left, path_up, path_right)
    player_group = pg.sprite.GroupSingle(protagonista)
except FileNotFoundError: 
    print("ERRO CRÍTICO: Imagens do player não encontradas.")
    exit()

# --- Inicialização de Sistemas ---
menu_inv = MenuInventario()
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, map_w, map_h)

# Gera o visual do chão
caminho_tileset = os.path.join(DIRETORIO_BASE, "assets/backgrounds/tileset.png")
fundo_grama = definir_piso(map_w, map_h, caminho_tileset)

# --- Equipe Inicial ---
charmander = criar_pokemon("Charmander", 5)
squirtle = criar_pokemon("Squirtle", 5)
equipe_jogador = [charmander, squirtle] 

# --- CONFIGURAÇÃO DE TEXTO (Estilo Pokémon) ---
font_aviso = pg.font.SysFont("courier new", 20, bold=True)

# Cores da caixa estilo Pokémon
POKE_BLUE = (48, 80, 192)     # Borda
POKE_WHITE = (248, 248, 248)  # Fundo
POKE_BLACK = (32, 32, 32)     # Texto

texto_aviso = font_aviso.render('Pressione a tecla "F" para coletar este item.', True, POKE_BLACK)

# =============================================================================
# FLUXO DE INTRODUÇÃO
# =============================================================================
jogo_ativo = exibir_intro(screen, clock) 
nome_jogador = "Player"

if jogo_ativo:
    jogo_ativo, nome_escolhido = cena_professor(screen, clock)
    
    if nome_escolhido:
        nome_jogador = nome_escolhido
        print(f"Bem-vindo ao mangue, {nome_jogador}!") 
        
        if jogo_ativo:
            try: 
                pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3"))

                pg.mixer.music.set_volume(0.2)
                pg.mixer.music.play(-1, fade_ms=2000)
            except: pass

# =============================================================================
# LOOP PRINCIPAL (GAME LOOP)
# =============================================================================

estado_jogo = "MUNDO"
sistema_batalha = None
running = jogo_ativo 
path_sound = os.path.join(DIRETORIO_BASE, "assets/sfx/itemfound.wav")

while running:
    
    # -------------------------------------------------------------------------
    # ESTADO: MUNDO (Exploração)
    # -------------------------------------------------------------------------
    if estado_jogo == "MUNDO":
        
        # --- 1. LÓGICA DE UPDATE ---
        
        # Verifica se algum NPC está falando
        npc_falando_agora = None
        for npc in grupo_npcs:
            if npc.falando:
                npc_falando_agora = npc
                break
        
        # Eventos
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                running = False
            
            if event.type == pg.KEYDOWN:
                
                # --- CONTROLES DE DIÁLOGO ---
                if npc_falando_agora:
                    # Tecla F: Fecha o diálogo (se já tiver terminado)
                    if event.key == pg.K_f:
                        npc_falando_agora.interagir()
                    
                    # Setas/A/D: Mudam a opção (Sim/Não)
                    elif event.key == pg.K_LEFT or event.key == pg.K_a:
                        npc_falando_agora.mudar_selecao(-1)
                    elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                        npc_falando_agora.mudar_selecao(1)
                    
                    # Enter: Confirma a escolha ou avança texto
                    elif event.key == pg.K_RETURN:
                        # Se ainda não respondeu, processa a resposta
                        if not npc_falando_agora.respondeu:
                            npc_falando_agora.respondeu = True
                            if npc_falando_agora.indice_selecionado == 0: # Sim
                                npc_falando_agora.texto_atual = "Ótimo! Prepare-se para a batalha!"
                            else: # Não
                                npc_falando_agora.texto_atual = "Volte quando estiver pronto."
                        # Se já respondeu, fecha
                        else:
                            npc_falando_agora.interagir()

                # --- CONTROLES DE MUNDO ---
                else:
                    # Tecla E: Inventário
                    if event.key == pg.K_e:
                        menu_inv.alternar() 
                    
                    # Tecla F: Coletar itens próximos
                    if event.key == pg.K_f:
                        area_interacao = protagonista.rect.inflate(10, 10)
                        for item in grupo_coletaveis:
                            if area_interacao.colliderect(item.rect):
                                item.coletar(protagonista)
                                #pg.mixer.Sound(path_sound).play()

                    
                    # Tecla F: Interagir com npc
                    if event.key == pg.K_f:
                        # Verifica se o player colide com a área aumentada (1.5x) do NPC
                        hits_npc = pg.sprite.spritecollide(protagonista, grupo_npcs, False)
                        
                        # Se não colidiu diretamente, tenta expandir a busca
                        if not hits_npc:
                             # Cria um rect temporário maior ao redor do player
                             area_busca = protagonista.rect.inflate(20, 20) 
                             for npc in grupo_npcs:
                                 if area_busca.colliderect(npc.rect):
                                     npc.interagir()
                                     break
                        else:
                            # Se colidiu, interage com o primeiro
                            hits_npc[0].interagir()

        # Atualização do Mundo (Só roda se não estiver conversando)
        if not npc_falando_agora:
            antigo_rect = protagonista.rect.copy()
            player_group.update()
            
            # Lógica do Mato
            if protagonista.direction.magnitude() > 0:
                if pg.sprite.spritecollide(protagonista, grupo_mato, False):
                    if random.random() < 0.015: 
                        animacao_transicao(screen)
                        estado_jogo = "BATALHA"

                        # GERA O POKEMON NO MATO
                        inimigo_pokemon = criar_pokemon("Bulbasaur", random.randint(3, 5))
                        
                        inv_batalha = {'Pocao': 5, 'Pokebola': 5}
                        try:
                            if hasattr(menu_inv, 'itens'): 
                                inv_batalha = menu_inv.itens
                            elif hasattr(protagonista, 'inventario'):
                                inv_batalha = protagonista.inventario.itens
                        except: pass

                        try:
                            sistema_batalha = BatalhaPokemon(equipe_jogador, inimigo_pokemon, inv_batalha)
                        except Exception as e:
                            print(f"ERRO AO INICIAR BATALHA: {e}")
                            estado_jogo = "MUNDO"

            # Colisões com obstáculos e coletáveis
            colisao_obs = pg.sprite.spritecollide(protagonista, grupo_obstaculos, False)
            colisao_item = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False)
            if colisao_obs or colisao_item:
                protagonista.rect = antigo_rect

            # Câmera
            camera.update(protagonista.rect)


        # --- 2. LÓGICA DE DESENHO  ---
        # --- 2. LÓGICA DE DESENHO ---
        
        # Desenha o Mundo (SEMPRE desenha isso primeiro)
        screen.fill((0,0,0)) 
        screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))

        for item in grupo_mato: 
            screen.blit(item.image, camera.apply(item.rect))
        for parede in grupo_obstaculos: 
            screen.blit(parede.image, camera.apply(parede.rect))
        for item in grupo_coletaveis: 
            screen.blit(item.image, camera.apply(item.rect))
        
        # Desenha NPCs
        for npc in grupo_npcs:
            screen.blit(npc.image, camera.apply(npc.rect))

        # Desenha Player
        for sprite in player_group: 
            screen.blit(sprite.image, camera.apply(sprite.rect))
        
        # Desenha Interface (Por cima do mundo)
        menu_inv.desenhar(screen, protagonista.inventario)

        # Desenha Caixa de Diálogo do NPC (SE TIVER UM FALANDO)
        if npc_falando_agora:
            # Configuração da caixa
            rect_fundo = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
            rect_interno = rect_fundo.inflate(-10, -10)
            
            # Desenha Fundo
            pg.draw.rect(screen, (40, 40, 160), rect_fundo, border_radius=10) # Borda Azul
            pg.draw.rect(screen, (255, 255, 255), rect_interno, border_radius=10) # Fundo Branco

            # Desenha Texto
            fonte = pg.font.SysFont("Arial", 22)
            linhas = npc_falando_agora.texto_atual.split('\n')
            y_texto = rect_interno.y + 20
            for linha in linhas:
                texto_surf = fonte.render(linha, True, (0, 0, 0))
                screen.blit(texto_surf, (rect_interno.x + 20, y_texto))
                y_texto += 30

            # Desenha Seta Piscante
            if running:
                pontos_seta = [
                    (rect_interno.right - 30, rect_interno.bottom - 20),
                    (rect_interno.right - 10, rect_interno.bottom - 20),
                    (rect_interno.right - 20, rect_interno.bottom - 10)
                ]
                pg.draw.polygon(screen, (200, 0, 0), pontos_seta)

            # Desenha Opções (Sim/Não) se necessário
            if not npc_falando_agora.respondeu:
                fonte_opcoes = pg.font.SysFont("Arial", 22, bold=True)
                
                cor_sim = (200, 0, 0) if npc_falando_agora.indice_selecionado == 0 else (0, 0, 0)
                cor_nao = (200, 0, 0) if npc_falando_agora.indice_selecionado == 1 else (0, 0, 0)

                sim_surf = fonte_opcoes.render("> Sim" if npc_falando_agora.indice_selecionado == 0 else "  Sim", True, cor_sim)
                nao_surf = fonte_opcoes.render("> Não" if npc_falando_agora.indice_selecionado == 1 else "  Não", True, cor_nao)

                screen.blit(sim_surf, (rect_interno.x + 50, rect_interno.y + 80))
                screen.blit(nao_surf, (rect_interno.x + 200, rect_interno.y + 80))


    # -------------------------------------------------------------------------
    # ESTADO: BATALHA
    # -------------------------------------------------------------------------
    elif estado_jogo == "BATALHA":
        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                running = False
            
            # Input da Batalha
            if event.type == pg.KEYDOWN:
                if sistema_batalha and sistema_batalha.battle_over:
                    # Se batalha acabou, Espaço para sair
                    if event.key == pg.K_SPACE:
                        if sistema_batalha.vencedor == "INIMIGO":
                            print("GAME OVER")
                            running = False
                        else:
                            estado_jogo = "MUNDO"
                            try: 
                                pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3"))
                                pg.mixer.music.play(-1)
                            except: pass
                else:
                    # Input normal de batalha
                    if sistema_batalha: 
                        sistema_batalha.processar_input(event)

        # Desenha a batalha
        if sistema_batalha: 
            sistema_batalha.desenhar(screen)

    # --- Atualização de Frame ---
    pg.display.flip()
    clock.tick(FPS)

pg.quit()

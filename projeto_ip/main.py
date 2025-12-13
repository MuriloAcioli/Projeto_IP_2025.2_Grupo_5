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
from pokedex import POKEDEX
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
lista_pokemons_disponiveis =  list(POKEDEX.keys())
lista_pokemons_comuns = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "comum"]
lista_pokemons_raros = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "raro"]
lista_pokemons_super_raros = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "super_raro"]
lista_pokemons_lendarios = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "lendario"]

# =============================================================================
# DADOS DO MAPA
# =============================================================================
MAPA_MATRIZ = [
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'M', 'M', 'M', '.', '.', '.', '.', '.', 'N', '.', '.', 'T'],
    ['T', '.', 'P', '.', '.', '.', '.', '.', '.', 'B', '.', '.', 'T', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'M', 'M', 'M', 'T', '.', '.', 'B', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', 'M', 'M', 'M', '.', '.', 'T', 'M', 'M', 'M', 'T', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', 'H', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', 'T', 'G', '.', 'M', 'T', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'B', '.', 'T'],
    ['T', '.', '.', 'M', 'M', '.', '.', '.', '.', '.', 'M', 'M', 'T', '.', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', ',', 'T'],
    ['T', '.', 'M', 'M', 'M', '.', '.', '.', '.', 'M', 'M', 'M', 'T', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', 'M', 'M', '.', '.', '.', '.', 'M', 'M', 'M', 'T', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', 'M', 'T', 'T', 'T', '.', '.', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'H', 'M', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'T'],
    ['T', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'H', '.', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '.', '.', 'T'],
    ['T', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'G', '.', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '.', '.', 'T'],
    ['T', '.', 'M', '.', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'G', '.', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '.', '.', 'T'],
    ['T', '.', '.', '.', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'H', '.', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '.', '.', 'T'],
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
                grupo_col.add(Pokebola(x+15, y+15))
                 
            elif letra == 'G':
                grupo_col.add(GreatBall(x+15, y+15))
            elif letra == 'H':
                grupo_col.add(Pocao(x+15, y+15))
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

# =============================================================================
# FLUXO DE INTRODUÇÃO
# =============================================================================
jogo_ativo = exibir_intro(screen, clock) 
nome_jogador = "Player"
inicial_escolhido = "Charmander" # Padrão caso algo falhe

if jogo_ativo:
    # AQUI ESTÁ A MUDANÇA PRINCIPAL: Recebe 3 valores agora
    jogo_ativo, nome_input, pokemon_input = cena_professor(screen, clock)
    
    if nome_input:
        nome_jogador = nome_input
    if pokemon_input:
        inicial_escolhido = pokemon_input
        
    print(f"Bem-vindo ao mangue, {nome_jogador}!")
    print(f"Seu inicial é: {inicial_escolhido}")
    
    if jogo_ativo:
        try: 
            pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3"))
            pg.mixer.music.set_volume(0.2)
            pg.mixer.music.play(-1, fade_ms=2000)
        except: pass

# --- CRIAÇÃO DA EQUIPE COM O INICIAL ESCOLHIDO ---
equipe_jogador = []
pokemon_inicial = criar_pokemon(inicial_escolhido, 5) # Cria Nível 5
if pokemon_inicial:
    equipe_jogador.append(pokemon_inicial)
else:
    # Fallback de segurança
    equipe_jogador.append(criar_pokemon("Charmander", 5))

# =============================================================================
# LOOP PRINCIPAL (GAME LOOP)
# =============================================================================

estado_jogo = "MUNDO"
sistema_batalha = None
running = jogo_ativo 
path_sound = os.path.join(DIRETORIO_BASE, "assets/sfx/itemfound.wav")

mensagem_tela = None

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
                    # Tecla f: Fecha o diálogo (se já tiver terminado)
                    if event.key == pg.K_f:
                        npc_falando_agora.interagir()
                    
                    # Setas/A/D: Mudam a opção (Sim/Não)
                    elif event.key == pg.K_LEFT or event.key == pg.K_a:
                        npc_falando_agora.mudar_selecao(-1)
                    elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                        npc_falando_agora.mudar_selecao(1)
                    
                    # Space: Confirma a escolha ou avança texto
                    elif event.key == pg.K_SPACE:
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
                    
                    # Tecla Space: Coletar itens próximos
                    if event.key == pg.K_SPACE:
                        if mensagem_tela:
                            mensagem_tela = None
                        
                        # SE NÃO TEM MENSAGEM -> TENTA PEGAR ITEM
                        else:
                            area_interacao = protagonista.rect.inflate(10, 10)
                            # Usar uma flag para pegar só 1 item por vez
                            item_pegado = False 
                            
                            for item in grupo_coletaveis:
                                if area_interacao.colliderect(item.rect):
                                    # Salva o nome ANTES de remover o item
                                    nome_item = item.nome_item 
                                    item.coletar(protagonista)
                                    
                                    # AQUI: Apenas salvamos o texto na variável!
                                    mensagem_tela = f"Você pegou: {nome_item}"
                                    item_pegado = True
                                    break

                                #pg.mixer.Sound(path_sound).play()
                    
                    # Tecla Space: Interagir com NPC
                    if event.key == pg.K_SPACE:
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
                    if random.random() < 0.0115: # Chance de encontro
                        animacao_transicao(screen)
                        estado_jogo = "BATALHA"
 
                        # GERA O POKEMON NO MATO
                        raridade = random.randint(0, 100)
                        if raridade < 75:
                            pokemon_random = random.choice(lista_pokemons_comuns)
                            lvl_chao = 3
                            lvl_teto = 5
                        elif raridade < 93:
                            pokemon_random = random.choice(lista_pokemons_raros)
                            lvl_chao = 5
                            lvl_teto = 10
                        elif raridade < 98:
                            pokemon_random = random.choice(lista_pokemons_super_raros)
                            lvl_chao = 5
                            lvl_teto = 10
                        else:
                            lvl_chao = 50
                            lvl_teto = 50
                            pokemon_random = random.choice(lista_pokemons_lendarios)
                        
                        inimigo_pokemon = criar_pokemon(pokemon_random, random.randint(lvl_chao, lvl_teto))
                        
                        inv_batalha = {'Poção': 5, 'Pokebola': 5}
                        try:
                            if hasattr(menu_inv, 'itens'): 
                                inv_batalha = menu_inv.itens
                            elif hasattr(protagonista, 'inventario'):
                                inv_batalha = protagonista.inventario
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
        # ... (código que desenha mapa, player, npcs...)

    # --- DESENHA A MENSAGEM (SE HOUVER UMA) ---
    if mensagem_tela:
        rect_fundo = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
        rect_interno = rect_fundo.inflate(-10, -10)

        # Desenha a caixa
        pg.draw.rect(screen, (40, 40, 160), rect_fundo, border_radius=10)
        pg.draw.rect(screen, (255, 255, 255), rect_interno, border_radius=10)

        # Desenha o texto
        fonte = pg.font.SysFont("Arial", 22)
        texto_surf = fonte.render(mensagem_tela, True, (0, 0, 0))
        
        # Centraliza o texto um pouco
        screen.blit(texto_surf, (rect_interno.x + 20, rect_interno.y + 50))
        
        # Opcional: Aviso para fechar
        fonte_pequena = pg.font.SysFont("Arial", 16)
        aviso = fonte_pequena.render("[F] para fechar", True, (100, 100, 100))
        screen.blit(aviso, (rect_interno.right - 120, rect_interno.bottom - 30))


    # --- Atualização de Frame ---
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
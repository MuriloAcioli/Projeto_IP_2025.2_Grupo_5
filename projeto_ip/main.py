import pygame as pg
import random
from player import Player   
from camera import Camera
from coletaveis import Pokebola, GreatBall, Pocao
from inventario import MenuInventario
from npc import NPC
import os

DIRETORIO_BASE = os.path.dirname(__file__)  # Caminho do diretório atual
# --- Configurações Globais ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48 # Tamanho de cada quadrado do mapa (64x64)
FPS = 60

# --- 1. DEFINIÇÃO DO MAPA (Visualize sua fase aqui!) ---
# P = Player (Onde começa)
# M = Mato (gerador de encontros)
# N = NPC (Professor)
# T = Tree/Tronco (Obstáculo)
# B = Pokebola
# G = GreatBall
# H = Health Potion (Poção)
# . = Grama (Chão livre)

MAPA_MATRIZ = [
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', 'P', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', 'M', 'M', 'M', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'G', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'B', '.', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'N', 'T'],
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

# --- 3. Classe Mato ---
class Mato(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
        # Cor diferente (Verde Limão para destacar)
        self.image.fill((100, 200, 50)) 
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Função para Ler o Mapa ---
def carregar_mapa(mapa, grupo_obs, grupo_col, grupo_mato, grupo_npcs):
    pos_player = (100, 100) # Valor padrão caso não tenha 'P'
    path_professor = os.path.join(DIRETORIO_BASE, "assets/professor/professor.png")
    
    for row_index, row in enumerate(mapa):
        for col_index, letra in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            if letra == 'T':
                grupo_obs.add(Obstaculo(x, y))

            elif letra == 'B':
                grupo_col.add(Pokebola(x, y))

            elif letra == 'N':
                # Cria o NPC com um texto personalizado
                npc = NPC(x, y, path_professor, "Está pronto para derrotar o Mangue Vermelho?")
                grupo_npcs.add(npc)
                grupo_obs.add(npc) # Opcional: Adiciona em obs para o player não atravessar ele

            elif letra == 'M':
                grupo_mato.add(Mato(x, y))
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
grupo_mato = pg.sprite.Group()
grupo_npcs = pg.sprite.Group()

# 3. Carregando o Mapa
map_w, map_h, player_pos = carregar_mapa(MAPA_MATRIZ, grupo_obstaculos, grupo_coletaveis, grupo_mato, grupo_npcs)

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
    # 1. --- LÓGICA DE JOGO (QUEM ESTÁ FALANDO?) ---
    # Verifica se existe ALGUM NPC falando neste exato momento
    npc_falando_agora = None
    for npc in grupo_npcs:
        if npc.falando:
            npc_falando_agora = npc
            break

    # --- EVENTOS (Teclado e Mouse) ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
        if event.type == pg.KEYDOWN:
            # === MODO DIÁLOGO (Se tem alguém falando) ===
            if npc_falando_agora:
                # Tecla T: Fecha o diálogo
                if event.key == pg.K_t:
                    npc_falando_agora.interagir()
                
                # Setas/A/D: Mudam a opção
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    npc_falando_agora.mudar_selecao(-1)
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    npc_falando_agora.mudar_selecao(1)
                
                # Enter: Confirma a escolha
                elif event.key == pg.K_RETURN:
                    # CASO 1: Ainda não respondeu -> Confirma a seleção (Sim/Não)
                    if not npc_falando_agora.respondeu:
                        npc_falando_agora.respondeu = True
                        if npc_falando_agora.indice_selecionado == 0: # Sim
                            npc_falando_agora.texto_atual = "Ótimo! Prepare-se para a batalha!"
                        else: # Não
                            npc_falando_agora.texto_atual = "Volte quando estiver pronto."
                    
                    # CASO 2: Já respondeu -> Fecha o diálogo (igual ao T)
                    else:
                        npc_falando_agora.interagir()

            # === MODO NORMAL (Se ninguém está falando) ===
            else:
                # Tecla E: Inventário
                if event.key == pg.K_e:
                    menu_inv.alternar() 

                # Tecla T: Interagir (Procura NPCs próximos)
                if event.key == pg.K_t:
                    # Verifica se o player colide com a área aumentada (1.5x) do NPC
                    hits_npc = pg.sprite.spritecollide(protagonista, grupo_npcs, False, pg.sprite.collide_rect_ratio(1.5))
                    for npc in hits_npc:
                        npc.interagir()
                        # Interrompe após achar o primeiro para não bugar se tiver 2 juntos
                        break 

    # --- ATUALIZAÇÃO (UPDATE) ---
    
    # Se o NPC estiver falando, o jogo PAUSA (player não anda)
    if npc_falando_agora:
        # O player fica parado, mas podemos continuar atualizando animações se quiser
        # Por enquanto, não chamamos player_group.update() para travar ele
        pass
    else:
        # Jogo Normal: Player anda, monstros aparecem, etc.
        antigo_rect = protagonista.rect.copy()
        player_group.update()

        # Lógica de encontro no mato
        if protagonista.direction.magnitude() > 0:
            if pg.sprite.spritecollide(protagonista, grupo_mato, False):
                if random.random() < 0.005: 
                    print("!!! UM POKÉMON SELVAGEM APARECEU !!!")
        
        # Colisão com Árvores/Paredes
        if pg.sprite.spritecollide(protagonista, grupo_obstaculos, False):
            protagonista.rect = antigo_rect

        # Coletar Itens
        hits = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False)
        for item in hits:
            item.coletar(protagonista)

    # Atualiza câmera (Sempre foca no player)
    camera.update(protagonista.rect)

    # --- DESENHO (DRAW) ---
    screen.fill((0,0,0)) 

    # 1. Desenha o Mundo
    screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))
    for mato in grupo_mato:
        screen.blit(mato.image, camera.apply(mato.rect))
    for parede in grupo_obstaculos:
        screen.blit(parede.image, camera.apply(parede.rect))
    for item in grupo_coletaveis:
        screen.blit(item.image, camera.apply(item.rect))
    for sprite in player_group:
        screen.blit(sprite.image, camera.apply(sprite.rect))

    # 2. Desenha NPCs e Interface de Diálogo
    for npc in grupo_npcs:
        screen.blit(npc.image, camera.apply(npc.rect))
        
        # Desenha balão de fala se este NPC específico estiver falando
        if npc.falando:
            # --- ESTILO IDÊNTICO AO DA INTRO ---
            COR_CAIXA = (255, 255, 255)  # Branco
            COR_BORDA = (40, 40, 160)    # Azul Escuro do Prof
            COR_TEXTO = (0, 0, 0)        # Preto
            
            # Define a posição da caixa (estilo largo na parte inferior)
            # Usando proporções similares à intro
            rect_fundo = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
            
            # 1. Desenha a Borda (Retângulo externo arredondado)
            pg.draw.rect(screen, COR_BORDA, rect_fundo, border_radius=10)
            
            # 2. Desenha o Fundo (Retângulo interno menor arredondado)
            rect_interno = rect_fundo.inflate(-10, -10) # Diminui 10px
            pg.draw.rect(screen, COR_CAIXA, rect_interno, border_radius=10)

            # 3. Texto da Fala
            # Fonte Arial tamanho 22 (igual à intro)
            fonte = pg.font.SysFont("Arial", 22)
            # Renderiza o texto (permite quebra de linha manual se tiver \n)
            linhas = npc.texto_atual.split('\n')
            y_texto = rect_interno.y + 20
            for linha in linhas:
                texto_surf = fonte.render(linha, True, COR_TEXTO)
                screen.blit(texto_surf, (rect_interno.x + 20, y_texto))
                y_texto += 30

            # 4. A "Setinha" Vermelha Piscando
            # Pisca a cada meio segundo (500ms)
            if running:
                # Triângulo vermelho apontando para baixo
                pontos_seta = [
                    (rect_interno.right - 30, rect_interno.bottom - 20), # Ponto esquerdo
                    (rect_interno.right - 10, rect_interno.bottom - 20), # Ponto direito
                    (rect_interno.right - 20, rect_interno.bottom - 10)  # Ponto baixo (bico)
                ]
                pg.draw.polygon(screen, (200, 0, 0), pontos_seta)

            # 5. Opções (Sim/Não) - Se for hora de responder
            if not npc.respondeu:
                fonte_opcoes = pg.font.SysFont("Arial", 22, bold=True)
                
                # Cores de destaque
                cor_destaque = (200, 0, 0) # Vermelho (igual a seta)
                cor_normal = (0, 0, 0)     # Preto
                
                cor_sim = cor_destaque if npc.indice_selecionado == 0 else cor_normal
                cor_nao = cor_destaque if npc.indice_selecionado == 1 else cor_normal

                sim_surf = fonte_opcoes.render("> Sim" if npc.indice_selecionado == 0 else "  Sim", True, cor_sim)
                nao_surf = fonte_opcoes.render("> Não" if npc.indice_selecionado == 1 else "  Não", True, cor_nao)

                # Posiciona as opções um pouco mais abaixo do texto
                screen.blit(sim_surf, (rect_interno.x + 50, rect_interno.y + 80))
                screen.blit(nao_surf, (rect_interno.x + 200, rect_interno.y + 80))

    # 3. Interface (Inventário) - Sempre por último
    menu_inv.desenhar(screen, protagonista.inventario)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()


"""

"""

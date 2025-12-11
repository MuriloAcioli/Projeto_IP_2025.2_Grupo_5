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
DIRETORIO_BASE = os.path.dirname(__file__)  # Caminho do diretório atual
# --- Configurações Globais ---
# IMPORTANTE: Importamos a função de criar agora!
from pokemon import Pokemon, criar_pokemon 
from batalha import BatalhaPokemon

# --- Configurações Gerais ---
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48 
FPS = 60

# --- CLASSE MATO ---
#class Mato(pg.sprite.Sprite):
#    def __init__(self, x, y):
#        super().__init__()
#        self.image = pg.Surface((TILE_SIZE, TILE_SIZE))
#        self.image.fill((20, 100, 20)) 
#        self.image.set_alpha(150)
#        self.rect = self.image.get_rect(topleft=(x, y))

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
# --- Função de Carregamento do Mapa ---
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


# --- FUNÇÕES DE CENA (Intro e Dialogo) ---

def definir_piso(largura_mapa, altura_mapa, caminho_tileset):
    # 1. Cria a superfície base onde desenharemos o chão
    superficie_chao = pg.Surface((largura_mapa, altura_mapa))
    
    try:
        # 2. Carrega a imagem do tileset
        img_tileset = pg.image.load(caminho_tileset).convert_alpha()
    except FileNotFoundError:
        print("Erro: Tileset não encontrado. Usando cor sólida.")
        superficie_chao.fill((34, 139, 34))
        return superficie_chao

    TAMANHO_ORIGINAL = 64

    TILE_PADRAO = (0, 0)    # Um quadrado de grama comum
    TILE_GRAMA_LISA = (0, 1)    # Um quadrado de grama comum
    TILE_GRAMA_DETALHE = (2, 1) # Grama com pontinhos
    TILE_FLOR_AMARELA = (0, 4)  # Exemplo de flor
    TILE_FLOR_ROSA = (1, 4)     # Exemplo de flor
    
    # Lista com opções e "pesos" (probabilidade).
    # Queremos muita grama e poucas flores.
    opcoes = [TILE_GRAMA_LISA] * 30 + 30 * [TILE_PADRAO]+ [TILE_GRAMA_DETALHE] * 30 + [TILE_FLOR_AMARELA] * 5 + [TILE_FLOR_ROSA] * 5

    # 4. Loop para preencher todo o mapa
    for y in range(0, altura_mapa, TILE_SIZE):
        for x in range(0, largura_mapa, TILE_SIZE):
            
            # Escolhe um tile aleatório da lista
            escolha = random.choice(opcoes)
            coluna_img, linha_img = escolha
            
            # Recorta o tile da imagem original
            rect_recorte = pg.Rect(coluna_img * TAMANHO_ORIGINAL, 
                                   linha_img * TAMANHO_ORIGINAL, 
                                   TAMANHO_ORIGINAL, 
                                   TAMANHO_ORIGINAL)
            
            tile_imagem = img_tileset.subsurface(rect_recorte)
            
            # Aumenta para o tamanho do jogo (48x48)
            tile_escalado = pg.transform.scale(tile_imagem, (TILE_SIZE, TILE_SIZE))
            
            # Desenha no chão
            superficie_chao.blit(tile_escalado, (x, y))

    return superficie_chao

def exibir_intro(screen):
    intro = True
    
    # Configuração de Fontes
    font_titulo = pg.font.SysFont("Arial", 50, bold=True)
    font_start = pg.font.SysFont("Arial", 30, bold=True)
    
    texto_titulo = font_titulo.render("PokéCIn: a Ameaça do Mangue", True, (0,0,0))
    texto_start = font_start.render("ENTER para Jogar", True, (50,50,50))
    
    rect_titulo = texto_titulo.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    rect_start = texto_start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))
    
    # Tenta carregar imagem de fundo
    try: 
        bg_intro = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/backgrounds/intro_bg.jpg")).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    except: 
        bg_intro = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); bg_intro.fill((255,255,255))
        
    # Tenta carregar musica
    try: 
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/intro.mp3"))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1, start=1.0)
    except: pass
    
    # Loop da Intro
    while intro:
        clock.tick(15)
        for event in pg.event.get():
            if event.type == pg.QUIT: return False
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_RETURN: 
                    intro = False
                    pg.mixer.music.fadeout(1000)
                    return True
                    
        screen.blit(bg_intro, (0,0))
        screen.blit(texto_titulo, rect_titulo)
        screen.blit(texto_start, rect_start)
        pg.display.flip()
        
    return True

def cena_professor(screen):
    # Cores e Fontes
    COR_CAIXA = (255, 255, 255)
    COR_BORDA = (40, 40, 160)
    COR_TEXTO = (0, 0, 0)
    font_texto = pg.font.SysFont("Arial", 22)
    font_nome = pg.font.SysFont("Arial", 30, bold=True)
    
    # --- Carregamento de Assets (Seguro) ---
    sfx_blip = None
    try: 
        sfx_blip = pg.mixer.Sound(os.path.join(DIRETORIO_BASE, "assets/sfx/sfx_blip.wav"))
        sfx_blip.set_volume(0.3)
    except: pass
    
    try: 
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/professor_theme.mp3"))
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1, fade_ms=2000) 
    except: pass
    
    try: 
        bg_imagem = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/backgrounds/lab.jpg")).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    except: 
        bg_imagem = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); bg_imagem.fill((200, 200, 250))
        
    try: 
        img_professor = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/professor/professor.png")).convert_alpha(), (400, 400)) 
    except: 
        img_professor = pg.Surface((400, 400)); img_professor.fill((100, 100, 100))
         
    # --- Textos do Roteiro ---
    falas_intro = [
        "Olá! Bem-vindo ao fantástico mundo de Pokémon", "Esse mundo é habitado por diversas criaturas misteriosas", 
        "Meu nome é Ricardo Massa", "As pessoas me chamam de Professor Python.", 
        "Estamos precisando de ajuda aqui no CIn.", "O Coletivo Mangue Vermelho quer usar seus Pokémons\npara destruir nossos computadores!", 
        "Precisamos de alguém para derrotá-los!", "Será que você é o candidato ideal?", 
        "Antes que eu forneça Pokémons Fortes para você usar contra eles", "Vamos fazer um teste para ver sua competência", 
        "Mas primeiro, diga-me algo sobre você."
    ]
    falas_final = [
        "Ah, certo! Então seu nome é {NOME}?", "Forme uma equipe de até 6 pokémons e me desafie numa batalha", 
        "Se você me vencer, será destinado a enfrentar o Mangue Vermelho!!", "Sua jornada começa agora!", 
        "Escolha um dos 3 Pokémons na mesa", "Após isso, sinta-se à vontade para capturar mais alguns no mato", 
        "Estarei esperando por você!"
    ]
    
    # Variáveis de Estado da Cena
    indice = 0
    estado = "INTRO"
    nome_digitado = ""
    nome_final = "Player"
    rect_caixa = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
    
    clock = pg.time.Clock()
    running = True
    
    while running:
        clock.tick(30)
        
        # Eventos
        for event in pg.event.get():
            if event.type == pg.QUIT: return False, None
            
            if event.type == pg.KEYDOWN:
                # Se estiver na fala
                if estado == "INTRO" or estado == "FINAL":
                    if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        if sfx_blip: sfx_blip.play()
                        indice += 1
                        if estado == "INTRO" and indice >= len(falas_intro): estado = "INPUT"; indice = 0
                        elif estado == "FINAL" and indice >= len(falas_final): pg.mixer.music.fadeout(1000); return True, nome_final
                
                # Se estiver digitando
                elif estado == "INPUT":
                    if event.key == pg.K_RETURN:
                        if len(nome_digitado) > 0: 
                            if sfx_blip: sfx_blip.play()
                            nome_final = nome_digitado; estado = "FINAL"; indice = 0
                    elif event.key == pg.K_BACKSPACE: nome_digitado = nome_digitado[:-1]
                    else:
                        if len(nome_digitado) < 10 and event.unicode.isprintable(): nome_digitado += event.unicode
                        
        # Desenha Fundo
        screen.blit(bg_imagem, (0, 0))
        
        # Desenha Professor e Sombra
        prof_x = SCREEN_WIDTH // 2 - img_professor.get_width() // 2; prof_y = 40 
        largura_sombra = 300; altura_sombra = 40
        sombra_x = prof_x + (img_professor.get_width() - largura_sombra) // 2; sombra_y = prof_y + 360
        sombra_surf = pg.Surface((largura_sombra, altura_sombra), pg.SRCALPHA)
        pg.draw.ellipse(sombra_surf, (0, 0, 0, 80), (0,0, largura_sombra, altura_sombra))
        screen.blit(sombra_surf, (sombra_x, sombra_y)); screen.blit(img_professor, (prof_x, prof_y))
        
        # Desenha Caixa de Texto
        pg.draw.rect(screen, COR_BORDA, rect_caixa, border_radius=10)
        rect_interno = rect_caixa.inflate(-10, -10)
        pg.draw.rect(screen, COR_CAIXA, rect_interno, border_radius=10)
        
        # Lógica do Texto
        texto_para_exibir = ""
        if estado == "INTRO":
            if indice < len(falas_intro): texto_para_exibir = falas_intro[indice]
        elif estado == "FINAL":
            if indice < len(falas_final): texto_para_exibir = falas_final[indice].replace("{NOME}", nome_final)
        elif estado == "INPUT":
            pergunta = font_texto.render("Qual é o seu nome?", True, COR_TEXTO); screen.blit(pergunta, (rect_interno.x + 20, rect_interno.y + 20))
            txt_nome = font_nome.render(nome_digitado + "_", True, (0, 0, 200)); screen.blit(txt_nome, (rect_interno.x + 20, rect_interno.y + 60))
            dica = font_texto.render("(ENTER para confirmar)", True, (150, 150, 150)); screen.blit(dica, (rect_interno.x + 20, rect_interno.y + 100))
            
        # Renderiza o texto quebrado em linhas
        if texto_para_exibir != "":
            linhas = texto_para_exibir.split('\n'); y_atual = rect_interno.y + 20
            for linha in linhas:
                surf_linha = font_texto.render(linha, True, COR_TEXTO); screen.blit(surf_linha, (rect_interno.x + 20, y_atual)); y_atual += 30 
            
            # Pisca a setinha vermelha
            if pg.time.get_ticks() % 1000 < 500: pg.draw.polygon(screen, (200, 0, 0), [(rect_interno.right - 30, rect_interno.bottom - 20), (rect_interno.right - 10, rect_interno.bottom - 20), (rect_interno.right - 20, rect_interno.bottom - 10)])
            
        pg.display.flip()
    return False, None

# --- ANIMAÇÃO DE TRANSIÇÃO (Piscar tela) ---
def animacao_transicao(screen):
    try:
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/battle_theme.mp3"))
        pg.mixer.music.play(-1)
    except: pass
    
    for i in range(8): 
        screen.fill((255, 255, 255)); pg.display.flip(); pg.time.delay(160)
        screen.fill((10, 10, 10)); pg.display.flip(); pg.time.delay(160)

# =============================================================================
# --- SETUP INICIAL ---
# =============================================================================
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("PokeCIn - Fim do Mangue Vermelho")
clock = pg.time.Clock()

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

# Gera o chão texturizado
fundo_grama = definir_piso(map_w, map_h, caminho_img_tileset)

#fundo_grama = pg.Surface((map_w, map_h))
#fundo_grama.fill((34, 139, 34))

# --- EQUIPE INICIAL ---
charmander = criar_pokemon("Charmander", 5)
squirtle = criar_pokemon("Squirtle", 5)
equipe_jogador = [charmander, squirtle] 

# =============================================================================
# --- FLUXO PRINCIPAL DO JOGO ---
# =============================================================================
jogo_ativo = exibir_intro(screen)
nome_jogador = "Player"

# Roda a cena do professor se passou da intro
if jogo_ativo:
    jogo_ativo, nome_escolhido = cena_professor(screen)
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
                    # Animação
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
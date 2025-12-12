import pygame as pg
import random
import os

# --- Imports ---
from player import Player
from camera import Camera
from coletaveis import Pokebola, GreatBall, Pocao
from inventario import MenuInventario
from Obstaculo import Obstaculo
from mato import Mato

# --- Configurações Globais ---
from pokemon import Pokemon, criar_pokemon 
from batalha import BatalhaPokemon

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


# --- FUNÇÕES DE CENA ---

def definir_piso(largura_mapa, altura_mapa, caminho_tileset):
    superficie_chao = pg.Surface((largura_mapa, altura_mapa))
    try:
        img_tileset = pg.image.load(caminho_tileset).convert_alpha()
    except FileNotFoundError:
        superficie_chao.fill((34, 139, 34))
        return superficie_chao

    TAMANHO_ORIGINAL = 64
    TILE_PADRAO = (0, 0)
    TILE_GRAMA_LISA = (0, 1)
    TILE_GRAMA_DETALHE = (2, 1)
    TILE_FLOR_AMARELA = (0, 4)
    TILE_FLOR_ROSA = (1, 4)
    
    opcoes = [TILE_GRAMA_LISA] * 30 + 30 * [TILE_PADRAO]+ [TILE_GRAMA_DETALHE] * 30 + [TILE_FLOR_AMARELA] * 5 + [TILE_FLOR_ROSA] * 5

    for y in range(0, altura_mapa, TILE_SIZE):
        for x in range(0, largura_mapa, TILE_SIZE):
            escolha = random.choice(opcoes)
            coluna_img, linha_img = escolha
            rect_recorte = pg.Rect(coluna_img * TAMANHO_ORIGINAL, linha_img * TAMANHO_ORIGINAL, TAMANHO_ORIGINAL, TAMANHO_ORIGINAL)
            tile_imagem = img_tileset.subsurface(rect_recorte)
            tile_escalado = pg.transform.scale(tile_imagem, (TILE_SIZE, TILE_SIZE))
            superficie_chao.blit(tile_escalado, (x, y))

    return superficie_chao

def exibir_intro(screen):
    intro = True
    font_titulo = pg.font.SysFont("Arial", 50, bold=True)
    font_start = pg.font.SysFont("Arial", 30, bold=True)
    texto_titulo = font_titulo.render("PokéCIn: a Ameaça do Mangue", True, (0,0,0))
    texto_start = font_start.render("ENTER para Jogar", True, (50,50,50))
    rect_titulo = texto_titulo.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    rect_start = texto_start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))
    
    try: 
        bg_intro = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/backgrounds/intro_bg.jpg")).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    except: 
        bg_intro = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); bg_intro.fill((255,255,255))
        
    try: 
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/intro.mp3"))
        pg.mixer.music.set_volume(0.2); pg.mixer.music.play(-1, start=1.0)
    except: pass
    
    while intro:
        clock.tick(15)
        for event in pg.event.get():
            if event.type == pg.QUIT: return False
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_RETURN: 
                    intro = False; pg.mixer.music.fadeout(1000); return True
                    
        screen.blit(bg_intro, (0,0))
        screen.blit(texto_titulo, rect_titulo)
        screen.blit(texto_start, rect_start)
        pg.display.flip()
        
    return True

def cena_professor(screen):
    COR_CAIXA = (255, 255, 255); COR_BORDA = (40, 40, 160); COR_TEXTO = (0, 0, 0)
    font_texto = pg.font.SysFont("Arial", 22); font_nome = pg.font.SysFont("Arial", 30, bold=True)
    
    sfx_blip = None
    try: 
        sfx_blip = pg.mixer.Sound(os.path.join(DIRETORIO_BASE, "assets/sfx/sfx_blip.wav")); sfx_blip.set_volume(0.3)
    except: pass
    
    try: 
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/professor_theme.mp3")); pg.mixer.music.set_volume(0.2); pg.mixer.music.play(-1, fade_ms=2000) 
    except: pass
    
    try: 
        bg_imagem = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/backgrounds/lab.jpg")).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    except: 
        bg_imagem = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); bg_imagem.fill((200, 200, 250))
        
    try: 
        img_professor = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/professor/professor.png")).convert_alpha(), (400, 400)) 
    except: 
        img_professor = pg.Surface((400, 400)); img_professor.fill((100, 100, 100))
         
    falas_intro = ["Olá! Bem-vindo ao fantástico mundo de Pokémon", "Esse mundo é habitado por diversas criaturas misteriosas", "Meu nome é Ricardo Massa", "As pessoas me chamam de Professor Python.", "Estamos precisando de ajuda aqui no CIn.", "O Coletivo Mangue Vermelho quer usar seus Pokémons\npara destruir nossos computadores!", "Precisamos de alguém para derrotá-los!", "Será que você é o candidato ideal?", "Antes que eu forneça Pokémons Fortes para você usar contra eles", "Vamos fazer um teste para ver sua competência", "Mas primeiro, diga-me algo sobre você."]
    falas_final = ["Ah, certo! Então seu nome é {NOME}?", "Forme uma equipe de até 6 pokémons e me desafie numa batalha", "Se você me vencer, será destinado a enfrentar o Mangue Vermelho!!", "Sua jornada começa agora!", "Escolha um dos 3 Pokémons na mesa", "Após isso, sinta-se à vontade para capturar mais alguns no mato", "Estarei esperando por você!"]
    
    indice = 0; estado = "INTRO"; nome_digitado = ""; nome_final = "Player"
    rect_caixa = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
    
    clock = pg.time.Clock(); running = True
    
    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT: return False, None
            if event.type == pg.KEYDOWN:
                if estado == "INTRO" or estado == "FINAL":
                    if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        if sfx_blip: sfx_blip.play()
                        indice += 1
                        if estado == "INTRO" and indice >= len(falas_intro): estado = "INPUT"; indice = 0
                        elif estado == "FINAL" and indice >= len(falas_final): pg.mixer.music.fadeout(1000); return True, nome_final
                elif estado == "INPUT":
                    if event.key == pg.K_RETURN:
                        if len(nome_digitado) > 0: 
                            if sfx_blip: sfx_blip.play()
                            nome_final = nome_digitado; estado = "FINAL"; indice = 0
                    elif event.key == pg.K_BACKSPACE: nome_digitado = nome_digitado[:-1]
                    else:
                        if len(nome_digitado) < 10 and event.unicode.isprintable(): nome_digitado += event.unicode
                        
        screen.blit(bg_imagem, (0, 0))
        prof_x = SCREEN_WIDTH // 2 - img_professor.get_width() // 2; prof_y = 40 
        sombra_surf = pg.Surface((300, 40), pg.SRCALPHA)
        pg.draw.ellipse(sombra_surf, (0, 0, 0, 80), (0,0, 300, 40))
        screen.blit(sombra_surf, (prof_x + 50, prof_y + 360)); screen.blit(img_professor, (prof_x, prof_y))
        
        pg.draw.rect(screen, COR_BORDA, rect_caixa, border_radius=10)
        rect_interno = rect_caixa.inflate(-10, -10)
        pg.draw.rect(screen, COR_CAIXA, rect_interno, border_radius=10)
        
        texto_para_exibir = ""
        if estado == "INTRO":
            if indice < len(falas_intro): texto_para_exibir = falas_intro[indice]
        elif estado == "FINAL":
            if indice < len(falas_final): texto_para_exibir = falas_final[indice].replace("{NOME}", nome_final)
        elif estado == "INPUT":
            pergunta = font_texto.render("Qual é o seu nome?", True, COR_TEXTO); screen.blit(pergunta, (rect_interno.x + 20, rect_interno.y + 20))
            txt_nome = font_nome.render(nome_digitado + "_", True, (0, 0, 200)); screen.blit(txt_nome, (rect_interno.x + 20, rect_interno.y + 60))
            dica = font_texto.render("(ENTER para confirmar)", True, (150, 150, 150)); screen.blit(dica, (rect_interno.x + 20, rect_interno.y + 100))
            
        if texto_para_exibir != "":
            linhas = texto_para_exibir.split('\n'); y_atual = rect_interno.y + 20
            for linha in linhas:
                surf_linha = font_texto.render(linha, True, COR_TEXTO); screen.blit(surf_linha, (rect_interno.x + 20, y_atual)); y_atual += 30 
            if pg.time.get_ticks() % 1000 < 500: pg.draw.polygon(screen, (200, 0, 0), [(rect_interno.right - 30, rect_interno.bottom - 20), (rect_interno.right - 10, rect_interno.bottom - 20), (rect_interno.right - 20, rect_interno.bottom - 10)])
        pg.display.flip()
    return False, None

def animacao_transicao(screen):
    try:
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/battle_theme.mp3")); pg.mixer.music.play(-1)
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

grupo_obstaculos = pg.sprite.Group()
grupo_coletaveis = pg.sprite.Group()
grupo_mato = pg.sprite.Group()

map_w, map_h, player_pos = carregar_mapa(MAPA_MATRIZ, grupo_obstaculos, grupo_coletaveis, grupo_mato)

try:
    protagonista = Player(player_pos[0], player_pos[1], os.path.join(DIRETORIO_BASE, "assets/mc/mc_down.png"), os.path.join(DIRETORIO_BASE, "assets/mc/mc_left.png"), os.path.join(DIRETORIO_BASE, "assets/mc/mc_up.png"), os.path.join(DIRETORIO_BASE, "assets/mc/mc_right.png"))
    player_group = pg.sprite.GroupSingle(protagonista)
except FileNotFoundError: 
    print("ERRO: Imagens do player não encontradas."); exit()

menu_inv = MenuInventario()
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, map_w, map_h)
caminho_img_tileset = os.path.join(DIRETORIO_BASE, "assets/backgrounds/tileset.png")
fundo_grama = definir_piso(map_w, map_h, caminho_img_tileset)

charmander = criar_pokemon("Charmander", 5)
squirtle = criar_pokemon("Squirtle", 5)
equipe_jogador = [charmander, squirtle] 

jogo_ativo = exibir_intro(screen)
nome_jogador = "Player"

if jogo_ativo:
    jogo_ativo, nome_escolhido = cena_professor(screen)
    if nome_escolhido:
        nome_jogador = nome_escolhido
        if jogo_ativo:
            try: 
                pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3")); pg.mixer.music.set_volume(0.2); pg.mixer.music.play(-1, fade_ms=2000)
            except: pass

# --- CONFIGURAÇÃO DO TEXTO DE AVISO (Estilo Pokémon) ---
# Usamos 'courier new' para dar um ar mais "computador/game boy" sem mudar as outras fontes
font_aviso = pg.font.SysFont("courier new", 20, bold=True)

# Cores da caixa estilo Pokémon
POKE_BLUE = (48, 80, 192)     # Borda
POKE_WHITE = (248, 248, 248)  # Fundo
POKE_BLACK = (32, 32, 32)     # Texto

texto_aviso = font_aviso.render('Pressione a tecla "Q" para coletar este item.', True, POKE_BLACK)

# --- LOOP DO JOGO ---
estado_jogo = "MUNDO"
sistema_batalha = None
running = jogo_ativo 

while running:
    if estado_jogo == "MUNDO":
        for event in pg.event.get():
            if event.type == pg.QUIT: running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e: menu_inv.alternar() 

                if event.key == pg.K_q:
                    area_interacao = protagonista.rect.inflate(10, 10)
                    for item in grupo_coletaveis:
                        if area_interacao.colliderect(item.rect):
                            item.coletar(protagonista)

        antigo_rect = protagonista.rect.copy()
        player_group.update()
        
        if protagonista.direction.magnitude() > 0:
            if pg.sprite.spritecollide(protagonista, grupo_mato, False):
                if random.random() < 0.015: 
                    animacao_transicao(screen)
                    estado_jogo = "BATALHA"
                    inimigo_pokemon = criar_pokemon("Bulbasaur", random.randint(3, 5))
                    inv_batalha = {'Pocao': 5, 'Pokebola': 5}
                    try:
                        if hasattr(menu_inv, 'itens'): inv_batalha = menu_inv.itens
                        elif hasattr(protagonista, 'inventario') and hasattr(protagonista.inventario, 'itens'): inv_batalha = protagonista.inventario.itens
                    except: pass

                    try:
                        sistema_batalha = BatalhaPokemon(equipe_jogador, inimigo_pokemon, inv_batalha)
                    except Exception as e:
                        print(f"ERRO: {e}"); estado_jogo = "MUNDO"

        colisao_obs = pg.sprite.spritecollide(protagonista, grupo_obstaculos, False)
        colisao_item = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False)
        if colisao_obs or colisao_item: protagonista.rect = antigo_rect
        
        camera.update(protagonista.rect)
        
        screen.fill((0,0,0)) 
        screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))

        for item in grupo_mato: screen.blit(item.image, camera.apply(item.rect))
        for parede in grupo_obstaculos: screen.blit(parede.image, camera.apply(parede.rect))
        for item in grupo_coletaveis: screen.blit(item.image, camera.apply(item.rect))
        for sprite in player_group: screen.blit(sprite.image, camera.apply(sprite.rect))
        
        menu_inv.desenhar(screen, protagonista.inventario)

        # --- EXIBIR AVISO "PRESSIONE Q" (Estilo Pokémon) ---
        area_check = protagonista.rect.inflate(10, 10)
        aviso_ativo = False
        for item in grupo_coletaveis:
            if area_check.colliderect(item.rect):
                aviso_ativo = True
                break
        
        if aviso_ativo:
            padding_box = 10
            largura_box = texto_aviso.get_width() + padding_box * 2
            altura_box = texto_aviso.get_height() + padding_box * 2
            
            x_pos = SCREEN_WIDTH // 2 - largura_box // 2
            y_pos = SCREEN_HEIGHT - 60
            
            rect_aviso = pg.Rect(x_pos, y_pos, largura_box, altura_box)
            
            # Desenha borda azul arredondada
            pg.draw.rect(screen, POKE_BLUE, rect_aviso, border_radius=8)
            # Desenha interior branco
            pg.draw.rect(screen, POKE_WHITE, rect_aviso.inflate(-6, -6), border_radius=6)
            # Desenha texto
            screen.blit(texto_aviso, (x_pos + padding_box, y_pos + padding_box))

    elif estado_jogo == "BATALHA":
        for event in pg.event.get():
            if event.type == pg.QUIT: running = False
            if event.type == pg.KEYDOWN:
                if sistema_batalha and sistema_batalha.battle_over:
                    if event.key == pg.K_SPACE:
                        if sistema_batalha.vencedor == "INIMIGO": print("GAME OVER"); running = False
                        else:
                            estado_jogo = "MUNDO"
                            try: pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3")); pg.mixer.music.play(-1)
                            except: pass
                else:
                    if sistema_batalha: sistema_batalha.processar_input(event)

        if sistema_batalha: sistema_batalha.desenhar(screen)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
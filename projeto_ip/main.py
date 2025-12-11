import pygame as pg
from player import Player
from camera import Camera
from coletaveis import Pokebola, GreatBall, Pocao
from inventario import MenuInventario
from Obstaculo import Obstaculo
import os 

DIRETORIO_BASE = os.path.dirname(__file__)
# --- Configurações Globais ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48 
FPS = 60

# --- 1. DEFINIÇÃO DO MAPA ---
MAPA_MATRIZ = [
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', 'P', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'G', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'B', '.', '.', '.', 'T', 'T', 'T', 'M', 'T', 'T', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'G', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
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

# --- Função para Ler o Mapa ---
def carregar_mapa(mapa, grupo_obs, grupo_col):
    pos_player = (100, 100)
    for row_index, row in enumerate(mapa):
        for col_index, letra in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if letra == 'T': grupo_obs.add(Obstaculo(x, y))
            elif letra == 'B': grupo_col.add(Pokebola(x, y))
            elif letra == 'G': grupo_col.add(GreatBall(x, y))
            elif letra == 'H': grupo_col.add(Pocao(x, y))
            elif letra == 'P': pos_player = (x, y)
    return len(mapa[0]) * TILE_SIZE, len(mapa) * TILE_SIZE, pos_player

def exibir_intro(screen):
    intro = True
    font_titulo = pg.font.SysFont("Arial", 50, bold=True) 
    font_start = pg.font.SysFont("Arial", 30, bold=True)
    texto_titulo = font_titulo.render("PokéCIn - Ameaça do Mangue", True, (0, 0, 0))
    texto_start = font_start.render("Pressione ENTER para Jogar", True, (50, 50, 50))
    rect_titulo = texto_titulo.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    rect_start = texto_start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

    bg_intro = None
    try:
        caminho_bg = os.path.join(DIRETORIO_BASE, "assets/backgrounds/intro_bg.jpg")
        img_raw = pg.image.load(caminho_bg).convert()
        bg_intro = pg.transform.scale(img_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        bg_intro = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); bg_intro.fill((255, 255, 255))

    # --- MÚSICA INTRO ---
    try:
        caminho_musica = os.path.join(DIRETORIO_BASE, "assets/músicas/intro.mp3")
        pg.mixer.music.load(caminho_musica)
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(-1, start=1.0)
    except pg.error:
        pass

    while intro:
        clock.tick(15)
        for event in pg.event.get():
            if event.type == pg.QUIT: return False 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN: 
                    intro = False 
                    # Fadeout de 1 segundo (a música vai baixando)
                    pg.mixer.music.fadeout(1000)
                    return True

        screen.blit(bg_intro, (0,0))
        screen.blit(texto_titulo, rect_titulo)
        screen.blit(texto_start, rect_start)
        pg.display.flip()
    return True

def cena_professor(screen):
    # --- CONFIGURAÇÕES VISUAIS ---
    COR_CAIXA = (255, 255, 255); COR_BORDA = (40, 40, 160); COR_TEXTO = (0, 0, 0)
    font_texto = pg.font.SysFont("Arial", 22); font_nome = pg.font.SysFont("Arial", 30, bold=True)

    # --- CARREGAR EFEITO SONORO (SFX) ---
    sfx_blip = None
    try:
        caminho_sfx = os.path.join(DIRETORIO_BASE, "assets/sfx/sfx_blip.wav")
        sfx_blip = pg.mixer.Sound(caminho_sfx)
        sfx_blip.set_volume(0.3) # Volume do efeito
    except FileNotFoundError:
        print("Aviso: SFX 'blip.wav' não encontrado.")

    # --- CARREGAR MÚSICA DO PROFESSOR ---
    try:
        caminho_musica_lab = os.path.join(DIRETORIO_BASE, "assets/músicas/professor_theme.mp3") 
        pg.mixer.music.load(caminho_musica_lab)
        pg.mixer.music.set_volume(0.2) 
        pg.mixer.music.play(-1, fade_ms=2000) 
    except pg.error:
        pass

    # --- CARREGAR IMAGENS ---
    try:
        img_bg_raw = os.path.join(DIRETORIO_BASE, "assets/backgrounds/lab.jpg")
        bg_imagem = pg.transform.scale(pg.image.load(img_bg_raw).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        bg_imagem = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); bg_imagem.fill((200, 200, 250))

    try:
        img_prof_raw = os.path.join(DIRETORIO_BASE, "assets/professor/professor.png")
        img_professor = pg.transform.scale(pg.image.load(img_prof_raw).convert_alpha(), (400, 400)) 
    except FileNotFoundError:
        img_professor = pg.Surface((400, 400)); img_professor.fill((100, 100, 100))

    # --- ROTEIRO ---
    falas_intro = [
        "Olá! Bem-vindo ao fantástico mundo de Pokémon",
        "Esse mundo é habitado por diversas criaturas misteriosas",
        "Meu nome é Ricardo Massa",
        "As pessoas me chamam de Professor de Python.",
        "Estamos precisando de ajuda aqui no CIn.",
        "O Coletivo Mangue Vermelho quer usar seus Pokémons\npara destruir nossos computadores!",
        "Precisamos de alguém para derrotá-los!",
        "Será que você é o candidato ideal?",
        "Antes que eu forneça Pokémons Fortes para você usar contra eles",
        "Vamos fazer um teste para ver sua competência",
        "Mas primeiro, diga-me algo sobre você."
    ]
    falas_final = [
        "Ah, certo! Então seu nome é {NOME}?", 
        "Forme uma equipe de até 6 pokémons e me desafie numa batalha",
        "Se você me vencer, será destinado a enfrentar o Mangue Vermelho!!",
        "Sua jornada começa agora!",
        "Escolha um dos 3 Pokémons na mesa",
        "Após isso, sinta-se à vontade para capturar mais alguns no mato",
        "Estarei esperando por você!"
    ]

    # --- VARIÁVEIS ---
    indice = 0; estado = "INTRO"; nome_digitado = ""; nome_final = "Player"
    rect_caixa = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
    clock = pg.time.Clock(); running = True
    
    while running:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT: return False, None
            if event.type == pg.KEYDOWN:
                
                # -- ESTADO DE DIÁLOGO --
                if estado == "INTRO" or estado == "FINAL":
                    if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        
                        if sfx_blip: sfx_blip.play()

                        indice += 1
                        if estado == "INTRO" and indice >= len(falas_intro): estado = "INPUT"; indice = 0
                        elif estado == "FINAL" and indice >= len(falas_final): 
                            pg.mixer.music.fadeout(1000)
                            return True, nome_final

                # -- ESTADO DE DIGITAR NOME --
                elif estado == "INPUT":
                    if event.key == pg.K_RETURN:
                        if len(nome_digitado) > 0: 
                            if sfx_blip: sfx_blip.play()
                            
                            nome_final = nome_digitado; estado = "FINAL"; indice = 0
                    elif event.key == pg.K_BACKSPACE: 
                        nome_digitado = nome_digitado[:-1]
                    else:
                        if len(nome_digitado) < 10 and event.unicode.isprintable(): 
                            nome_digitado += event.unicode

        screen.blit(bg_imagem, (0, 0))
        prof_x = SCREEN_WIDTH // 2 - img_professor.get_width() // 2; prof_y = 40 
        largura_sombra = 300; altura_sombra = 40
        sombra_x = prof_x + (img_professor.get_width() - largura_sombra) // 2; sombra_y = prof_y + 360
        sombra_surf = pg.Surface((largura_sombra, altura_sombra), pg.SRCALPHA)
        pg.draw.ellipse(sombra_surf, (0, 0, 0, 80), (0,0, largura_sombra, altura_sombra))
        screen.blit(sombra_surf, (sombra_x, sombra_y))
        screen.blit(img_professor, (prof_x, prof_y))
        
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
            if pg.time.get_ticks() % 1000 < 500:
                pg.draw.polygon(screen, (200, 0, 0), [(rect_interno.right - 30, rect_interno.bottom - 20), (rect_interno.right - 10, rect_interno.bottom - 20), (rect_interno.right - 20, rect_interno.bottom - 10)])
        pg.display.flip()
    return False, None

# --- INICIALIZAÇÃO ---
pg.init()
pg.mixer.init() # Garante que o som inicie
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("PokeCIn - Fim do Mangue Vermelho")
clock = pg.time.Clock()

# Grupos e Mapa
grupo_obstaculos = pg.sprite.Group()
grupo_coletaveis = pg.sprite.Group()
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
    exit()

menu_inv = MenuInventario()
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, map_w, map_h)
fundo_grama = pg.Surface((map_w, map_h))
fundo_grama.fill((34, 139, 34)) 

# --- FLUXO DO JOGO ---
jogo_ativo = exibir_intro(screen)
nome_jogador = "Player"

# 1. Cena do Professor
if jogo_ativo:
    jogo_ativo, nome_escolhido = cena_professor(screen)
    
    if nome_escolhido:
        nome_jogador = nome_escolhido
        print(f"Bem-vindo ao mangue, {nome_jogador}!") 
        
        # 2. Carregar MÚSICA DO MUNDO
        # Só carrega se o jogo continuar ativo após o professor
        if jogo_ativo:
            try:
                caminho_world = os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3")
                pg.mixer.music.load(caminho_world)
                pg.mixer.music.set_volume(0.2) # Ajuste o volume se precisar
                
                # Toca em loop infinito com entrada suave de 2 segundos
                pg.mixer.music.play(-1, fade_ms=2000) 
            except pg.error:
                print("Erro: Música 'world_theme.mp3' não encontrada.")

running = jogo_ativo 

# 3. Loop Principal
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                menu_inv.alternar() 

    antigo_rect = protagonista.rect.copy()
    player_group.update()
    
    # Colisão com Obstáculos
    if pg.sprite.spritecollide(protagonista, grupo_obstaculos, False):
        protagonista.rect = antigo_rect

    # Câmera
    camera.update(protagonista.rect)
    
    # Coletáveis
    hits = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False)
    for item in hits:
        item.coletar(protagonista)

    # --- DESENHO ---
    screen.fill((0,0,0)) 
    
    # 1. Fundo
    screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))

    # 2. Objetos
    for parede in grupo_obstaculos:
        screen.blit(parede.image, camera.apply(parede.rect))
    for item in grupo_coletaveis:
        screen.blit(item.image, camera.apply(item.rect))
    
    # 3. Player
    for sprite in player_group:
        screen.blit(sprite.image, camera.apply(sprite.rect))
        
    # 4. Interface
    menu_inv.desenhar(screen, protagonista.inventario)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
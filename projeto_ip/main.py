import pygame as pg
from player import Player
from camera import Camera
from coletaveis import Pokebola, Pocao, GreatBall 
from inventario import MenuInventario
import os # Importante para garantir caminhos de arquivo

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

# --- Função para Ler o Mapa ---
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

def exibir_intro(screen):
    intro = True
    font = pg.font.SysFont("Arial", 40)
    texto_titulo = font.render("PokéCIn - Ameaça do Mangue", True, (255, 255, 255))
    texto_start = font.render("Pressione ENTER para Jogar", True, (200, 200, 200))

    rect_titulo = texto_titulo.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    rect_start = texto_start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

    while intro:
        clock.tick(15)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN: 
                    intro = False 
                    return True

        screen.fill((0, 0, 0))
        screen.blit(texto_titulo, rect_titulo)
        screen.blit(texto_start, rect_start)
        pg.display.flip()
    return True

def cena_professor(screen):
    # --- CONFIGURAÇÕES VISUAIS ---
    COR_CAIXA = (255, 255, 255)      
    COR_BORDA = (40, 40, 160)        
    COR_TEXTO = (0, 0, 0)
    
    font_texto = pg.font.SysFont("Arial", 22)
    font_nome = pg.font.SysFont("Arial", 30, bold=True)

    # --- CARREGAR IMAGENS ---
    # 1. Fundo
    try:
        img_bg_raw = pg.image.load("assets/backgrounds/lab.jpg").convert()
        bg_imagem = pg.transform.scale(img_bg_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        print("Aviso: Background não encontrado. Usando cor sólida.")
        bg_imagem = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_imagem.fill((200, 200, 250))

    # 2. Professor
    try:
        img_prof_raw = pg.image.load("assets/professor/professor.png").convert_alpha()
        img_professor = pg.transform.scale(img_prof_raw, (400, 400)) 
    except FileNotFoundError:
        print("Erro: Imagem do professor não encontrada.")
        img_professor = pg.Surface((400, 400))
        img_professor.fill((100, 100, 100))

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
    indice = 0
    estado = "INTRO"
    nome_digitado = ""
    nome_final = "Player"
    rect_caixa = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
    clock = pg.time.Clock()
    running = True
    
    while running:
        clock.tick(30)
        
        # --- EVENTOS ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False, None

            if event.type == pg.KEYDOWN:
                if estado == "INTRO" or estado == "FINAL":
                    if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        indice += 1
                        if estado == "INTRO" and indice >= len(falas_intro):
                            estado = "INPUT"
                            indice = 0
                        elif estado == "FINAL" and indice >= len(falas_final):
                            return True, nome_final

                elif estado == "INPUT":
                    if event.key == pg.K_RETURN:
                        if len(nome_digitado) > 0:
                            nome_final = nome_digitado
                            estado = "FINAL"
                            indice = 0
                    elif event.key == pg.K_BACKSPACE:
                        nome_digitado = nome_digitado[:-1]
                    else:
                        if len(nome_digitado) < 10 and event.unicode.isprintable():
                            nome_digitado += event.unicode

        # --- DESENHOS ---
        
        # 1. Fundo
        screen.blit(bg_imagem, (0, 0))

        # 2. Professor (Centralizado)
        prof_x = SCREEN_WIDTH // 2 - img_professor.get_width() // 2
        prof_y = 40 
        
        # Sombra posição
        largura_sombra = 300
        altura_sombra = 40
        sombra_x = prof_x + (img_professor.get_width() - largura_sombra) // 2
        sombra_y = prof_y + 360 # 40 (pos Y) + 360 (altura relativa)

        sombra_surf = pg.Surface((largura_sombra, altura_sombra), pg.SRCALPHA)
        pg.draw.ellipse(sombra_surf, (0, 0, 0, 80), (0,0, largura_sombra, altura_sombra))
        screen.blit(sombra_surf, (sombra_x, sombra_y))

        # Desenha o sprite do professor
        screen.blit(img_professor, (prof_x, prof_y))
        
        # 3. Caixa de Diálogo
        pg.draw.rect(screen, COR_BORDA, rect_caixa, border_radius=10)
        rect_interno = rect_caixa.inflate(-10, -10)
        pg.draw.rect(screen, COR_CAIXA, rect_interno, border_radius=10)
        
        # --- LÓGICA DO TEXTO ---
        texto_para_exibir = ""
        
        if estado == "INTRO":
            if indice < len(falas_intro):
                texto_para_exibir = falas_intro[indice]
                
        elif estado == "FINAL":
            if indice < len(falas_final):
                texto_para_exibir = falas_final[indice].replace("{NOME}", nome_final)
        
        elif estado == "INPUT":
            pergunta = font_texto.render("Qual é o seu nome?", True, COR_TEXTO)
            screen.blit(pergunta, (rect_interno.x + 20, rect_interno.y + 20))
            txt_nome = font_nome.render(nome_digitado + "_", True, (0, 0, 200))
            screen.blit(txt_nome, (rect_interno.x + 20, rect_interno.y + 60))
            dica = font_texto.render("(ENTER para confirmar)", True, (150, 150, 150))
            screen.blit(dica, (rect_interno.x + 20, rect_interno.y + 100))

        # Renderiza o texto multilinha
        if texto_para_exibir != "":
            linhas = texto_para_exibir.split('\n')
            y_atual = rect_interno.y + 20
            for linha in linhas:
                surf_linha = font_texto.render(linha, True, COR_TEXTO)
                screen.blit(surf_linha, (rect_interno.x + 20, y_atual))
                y_atual += 30 

            if pg.time.get_ticks() % 1000 < 500:
                pg.draw.polygon(screen, (200, 0, 0), [
                    (rect_interno.right - 30, rect_interno.bottom - 20),
                    (rect_interno.right - 10, rect_interno.bottom - 20),
                    (rect_interno.right - 20, rect_interno.bottom - 10)
                ])

        pg.display.flip()
        
    return False, None

# --- INICIALIZAÇÃO ---
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("PokeCIn - Fim do Mangue Vermelho")
clock = pg.time.Clock()

# Grupos
grupo_obstaculos = pg.sprite.Group()
grupo_coletaveis = pg.sprite.Group()

# 3. Carregando o Mapa
map_w, map_h, player_pos = carregar_mapa(MAPA_MATRIZ, grupo_obstaculos, grupo_coletaveis)

# 4. Player
try:
    protagonista = Player(player_pos[0], player_pos[1], 
                          "assets/mc/mc_down.png", 
                          "assets/mc/mc_left.png", 
                          "assets/mc/mc_up.png", 
                          "assets/mc/mc_right.png")
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

if jogo_ativo:
    jogo_ativo, nome_escolhido = cena_professor(screen)
    if nome_escolhido:
        nome_jogador = nome_escolhido
        print(f"Bem-vindo ao mangue, {nome_jogador}!") 

running = jogo_ativo 

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                menu_inv.alternar() 

    antigo_rect = protagonista.rect.copy()
    player_group.update()
    
    if pg.sprite.spritecollide(protagonista, grupo_obstaculos, False):
        protagonista.rect = antigo_rect

    camera.update(protagonista.rect)
    
    hits = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False)
    for item in hits:
        item.coletar(protagonista)

    screen.fill((0,0,0)) 
    screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))

    for parede in grupo_obstaculos:
        screen.blit(parede.image, camera.apply(parede.rect))
    for item in grupo_coletaveis:
        screen.blit(item.image, camera.apply(item.rect))
    for sprite in player_group:
        screen.blit(sprite.image, camera.apply(sprite.rect))
        
    menu_inv.desenhar(screen, protagonista.inventario)
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
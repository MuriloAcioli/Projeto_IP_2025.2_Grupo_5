import pygame as pg
import os
import random
import math
# =============================================================================
# CONFIGURAÇÕES LOCAIS
# =============================================================================
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48

# =============================================================================
# FUNÇÕES DE AMBIENTE (GRÁFICOS)
# =============================================================================

def definir_piso(largura_mapa, altura_mapa, caminho_tileset):
    """
    Gera uma superfície estática com tiles de grama aleatórios.
    Isso otimiza o jogo, pois não precisamos redesenhar cada tile por frame.
    """
    superficie_chao = pg.Surface((largura_mapa, altura_mapa))
    
    # Tenta carregar o tileset
    try:
        img_tileset = pg.image.load(caminho_tileset).convert_alpha()
    except FileNotFoundError:
        print("AVISO: Tileset não encontrado. Usando cor sólida.")
        superficie_chao.fill((34, 139, 34))
        return superficie_chao

    # Configurações de recorte do Tileset (64x64 original)
    TAMANHO_ORIGINAL = 64
    
    # Coordenadas (coluna, linha) na imagem do tileset
    TILE_PADRAO = (0, 0)
    TILE_GRAMA_LISA = (2, 1)
    TILE_GRAMA_DETALHE = (3, 0)
    TILE_DETALHEZINHO_GRAMA_SD = (0, 4)
    TILE_DETALHEZINHO_GRAMA_BD = (1, 4)
  

    # Lista de probabilidade (Mais grama simples, poucas flores)
    opcoes = [TILE_GRAMA_LISA] * 15 + [TILE_PADRAO] * 40 + [TILE_GRAMA_DETALHE] * 30 + [TILE_DETALHEZINHO_GRAMA_SD] * 5 + [TILE_DETALHEZINHO_GRAMA_BD] * 5 
    # Preenche a superfície do chão
    for y in range(0, altura_mapa, TILE_SIZE):
        for x in range(0, largura_mapa, TILE_SIZE):
            escolha = random.choice(opcoes)
            coluna_img, linha_img = escolha
            
            # Recorta o tile da imagem original
            rect_recorte = pg.Rect(coluna_img * TAMANHO_ORIGINAL, 
                                   linha_img * TAMANHO_ORIGINAL, 
                                   TAMANHO_ORIGINAL, TAMANHO_ORIGINAL)
            
            tile_imagem = img_tileset.subsurface(rect_recorte)
            
            # Escala para o tamanho do jogo (48x48)
            tile_escalado = pg.transform.scale(tile_imagem, (TILE_SIZE, TILE_SIZE))
            
            # Desenha na superfície final
            superficie_chao.blit(tile_escalado, (x, y))

    return superficie_chao


# =============================================================================
# FUNÇÕES DE CENA (HISTÓRIA E UI)
# =============================================================================

def exibir_intro(screen, clock):
    """Exibe a tela de título inicial."""
    intro = True
    
    # Fontes
    font_titulo = pg.font.SysFont("Arial", 50, bold=True)
    font_start = pg.font.SysFont("Arial", 30, bold=True)

    texto_titulo = font_titulo.render("PokéCIn: a Ameaça do Mangue", True, (0,0,0))
    
    try:
        img_titulo = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/intro_font/PokeCin.png")).convert_alpha(), (600, 300))
    except Exception as e:
        print(f"Erro ao carregar imagem do título: {e}")
        img_titulo = font_titulo.render("PokéCIn", True, (0,0,0))

    try: 
        img_enter = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/intro_font/PressEnter.png")).convert_alpha(), (400, 200))
    except Exception as e:
        print(f"Erro ao carregar imagem do ENTER: {e}")
        img_enter = font_start.render("ENTER para Jogar", True, (50,50,50))

    texto_start = font_start.render("ENTER para Jogar", True, (50,50,50))
    
    rect_titulo = texto_titulo.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    rect_start = texto_start.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50))
    
    # Assets da Intro
    try: 
        bg_intro = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/backgrounds/intro_bg.jpg")).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
    except: 
        bg_intro = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); bg_intro.fill((255,255,255))
        
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
        screen.blit(img_titulo, (SCREEN_WIDTH/2 - img_titulo.get_width()/2, 0))

        if pg.time.get_ticks() %1000 < 600:
            pos_x_enter =   SCREEN_WIDTH //2 - img_enter.get_width() // 2
            screen.blit(img_enter, (pos_x_enter, 350))

        pg.display.flip()
        
    return True


def cena_professor(screen, clock):
    """Gerencia a cena do Professor Python e a entrada do nome do jogador."""
    
    # Cores e Fontes
    COR_CAIXA = (255, 255, 255)
    COR_BORDA = (40, 40, 160)
    COR_TEXTO = (0, 0, 0)
    font_texto = pg.font.SysFont("Arial", 22)
    font_nome = pg.font.SysFont("Arial", 30, bold=True)
    
    # --- Carregamento de Assets ---
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
        # Imagem padrão (Professor 1)
        img_professor1 = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/professor/proff_massa_1.png")).convert_alpha(), (400, 400)) 
    except: 
        print("Erro ao carregar proff_massa_1.png")
        img_professor1 = pg.Surface((400, 400)); img_professor1.fill((100, 100, 100))
          
    try:
        
        prop = 637/1024
        base = 370
        
        img_original = pg.image.load(os.path.join(DIRETORIO_BASE, "assets/professor/proff_massa_2.png")).convert_alpha()
        
        novo_tamanho = (int(base * prop), int(base))
        
        img_professor2 = pg.transform.scale(img_original, novo_tamanho)

    except Exception as e:
        print(f"Erro ao carregar proff_massa_2.png: {e}")
        img_professor2 = img_professor1


    # --- Roteiro ---
    falas_intro = [
        "Olá! Bem-vindo ao fantástico mundo de Pokémon.", 
        "Esse mundo é habitado por diversas criaturas misteriosas.", 
        "Meu nome é Ricardo Massa.", 
        "As pessoas me chamam de Professor Python.", 
        "Estamos precisando de ajuda aqui no CIn.", 
        "O Coletivo Mangue Vermelho quer usar seus Pokémons\npara destruir nossos computadores!", 
        "Precisamos de alguém para derrotá-los!", 
        "Será que você é o candidato ideal?", 
        #"Antes que eu forneça Pokémons Fortes para você usar contra eles", 
        "Vamos fazer um teste para ver sua competência.", 
        "Mas primeiro, diga-me algo sobre você."
    ]

    indice_troca_imagem = len(falas_intro) - 1

    falas_final = [
        "Ah, certo! Então seu nome é {NOME}?", 
        "Forme uma equipe de até 6 pokémons e me desafie numa batalha.", 
        "Se você me vencer, será destinado a enfrentar o Mangue Vermelho!!", 
        "Sua jornada começa agora!", 
        "Escolha um dos 3 Pokémons na mesa.", 
        "Após isso, sinta-se à vontade para capturar mais alguns no mato.", 
        "Te dei três Pokébolas e uma Poção de Vida para começar, boa sorte!", 
        "Estarei esperando por você!"
    ]
    
    # Estado da Cena
    indice = 0
    estado = "INTRO"
    nome_digitado = ""
    nome_final = "Player"
    rect_caixa = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
    
    running = True
    
    while running:
        clock.tick(30)
        
        for event in pg.event.get():
            if event.type == pg.QUIT: return False, None, None # Retorna 3 valores agora
            
            if event.type == pg.KEYDOWN:
                # Navegação nos diálogos
                if estado == "INTRO" or estado == "FINAL":
                    if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        if sfx_blip: sfx_blip.play()
                        indice += 1
                        if estado == "INTRO" and indice >= len(falas_intro): 
                            estado = "INPUT"
                            indice = 0
                        elif estado == "FINAL" and indice >= len(falas_final): 
                            # ACABOU O DIÁLOGO, VAI PARA A SELEÇÃO
                            pokemon_escolhido = escolher_pokemon(screen, clock)
                            pg.mixer.music.fadeout(1000)
                            # Retorna: Sucesso, Nome, Pokemon
                            return True, nome_final, pokemon_escolhido
                
                # Input de texto (Nome)
                elif estado == "INPUT":
                    if event.key == pg.K_RETURN:
                        if len(nome_digitado) > 0: 
                            if sfx_blip: sfx_blip.play()
                            nome_final = nome_digitado
                            estado = "FINAL"
                            indice = 0
                    elif event.key == pg.K_BACKSPACE: 
                        nome_digitado = nome_digitado[:-1]
                    else:
                        if len(nome_digitado) < 10 and event.unicode.isprintable(): 
                            nome_digitado += event.unicode
                        
        # --- Desenho ---
        screen.blit(bg_imagem, (0, 0))
        
        # Professor + Sombra
        prof_x = SCREEN_WIDTH // 2 - img_professor1.get_width() // 2
        
        prof_y = 40 
        largura_sombra = 300
        altura_sombra = 40
        sombra_x = prof_x + (img_professor1.get_width() - largura_sombra) // 2
        sombra_y = prof_y + 360
        sombra_surf = pg.Surface((largura_sombra, altura_sombra), pg.SRCALPHA)
        pg.draw.ellipse(sombra_surf, (0, 0, 0, 80), (0,0, largura_sombra, altura_sombra))
        screen.blit(sombra_surf, (sombra_x, sombra_y))

        # ### ALTERADO: Lógica para escolher qual imagem desenhar ###
        img_atual = img_professor1 # Começa com a imagem padrão

        # Se estamos na fase de INTRO E o índice atual é o da fala específica:
        if estado == "INTRO" and (indice == indice_troca_imagem or indice == indice_troca_imagem - 1):
             img_atual = img_professor2
             prof_x = SCREEN_WIDTH // 2 - img_professor2.get_width() // 2
             prof_y = 70
        elif estado == "FINAL" and indice in (1,2):
             img_atual = img_professor2
             prof_x = SCREEN_WIDTH // 2 - img_professor2.get_width() // 2
             prof_y = 70
        
        screen.blit(img_atual, (prof_x, prof_y))
        
        # Caixa de Texto
        pg.draw.rect(screen, COR_BORDA, rect_caixa, border_radius=10)
        rect_interno = rect_caixa.inflate(-10, -10)
        pg.draw.rect(screen, COR_CAIXA, rect_interno, border_radius=10)
        
        # Conteúdo do Texto
        texto_para_exibir = ""
        if estado == "INTRO":
            if indice < len(falas_intro): texto_para_exibir = falas_intro[indice]
        elif estado == "FINAL":
            if indice < len(falas_final): texto_para_exibir = falas_final[indice].replace("{NOME}", nome_final)
        elif estado == "INPUT":
            pergunta = font_texto.render("Qual é o seu nome?", True, COR_TEXTO)
            screen.blit(pergunta, (rect_interno.x + 20, rect_interno.y + 20))
            txt_nome = font_nome.render(nome_digitado + "_", True, (0, 0, 200))
            screen.blit(txt_nome, (rect_interno.x + 20, rect_interno.y + 60))
            dica = font_texto.render("(ENTER para confirmar)", True, (150, 150, 150))
            screen.blit(dica, (rect_interno.x + 20, rect_interno.y + 100))
            
        # Renderiza texto com quebra de linha
        if texto_para_exibir != "":
            linhas = texto_para_exibir.split('\n')
            y_atual = rect_interno.y + 20
            for linha in linhas:
                surf_linha = font_texto.render(linha, True, COR_TEXTO)
                screen.blit(surf_linha, (rect_interno.x + 20, y_atual))
                y_atual += 30 
            
            # Animação da setinha
            if pg.time.get_ticks() % 1000 < 500: 
                pg.draw.polygon(screen, (200, 0, 0), [
                    (rect_interno.right - 30, rect_interno.bottom - 20), 
                    (rect_interno.right - 10, rect_interno.bottom - 20), 
                    (rect_interno.right - 20, rect_interno.bottom - 10)
                ])
            
        pg.display.flip()
    return False, None, None


def animacao_transicao(screen):
    """Efeito visual de piscar a tela antes da batalha."""
    try:
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/battle_theme.mp3"))
        pg.mixer.music.play(-1)
    except: pass
    
    for i in range(8): 
        screen.fill((255, 255, 255))
        pg.display.flip()
        pg.time.delay(160)
        screen.fill((10, 10, 10))
        pg.display.flip()
        pg.time.delay(160)

def animacao_treinador(screen):
    """Efeito visual de piscar a tela antes da batalha."""
    try:
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/trainer_theme.mp3"))
        pg.mixer.music.play(-1)
    except: pass
    
    for i in range(8): 
        screen.fill((255, 255, 255))
        pg.display.flip()
        pg.time.delay(160)
        screen.fill((10, 10, 10))
        pg.display.flip()
        pg.time.delay(160)

# =============================================================================
# NOVA FUNÇÃO: SELEÇÃO DE INICIAL
# =============================================================================
def escolher_pokemon(screen, clock):
    """Tela de seleção do Pokémon inicial com sprites e pokébolas."""
    
    # Configuração de Fontes e Cores
    font_titulo = pg.font.SysFont("Arial", 40, bold=True)
    font_nome = pg.font.SysFont("Arial", 30, bold=True)
    
    # --- Carregar Assets ---
    # Fundo (Lab)
    try:
        bg = pg.image.load(os.path.join(DIRETORIO_BASE, "assets/backgrounds/lab.jpg")).convert()
        bg = pg.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        bg = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((200, 200, 200))
        
    # Imagem da Pokébola

    path_balls = os.path.join(DIRETORIO_BASE, "assets/coletaveis/pokebolas.png")
    sheet_balls = pg.image.load(path_balls).convert_alpha()
            # Recorta as bolas ( x=0, x=11, x=23 | w=12, h=12)
            # Escalamos para 32x32 para ficar visível na tela
    scale_size = (48, 48)
            

    pokebola_img = sheet_balls.subsurface((0, 0, 12, 12))

    pokebola_img = pg.transform.scale(pokebola_img, (42, 42))
 
 

    # Dados dos Iniciais
    iniciais = [
        {"nome": "Soim", "arquivo": "assets/pokemons/soim.png", "cor": (0, 180, 0)},
        {"nome": "Flamare", "arquivo": "assets/pokemons/flamare.png", "cor": (255, 100, 0)},
        {"nome": "Caprio", "arquivo": "assets/pokemons/caprio.png", "cor": (50, 100, 255)}
    ]
    
    # Carregar Sprites dos Pokémons
    for p in iniciais:
        try:
            img = pg.image.load(os.path.join(DIRETORIO_BASE, p["arquivo"])).convert_alpha()
            # Aumenta um pouco o sprite para a seleção
            p["sprite"] = pg.transform.scale(img, (160, 160))
        except:
            p["sprite"] = pg.Surface((160, 160))
            p["sprite"].fill(p["cor"])

    selecionado = 1 # Começa no meio (Charmander)
    running = True
    
    # Posições
    espacamento = 200
    centro_x = SCREEN_WIDTH // 2
    y_bolas = 400
    
    while running:
        clock.tick(30)
        
        # --- Eventos ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return None # Sai do jogo
            
            if event.type == pg.KEYDOWN:
                # Mover seleção
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    selecionado = (selecionado - 1) % 3
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    selecionado = (selecionado + 1) % 3
                
                # Confirmar
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    return iniciais[selecionado]["nome"]

        # --- Desenho ---
        screen.blit(bg, (0, 0))
        
        # Título
        titulo_surf = font_titulo.render("Escolha seu Parceiro!", True, (0, 0, 0))
        # Sombra do título
        titulo_sombra = font_titulo.render("Escolha seu Parceiro!", True, (200, 200, 200))
        
        rect_titulo = titulo_surf.get_rect(center=(centro_x, 100))
        screen.blit(titulo_sombra, (rect_titulo.x + 2, rect_titulo.y + 2))
        screen.blit(titulo_surf, rect_titulo)
        
        # Desenha as 3 Pokébolas e o Pokémon selecionado
        for i in range(3):
            # Calcula X: Esquerda, Centro, Direita
            pos_x = centro_x + (i - 1) * espacamento
            
            # Desenha Pokébola
            rect_bola = pokebola_img.get_rect(center=(pos_x, y_bolas))
            screen.blit(pokebola_img, rect_bola)
            
            # Se for o selecionado, mostra o Pokémon em cima
            if i == selecionado:
                p = iniciais[i]
                
                # Sprite pulando levemente (Animação simples)
                tempo = pg.time.get_ticks()
                #    tempo * velocidade ) * amplitude                                        
                flutuacao = math.sin(tempo * 0.003) * 10
                offset_y = -130 + flutuacao
                # Vamos simplificar: fixo em cima
                
                rect_sprite = p["sprite"].get_rect(center=(pos_x, y_bolas + offset_y))
                screen.blit(p["sprite"], rect_sprite)
                
                # Nome do Pokémon
                nome_surf = font_nome.render(p["nome"], True, p["cor"])
                rect_nome = nome_surf.get_rect(center=(pos_x, y_bolas + 60))
                
                # Fundo do nome para leitura
                bg_nome = rect_nome.inflate(20, 10)
                pg.draw.rect(screen, (255, 255, 255), bg_nome, border_radius=5)
                pg.draw.rect(screen, (0, 0, 0), bg_nome, 2, border_radius=5)
                screen.blit(nome_surf, rect_nome)
                
                # Seta indicadora na Pokébola
                pg.draw.polygon(screen, (255, 255, 0), [
                    (rect_bola.centerx - 10, rect_bola.top - 20),
                    (rect_bola.centerx + 10, rect_bola.top - 20),
                    (rect_bola.centerx, rect_bola.top - 10)
                ])

        pg.display.flip()
    
    return "Charmander" # Default
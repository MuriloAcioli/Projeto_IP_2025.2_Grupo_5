import pygame as pg
import os
import random

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
    TILE_GRAMA_LISA = (0, 1)
    TILE_GRAMA_DETALHE = (2, 1)
    TILE_FLOR_AMARELA = (0, 4)
    TILE_FLOR_ROSA = (1, 4)
    
    # Lista de probabilidade (Mais grama simples, poucas flores)
    opcoes = [TILE_GRAMA_LISA] * 30 + [TILE_PADRAO] * 30 + \
             [TILE_GRAMA_DETALHE] * 30 + [TILE_FLOR_AMARELA] * 5 + [TILE_FLOR_ROSA] * 5

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
        #screen.blit(texto_titulo, rect_titulo)
        screen.blit(img_titulo, (SCREEN_WIDTH/2 - img_titulo.get_width()/2, 0))
        screen.blit(img_enter, (SCREEN_WIDTH/2 - img_titulo.get_width()/2, 400))

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
        
    # ### ALTERADO: Carregamento das Imagens do Professor ###
    try: 
        # Imagem padrão (Professor 1)
        img_professor1 = pg.transform.scale(pg.image.load(os.path.join(DIRETORIO_BASE, "assets/professor/proff_massa_1.png")).convert_alpha(), (400, 400)) 
    except: 
        print("Erro ao carregar proff_massa_1.png")
        img_professor1 = pg.Surface((400, 400)); img_professor1.fill((100, 100, 100))

    try:
        # ### NOVO: Imagem alternativa (Professor 2) ###
        prop = 637/1024
        base = 370
        
        # 1. Carrega a imagem
        img_original = pg.image.load(os.path.join(DIRETORIO_BASE, "assets/professor/proff_massa_2.png")).convert_alpha()
        
        # 2. Calcula o tamanho (convertendo para int)
        novo_tamanho = (int(base * prop), int(base))
        
        # 3. Escala passando a tupla correta
        img_professor2 = pg.transform.scale(img_original, novo_tamanho)

    except Exception as e:
        print(f"Erro ao carregar proff_massa_2.png: {e}")
        img_professor2 = img_professor1

          
    # --- Roteiro ---
    falas_intro = [
        "Olá! Bem-vindo ao fantástico mundo de Pokémon", 
        "Esse mundo é habitado por diversas criaturas misteriosas", 
        "Meu nome é Ricardo Massa", 
        "As pessoas me chamam de Professor Python.", 
        "Estamos precisando de ajuda aqui no CIn.", 
        "O Coletivo Mangue Vermelho quer usar seus Pokémons\npara destruir nossos computadores!", 
        "Precisamos de alguém para derrotá-los!", 
        "Será que você é o candidato ideal?", 
        "Antes que eu forneça Pokémons Fortes para você usar contra eles", 
        "Vamos fazer um teste para ver sua competência", 
        "Mas primeiro, diga-me algo sobre você." # Esta é a fala chave (índice 10)
    ]
    
    # ### NOVO: Identifica o índice da fala que deve trocar a imagem ###
    # É a última fala da lista falas_intro
    indice_troca_imagem = len(falas_intro) - 1
    
    falas_final = [
        "Ah, certo! Então seu nome é {NOME}?", 
        "Forme uma equipe de até 6 pokémons e me desafie numa batalha", 
        "Se você me vencer, será destinado a enfrentar o Mangue Vermelho!!", 
        "Sua jornada começa agora!", 
        "Escolha um dos 3 Pokémons na mesa", 
        "Após isso, sinta-se à vontade para capturar mais alguns no mato", 
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
            if event.type == pg.QUIT: return False, None
            
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
                            pg.mixer.music.fadeout(1000)
                            return True, nome_final
                
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
        # Opcional: Se quiser manter a imagem 2 enquanto o jogador digita o nome:
        #elif estado == "INPUT":
        #     img_atual = img_professor2
        
        # Desenha a imagem escolhida
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
    return False, None


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
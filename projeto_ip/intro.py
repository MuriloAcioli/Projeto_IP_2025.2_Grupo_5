import pygame as pg
import os
import random

# --- CONFIGURAÇÕES BÁSICAS (Precisam vir do main, mas as definimos aqui para evitar quebrar) ---
# Em um código mais limpo, isso viria de um arquivo config.py
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__)) 


# --- FUNÇÕES DE CENA (Intro e Dialogo) ---

def definir_piso(largura_mapa, altura_mapa, caminho_tileset, TILE_SIZE=48):
    """Gera uma Surface com a textura de grama aleatória."""
    superficie_chao = pg.Surface((largura_mapa, altura_mapa))
    
    try:
        img_tileset = pg.image.load(caminho_tileset).convert_alpha()
    except FileNotFoundError:
        print("Erro: Tileset não encontrado. Usando cor sólida.")
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
            
            rect_recorte = pg.Rect(coluna_img * TAMANHO_ORIGINAL, 
                                     linha_img * TAMANHO_ORIGINAL, 
                                     TAMANHO_ORIGINAL, 
                                     TAMANHO_ORIGINAL)
            
            tile_imagem = img_tileset.subsurface(rect_recorte)
            tile_escalado = pg.transform.scale(tile_imagem, (TILE_SIZE, TILE_SIZE))
            
            superficie_chao.blit(tile_escalado, (x, y))

    return superficie_chao

def exibir_intro(screen, clock):
    """Exibe a tela de título e espera pelo ENTER."""
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

def cena_professor(screen, clock):
    """Executa a cena do diálogo com o professor e coleta o nome do jogador."""
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

def animacao_transicao(screen):
    """Animação de transição para batalha (pisca a tela) e toca a música."""
    try:
        pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/battle_theme.mp3"))
        pg.mixer.music.play(-1)
    except: pass
    
    for i in range(8): 
        screen.fill((255, 255, 255)); pg.display.flip(); pg.time.delay(160)
        screen.fill((10, 10, 10)); pg.display.flip(); pg.time.delay(160)
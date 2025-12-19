import pygame as pg
import os

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def exibir_vitoria(screen, clock):
    vitoria = True
    font_ESC = pg.font.SysFont("Arial", 30, bold=True)

    try:
        caminho_enter = os.path.join(DIRETORIO_BASE, "assets", "backgrounds", "game_over_esc.png")
        img_esc = pg.image.load(caminho_enter).convert_alpha()
        img_esc = pg.transform.scale(img_esc, (400, 200))
    except Exception as e:
        print(f"Erro ao carregar imagem do ENTER: {e}")
        img_esc = font_ESC.render("Pressione ESC para sair", True, (50, 50, 50))

    try:
        caminho_bg = os.path.join(DIRETORIO_BASE, "assets", "backgrounds", "vitoria.png")
        bg_game_over = pg.image.load(caminho_bg).convert()
        bg_game_over = pg.transform.scale(bg_game_over, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"Erro no background: {e}")
        bg_game_over = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_game_over.fill((255, 255, 255)) 

    try:
        caminho_cracha = os.path.join(DIRETORIO_BASE, "assets", "coletaveis", "cracha_quebrado.png")
        cracha_quebrado = pg.image.load(caminho_cracha).convert_alpha() # Use alpha se tiver transparência
        cracha_quebrado = pg.transform.scale(cracha_quebrado, (200, 200)) 
    except Exception as e:
        print(f"Erro no cracha: {e}")
        cracha_quebrado = pg.Surface((150, 150))
        cracha_quebrado.fill((100, 100, 100)) 

    try:
        caminho_musica = os.path.join(DIRETORIO_BASE, "assets", "músicas", "vitoria.mp3")
        pg.mixer.music.load(caminho_musica)
        pg.mixer.music.set_volume(0.8)
        pg.mixer.music.play(-1)
    except Exception as e:
        print(f"Erro na música: {e}")

    # Loop Principal 
    while vitoria:
        clock.tick(15)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False # Fecha o jogo
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    vitoria = False
                    pg.mixer.music.fadeout(1000)
                    return True # Volta pro menu ou sai do estado game over

        screen.blit(bg_game_over, (0, 0))

        #screen.blit(cracha_quebrado, (600, 300))

        if pg.time.get_ticks() % 1000 < 600:
            pos_x_enter = SCREEN_WIDTH // 2 - img_esc.get_width() // 2
            screen.blit(img_esc, (pos_x_enter, 350))

        pg.display.flip()

    return True
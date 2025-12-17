import pygame as pg

class NPC(pg.sprite.Sprite):
    def __init__(self, x, y, image_path, texto_dialogo):
        super().__init__()
        
        # Carregar imagem
        try:
           
            img_bruta = pg.image.load(image_path).convert_alpha()
            img_w = img_bruta.get_width()
            img_h = img_bruta.get_height()
            prop = img_w/img_h
            w = 62
            h = prop*w

            self.image = pg.transform.scale(img_bruta, (h, w )) 
        except Exception:
            self.image = pg.Surface((64, 64))
            self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()
        # --- Lógica de Diálogo ---
        self.texto_original = texto_dialogo # Guarda a pergunta original
        self.texto_atual = texto_dialogo    # Texto que muda (pergunta ou resposta)
        self.falando = False
        
        # Opções de resposta
        self.opcoes = ["Sim", "Não"]
        self.indice_selecionado = 0 # 0 = Sim, 1 = Não
        self.respondeu = False      # Trava para não selecionar depois de responder

    def interagir(self):
        # Abre ou fecha o diálogo
        self.falando = not self.falando
        if self.falando:
            # Reseta tudo quando abre o diálogo
            self.texto_atual = self.texto_original
            self.respondeu = False
            self.indice_selecionado = 0

    def mudar_selecao(self, direcao):
        # Só muda se ainda não respondeu
        if not self.respondeu:
            self.indice_selecionado += direcao
            # Garante que não saia do limite (loop entre 0 e 1)
            if self.indice_selecionado < 0: 
                self.indice_selecionado = 1
            elif self.indice_selecionado > 1: 
                self.indice_selecionado = 0
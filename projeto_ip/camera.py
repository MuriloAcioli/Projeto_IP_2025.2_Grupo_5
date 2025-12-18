import pygame as pg

class Camera:
    def __init__(self, width, height, map_width, map_height):
        # Guardamos o tamanho original da tela (Display)
        self.display_width = width
        self.display_height = height
        
        self.map_width = map_width
        self.map_height = map_height
        
        self.camera_rect = pg.Rect(0, 0, width, height)
        
        # ISSO NÃO FUNCIONA, POIS PRECISAMOS MUDAR O TAMANHO EM TODOS OS OBJETOS, COISA QUE A GENTE NÃO VAI FAZER PQ NÃO TEM NECESSIDADE kkk
        # DEIXA 1 pelo amor de deus se não fica bizarro
        self.zoom = 1

    def apply(self, entity_rect):
        # Transforma a posição do mundo para a posição na tela aplicando o Zoom.
        # calculo da posição relativa da camera
        x_rel = entity_rect.x - self.camera_rect.x
        y_rel = entity_rect.y - self.camera_rect.y
        
        # Aplica o Zoom na posição
        # Se zoom for 2, o objeto se afasta do centro 2x mais 
        x_screen = int(x_rel * self.zoom)
        y_screen = int(y_rel * self.zoom)
        
        # Aplica o Zoom no tamanho do objeto
        w_screen = int(entity_rect.width * self.zoom)
        h_screen = int(entity_rect.height * self.zoom)
        
        return pg.Rect(x_screen, y_screen, w_screen, h_screen)

    def apply_rect(self, rect): 
        return self.apply(rect)

    def update(self, target_rect):
        # calculo da nova posição da câmera 
        
        # ajuste no campo de visão 
        self.camera_rect.width = int(self.display_width / self.zoom)
        self.camera_rect.height = int(self.display_height / self.zoom)
        
        # centralizar o jogador
        x = target_rect.centerx - int(self.camera_rect.width / 2)
        y = target_rect.centery - int(self.camera_rect.height / 2)

        # limitador do mapa 
        x = max(0, x) # o menor x é 0
        y = max(0, y) # o menor y é 0
        x = min(x, self.map_width - self.camera_rect.width) # o maior x é a largura do mapa
        y = min(y, self.map_height - self.camera_rect.height) # o maior y é a largura do mapa

        # aqui aplica no objeto
        self.camera_rect.x = x
        self.camera_rect.y = y
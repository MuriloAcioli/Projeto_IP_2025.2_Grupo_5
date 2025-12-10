import pygame as pg

class Camera:
    def __init__(self, width, height, map_width, map_height):
        # width/height: tamanho da janela
        # map_width/map_height: tamanho total do mundo
        self.camera_rect = pg.Rect(0, 0, width, height)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity_rect):
        """ 
        Recebe o rect de um objeto (ex: player) e retorna 
        um novo rect deslocado pela posição da câmera.
        """
        return entity_rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def apply_rect(self, rect):
        """ Mesma coisa, mas para rects soltos (útil para o fundo) """
        return rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target_rect):
        """ Calcula a nova posição da câmera baseada no alvo (player) """
        
        # 1. Centraliza a câmera no alvo
        x = target_rect.centerx - int(self.camera_rect.width / 2)
        y = target_rect.centery - int(self.camera_rect.height / 2)

        # 2. Limita a câmera para não sair do mapa (Clamp)
        # Não deixa ir para a esquerda de 0
        x = max(0, x) 
        # Não deixa ir para cima de 0
        y = max(0, y) 
        # Não deixa passar da largura do mapa
        x = min(x, self.map_width - self.camera_rect.width) 
        # Não deixa passar da altura do mapa
        y = min(y, self.map_height - self.camera_rect.height)

        # Atualiza o retângulo da câmera
        self.camera_rect.x = x
        self.camera_rect.y = y
import pygame as pg

class MenuInventario:
    def __init__(self):
        self.aberto = False # Começa fechado
        # Cria uma fonte: (Nome da fonte, tamanho, negrito)
        # None usa a fonte padrão do Pygame
        self.fonte = pg.font.SysFont('Arial', 20, bold=True)
        
    def alternar(self):
        """Abre se estiver fechado, fecha se estiver aberto"""
        self.aberto = not self.aberto
        
    def desenhar(self, tela, inventario_do_player):
        # Se não estiver aberto, não desenha nada
        if not self.aberto:
            return

        # Configurações de posição (Canto Superior Esquerdo)
        x_inicial = 10
        y_inicial = 10
        espacamento_linha = 25
        
        # Cria uma superfície preta com transparência (alpha)
        fundo = pg.Surface((200, 300)) 
        fundo.set_alpha(128) # 0 é invisível, 255 é sólido
        fundo.fill((0, 0, 0))
        tela.blit(fundo, (0, 0))

        # Título
        titulo = self.fonte.render("--- MOCHILA ---", True, (255, 255, 0))
        tela.blit(titulo, (x_inicial, y_inicial))
        y_atual = y_inicial + 30

        # Loop para desenhar cada item do dicionário
        # inventario_do_player deve ser algo como: {'Pocao': 2, 'Pokebola': 5}
        if not inventario_do_player:
            texto_vazio = self.fonte.render("(Vazio)", True, (200, 200, 200))
            tela.blit(texto_vazio, (x_inicial, y_atual))
        else:
            for nome_item, quantidade in inventario_do_player.items():
                texto = f"{nome_item}: {quantidade}"
                # Renderiza o texto (String, Anti-aliasing, Cor)
                superficie_texto = self.fonte.render(texto, True, (255, 255, 255))
                
                tela.blit(superficie_texto, (x_inicial, y_atual))
                y_atual += espacamento_linha
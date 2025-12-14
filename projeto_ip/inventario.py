import pygame as pg

# =============================================================================
# CONSTANTES DE ESTADO
# =============================================================================
ESTADO_MENU_PRINCIPAL = 0
ESTADO_LISTA_ITENS = 1
ESTADO_OPCOES_ITEM = 2
ESTADO_ESCOLHER_POKEMON = 3
ESTADO_MENSAGEM = 4  

class MenuInventario:
    def __init__(self):
        self.aberto = False 
        
        self.fonte_tamanho = 20
        try:
            self.fonte = pg.font.Font("pokemon_font.ttf", self.fonte_tamanho)
        except FileNotFoundError:
            self.fonte = pg.font.SysFont('couriernew', 20, bold=True)
        
        # Cores
        self.COR_BRANCO = (248, 248, 248) 
        self.COR_PRETO = (8, 8, 8)        
        self.COR_VERDE_HP = (80, 200, 120)
        self.COR_CINZA_BARRA = (200, 200, 200)

        # Variáveis de Controle
        self.estado_atual = ESTADO_MENU_PRINCIPAL
        self.index_menu_principal = 0 
        self.index_lista_itens = 0
        self.index_opcoes = 0 
        self.index_pokemon = 0
        self.item_focado = None 
        
        self.texto_mensagem = ""
        self.estado_anterior_mensagem = ESTADO_MENU_PRINCIPAL 

    def alternar(self):
        self.aberto = not self.aberto
        if self.aberto:
            self.estado_atual = ESTADO_MENU_PRINCIPAL
            self.index_menu_principal = 0

    def mostrar_mensagem(self, texto):
        self.texto_mensagem = texto
        self.estado_anterior_mensagem = self.estado_atual 
        self.estado_atual = ESTADO_MENSAGEM

    def processar_input(self, evento, inventario_do_player, equipe_jogador):
        if not self.aberto:
            return None
        if evento.type != pg.KEYDOWN:
            return None
        
        tecla = evento.key

        # === MENSAGEM ===
        if self.estado_atual == ESTADO_MENSAGEM:
            if tecla == pg.K_SPACE or tecla == pg.K_RETURN or tecla == pg.K_ESCAPE or tecla == pg.K_z:
                self.estado_atual = self.estado_anterior_mensagem
            return None

        # === MENU PRINCIPAL ===
        if self.estado_atual == ESTADO_MENU_PRINCIPAL:
            if tecla == pg.K_w or tecla == pg.K_UP:
                self.index_menu_principal = 0 
            elif tecla == pg.K_s or tecla == pg.K_DOWN:
                self.index_menu_principal = 1 
            elif tecla == pg.K_RETURN or tecla == pg.K_SPACE:
                if self.index_menu_principal == 0: 
                    self.estado_atual = ESTADO_LISTA_ITENS
                    self.index_lista_itens = 0
                else: 
                    self.alternar()
            elif tecla == pg.K_ESCAPE:
                self.alternar()

        # === LISTA DE ITENS ===
        elif self.estado_atual == ESTADO_LISTA_ITENS:
            lista_nomes = list(inventario_do_player.keys())
            if tecla == pg.K_ESCAPE:
                self.estado_atual = ESTADO_MENU_PRINCIPAL 
            
            if len(lista_nomes) > 0:
                if tecla == pg.K_w or tecla == pg.K_UP:
                    self.index_lista_itens -= 1
                    if self.index_lista_itens < 0: self.index_lista_itens = len(lista_nomes) - 1
                elif tecla == pg.K_s or tecla == pg.K_DOWN:
                    self.index_lista_itens += 1
                    if self.index_lista_itens >= len(lista_nomes): self.index_lista_itens = 0
                elif tecla == pg.K_RETURN or tecla == pg.K_SPACE:
                    self.item_focado = lista_nomes[self.index_lista_itens]
                    self.estado_atual = ESTADO_OPCOES_ITEM
                    self.index_opcoes = 0

        # === OPÇÕES (USAR / DESCARTAR) ===
        elif self.estado_atual == ESTADO_OPCOES_ITEM:
            eh_pocao = "Pocao" in self.item_focado or "Potion" in self.item_focado
            opcoes_disponiveis = ["DESCARTAR"]
            if eh_pocao:
                opcoes_disponiveis = ["USAR", "DESCARTAR"]
            
            if tecla == pg.K_ESCAPE:
                self.estado_atual = ESTADO_LISTA_ITENS 
            elif tecla == pg.K_w or tecla == pg.K_UP:
                self.index_opcoes = 0
            elif tecla == pg.K_s or tecla == pg.K_DOWN:
                if len(opcoes_disponiveis) > 1:
                    self.index_opcoes = 1
            
            elif tecla == pg.K_RETURN or tecla == pg.K_SPACE:
                acao_escolhida = opcoes_disponiveis[self.index_opcoes]
                
                if acao_escolhida == "DESCARTAR":
                    if self.item_focado in inventario_do_player:
                        inventario_do_player[self.item_focado] -= 1
                        if inventario_do_player[self.item_focado] <= 0:
                            del inventario_do_player[self.item_focado]
                    self.estado_atual = ESTADO_LISTA_ITENS 
                
                elif acao_escolhida == "USAR":
                    self.estado_atual = ESTADO_ESCOLHER_POKEMON
                    self.index_pokemon = 0

        # === ESCOLHER POKEMON ===
        elif self.estado_atual == ESTADO_ESCOLHER_POKEMON:
            
            if tecla == pg.K_ESCAPE:
                if self.item_focado in inventario_do_player:
                    self.estado_atual = ESTADO_OPCOES_ITEM
                else:
                    self.estado_atual = ESTADO_LISTA_ITENS
            
            if len(equipe_jogador) > 0:
                if tecla == pg.K_w or tecla == pg.K_UP:
                    self.index_pokemon -= 1
                    if self.index_pokemon < 0: self.index_pokemon = len(equipe_jogador) - 1
                elif tecla == pg.K_s or tecla == pg.K_DOWN:
                    self.index_pokemon += 1
                    if self.index_pokemon >= len(equipe_jogador): self.index_pokemon = 0
                
                # USAR A POÇÃO
                elif tecla == pg.K_RETURN or tecla == pg.K_SPACE:
                    
                    if self.item_focado not in inventario_do_player:
                        self.mostrar_mensagem("Acabaram os itens!")
                        return None

                    pokemon_alvo = equipe_jogador[self.index_pokemon]
                    vida_atual = pokemon_alvo.hp_atual
                    vida_max = pokemon_alvo.hp_max
                    
                    if vida_atual >= vida_max:
                        self.mostrar_mensagem("Isso nao tera efeito!") 
                    else:
                        cura = 5
                        pokemon_alvo.hp_atual += cura
                        if pokemon_alvo.hp_atual > vida_max:
                            pokemon_alvo.hp_atual = vida_max
                        
                        inventario_do_player[self.item_focado] -= 1
                        
                        if inventario_do_player[self.item_focado] <= 0:
                            del inventario_do_player[self.item_focado]
                            
                        self.mostrar_mensagem(f"Recuperou {cura} HP!") 

        return None

    # --- FUNÇÕES DE DESENHO ---

    def desenhar_caixa_gb(self, tela, rect):
        """Desenha caixa branca com borda preta grossa"""
        pg.draw.rect(tela, self.COR_BRANCO, rect)
        pg.draw.rect(tela, self.COR_PRETO, rect, width=4)
        pg.draw.line(tela, self.COR_PRETO, (rect.left+4, rect.top+4), (rect.right-4, rect.top+4), 1)
        pg.draw.line(tela, self.COR_PRETO, (rect.left+4, rect.bottom-4), (rect.right-4, rect.bottom-4), 1)
        pg.draw.line(tela, self.COR_PRETO, (rect.left+4, rect.top+4), (rect.left+4, rect.bottom-4), 1)
        pg.draw.line(tela, self.COR_PRETO, (rect.right-4, rect.top+4), (rect.right-4, rect.bottom-4), 1)

    def desenhar_cursor(self, tela, x, y):
        pontos = [(x, y), (x, y + 10), (x + 8, y + 5)]
        pg.draw.polygon(tela, self.COR_PRETO, pontos)

    def desenhar_barra_hp(self, tela, x, y, atual, maximo):
        largura_barra = 100
        altura_barra = 10
        
        # Texto HP
        surf_hp = self.fonte.render("HP:", True, self.COR_PRETO)
        tela.blit(surf_hp, (x - 35, y - 5))
        
        # Fundo da barra
        rect_fundo = pg.Rect(x, y, largura_barra, altura_barra)
        pg.draw.rect(tela, self.COR_CINZA_BARRA, rect_fundo)
        pg.draw.rect(tela, self.COR_PRETO, rect_fundo, width=1)
        
        # Parte Verde
        if maximo > 0 and atual > 0:
            porcentagem = atual / maximo
            largura_verde = int(largura_barra * porcentagem)
            if largura_verde > largura_barra: largura_verde = largura_barra
            
            rect_verde = pg.Rect(x + 1, y + 1, largura_verde - 2, altura_barra - 2)
            pg.draw.rect(tela, self.COR_VERDE_HP, rect_verde)

    def desenhar(self, tela, inventario_do_player, equipe_jogador):
        if not self.aberto:
            return

        screen_w, screen_h = tela.get_size()
        
        # === MENU LATERAL ===
        if self.estado_atual == ESTADO_MENU_PRINCIPAL:
            rect_menu = pg.Rect(screen_w - 220, 20, 200, 250)
            self.desenhar_caixa_gb(tela, rect_menu)
            
            x_texto = rect_menu.x + 30
            y_atual = rect_menu.y + 40
            
            opcoes = ["ITEM", "SAIR"]
            for i, opcao in enumerate(opcoes):
                if i == self.index_menu_principal:
                    self.desenhar_cursor(tela, x_texto - 15, y_atual + 5)
                surf = self.fonte.render(opcao, True, self.COR_PRETO)
                tela.blit(surf, (x_texto, y_atual))
                y_atual += 40

        # === LISTA DE ITENS ===
        if self.estado_atual >= ESTADO_LISTA_ITENS and self.estado_atual != ESTADO_ESCOLHER_POKEMON:
            largura_lista = 400
            altura_lista = 400
            pos_x = (screen_w - largura_lista) // 2
            pos_y = (screen_h - altura_lista) // 2
            
            rect_lista = pg.Rect(pos_x, pos_y, largura_lista, altura_lista)
            self.desenhar_caixa_gb(tela, rect_lista)
            
            x_texto = rect_lista.x + 40
            y_atual = rect_lista.y + 30
            
            if not inventario_do_player:
                tela.blit(self.fonte.render("MOCHILA VAZIA", True, (100,100,100)), (x_texto, y_atual))
            else:
                for i, (nome, qtd) in enumerate(inventario_do_player.items()):
                    if self.estado_atual == ESTADO_LISTA_ITENS and i == self.index_lista_itens:
                        self.desenhar_cursor(tela, x_texto - 15, y_atual + 5)
                    elif self.estado_atual > ESTADO_LISTA_ITENS and nome == self.item_focado:
                        self.desenhar_cursor(tela, x_texto - 15, y_atual + 5)
                    
                    texto = f"{nome.upper()}"
                    texto_qtd = f"x{qtd}"
                    
                    tela.blit(self.fonte.render(texto, True, self.COR_PRETO), (x_texto, y_atual))
                    tela.blit(self.fonte.render(texto_qtd, True, self.COR_PRETO), (x_texto + 220, y_atual))
                    
                    y_atual += 40

        # === POP-UP DE AÇÕES ===
        if self.estado_atual == ESTADO_OPCOES_ITEM:
            cx = (screen_w // 2) + 100
            cy = (screen_h // 2) + 50
            rect_pop = pg.Rect(cx, cy, 150, 120)
            self.desenhar_caixa_gb(tela, rect_pop)
            
            eh_pocao = "Pocao" in self.item_focado or "Potion" in self.item_focado
            opcoes_disp = ["DESCARTAR"]
            if eh_pocao:
                opcoes_disp = ["USAR", "DESCARTAR"]
            
            px, py = rect_pop.x + 30, rect_pop.y + 30
            for i, op in enumerate(opcoes_disp):
                if i == self.index_opcoes:
                    self.desenhar_cursor(tela, px - 15, py + 5)
                tela.blit(self.fonte.render(op, True, self.COR_PRETO), (px, py))
                py += 35

        # === ESCOLHER POKEMON ===
        if self.estado_atual == ESTADO_ESCOLHER_POKEMON or (self.estado_atual == ESTADO_MENSAGEM and self.estado_anterior_mensagem == ESTADO_ESCOLHER_POKEMON):
            
            # REMOVIDO: pg.draw.rect(tela, self.COR_BRANCO, (0, 0, screen_w, screen_h)) 
            # AGORA O FUNDO SERÁ O JOGO (TRANSPARENTE FORA DA CAIXA)
            
            rect_poke = pg.Rect(20, 20, screen_w - 40, screen_h - 160)
            self.desenhar_caixa_gb(tela, rect_poke)
            
            tela.blit(self.fonte.render("USAR EM QUEM?", True, self.COR_PRETO), (rect_poke.x + 20, rect_poke.y + 20))
            
            y_base = rect_poke.y + 60
            for i, poke in enumerate(equipe_jogador):
                x_base = rect_poke.x + 40
                
                if self.index_pokemon == i:
                    self.desenhar_cursor(tela, x_base - 20, y_base + 10)
                
                nome = getattr(poke, 'nome', 'Pokemon').upper()
                tela.blit(self.fonte.render(nome, True, self.COR_PRETO), (x_base, y_base))
                
                v_atual = poke.hp_atual
                v_max = poke.hp_max
                
                self.desenhar_barra_hp(tela, x_base + 250, y_base + 10, v_atual, v_max)
                
                texto_nums = f"{v_atual: >3}/ {v_max: >3}"
                tela.blit(self.fonte.render(texto_nums, True, self.COR_PRETO), (x_base + 260, y_base + 25))
                
                y_base += 70

        # === MENSAGEM INFERIOR ===
        if self.estado_atual == ESTADO_MENSAGEM:
            rect_msg = pg.Rect(0, screen_h - 120, screen_w, 120)
            pg.draw.rect(tela, self.COR_BRANCO, rect_msg)
            pg.draw.rect(tela, self.COR_PRETO, rect_msg, width=4)
            
            tela.blit(self.fonte.render(self.texto_mensagem, True, self.COR_PRETO), (30, screen_h - 80))
            
            if (pg.time.get_ticks() // 500) % 2 == 0:
                pg.draw.polygon(tela, (200, 0, 0), [(screen_w-40, screen_h-30), (screen_w-20, screen_h-30), (screen_w-30, screen_h-20)])
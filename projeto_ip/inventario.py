import pygame as pg
import os

# ESTADOS DO MENU 
ESTADO_MENU_PRINCIPAL = 0
ESTADO_LISTA_ITENS = 1
ESTADO_OPCOES_ITEM = 2
ESTADO_ESCOLHER_POKEMON = 3
ESTADO_MENSAGEM = 4  
ESTADO_TROCAR_POKEMON = 5
ESTADO_POKEDEX_LISTA = 6
ESTADO_POKEDEX_DETALHES = 7

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))

class MenuInventario:
    def __init__(self):
        self.aberto = False 
        
        # Configuração de Fontes 
        self.fonte_tamanho = 20
        try:
            # Tenta carregar fonte personalizada, senão usa padrão
            self.fonte = pg.font.Font("assets/fonts/pokemon_font.ttf", self.fonte_tamanho)
        except FileNotFoundError:
            self.fonte = pg.font.SysFont('couriernew', 20, bold=True)
        
        # Cores
        self.COR_BRANCO = (248, 248, 248) 
        self.COR_PRETO = (8, 8, 8)        
        self.COR_VERDE_HP = (80, 200, 120)
        self.COR_CINZA_BARRA = (200, 200, 200)
        self.COR_SALMAO = (200,  100, 100)

        # Navgação do Menu
        self.estado_atual = ESTADO_MENU_PRINCIPAL
        self.index_menu_principal = 0 
        self.index_lista_itens = 0
        self.index_opcoes = 0 
        self.index_pokemon = 0
        
        # Variáveis auxiliares
        self.poke_troca_origem = -1 
        self.item_focado = None 
        self.texto_mensagem = ""
        self.estado_anterior_mensagem = ESTADO_MENU_PRINCIPAL 
        
        # Sistema de visualização de insígnia
        self.mostrar_insignia = False
        self.timer_insignia = 0
        
        # POKEDEX
        self.index_pokedex = 0
        self.cache_imagens = {} 

    def alternar(self):
        """Abre/fecha o menu"""
        self.aberto = not self.aberto
        if self.aberto:
            self.estado_atual = ESTADO_MENU_PRINCIPAL
            self.index_menu_principal = 0

    def mostrar_mensagem(self, texto):
        self.texto_mensagem = texto
        self.estado_anterior_mensagem = self.estado_atual 
        self.estado_atual = ESTADO_MENSAGEM

    def criar_silhueta(self, surface):
        if surface is None: return None
        mask = pg.mask.from_surface(surface)
        return mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))

    def get_imagem_cache(self, caminho): # essa dica foi muito boa
        if caminho not in self.cache_imagens:
            try:
                if os.path.exists(caminho):
                    img = pg.image.load(caminho).convert_alpha()
                    self.cache_imagens[caminho] = img
                else:
                    return None
            except Exception as e:
                print(f"Erro ao carregar sprite {caminho}: {e}")
                return None
        return self.cache_imagens[caminho]

    def desenhar_caixa_gb(self, tela, rect):
        pg.draw.rect(tela, self.COR_SALMAO, rect)
        pg.draw.rect(tela, self.COR_PRETO, rect, width=4)
        # Detalhes nos cantos 
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
        
        surf_hp = self.fonte.render("HP:", True, self.COR_PRETO)
        tela.blit(surf_hp, (x - 35, y - 5))
        
        rect_fundo = pg.Rect(x, y, largura_barra, altura_barra)
        pg.draw.rect(tela, self.COR_CINZA_BARRA, rect_fundo)
        pg.draw.rect(tela, self.COR_PRETO, rect_fundo, width=1)
        
        if maximo > 0 and atual > 0:
            porcentagem = atual / maximo
            largura_verde = int(largura_barra * porcentagem)
            if largura_verde > largura_barra: largura_verde = largura_barra
            rect_verde = pg.Rect(x + 1, y + 1, largura_verde - 2, altura_barra - 2)
            pg.draw.rect(tela, self.COR_VERDE_HP, rect_verde)



    # LÓGICA DE INPUT

    def processar_input(self, evento, inventario_do_player, equipe_jogador, db_pokemons):
        if not self.aberto: return None
        if evento.type != pg.KEYDOWN: return None
        
        tecla = evento.key

        # Mensagem
        if self.estado_atual == ESTADO_MENSAGEM:
            if tecla in [pg.K_SPACE, pg.K_RETURN, pg.K_ESCAPE, pg.K_z]:
                self.estado_atual = self.estado_anterior_mensagem
            return None

        # MENU PRINCIPAL
        if self.estado_atual == ESTADO_MENU_PRINCIPAL:
            if tecla in [pg.K_w, pg.K_UP]:
                self.index_menu_principal -= 1
                if self.index_menu_principal < 0: self.index_menu_principal = 3
            elif tecla in [pg.K_s, pg.K_DOWN]:
                self.index_menu_principal += 1 
                if self.index_menu_principal > 3: self.index_menu_principal = 0
            
            elif tecla in [pg.K_RETURN, pg.K_SPACE]:
                if self.index_menu_principal == 0:   # Item
                    self.estado_atual = ESTADO_LISTA_ITENS
                    self.index_lista_itens = 0
                elif self.index_menu_principal == 1: # Pokemons
                    self.estado_atual = ESTADO_TROCAR_POKEMON
                    self.index_pokemon = 0
                    self.poke_troca_origem = -1
                elif self.index_menu_principal == 2: # Pokedex
                    self.estado_atual = ESTADO_POKEDEX_LISTA
                    self.index_pokedex = 0
                else: # Sair
                    self.alternar()
            elif tecla == pg.K_ESCAPE:
                self.alternar()

        # POKÉDEX: LISTA
        elif self.estado_atual == ESTADO_POKEDEX_LISTA:
            lista_chaves = sorted(
                                [k for k in db_pokemons.keys() if not k.endswith('*')], 
                                key=lambda k: db_pokemons[k]['id']
                            )
            
            if tecla == pg.K_ESCAPE:
                self.estado_atual = ESTADO_MENU_PRINCIPAL
            
            if len(lista_chaves) > 0:
                if tecla in [pg.K_w, pg.K_UP]:
                    self.index_pokedex -= 1
                    if self.index_pokedex < 0: self.index_pokedex = len(lista_chaves) - 1
                elif tecla in [pg.K_s, pg.K_DOWN]:
                    self.index_pokedex += 1
                    if self.index_pokedex >= len(lista_chaves): self.index_pokedex = 0
                elif tecla in [pg.K_RETURN, pg.K_SPACE]:
                    self.estado_atual = ESTADO_POKEDEX_DETALHES

        # POKÉDEX: DETALHES
        elif self.estado_atual == ESTADO_POKEDEX_DETALHES:
            if tecla in [pg.K_ESCAPE, pg.K_RETURN, pg.K_SPACE, pg.K_BACKSPACE]:
                self.estado_atual = ESTADO_POKEDEX_LISTA

        # LISTA DE ITENS
        elif self.estado_atual == ESTADO_LISTA_ITENS:
            lista_nomes = list(inventario_do_player.keys())
            if self.index_lista_itens >= len(lista_nomes): 
                self.index_lista_itens = max(0, len(lista_nomes) - 1)
            
            if tecla == pg.K_ESCAPE:
                self.estado_atual = ESTADO_MENU_PRINCIPAL 
            
            if len(lista_nomes) > 0:
                if tecla in [pg.K_w, pg.K_UP]:
                    self.index_lista_itens -= 1
                    if self.index_lista_itens < 0: self.index_lista_itens = len(lista_nomes) - 1
                elif tecla in [pg.K_s, pg.K_DOWN]:
                    self.index_lista_itens += 1
                    if self.index_lista_itens >= len(lista_nomes): self.index_lista_itens = 0
                elif tecla in [pg.K_RETURN, pg.K_SPACE]:
                    self.item_focado = lista_nomes[self.index_lista_itens]
                    self.estado_atual = ESTADO_OPCOES_ITEM
                    self.index_opcoes = 0

        # OPÇÕES DO ITEM
        elif self.estado_atual == ESTADO_OPCOES_ITEM:
            lower_item = self.item_focado.lower()
            eh_pocao = "poção" in lower_item
            eh_insignia = "insígnia" in lower_item or "insignia" in lower_item
            # Insígnias não podem ser usadas nem descartadas
            if eh_insignia:
                opcoes_disponiveis = ["VISUALIZAR", "VOLTAR"]
            else:
                opcoes_disponiveis = ["USAR", "DESCARTAR"] if eh_pocao else ["DESCARTAR"]
            
            if tecla == pg.K_ESCAPE:
                self.estado_atual = ESTADO_LISTA_ITENS 
            elif tecla in [pg.K_w, pg.K_UP]:
                self.index_opcoes = (self.index_opcoes - 1) % len(opcoes_disponiveis)
            elif tecla in [pg.K_s, pg.K_DOWN]:
                self.index_opcoes = (self.index_opcoes + 1) % len(opcoes_disponiveis)
            
            elif tecla in [pg.K_RETURN, pg.K_SPACE]:
                acao = opcoes_disponiveis[self.index_opcoes]
                
                if acao == "VISUALIZAR":
                    self.mostrar_insignia = True
                    self.timer_insignia = pg.time.get_ticks()
                    self.estado_atual = ESTADO_LISTA_ITENS
                
                elif acao == "VOLTAR":
                    self.estado_atual = ESTADO_LISTA_ITENS
                
                elif acao == "DESCARTAR":
                    if self.item_focado in inventario_do_player:
                        inventario_do_player[self.item_focado] -= 1
                        if inventario_do_player[self.item_focado] <= 0:
                            del inventario_do_player[self.item_focado]
                            self.index_lista_itens -= 1
                        self.estado_atual = ESTADO_LISTA_ITENS 
                
                elif acao == "USAR":
                    self.estado_atual = ESTADO_ESCOLHER_POKEMON
                    self.index_pokemon = 0

        # ESCOLHER POKEMON (Para usar item)
        elif self.estado_atual == ESTADO_ESCOLHER_POKEMON:
            if tecla == pg.K_ESCAPE:
                self.estado_atual = ESTADO_OPCOES_ITEM if self.item_focado in inventario_do_player else ESTADO_LISTA_ITENS
            
            if len(equipe_jogador) > 0:
                if tecla in [pg.K_w, pg.K_UP]:
                    self.index_pokemon = (self.index_pokemon - 1) % len(equipe_jogador)
                elif tecla in [pg.K_s, pg.K_DOWN]:
                    self.index_pokemon = (self.index_pokemon + 1) % len(equipe_jogador)
                
                elif tecla in [pg.K_RETURN, pg.K_SPACE]:
                    pokemon_alvo = equipe_jogador[self.index_pokemon]
                    if pokemon_alvo.hp_atual >= pokemon_alvo.hp_max:
                        self.mostrar_mensagem("Vida já está cheia!") 
                    else:
                        cura = 20
                        if "super" in self.item_focado.lower(): cura = 50
                        if "hyper" in self.item_focado.lower(): cura = 200
                        
                        pokemon_alvo.hp_atual = min(pokemon_alvo.hp_max, pokemon_alvo.hp_atual + cura)
                        
                        inventario_do_player[self.item_focado] -= 1
                        if inventario_do_player[self.item_focado] <= 0:
                            del inventario_do_player[self.item_focado]
                            self.estado_atual = ESTADO_LISTA_ITENS 
                        self.mostrar_mensagem(f"{pokemon_alvo.nome}: Recuperou {cura} HP!")

        # TROCAR ORDEM
        elif self.estado_atual == ESTADO_TROCAR_POKEMON:
            if tecla == pg.K_ESCAPE:
                self.estado_atual = ESTADO_MENU_PRINCIPAL 
            
            if len(equipe_jogador) > 1:
                if tecla in [pg.K_w, pg.K_UP]:
                    self.index_pokemon = (self.index_pokemon - 1) % len(equipe_jogador)
                elif tecla in [pg.K_s, pg.K_DOWN]:
                    self.index_pokemon = (self.index_pokemon + 1) % len(equipe_jogador)
                elif tecla in [pg.K_RETURN, pg.K_SPACE]:
                    if self.poke_troca_origem == -1:
                        self.poke_troca_origem = self.index_pokemon
                    else:
                        if self.poke_troca_origem != self.index_pokemon:
                            equipe_jogador[self.poke_troca_origem], equipe_jogador[self.index_pokemon] = \
                            equipe_jogador[self.index_pokemon], equipe_jogador[self.poke_troca_origem]
                        self.poke_troca_origem = -1    
        return None



    # LÓGICA DE DESENHO

    def desenhar(self, tela, inventario_do_player, equipe_jogador, db_pokemons, progresso_pokedex):
        # Exibe pop-up da insígnia se ativado
        if self.mostrar_insignia:
            tempo_atual = pg.time.get_ticks()
            if tempo_atual - self.timer_insignia < 3000:  # Mostra por 3 segundos
                # Fundo escurecido
                overlay = pg.Surface((800, 600))
                overlay.set_alpha(200)
                overlay.fill((0, 0, 0))
                tela.blit(overlay, (0, 0))
                
                # Caixa da insígnia
                rect_insignia = pg.Rect(200, 150, 400, 300)
                self.desenhar_caixa_gb(tela, rect_insignia)
                
                # Título
                fonte_titulo = pg.font.SysFont('couriernew', 28, bold=True)
                titulo = fonte_titulo.render("INSÍGNIA DO PROFESSOR", True, (218, 165, 32))
                tela.blit(titulo, (rect_insignia.centerx - titulo.get_width()//2, rect_insignia.y + 20))
                
                # Tenta carregar imagem da insígnia
                try:
                    img_insignia = pg.image.load(os.path.join(DIRETORIO_BASE, "assets/coletaveis/cracha_cin.png"))
                    img_insignia = pg.transform.scale(img_insignia, (300, 300))
                    tela.blit(img_insignia, (rect_insignia.centerx - 140, rect_insignia.centery - 175))
                except:
                    # Fallback: desenha uma estrela dourada
                    pg.draw.circle(tela, (255, 215, 0), (rect_insignia.centerx, rect_insignia.centery), 60)
                    pg.draw.circle(tela, (218, 165, 32), (rect_insignia.centerx, rect_insignia.centery), 60, 5)
                
                # Mensagem
                msg = self.fonte.render("Vitória sobre o Professor!", True, self.COR_PRETO)
                tela.blit(msg, (rect_insignia.centerx - msg.get_width()//2, rect_insignia.bottom - 60))
                return
            else:
                self.mostrar_insignia = False
        
        if not self.aberto: return

        screen_w, screen_h = tela.get_size()
        
        # menu lateral
        if self.estado_atual == ESTADO_MENU_PRINCIPAL:
            rect_menu = pg.Rect(screen_w - 220, 20, 200, 250)
            self.desenhar_caixa_gb(tela, rect_menu)
            
            opcoes = ["ITEM", "POKÉMONS", "POKÉDEX", "SAIR"]
            for i, opcao in enumerate(opcoes):
                x_texto = rect_menu.x + 30
                y_texto = rect_menu.y + 40 + (i * 40)
                
                if i == self.index_menu_principal:
                    self.desenhar_cursor(tela, x_texto - 15, y_texto + 5)
                
                tela.blit(self.fonte.render(opcao, True, self.COR_PRETO), (x_texto, y_texto))

        # Pokedex: Lista
        elif self.estado_atual == ESTADO_POKEDEX_LISTA:
            largura, altura = 500, 450
            pos_x, pos_y = (screen_w - largura) // 2, (screen_h - altura) // 2
            
            self.desenhar_caixa_gb(tela, pg.Rect(pos_x, pos_y, largura, altura))
            tela.blit(self.fonte.render("POKÉDEX", True, self.COR_PRETO), (pos_x + 20, pos_y + 20))
            lista_chaves = sorted(
                                [k for k in db_pokemons.keys() if not k.endswith('*')], 
                                key=lambda k: db_pokemons[k]['id']
                            )

            
            # Scrolling simples
            inicio = max(0, self.index_pokedex - 4)
            fim = min(len(lista_chaves), inicio + 9)
            
            y_atual = pos_y + 60
            for i in range(inicio, fim):
                nome_chave = lista_chaves[i]
                dados = db_pokemons[nome_chave]
                
                status = progresso_pokedex.get(nome_chave, "desconhecido")
                
                if i == self.index_pokedex:
                    self.desenhar_cursor(tela, pos_x + 30, y_atual + 5)
                
                id_txt = f"No.{dados['id']:03d}"
                
                if status == "desconhecido":
                    nome_display = "???"
                    icone = ""
                else:
                    nome_display = nome_chave.upper()
                    icone = "(CAPTURADO)" if status == "capturado" else "(VISTO)"
                
                texto_linha = f"{id_txt}  {nome_display} {icone}"
                tela.blit(self.fonte.render(texto_linha, True, self.COR_PRETO), (pos_x + 45, y_atual))
                y_atual += 40

        # POKÉDEX: DETALHES
        elif self.estado_atual == ESTADO_POKEDEX_DETALHES:
            lista_chaves = sorted( # a função lambda nos permite colocar filtros em funções mais complexas!! (e a list comprehencion cria uma lista filtrada basicamente)
                                [k for k in db_pokemons.keys() if not k.endswith('*')], # básicamente tá falando. [adicione o pokemon na lista caso não seja shine], organize ela lista pelos id de modo crescente
                                key=lambda k: db_pokemons[k]['id']
                            )

            nome_chave = lista_chaves[self.index_pokedex]
            dados = db_pokemons[nome_chave]
            
            # Pega o status
            status = progresso_pokedex.get(nome_chave, "desconhecido")
            
            largura, altura = 600, 500
            px, py = (screen_w - largura) // 2, (screen_h - altura) // 2 # aqui é onde as informações dos pokemons vão ficar
            self.desenhar_caixa_gb(tela, pg.Rect(px, py, largura, altura))
            
            # IMAGEM
            caminho_img = dados.get('sprite', '')
            caminho_img = os.path.join(DIRETORIO_BASE, caminho_img) 

            img_surface = self.get_imagem_cache(caminho_img)
            cx_img, cy_img = px + 40, py + 40
            
            if img_surface:
                img_grande = pg.transform.scale(img_surface, (200, 200))
                if status == "desconhecido": 
                    # Se desconhecido, pinta de preto
                    silhueta = self.criar_silhueta(img_grande)
                    tela.blit(silhueta, (cx_img, cy_img))
                else: 
                    # Se visto ou capturado, mostra colorido
                    tela.blit(img_grande, (cx_img, cy_img))
            else:
                pg.draw.rect(tela, (0,0,0), (cx_img, cy_img, 200, 200))

            # INFO BÁSICA
            x_info, y_info = px + 260, py + 50
            tela.blit(self.fonte.render(f"No.{dados['id']:03d}", True, self.COR_PRETO), (x_info, y_info))
            
            if status == "desconhecido":
                tela.blit(self.fonte.render("Nome: ???", True, self.COR_PRETO), (x_info, y_info + 40))
                tela.blit(self.fonte.render("Status: Desconhecido", True, self.COR_PRETO), (x_info, y_info + 80))
            else:
                tela.blit(self.fonte.render(f"Nome: {nome_chave}", True, self.COR_PRETO), (x_info, y_info + 40))
                # .capitalize() deixa bonito: "visto" -> "Visto"
                tela.blit(self.fonte.render(f"Status: {status.capitalize()}", True, self.COR_PRETO), (x_info, y_info + 80))
            
            # STATS DETALHADOS (SÓ SE CAPTURADO)
            y_stats = py + 260
            pg.draw.line(tela, self.COR_PRETO, (px+40, y_stats-10), (px+largura-40, y_stats-10), 2)
            
            if status == "capturado":
                tipo = dados.get('tipo', '???')
                stats = dados.get('stats', (0,0,0,0)) # HP, Atk, Def, Vel
                golpes = dados.get('golpes', [])
                
                tela.blit(self.fonte.render(f"Tipo: {tipo}", True, self.COR_PRETO), (px+40, y_stats))
                
                hp, atk, df, vel = stats
                tela.blit(self.fonte.render(f"HP: {hp}   Atk: {atk}", True, self.COR_PRETO), (px+40, y_stats + 35))
                tela.blit(self.fonte.render(f"Def: {df}  Vel: {vel}", True, self.COR_PRETO), (px+40, y_stats + 65))
                
                tela.blit(self.fonte.render("Golpes:", True, self.COR_PRETO), (px+40, y_stats + 100))
                for i, golpe in enumerate(golpes):
                    if i > 3: break 
                    tela.blit(self.fonte.render(f"- {golpe}", True, self.COR_PRETO), (px+40, y_stats + 130 + (i*25)))
            
            else:
                tela.blit(self.fonte.render("Dados indisponiveis.", True, self.COR_PRETO), (px+40, y_stats))
                tela.blit(self.fonte.render("Capture para ver mais.", True, self.COR_PRETO), (px+40, y_stats + 35))

        # OUTRAS TELAS 
        elif self.estado_atual in [ESTADO_LISTA_ITENS, ESTADO_OPCOES_ITEM, ESTADO_ESCOLHER_POKEMON, ESTADO_TROCAR_POKEMON]:
            # Lista Itens / Opções
            if self.estado_atual == ESTADO_LISTA_ITENS or self.estado_atual == ESTADO_OPCOES_ITEM:
                largura, altura = 400, 400
                px, py = (screen_w - largura) // 2, (screen_h - altura) // 2
                self.desenhar_caixa_gb(tela, pg.Rect(px, py, largura, altura))
                
                x_texto = px + 40
                y_atual = py + 30
                
                if not inventario_do_player:
                    tela.blit(self.fonte.render("MOCHILA VAZIA", True, (100,100,100)), (x_texto, y_atual))
                else:
                    items_list = list(inventario_do_player.items())
                    for i, (nome, qtd) in enumerate(items_list):
                        is_sel = (self.estado_atual == ESTADO_LISTA_ITENS and i == self.index_lista_itens)
                        is_foc = (self.estado_atual > ESTADO_LISTA_ITENS and nome == self.item_focado)
                        
                        # Detecta se é uma insígnia para destacar
                        eh_insignia = "insígnia" in nome.lower() or "insignia" in nome.lower()
                        
                        # Desenha um ícone especial para insígnias
                        if eh_insignia:
                            pg.draw.circle(tela, (255, 215, 0), (x_texto + 5, y_atual + 10), 6)
                            pg.draw.circle(tela, (218, 165, 32), (x_texto + 5, y_atual + 10), 6, 2)
                            cor_texto = (218, 165, 32)  
                        else:
                            cor_texto = self.COR_PRETO
                        
                        if is_sel or is_foc:
                            self.desenhar_cursor(tela, x_texto - 15, y_atual + 5)
                        
                        texto_nome = self.fonte.render(nome.upper(), True, cor_texto)
                        tela.blit(texto_nome, (x_texto + 15, y_atual))
                        
                        if not eh_insignia:
                            tela.blit(self.fonte.render(f"x{qtd}", True, cor_texto), (x_texto + 220, y_atual))
                        
                        y_atual += 40

            # Pop-up Opções
            if self.estado_atual == ESTADO_OPCOES_ITEM:
                rect_pop = pg.Rect((screen_w//2)+100, (screen_h//2)+50, 200, 120)
                self.desenhar_caixa_gb(tela, rect_pop)
                eh_pocao = "poção" in self.item_focado.lower() 
                eh_insignia = "insígnia" in self.item_focado.lower() or "insignia" in self.item_focado.lower()
                if eh_insignia:
                    ops = ["VISUALIZAR", "VOLTAR"]
                else:
                    ops = ["USAR", "DESCARTAR"] if eh_pocao else ["DESCARTAR"]
                for i, op in enumerate(ops):
                    px, py = rect_pop.x + 30, rect_pop.y + 30 + (i*35)
                    if i == self.index_opcoes: self.desenhar_cursor(tela, px - 15, py + 5) # px,py = posiçãox e posiçãoy
                    tela.blit(self.fonte.render(op, True, self.COR_PRETO), (px, py))

            # Equipe
            if self.estado_atual in [ESTADO_ESCOLHER_POKEMON, ESTADO_TROCAR_POKEMON]:
                titulo = "TROCAR QUEM?" if self.estado_atual == ESTADO_TROCAR_POKEMON else "USAR EM QUEM?"
                rect_poke = pg.Rect(20, 20, screen_w - 40, screen_h - 160)
                self.desenhar_caixa_gb(tela, rect_poke)
                tela.blit(self.fonte.render(titulo, True, self.COR_PRETO), (rect_poke.x + 20, rect_poke.y + 20))
                
                y_base = rect_poke.y + 60
                for i, poke in enumerate(equipe_jogador):
                    x_base = rect_poke.x + 40
                    cor_texto = self.COR_PRETO
                    if self.estado_atual == ESTADO_TROCAR_POKEMON and self.poke_troca_origem == i:
                        cor_texto = (200, 50, 50) 
                    
                    if self.index_pokemon == i: self.desenhar_cursor(tela, x_base - 20, y_base + 10)
                    
                    nome = getattr(poke, 'nome', 'Pokemon').upper()
                    tela.blit(self.fonte.render(nome, True, cor_texto), (x_base, y_base))
                    self.desenhar_barra_hp(tela, x_base + 250, y_base + 10, poke.hp_atual, poke.hp_max)
                    txt_hp = f"{int(poke.hp_atual): >3}/ {int(poke.hp_max): >3}"
                    tela.blit(self.fonte.render(txt_hp, True, self.COR_PRETO), (x_base + 260, y_base + 25))
                    y_base += 70

        # MENSAGENS 
        if self.estado_atual == ESTADO_MENSAGEM:
            rect_msg = pg.Rect(0, screen_h - 120, screen_w, 120)
            pg.draw.rect(tela, self.COR_BRANCO, rect_msg)
            pg.draw.rect(tela, self.COR_PRETO, rect_msg, width=4)
            tela.blit(self.fonte.render(self.texto_mensagem, True, self.COR_PRETO), (30, screen_h - 80))
            if (pg.time.get_ticks() // 500) % 2 == 0:
                pg.draw.polygon(tela, (200, 0, 0), [(screen_w-40, screen_h-30), (screen_w-20, screen_h-30), (screen_w-30, screen_h-20)])
import pygame as pg
import random
import os
from pokemon import Golpe 

# Define o diretório base (onde este arquivo batalha.py está)
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))

class BatalhaPokemon:
    def __init__(self, player_data, enemy_pkmn, inventario):
        # Garante que equipe seja uma lista
        if isinstance(player_data, list):
            self.equipe = player_data
            self.player_pkmn = player_data[0] 
        else:
            self.equipe = [player_data]
            self.player_pkmn = player_data

        self.enemy_pkmn = enemy_pkmn
        self.inventario = inventario
        
        # Variáveis Visuais
        self.visual_hp_player = float(self.player_pkmn.hp_atual)
        self.visual_hp_enemy = float(self.enemy_pkmn.hp_atual)
        
        self.battle_over = False
        self.vencedor = None
        
        # Estados
        self.estado_atual = "ENTRADA_ANIMACAO"
        self.mensagem_sistema = "" 
        self.msg_extra = "" 
        
        # Variáveis de Controle de Captura
        self.captura_sucesso = False
        self.msg_falha_captura = ""

        # Posições para animação
        self.anim_x_player = -300 # Começa fora da tela (esquerda)
        self.target_x_player = 80 
        self.anim_x_enemy = 800   # Começa fora da tela (direita)
        self.target_x_enemy = 400
        
        self.cursor_pos = 0 
        self.max_opcoes = 3 

        # --- CARREGAMENTO DO BACKGROUND ---
        caminho_bg = os.path.join(DIRETORIO_BASE, "assets", "backgrounds", "battle_bg.jpg")
        
        if os.path.exists(caminho_bg):
            try:
                self.bg_batalha = pg.image.load(caminho_bg).convert()
                self.bg_batalha = pg.transform.scale(self.bg_batalha, (800, 600))
            except Exception as e:
                print(f"ERRO CRÍTICO ao ler a imagem: {e}")
                self.bg_batalha = None
        else:
            print("ERRO: O arquivo NÃO existe neste caminho.")
            self.bg_batalha = None 

        pg.font.init()
        self.font = pg.font.SysFont("Arial", 22)
        self.font_big = pg.font.SysFont("Arial", 30, bold=True)
        self.font_msg = pg.font.SysFont("Arial", 28, bold=True) 
        
        self.timer_espera = 0
        
        # Variáveis auxiliares de XP
        self.subiu_de_nivel = False
        self.xp_ganho = 0


    def processar_input(self, event):
        # Bloqueia input durante animações e espera
        bloqueados = ["ENTRADA_ANIMACAO", "TROCA_ANIMACAO", "AGUARDANDO_CAPTURA", 
                      "MENSAGEM_INICIAL", "ANIMANDO_PLAYER", "ANIMANDO_INIMIGO", "LEVEL_UP", "FIM_BATALHA"]
        
        if self.estado_atual in bloqueados:
            return

        if self.battle_over and self.animacao_concluida() and self.estado_atual != "LEVEL_UP":
            return

        # --- DEFINIÇÃO DINÂMICA DE COLUNAS ---
        # Aqui definimos quantas colunas tem cada menu
        n_colunas = 1  # Padrão (lista vertical)
        
        if self.estado_atual == "MENU_GOLPES":
            n_colunas = 2  # Golpes geralmente são 2x2
        elif self.estado_atual == "MENU_MOCHILA":
            n_colunas = 2  # Itens 2x2
        elif self.estado_atual == "MENU_TROCA":
            n_colunas = 2  # Pokemon team (2 colunas fica legal, ou 1 se preferir lista)
        elif self.estado_atual == "MENU_PRINCIPAL":
            n_colunas = 3  # Se for aquele menu embaixo na horizontal (Lutar/Bag/Fugir)

        total = self.max_opcoes

        # --- NAVEGAÇÃO DE CURSOR (GRID) ---
        
        # DIREITA
        if event.key == pg.K_d or event.key == pg.K_RIGHT:
            # Se não for borda da coluna E não estourar o total de itens
            if (self.cursor_pos + 1) % n_colunas != 0 and self.cursor_pos + 1 < total:
                self.cursor_pos += 1
            else:
                # Volta para o início da MESMA linha
                self.cursor_pos -= (self.cursor_pos % n_colunas)

        # ESQUERDA
        elif event.key == pg.K_a or event.key == pg.K_LEFT:
            # Se não for borda esquerda
            if self.cursor_pos % n_colunas != 0:
                self.cursor_pos -= 1
            else:
                # Vai para o fim da MESMA linha (ou último item disponível nela)
                fim_teorico = self.cursor_pos + (n_colunas - 1)
                self.cursor_pos = min(fim_teorico, total - 1)
        
        # BAIXO
        elif event.key == pg.K_s or event.key == pg.K_DOWN:
            if self.cursor_pos + n_colunas < total:
                self.cursor_pos += n_colunas
            else:
                # Wrap: volta para o topo da mesma coluna
                self.cursor_pos = self.cursor_pos % n_colunas

        # CIMA
        elif event.key == pg.K_w or event.key == pg.K_UP:
            if self.cursor_pos - n_colunas >= 0:
                self.cursor_pos -= n_colunas
            else:
                # Wrap: vai para o fundo da mesma coluna
                coluna_atual = self.cursor_pos % n_colunas
                linhas_totais = (total + n_colunas - 1) // n_colunas
                novo_index = coluna_atual + (linhas_totais - 1) * n_colunas
                if novo_index >= total: # Se cair num buraco
                    novo_index -= n_colunas
                self.cursor_pos = novo_index
        
        # --- CONFIRMAÇÃO (ENTER) ---
        elif event.key == pg.K_RETURN or event.key == pg.K_SPACE or event.key == pg.K_e:
            self.confirmar_selecao()
        
        # --- VOLTAR (ESC/BACKSPACE) ---
        elif event.key == pg.K_BACKSPACE or event.key == pg.K_ESCAPE:
            if self.estado_atual == "MENU_GOLPES":
                self.estado_atual = "MENU_PRINCIPAL"
                self.cursor_pos = 0
                self.max_opcoes = 3
                self.mensagem_sistema = "O que voce vai fazer?"
            
            elif self.estado_atual == "MENU_MOCHILA":
                self.estado_atual = "MENU_PRINCIPAL"
                self.cursor_pos = 1 
                self.max_opcoes = 3
                self.mensagem_sistema = "O que voce vai fazer?"

            elif self.estado_atual == "MENU_TROCA":
                self.estado_atual = "MENU_MOCHILA"
                self.cursor_pos = 0 
                self.max_opcoes = 4
                self.mensagem_sistema = "Mochila:"

    def animacao_concluida(self):
        margem = 0.5
        enemy_ok = abs(self.visual_hp_enemy - self.enemy_pkmn.hp_atual) < margem
        player_ok = abs(self.visual_hp_player - self.player_pkmn.hp_atual) < margem
        return enemy_ok and player_ok

    def confirmar_selecao(self):
        # --- MENU PRINCIPAL ---
        if self.estado_atual == "MENU_PRINCIPAL":
            if self.cursor_pos == 0: # LUTAR
                self.estado_atual = "MENU_GOLPES"
                self.cursor_pos = 0
                self.max_opcoes = len(self.player_pkmn.golpes)
                self.mensagem_sistema = "Escolha o ataque:"
            
            elif self.cursor_pos == 1: # BAG
                self.estado_atual = "MENU_MOCHILA"
                self.cursor_pos = 0
                self.max_opcoes = 4 
                self.mensagem_sistema = "Mochila:"
            
            elif self.cursor_pos == 2: # FUGIR
                self.tentar_fugir()

        # --- MENU GOLPES ---
        elif self.estado_atual == "MENU_GOLPES":
            self.turno_lutar(self.cursor_pos)

        # --- MENU MOCHILA ---
        elif self.estado_atual == "MENU_MOCHILA":
            if self.cursor_pos == 0: # Trocar
                self.estado_atual = "MENU_TROCA"
                self.cursor_pos = 0
                self.max_opcoes = len(self.equipe)
                self.mensagem_sistema = "Escolha um Pokemon:"
            elif self.cursor_pos == 1: # Poção
                self.usar_pocao()
            elif self.cursor_pos == 2: # Pokebola
                self.tentar_capturar("Pokebola")
            elif self.cursor_pos == 3: # Grande Bola
                self.tentar_capturar("Grande Bola")

        # --- MENU TROCA ---
        elif self.estado_atual == "MENU_TROCA":
            pkmn_escolhido = self.equipe[self.cursor_pos]
            
            if pkmn_escolhido == self.player_pkmn:
                self.mensagem_sistema = "Ele ja esta em batalha!"
            elif not pkmn_escolhido.esta_vivo():
                self.mensagem_sistema = "Ele esta desmaiado!"
            else:
                self.realizar_troca(pkmn_escolhido)

    def tentar_capturar(self, tipo_bola):
        # --- IMPLEMENTAÇÃO: LIMITE DE 6 POKEMONS ---
        if len(self.equipe) >= 6:
            self.mensagem_sistema = "Sua equipe esta cheia!"
            return
        # -------------------------------------------

        # Verifica quantidade
        qtd = self.inventario.get(tipo_bola, 0)
        if qtd <= 0:
            self.mensagem_sistema = f"Voce não tem {tipo_bola}!"
            return

        # Consome item
        self.inventario[tipo_bola] -= 1
        
        # Lógica de Chance
        chance_captura = 50 if tipo_bola == "Pokebola" else 90
        sorteio = random.randint(1, 100)
        
        if sorteio <= chance_captura:
            self.captura_sucesso = True
        else:
            self.captura_sucesso = False
            if tipo_bola == "Pokebola":
                self.msg_falha_captura = "Droga! A Pokebola quebrou!"
            else:
                self.msg_falha_captura = "Quase! A Grande Bola falhou!"

        # Inicia o suspense (delay)
        self.mensagem_sistema = f"Jogou {tipo_bola}..."
        self.estado_atual = "AGUARDANDO_CAPTURA"
        self.timer_espera = pg.time.get_ticks()

    def realizar_troca(self, novo_pkmn):
        self.player_pkmn = novo_pkmn
        self.visual_hp_player = float(self.player_pkmn.hp_atual)
        
        # Reseta posição para fazer a animação de entrada
        self.anim_x_player = -300 
        
        self.mensagem_sistema = f"Vai, {novo_pkmn.nome}!"
        self.msg_extra = ""
        
        # Inicia estado de animação de troca
        self.estado_atual = "TROCA_ANIMACAO"
        self.timer_espera = pg.time.get_ticks()

    def usar_pocao(self):
        nome_item = 'Poção de Vida'
        qtd = self.inventario.get(nome_item, 0)
        
        if qtd > 0:
            self.inventario[nome_item] -= 1
            cura = 20
            self.player_pkmn.hp_atual = min(self.player_pkmn.hp_max, self.player_pkmn.hp_atual + cura)
            self.mensagem_sistema = f"Usou Poção! +{cura} HP."
            self.msg_extra = "" 
            self.estado_atual = "ANIMANDO_PLAYER" 
            self.timer_espera = pg.time.get_ticks()
        else:
            self.mensagem_sistema = "Voce não tem Pocoes!"

    def tentar_fugir(self):
        if self.player_pkmn.speed >= self.enemy_pkmn.speed:
            self.battle_over = True
            self.vencedor = "FUGA"
            self.mensagem_sistema = "Fugiu com sucesso!"
        else:
            if random.random() < 0.5:
                self.battle_over = True
                self.vencedor = "FUGA"
                self.mensagem_sistema = "Fugiu por pouco!"
            else:
                self.mensagem_sistema = "Não conseguiu fugir!"
                self.msg_extra = ""
                self.estado_atual = "ANIMANDO_PLAYER"
                self.timer_espera = pg.time.get_ticks()

    def turno_lutar(self, indice):
        if indice >= len(self.player_pkmn.golpes): return
        golpe = self.player_pkmn.golpes[indice]
        
        dano, msg_efeito = self.calcular_dano(self.player_pkmn, self.enemy_pkmn, golpe)
        self.enemy_pkmn.receber_dano(dano)
        
        self.mensagem_sistema = f"{self.player_pkmn.nome} usou {golpe.nome}!"
        self.msg_extra = msg_efeito 
        self.estado_atual = "ANIMANDO_PLAYER"
        self.timer_espera = pg.time.get_ticks()

    def contra_ataque_inimigo(self):
        if not self.enemy_pkmn.esta_vivo(): return

        if len(self.enemy_pkmn.golpes) > 0:
            golpe = random.choice(self.enemy_pkmn.golpes)
        else:
            golpe = Golpe("Investida", 20, "Normal")

        dano, msg_efeito = self.calcular_dano(self.enemy_pkmn, self.player_pkmn, golpe)
        self.player_pkmn.receber_dano(dano)
        
        self.mensagem_sistema = f"Inimigo usou {golpe.nome}!"
        self.msg_extra = msg_efeito
        self.estado_atual = "ANIMANDO_INIMIGO"
        self.timer_espera = pg.time.get_ticks()

    def trocar_pokemon_auto(self):
        for pkmn in self.equipe:
            if pkmn.esta_vivo():
                self.player_pkmn = pkmn
                self.visual_hp_player = float(self.player_pkmn.hp_atual)
                self.mensagem_sistema = f"{pkmn.nome}, vai!"
                return True
        return False

    def get_cor_hp(self, atual, maximo):
        pct = atual / maximo
        if pct > 0.5: return (0, 200, 0)
        if pct > 0.2: return (255, 200, 0)
        return (200, 0, 0)

    def get_type_modifier(self, ataque_tipo, defensor_tipo):
        tabela = {
            "Fogo":  {"Grama": 2.0, "Agua": 0.5}, 
            "Agua":  {"Fogo": 2.0,  "Grama": 0.5}, 
            "Grama": {"Agua": 2.0,  "Fogo": 0.5}
        }
        return tabela.get(ataque_tipo, {}).get(defensor_tipo, 1.0)

    def calcular_dano(self, atq, defe, golpe):
        chance = random.randint(1, 100)
        if chance > golpe.precisao: return 0, "Errou!"
        
        mult = self.get_type_modifier(golpe.tipo, defe.tipo)
        nivel_factor = (2 * atq.nivel / 5) + 2
        stats_ratio = atq.atk / max(1, defe.defense)
        
        dano_base = ((nivel_factor * golpe.poder * stats_ratio) / 50) + 2
        dano_final = int(dano_base * mult)
        
        msg = ""
        if mult > 1: msg = "Foi super efetivo!"
        elif mult < 1: msg = "Não foi muito efetivo..."
        
        return max(1, dano_final), msg

    def desenhar(self, screen):
        # --- DESENHO DO FUNDO ---
        if self.bg_batalha:
            screen.blit(self.bg_batalha, (0, 0))
        else:
            screen.fill((40, 40, 40)) 
        
        velocidade_animacao = 0.3
        
        if self.visual_hp_enemy > self.enemy_pkmn.hp_atual:
            self.visual_hp_enemy -= velocidade_animacao
            if self.visual_hp_enemy < self.enemy_pkmn.hp_atual: self.visual_hp_enemy = self.enemy_pkmn.hp_atual
        
        if self.visual_hp_player > self.player_pkmn.hp_atual:
            self.visual_hp_player -= velocidade_animacao
            if self.visual_hp_player < self.player_pkmn.hp_atual: self.visual_hp_player = self.player_pkmn.hp_atual
        elif self.visual_hp_player < self.player_pkmn.hp_atual:
            self.visual_hp_player += velocidade_animacao
            if self.visual_hp_player > self.player_pkmn.hp_atual: self.visual_hp_player = self.player_pkmn.hp_atual

        agora = pg.time.get_ticks()
        
        # --- LÓGICA DE ESTADOS ---
        if self.estado_atual == "ENTRADA_ANIMACAO":
            # Anima entrada
            if self.anim_x_player < self.target_x_player:
                self.anim_x_player += 15
                if self.anim_x_player > self.target_x_player: self.anim_x_player = self.target_x_player
            if self.anim_x_enemy > self.target_x_enemy:
                self.anim_x_enemy -= 15
                if self.anim_x_enemy < self.target_x_enemy: self.anim_x_enemy = self.target_x_enemy
            
            if self.anim_x_player == self.target_x_player and self.anim_x_enemy == self.target_x_enemy:
                self.estado_atual = "MENSAGEM_INICIAL"
                self.mensagem_sistema = f"Um {self.enemy_pkmn.nome} selvagem apareceu!"
                self.timer_espera = agora

        elif self.estado_atual == "MENSAGEM_INICIAL":
            if agora - self.timer_espera > 2500:
                self.estado_atual = "MENU_PRINCIPAL"
                self.mensagem_sistema = "O que voce vai fazer?"

        # --- ESTADO DE ANIMAÇÃO DE TROCA ---
        elif self.estado_atual == "TROCA_ANIMACAO":
            # 1. Anima o Player entrando
            if self.anim_x_player < self.target_x_player:
                self.anim_x_player += 15
                if self.anim_x_player > self.target_x_player:
                    self.anim_x_player = self.target_x_player
            
            # 2. Quando chegar na posição, espera 1s para ler "Vai, Pokemon!"
            if self.anim_x_player == self.target_x_player:
                if agora - self.timer_espera > 1000:
                    # 3. Passa a vez para o inimigo atacar (Jogador perde turno)
                    self.contra_ataque_inimigo()

        # --- ESTADO DE ESPERA DA CAPTURA (SUSPENSE) ---
        elif self.estado_atual == "AGUARDANDO_CAPTURA":
            # IMPLEMENTAÇÃO: Espera exatos 1500ms (1.5s)
            if agora - self.timer_espera > 1500:
                if self.captura_sucesso:
                    self.battle_over = True
                    self.vencedor = "CAPTURA"
                    self.mensagem_sistema = f"Gotcha! {self.enemy_pkmn.nome} foi capturado!"
                    
                    # CORREÇÃO BUG 2: Adiciona APENAS UMA VEZ e muda estado para travar loop
                    self.equipe.append(self.enemy_pkmn)
                    self.estado_atual = "FIM_BATALHA" 
                else:
                    # Falhou: Mostra msg de erro e vai para ANIMANDO_PLAYER para delay de leitura
                    self.mensagem_sistema = self.msg_falha_captura
                    self.estado_atual = "ANIMANDO_PLAYER"
                    self.msg_extra = "" 
                    self.timer_espera = agora

        elif self.estado_atual == "ANIMANDO_PLAYER":
            if self.animacao_concluida():
                if self.msg_extra != "":
                    if agora - self.timer_espera > 1000: 
                        self.mensagem_sistema = self.msg_extra 
                        
                        # Se veio de falha de captura ou fuga falha, inimigo ataca
                        if "quebrou" in self.msg_extra or "falhou" in self.msg_extra or "escapou" in self.msg_extra: 
                            self.contra_ataque_inimigo() 
                        
                        self.msg_extra = "" 
                        self.timer_espera = agora 
                
                elif agora - self.timer_espera > 1500: # Delay padrão para ler mensagens
                    if not self.enemy_pkmn.esta_vivo():
                        self.battle_over = True
                        self.vencedor = "PLAYER"
                        xp_ganho = self.enemy_pkmn.nivel * 15
                        subiu = self.player_pkmn.ganhar_xp(xp_ganho)
                        
                        self.mensagem_sistema = f"Inimigo derrotado! Ganhou {xp_ganho} XP."
                        if subiu:
                            self.subiu_de_nivel = True
                        
                        self.estado_atual = "LEVEL_UP"
                        self.timer_espera = agora
                    else:
                        # Se ninguém morreu, turno do inimigo
                        self.contra_ataque_inimigo()

        elif self.estado_atual == "LEVEL_UP":
            if agora - self.timer_espera > 2000:
                if self.subiu_de_nivel:
                    self.mensagem_sistema = f"{self.player_pkmn.nome} subiu para o Nvl {self.player_pkmn.nivel}!"
                    self.subiu_de_nivel = False
                    self.timer_espera = agora
                else:
                    self.battle_over = True
                    self.vencedor = "PLAYER"

        elif self.estado_atual == "ANIMANDO_INIMIGO":
            if self.animacao_concluida():
                if self.msg_extra != "":
                    if agora - self.timer_espera > 1000:
                        self.mensagem_sistema = self.msg_extra
                        self.msg_extra = ""
                        self.timer_espera = agora
                elif agora - self.timer_espera > 1000:
                    if not self.player_pkmn.esta_vivo():
                        trocou = self.trocar_pokemon_auto()
                        if not trocou:
                            self.battle_over = True
                            self.vencedor = "INIMIGO"
                            self.mensagem_sistema = "Voce perdeu..."
                        else:
                            self.estado_atual = "MENU_PRINCIPAL"
                            self.cursor_pos = 0
                    else:
                        # CORREÇÃO BUG 1: Reseta max_opcoes para 3 ao voltar ao menu
                        self.estado_atual = "MENU_PRINCIPAL"
                        self.cursor_pos = 0
                        self.max_opcoes = 3 
                        self.mensagem_sistema = "O que voce vai fazer?"

        # --- DESENHO HUD ---
        mostrar_hud = self.estado_atual not in ["ENTRADA_ANIMACAO", "MENSAGEM_INICIAL"]

        if mostrar_hud:
            # HUD Inimigo
            pg.draw.rect(screen, (220, 220, 220), (50, 50, 300, 80), border_radius=8)
            nome_inimigo = f"{self.enemy_pkmn.nome} Lv.{self.enemy_pkmn.nivel}"
            screen.blit(self.font_big.render(nome_inimigo, True, (0,0,0)), (60, 55))
            
            pg.draw.rect(screen, (100,100,100), (60, 95, 200, 15))
            pct_enemy = self.visual_hp_enemy / self.enemy_pkmn.hp_max
            cor_enemy = self.get_cor_hp(self.visual_hp_enemy, self.enemy_pkmn.hp_max)
            pg.draw.rect(screen, cor_enemy, (60, 95, int(200 * pct_enemy), 15))

            # HUD Player
            pg.draw.rect(screen, (220, 220, 220), (450, 320, 320, 100), border_radius=8)
            nome_player = f"{self.player_pkmn.nome} Lv.{self.player_pkmn.nivel}"
            screen.blit(self.font_big.render(nome_player, True, (0,0,0)), (460, 330))
            screen.blit(self.font.render(f"HP: {int(self.visual_hp_player)}/{self.player_pkmn.hp_max}", True, (0,0,0)), (460, 370))
            
            pg.draw.rect(screen, (100,100,100), (600, 375, 150, 15))
            pct_player = self.visual_hp_player / self.player_pkmn.hp_max
            cor_player = self.get_cor_hp(self.visual_hp_player, self.player_pkmn.hp_max)
            pg.draw.rect(screen, cor_player, (600, 375, int(150 * pct_player), 15))

        # --- SPRITES ---

        rect_visivel_inimigo = self.enemy_pkmn.image.get_bounding_rect()
        pos_y_real_inimigo = 310 - rect_visivel_inimigo.bottom

        pos_inimigo = (self.anim_x_enemy - 10, pos_y_real_inimigo) 
        screen.blit(self.enemy_pkmn.image, pos_inimigo)

        # altura da tela é 600 

        rect_visivel_player = self.player_pkmn.back_image.get_bounding_rect()
        pos_y_real = 430 - rect_visivel_player.bottom
        pos_player = (self.anim_x_player, pos_y_real) # !!

        #print(self.player_pkmn.back_image.get_height())
        screen.blit(self.player_pkmn.back_image, pos_player)

        # --- MENU INFERIOR (AUMENTADO) ---
        pg.draw.rect(screen, (30, 30, 80), (0, 430, 800, 170))
        pg.draw.rect(screen, (255, 255, 255), (0, 430, 800, 170), 4)
        
        screen.blit(self.font_msg.render(self.mensagem_sistema, True, (255, 255, 0)), (30, 450))

        # Opções
        if mostrar_hud and not self.battle_over:
            cor_padrao = (200, 200, 200)
            cor_select = (255, 255, 255)
            y_base = 510 
            
            if self.estado_atual == "MENU_PRINCIPAL":
                opcoes = ["LUTAR", "BAG", "FUGIR"]
                x_base_princ = 80 
                spacing = 250
                for i, op in enumerate(opcoes):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    prefixo = "> " if i == self.cursor_pos else "   "
                    screen.blit(self.font_big.render(prefixo + op, True, cor), (x_base_princ + (i * spacing), y_base))
            
            elif self.estado_atual == "MENU_GOLPES":
                x_base_cols = 50 
                col_spacing = 400
                for i, golpe in enumerate(self.player_pkmn.golpes):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    prefixo = "> " if i == self.cursor_pos else "   "
                    
                    col = i % 2
                    row = i // 2
                    pos_x = x_base_cols + (col * col_spacing)
                    pos_y = y_base + (row * 30)
                    
                    screen.blit(self.font_big.render(prefixo + golpe.nome, True, cor), (pos_x, pos_y))

            elif self.estado_atual == "MENU_MOCHILA":
                q_pocao = self.inventario.get('Poção de Vida', 0)
                q_poke = self.inventario.get('Pokebola', 0)
                q_great = self.inventario.get('Grande Bola', 0)

                opcoes_bag = [
                    "Trocar Pokemon", 
                    f"Usar Poção ({q_pocao})", 
                    f"Pokebola ({q_poke})", 
                    f"Grande Bola ({q_great})"
                ]
                
                x_base_cols = 50
                col_spacing = 400
                
                for i, op in enumerate(opcoes_bag):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    prefixo = "> " if i == self.cursor_pos else "   "
                    
                    col = i % 2
                    row = i // 2
                    pos_x = x_base_cols + (col * col_spacing)
                    pos_y = y_base + (row * 30)
                    
                    screen.blit(self.font_big.render(prefixo + op, True, cor), (pos_x, pos_y))

            elif self.estado_atual == "MENU_TROCA":
                x_base_cols = 50
                col_spacing = 400
                
                for i, pkmn in enumerate(self.equipe):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    
                    if pkmn == self.player_pkmn or not pkmn.esta_vivo():
                        cor = (100, 100, 100)
                        if i == self.cursor_pos: cor = (150, 150, 150)

                    prefixo = "> " if i == self.cursor_pos else "   "
                    texto_pkmn = f"{prefixo}{pkmn.nome} (HP: {pkmn.hp_atual}/{pkmn.hp_max})"
                    
                    col = i % 2
                    row = i // 2
                    pos_x = x_base_cols + (col * col_spacing)
                    
                    # CORREÇÃO BUG 3: Ajuste de altura para caber 6 pokémons na tela
                    pos_y = 490 + (row * 30) 

                    screen.blit(self.font_big.render(texto_pkmn, True, cor), (pos_x, pos_y))
        
        elif self.battle_over and self.estado_atual != "LEVEL_UP":
             screen.blit(self.font_msg.render("Pressione ESPACO para sair", True, (255, 255, 255)), (30, 540))
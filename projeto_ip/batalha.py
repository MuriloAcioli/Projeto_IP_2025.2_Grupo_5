import pygame as pg
import random
from pokemon import Golpe 

class BatalhaPokemon:
    def __init__(self, player_data, enemy_pkmn, inventario):
        # --- 1. CONFIGURAÇÃO DA EQUIPE ---
        if isinstance(player_data, list):
            self.equipe = player_data
            self.player_pkmn = player_data[0] 
        else:
            self.equipe = [player_data]
            self.player_pkmn = player_data

        self.enemy_pkmn = enemy_pkmn
        self.inventario = inventario
        
        # --- 2. VARIÁVEIS PARA ANIMAÇÃO DE HP ---
        self.visual_hp_player = float(self.player_pkmn.hp_atual)
        self.visual_hp_enemy = float(self.enemy_pkmn.hp_atual)
        
        # --- 3. ESTADOS DA BATALHA ---
        self.turno = 1
        self.battle_over = False
        self.vencedor = None
        
        self.estado_atual = "MENU_PRINCIPAL"
        self.mensagem_sistema = "O que voce vai fazer?"
        
        # NOVA VARIÁVEL: Guarda a mensagem de "Super Efetivo" para mostrar depois
        self.msg_extra = "" 
        
        # --- 4. UI E CURSOR ---
        self.cursor_pos = 0 
        self.max_opcoes = 3 
        
        pg.font.init()
        # Fontes normais
        self.font = pg.font.SysFont("Arial", 22)
        self.font_big = pg.font.SysFont("Arial", 30, bold=True)
        
        # --- NOVA FONTE PARA A MENSAGEM (MAIOR) ---
        # Tamanho 28 Bold preenche bem o espaço sem encostar no menu de baixo
        self.font_msg = pg.font.SysFont("Arial", 28, bold=True) 
        
        self.timer_espera = 0

    # =========================================================================
    # INPUT E NAVEGAÇÃO
    # =========================================================================
    def processar_input(self, event):
        if self.estado_atual in ["ANIMANDO_PLAYER", "ANIMANDO_INIMIGO"]:
            return

        if self.battle_over and self.animacao_concluida():
            return

        # Navegação
        if event.key == pg.K_d or event.key == pg.K_RIGHT or event.key == pg.K_s or event.key == pg.K_DOWN:
            self.cursor_pos = (self.cursor_pos + 1) % self.max_opcoes
        
        elif event.key == pg.K_a or event.key == pg.K_LEFT or event.key == pg.K_w or event.key == pg.K_UP:
            self.cursor_pos = (self.cursor_pos - 1) % self.max_opcoes

        # Confirmar
        elif event.key == pg.K_RETURN or event.key == pg.K_SPACE or event.key == pg.K_e:
            self.confirmar_selecao()

        # Voltar
        elif event.key == pg.K_BACKSPACE or event.key == pg.K_ESCAPE:
            if self.estado_atual == "MENU_GOLPES":
                self.estado_atual = "MENU_PRINCIPAL"
                self.cursor_pos = 0
                self.max_opcoes = 3

    def animacao_concluida(self):
        margem = 0.5
        enemy_ok = abs(self.visual_hp_enemy - self.enemy_pkmn.hp_atual) < margem
        player_ok = abs(self.visual_hp_player - self.player_pkmn.hp_atual) < margem
        return enemy_ok and player_ok

    def confirmar_selecao(self):
        if self.estado_atual == "MENU_PRINCIPAL":
            if self.cursor_pos == 0: # LUTAR
                self.estado_atual = "MENU_GOLPES"
                self.cursor_pos = 0
                self.max_opcoes = len(self.player_pkmn.golpes)
                self.mensagem_sistema = "Escolha o ataque:"
            elif self.cursor_pos == 1: # BAG
                self.usar_pocao()
            elif self.cursor_pos == 2: # FUGIR
                self.tentar_fugir()

        elif self.estado_atual == "MENU_GOLPES":
            self.turno_lutar(self.cursor_pos)

    # =========================================================================
    # AÇÕES DO JOGADOR
    # =========================================================================
    def usar_pocao(self):
        qtd = self.inventario.get('Pocao', 0)
        if qtd > 0:
            self.inventario['Pocao'] -= 1
            cura = 20
            self.player_pkmn.hp_atual = min(self.player_pkmn.hp_max, self.player_pkmn.hp_atual + cura)
            self.mensagem_sistema = f"Usou Pocao! +{cura} HP."
            self.msg_extra = "" 
            
            self.estado_atual = "ANIMANDO_PLAYER" 
            self.timer_espera = pg.time.get_ticks()
        else:
            self.mensagem_sistema = "Voce nao tem Pocoes!"

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
                self.mensagem_sistema = "Nao conseguiu fugir!"
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

    # =========================================================================
    # AÇÕES DO INIMIGO
    # =========================================================================
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

    # =========================================================================
    # MATEMÁTICA E CORES
    # =========================================================================
    def get_cor_hp(self, atual, maximo):
        pct = atual / maximo
        if pct > 0.5: return (0, 200, 0)      # Verde
        if pct > 0.2: return (255, 200, 0)    # Amarelo
        return (200, 0, 0)                    # Vermelho

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
        elif mult < 1: msg = "Nao foi muito efetivo..."
        
        return max(1, dano_final), msg

    # =========================================================================
    # RENDERIZAÇÃO E LOGICA DE FLUXO
    # =========================================================================
    def desenhar(self, screen):
        screen.fill((40, 40, 40)) 
        
        # --- LÓGICA DE ANIMAÇÃO DE HP ---
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

        # --- GERENCIADOR DE TURNOS ---
        agora = pg.time.get_ticks()
        
        # >>> VEZ DO JOGADOR <<<
        if self.estado_atual == "ANIMANDO_PLAYER":
            if self.animacao_concluida():
                
                if self.msg_extra != "":
                    if agora - self.timer_espera > 1000: 
                        self.mensagem_sistema = self.msg_extra 
                        self.msg_extra = "" 
                        self.timer_espera = agora 
                
                elif agora - self.timer_espera > 1000: 
                    if not self.enemy_pkmn.esta_vivo():
                        self.battle_over = True
                        self.vencedor = "PLAYER"
                        self.mensagem_sistema = "Inimigo derrotado!"
                    else:
                        self.contra_ataque_inimigo()

        # >>> VEZ DO INIMIGO <<<
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
                        self.estado_atual = "MENU_PRINCIPAL"
                        self.cursor_pos = 0
                        self.mensagem_sistema = "O que voce vai fazer?"

        # --- DESENHO HUD ---
        # Inimigo
        pg.draw.rect(screen, (220, 220, 220), (50, 50, 300, 80), border_radius=8)
        screen.blit(self.font_big.render(self.enemy_pkmn.nome, True, (0,0,0)), (60, 55))
        pg.draw.rect(screen, (100,100,100), (60, 95, 200, 15))
        pct_enemy = self.visual_hp_enemy / self.enemy_pkmn.hp_max
        cor_enemy = self.get_cor_hp(self.visual_hp_enemy, self.enemy_pkmn.hp_max)
        pg.draw.rect(screen, cor_enemy, (60, 95, int(200 * pct_enemy), 15))

        # Player
        pg.draw.rect(screen, (220, 220, 220), (450, 320, 320, 100), border_radius=8)
        screen.blit(self.font_big.render(self.player_pkmn.nome, True, (0,0,0)), (460, 330))
        screen.blit(self.font.render(f"HP: {int(self.visual_hp_player)}/{self.player_pkmn.hp_max}", True, (0,0,0)), (460, 370))
        pg.draw.rect(screen, (100,100,100), (600, 375, 150, 15))
        pct_player = self.visual_hp_player / self.player_pkmn.hp_max
        cor_player = self.get_cor_hp(self.visual_hp_player, self.player_pkmn.hp_max)
        pg.draw.rect(screen, cor_player, (600, 375, int(150 * pct_player), 15))

        # Sprites
        screen.blit(self.enemy_pkmn.image, (500, 60))
        screen.blit(self.player_pkmn.image, (100, 280))

        # Menu Inferior
        pg.draw.rect(screen, (30, 30, 80), (0, 480, 800, 120))
        pg.draw.rect(screen, (255, 255, 255), (0, 480, 800, 120), 4)
        
        # --- AQUI ESTÁ A ALTERAÇÃO: Usando font_msg em vez de font ---
        screen.blit(self.font_msg.render(self.mensagem_sistema, True, (255, 255, 0)), (30, 490))

        # Opções
        if self.estado_atual in ["MENU_PRINCIPAL", "MENU_GOLPES"] and not self.battle_over:
            cor_padrao = (200, 200, 200)
            cor_select = (255, 255, 255)
            x_base, y_base = 30, 540
            
            if self.estado_atual == "MENU_PRINCIPAL":
                opcoes = ["LUTAR", "BAG", "FUGIR"]
                for i, op in enumerate(opcoes):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    prefixo = "> " if i == self.cursor_pos else "   "
                    screen.blit(self.font_big.render(prefixo + op, True, cor), (x_base + (i * 200), y_base))
            
            elif self.estado_atual == "MENU_GOLPES":
                for i, golpe in enumerate(self.player_pkmn.golpes):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    prefixo = "> " if i == self.cursor_pos else "   "
                    screen.blit(self.font_big.render(prefixo + golpe.nome, True, cor), (x_base + ((i%2) * 300), y_base + ((i//2) * 30)))
        
        elif self.battle_over:
             screen.blit(self.font_msg.render("Pressione ESPACO para sair", True, (255, 255, 255)), (30, 540))
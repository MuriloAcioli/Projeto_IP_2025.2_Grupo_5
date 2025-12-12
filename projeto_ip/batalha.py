import pygame as pg
import random
from pokemon import Golpe # Importando para garantir que o tipo exista

class BatalhaPokemon:
    def __init__(self, player_data, enemy_pkmn, inventario):
        # --- 1. CONFIGURAÇÃO DA EQUIPE ---
        # Garante que seja uma lista, mesmo se vier apenas um objeto
        if isinstance(player_data, list):
            self.equipe = player_data
            self.player_pkmn = player_data[0] 
        else:
            self.equipe = [player_data]
            self.player_pkmn = player_data

        self.enemy_pkmn = enemy_pkmn
        self.inventario = inventario
        
        # --- 2. ESTADOS DA BATALHA ---
        self.turno = 1
        self.battle_over = False
        self.vencedor = None
        
        self.estado_atual = "MENU_PRINCIPAL"
        self.mensagem_sistema = "O que voce vai fazer?"
        
        # --- 3. UI E CURSOR ---
        self.cursor_pos = 0 # Posição atual (0, 1, 2...)
        self.max_opcoes = 3 # Quantas opções tem no menu atual
        
        pg.font.init()
        self.font = pg.font.SysFont("Arial", 22)
        self.font_big = pg.font.SysFont("Arial", 30, bold=True)

    # =========================================================================
    # INPUT E NAVEGAÇÃO
    # =========================================================================
    def processar_input(self, event):
        if self.battle_over: return

        # --- A. NAVEGAÇÃO (Setas / WASD) ---
        if event.key == pg.K_d or event.key == pg.K_RIGHT or event.key == pg.K_s or event.key == pg.K_DOWN:
            self.cursor_pos = (self.cursor_pos + 1) % self.max_opcoes
        
        elif event.key == pg.K_a or event.key == pg.K_LEFT or event.key == pg.K_w or event.key == pg.K_UP:
            self.cursor_pos = (self.cursor_pos - 1) % self.max_opcoes

        # --- B. CONFIRMAR (Enter / Espaço / E) ---
        elif event.key == pg.K_RETURN or event.key == pg.K_SPACE or event.key == pg.K_e:
            self.confirmar_selecao()

        # --- C. VOLTAR (Backspace / Esc) ---
        elif event.key == pg.K_BACKSPACE or event.key == pg.K_ESCAPE:
            if self.estado_atual == "MENU_GOLPES":
                self.estado_atual = "MENU_PRINCIPAL"
                self.cursor_pos = 0
                self.max_opcoes = 3

    def confirmar_selecao(self):
        # 1. Lógica do MENU PRINCIPAL (0: Lutar, 1: Bag, 2: Fugir)
        if self.estado_atual == "MENU_PRINCIPAL":
            if self.cursor_pos == 0: # LUTAR
                self.estado_atual = "MENU_GOLPES"
                self.cursor_pos = 0
                self.max_opcoes = len(self.player_pkmn.golpes) # Limita cursor aos golpes que tem
                self.mensagem_sistema = "Escolha o ataque:"
            
            elif self.cursor_pos == 1: # BAG
                self.usar_pocao()
                
            elif self.cursor_pos == 2: # FUGIR
                self.tentar_fugir()

        # 2. Lógica do MENU DE GOLPES
        elif self.estado_atual == "MENU_GOLPES":
            # Usa o golpe selecionado pelo cursor
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
            
            # Usar item gasta turno
            self.contra_ataque_inimigo()
        else:
            self.mensagem_sistema = "Voce nao tem Pocoes!"

    def tentar_fugir(self):
        # Se for mais rápido, foge sempre. Se não, 50% de chance.
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
                self.contra_ataque_inimigo()

    def turno_lutar(self, indice):
        if indice >= len(self.player_pkmn.golpes): return
        
        golpe = self.player_pkmn.golpes[indice]
        
        # Player ataca
        dano, msg = self.calcular_dano(self.player_pkmn, self.enemy_pkmn, golpe)
        self.enemy_pkmn.receber_dano(dano)
        self.mensagem_sistema = f"Usou {golpe.nome}! {msg}"

        # Verifica vitória ou passa a vez
        if not self.enemy_pkmn.esta_vivo():
            self.battle_over = True
            self.vencedor = "PLAYER"
            self.mensagem_sistema = "Inimigo derrotado!"
        else:
            self.contra_ataque_inimigo()
            
        # Reseta menu após ataque
        self.estado_atual = "MENU_PRINCIPAL"
        self.cursor_pos = 0 
        self.max_opcoes = 3

    # =========================================================================
    # AÇÕES DO INIMIGO (IA SIMPLES)
    # =========================================================================
    def contra_ataque_inimigo(self):
        if len(self.enemy_pkmn.golpes) > 0:
            golpe = random.choice(self.enemy_pkmn.golpes)
        else:
            # Fallback seguro caso o inimigo não tenha golpes
            golpe = Golpe("Investida", 20, "Normal")

        # Inimigo ataca
        dano, msg = self.calcular_dano(self.enemy_pkmn, self.player_pkmn, golpe)
        self.player_pkmn.receber_dano(dano)
        self.mensagem_sistema += f" Inimigo: {golpe.nome}"

        # Verifica derrota do jogador
        if not self.player_pkmn.esta_vivo():
            trocou = self.trocar_pokemon_auto()
            if not trocou:
                self.battle_over = True
                self.vencedor = "INIMIGO"
                self.mensagem_sistema = "Todos seus Pokemons desmaiaram..."

    def trocar_pokemon_auto(self):
        """Tenta encontrar o próximo Pokémon vivo na equipe."""
        for pkmn in self.equipe:
            if pkmn.esta_vivo():
                self.player_pkmn = pkmn
                self.mensagem_sistema = f"{pkmn.nome}, vai!"
                return True
        return False

    # =========================================================================
    # MATEMÁTICA DE COMBATE
    # =========================================================================
    def get_type_modifier(self, ataque_tipo, defensor_tipo):
        tabela = {
            "Fogo":  {"Grama": 2.0, "Agua": 0.5}, 
            "Agua":  {"Fogo": 2.0,  "Grama": 0.5}, 
            "Grama": {"Agua": 2.0,  "Fogo": 0.5}
        }
        return tabela.get(ataque_tipo, {}).get(defensor_tipo, 1.0)

    def calcular_dano(self, atq, defe, golpe):
        # Precisão
        chance = random.randint(1, 100)
        if chance > golpe.precisao: return 0, "Errou!"
        
        # Multiplicadores
        mult = self.get_type_modifier(golpe.tipo, defe.tipo)
        
        # Fórmula de Dano
        dano = int((golpe.poder * (atq.atk / defe.defense)) * mult) + 2
        msg = "(Super Efetivo!)" if mult > 1 else ("(Pouco Efetivo...)" if mult < 1 else "")
        return max(1, dano), msg

    # =========================================================================
    # RENDERIZAÇÃO (DESENHO NA TELA)
    # =========================================================================
    def desenhar(self, screen):
        screen.fill((40, 40, 40)) 
        
        # --- HUD: INIMIGO ---
        pg.draw.rect(screen, (220, 220, 220), (50, 50, 300, 80), border_radius=8)
        screen.blit(self.font_big.render(self.enemy_pkmn.nome, True, (0,0,0)), (60, 55))
        
        # Barra de Vida Inimigo
        pg.draw.rect(screen, (100,100,100), (60, 95, 200, 15))
        pg.draw.rect(screen, (0,200,0), (60, 95, 200 * (self.enemy_pkmn.hp_atual/self.enemy_pkmn.hp_max), 15))

        # --- HUD: PLAYER ---
        pg.draw.rect(screen, (220, 220, 220), (450, 320, 320, 100), border_radius=8)
        screen.blit(self.font_big.render(self.player_pkmn.nome, True, (0,0,0)), (460, 330))
        screen.blit(self.font.render(f"HP: {self.player_pkmn.hp_atual}/{self.player_pkmn.hp_max}", True, (0,0,0)), (460, 370))
        
        # Barra de Vida Player
        pg.draw.rect(screen, (100,100,100), (600, 375, 150, 15))
        pg.draw.rect(screen, (0,200,0), (600, 375, 150 * (self.player_pkmn.hp_atual/self.player_pkmn.hp_max), 15))

        # --- SPRITES ---
        screen.blit(self.enemy_pkmn.image, (500, 60))
        screen.blit(self.player_pkmn.back_image, (100, 280))

        # --- MENU INFERIOR (CAIXA DE TEXTO) ---
        pg.draw.rect(screen, (30, 30, 80), (0, 480, 800, 120))
        pg.draw.rect(screen, (255, 255, 255), (0, 480, 800, 120), 4)
        
        screen.blit(self.font.render(self.mensagem_sistema, True, (255, 255, 0)), (30, 490))

        # --- DESENHO DAS OPÇÕES DO MENU ---
        if not self.battle_over:
            cor_padrao = (200, 200, 200)
            cor_select = (255, 255, 255) # Branco brilhante para o selecionado
            
            x_base = 30
            y_base = 540
            espaco = 200
            
            # Opções do Menu Principal
            if self.estado_atual == "MENU_PRINCIPAL":
                opcoes = ["LUTAR", "BAG", "FUGIR"]
                for i, op in enumerate(opcoes):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    prefixo = "> " if i == self.cursor_pos else "   " # Desenha a setinha
                    texto = self.font_big.render(prefixo + op, True, cor)
                    screen.blit(texto, (x_base + (i * espaco), y_base))
            
            # Opções do Menu de Golpes
            elif self.estado_atual == "MENU_GOLPES":
                for i, golpe in enumerate(self.player_pkmn.golpes):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    prefixo = "> " if i == self.cursor_pos else "   "
                    texto = self.font_big.render(prefixo + golpe.nome, True, cor)
                    
                    # Organiza em grade 2x2
                    coluna = i % 2
                    linha = i // 2
                    screen.blit(texto, (x_base + (coluna * 300), y_base + (linha * 30)))
        
        else:
            # Mensagem de fim de batalha
            screen.blit(self.font_big.render("Pressione ESPACO para sair", True, (255, 255, 255)), (30, 540))
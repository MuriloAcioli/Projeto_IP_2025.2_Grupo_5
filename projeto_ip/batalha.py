import pygame as pg
import random
import os
from pokemon import Golpe 
from pokedex import POKEDEX, progresso_pokedex
import math

# Define o diretório base
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))

class BatalhaPokemon:
    def __init__(self, player_data, enemy_data, inventario, tipo_batalha="SELVAGEM",inimigo_nome=None):
        # Tipo de batalha: "SELVAGEM" ou "TREINADOR"
        self.tipo_batalha = tipo_batalha
        self.nome_inimigo = inimigo_nome
        
        # --- Configuração da Equipe do Jogador ---
        if isinstance(player_data, list):
            self.equipe = player_data
            indice_poke_escolhido = 0
            
            for pokemon in player_data:
                if pokemon.hp_atual > 0:
                    indice_poke_escolhido = player_data.index(pokemon)
                    break
             
            self.player_pkmn = player_data[indice_poke_escolhido] 
        else:
            self.equipe = [player_data]
            self.player_pkmn = player_data

        # --- Configuração do Inimigo (Suporte a Time) ---
        if isinstance(enemy_data, list):
            self.enemy_equipe = enemy_data
            self.enemy_pkmn = self.enemy_equipe[0] # Começa com o primeiro
        else:
            self.enemy_equipe = [enemy_data]
            self.enemy_pkmn = enemy_data
            status_atual = progresso_pokedex.get(self.enemy_pkmn.nome, "desconhecido")
            if status_atual != "capturado":
                progresso_pokedex[self.enemy_pkmn.nome] = "visto"

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
        
        self.offset_y_player = 0
        self.offset_y_enemy = 0
        self.atacando = 0
        self.altura_pulo = 20

        self.cursor_pos = 0 
        self.max_opcoes = 3 
        
        # Variáveis de controle para troca obrigatória
        self.troca_obrigatoria = False
        self.confirmar_troca_inimigo = False
        self.cursor_confirmacao = 0  # 0 = Sim, 1 = Não
        self.troca_apos_derrota_inimigo = False  # Flag para controlar troca após derrotar inimigo

        try:
            path_balls = os.path.join(DIRETORIO_BASE, "assets/coletaveis/pokebolas.png")
            sheet_balls = pg.image.load(path_balls).convert_alpha()
            scale_size = (48, 48)
            
            self.sprites_balls = {}
            # Pokebola (0,0)
            img = sheet_balls.subsurface((0, 0, 12, 12))
            self.sprites_balls['Pokebola'] = pg.transform.scale(img, scale_size)
            
            # Grande Bola (11,0)
            img = sheet_balls.subsurface((12, 0, 12, 12))
            self.sprites_balls['Grande Bola'] = pg.transform.scale(img, scale_size)
            
            # Ultra Ball (23,0)
            img = sheet_balls.subsurface((24, 0, 12, 12)) 
            self.sprites_balls['Ultra Ball'] = pg.transform.scale(img, scale_size)
            
        except Exception as e:
            # print(f"Erro ao carregar bolas: {e}")
            self.sprites_balls = {}

        # --- VARIÁVEIS DA ANIMAÇÃO DA BOLA ---
        self.anim_bola_ativa = False
        self.bola_img_atual = None
        self.bola_pos = (0, 0)
        self.bola_rotacao = 0
        self.bola_start_time = 0
        self.bola_tipo_atual = ""
        self.bola_cor_filtro = None 
        self.bola_pos_alvo = (0, 0)
        # -------------------------------------

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
            # print("ERRO: O arquivo NÃO existe neste caminho.")
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
                      "MENSAGEM_INICIAL", "ANIMANDO_PLAYER", "ANIMANDO_INIMIGO", 
                      "LEVEL_UP", "FIM_BATALHA", "TROCA_ANIMACAO_INIMIGO", "ESPERANDO_TROCA_INIMIGO", "ANIMACAO_MORTE_INIMIGO"]
        
        if self.estado_atual in bloqueados:
            return
        
        # Menu de confirmação de troca após derrotar inimigo
        if self.estado_atual == "CONFIRMACAO_TROCA_INIMIGO":
            if event.key in [pg.K_a, pg.K_LEFT, pg.K_d, pg.K_RIGHT]:
                self.cursor_confirmacao = 1 - self.cursor_confirmacao  # Toggle entre 0 e 1
            elif event.key in [pg.K_RETURN, pg.K_SPACE, pg.K_e]:
                if self.cursor_confirmacao == 0:  # Sim
                    self.confirmar_troca_inimigo = False
                    self.troca_apos_derrota_inimigo = True  # Ativa flag
                    self.estado_atual = "MENU_TROCA"
                    self.troca_obrigatoria = True
                    self.cursor_pos = 0
                    self.max_opcoes = len(self.equipe)
                    self.mensagem_sistema = "Escolha um Pokemon:"
                else:  # Não
                    self.confirmar_troca_inimigo = False
                    self.trocar_inimigo_auto()
            return

        if self.battle_over and self.animacao_concluida() and self.estado_atual != "LEVEL_UP":
            return

        # --- DEFINIÇÃO DINÂMICA DE COLUNAS ---
        n_colunas = 1  
        
        if self.estado_atual == "MENU_GOLPES":
            n_colunas = 2  
        elif self.estado_atual == "MENU_MOCHILA":
            n_colunas = 2  
        elif self.estado_atual == "MENU_TROCA":
            n_colunas = 2  
        elif self.estado_atual == "MENU_PRINCIPAL":
            n_colunas = 3  

        total = self.max_opcoes

        # --- NAVEGAÇÃO DE CURSOR (GRID) ---
        
        # DIREITA
        if event.key == pg.K_d or event.key == pg.K_RIGHT:
            if (self.cursor_pos + 1) % n_colunas != 0 and self.cursor_pos + 1 < total:
                self.cursor_pos += 1
            else:
                self.cursor_pos -= (self.cursor_pos % n_colunas)

        # ESQUERDA
        elif event.key == pg.K_a or event.key == pg.K_LEFT:
            if self.cursor_pos % n_colunas != 0:
                self.cursor_pos -= 1
            else:
                fim_teorico = self.cursor_pos + (n_colunas - 1)
                self.cursor_pos = min(fim_teorico, total - 1)
        
        # BAIXO
        elif event.key == pg.K_s or event.key == pg.K_DOWN:
            if self.cursor_pos + n_colunas < total:
                self.cursor_pos += n_colunas
            else:
                self.cursor_pos = self.cursor_pos % n_colunas

        # CIMA
        elif event.key == pg.K_w or event.key == pg.K_UP:
            if self.cursor_pos - n_colunas >= 0:
                self.cursor_pos -= n_colunas
            else:
                coluna_atual = self.cursor_pos % n_colunas
                linhas_totais = (total + n_colunas - 1) // n_colunas
                novo_index = coluna_atual + (linhas_totais - 1) * n_colunas
                if novo_index >= total: 
                    novo_index -= n_colunas
                self.cursor_pos = novo_index
        
        # --- CONFIRMAÇÃO (ENTER) ---
        elif event.key == pg.K_RETURN or event.key == pg.K_SPACE or event.key == pg.K_e:
            self.confirmar_selecao()
        
        # --- VOLTAR (ESC/BACKSPACE) ---
        elif event.key == pg.K_BACKSPACE or event.key == pg.K_ESCAPE:
            # Bloqueia ESC se a troca for obrigatória
            if self.troca_obrigatoria and self.estado_atual == "MENU_TROCA":
                return
            
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
                self.itens_mochila = ["Trocar Pokemon"]      
                for item in list(self.inventario.keys()):
                    if self.inventario[item] > 0:
                        self.itens_mochila.append(item)

                self.max_opcoes = len(self.itens_mochila)
                self.mensagem_sistema = "Mochila:"
                            
            elif self.cursor_pos == 2: # FUGIR
                    self.tentar_fugir()

        # --- MENU GOLPES ---
        elif self.estado_atual == "MENU_GOLPES":
            self.turno_lutar(self.cursor_pos)

        # --- MENU MOCHILA ---
        elif self.estado_atual == "MENU_MOCHILA":
            item_escolhido = self.itens_mochila[self.cursor_pos]

            if item_escolhido == "Trocar Pokemon":
                self.estado_atual = "MENU_TROCA"
                self.cursor_pos = 0
                self.max_opcoes = len(self.equipe)
                self.mensagem_sistema = "Escolha um Pokemon:"
            
            else:
                if "Poção" in item_escolhido or "Potion" in item_escolhido:
                    self.usar_pocao(item_escolhido) 
                
                elif "Bola" in item_escolhido or "bola" in item_escolhido:
                    self.tentar_capturar(item_escolhido) 
                
                else:
                    self.mensagem_sistema = "Não pode usar isso agora!"

        # --- MENU TROCA ---
        elif self.estado_atual == "MENU_TROCA":
            pkmn_escolhido = self.equipe[self.cursor_pos]
            
            if pkmn_escolhido == self.player_pkmn:
                self.mensagem_sistema = "Ele já está em batalha!"
            elif not pkmn_escolhido.esta_vivo():
                self.mensagem_sistema = "Ele está desmaiado!"
            else:
                # Desabilita flag de troca obrigatória após escolha
                self.troca_obrigatoria = False
                self.realizar_troca(pkmn_escolhido)

    def tentar_capturar(self, tipo_bola):
        # BLOQUEIO TREINADOR
        if self.tipo_batalha in ["TREINADOR", "TREINADOR_REVANCHE"]:
            self.mensagem_sistema = "Não pode roubar o pokemon de um treinador!"
            return

        if len(self.equipe) >= 6:
            self.mensagem_sistema = "Sua equipe está cheia!"
            return

        # Verifica quantidade
        qtd = self.inventario.get(tipo_bola, 0)
        if qtd <= 0:
            self.mensagem_sistema = f"Você não tem {tipo_bola}!"
            return

        # Consome item
        self.inventario[tipo_bola] -= 1

        lvl_raridade = {
            'comum': 1,
            'raro': 1.5,
            'super_raro': 2,
            'lendario': 5
        }

        raridade = lvl_raridade.get(POKEDEX[self.enemy_pkmn.nome]['raridade'], 1)
        hp_atual = self.enemy_pkmn.hp_atual
        hp_max = self.enemy_pkmn.hp_max

        if "Pokebola" in tipo_bola: ball_multiplier = 1
        elif "Grande" in tipo_bola: ball_multiplier = 1.5
        elif "Ultra" in tipo_bola:  ball_multiplier = 2
        else: ball_multiplier = 1.4

        fator_vida = 1.0 - (hp_atual / hp_max)
        chance_base = 30 + (fator_vida * 40)
        dificuldade_raridade = raridade * 5 
        chance_final = (chance_base * ball_multiplier) - dificuldade_raridade            
        chance_final = max(1, min(100, int(chance_final)))

        sorteio = random.randint(1, 100)

        if sorteio <= chance_final:
            self.captura_sucesso = True
        else:
            self.captura_sucesso = False
            exclamacao = random.choice(["Droga!","Poxa","Quase!","Caramba!","Puts!"])
            quebra = random.choice(["falhou","quebrou","torou","fracassou","pifou","espatifou"])
            self.msg_falha_captura = f"{exclamacao}! A {tipo_bola} {quebra}!"

        # animação bola
        self.bola_tipo_atual = tipo_bola
        key_img = tipo_bola
        if "Poke" in tipo_bola: key_img = "Pokebola"
        elif "Grande" in tipo_bola: key_img = "Grande Bola"
        elif "Ultra" in tipo_bola: key_img = "Ultra Ball"
            
        self.bola_img_atual = self.sprites_balls.get(key_img, self.sprites_balls.get('Pokebola'))
        
        self.mensagem_sistema = f"Jogou {tipo_bola}!"
        self.estado_atual = "ANIMACAO_BOLA_JOGADA" 
        self.bola_start_time = pg.time.get_ticks()
        self.bola_cor_filtro = None 

    def realizar_troca(self, novo_pkmn):
        self.player_pkmn = novo_pkmn
        self.visual_hp_player = float(self.player_pkmn.hp_atual)
        
        self.anim_x_player = -300 
        
        self.mensagem_sistema = f"Vai, {novo_pkmn.nome}!"
        self.msg_extra = ""
        
        self.estado_atual = "TROCA_ANIMACAO"
        self.timer_espera = pg.time.get_ticks()

    def usar_pocao(self, nome_item):
        qtd = self.inventario.get(nome_item, 0)
        
        if qtd > 0:
            self.inventario[nome_item] -= 1
            
            cura = 20
            if "Super" in nome_item: cura = 50
            if "Hyper" in nome_item: cura = 200
            
            self.player_pkmn.hp_atual = min(self.player_pkmn.hp_max, self.player_pkmn.hp_atual + cura)
            
            self.mensagem_sistema = f"Usou {nome_item}! +{cura} HP."
            self.msg_extra = "" 
            self.estado_atual = "ANIMANDO_PLAYER" 
            self.atacando = False 
            self.timer_espera = pg.time.get_ticks()
        else:
            self.mensagem_sistema = f"Sem {nome_item}!"

    def tentar_fugir(self):
        # BLOQUEIO TREINADOR
        if self.tipo_batalha in ["TREINADOR", "TREINADOR_REVANCHE"]:
            self.mensagem_sistema = "Não pode fugir de uma batalha contra treinadores!"
            self.msg_extra = ""
            return

        self.atacando = False
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
        
        porcentagem = dano / self.enemy_pkmn.hp_max
        altura_calculada = 10 + (porcentagem * 10)
        self.altura_pulo = min(20, altura_calculada)
        self.atacando = True

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

        porcentagem = dano / self.player_pkmn.hp_max
        altura_calculada = 10 + (porcentagem * 10)
        self.altura_pulo = min(20, altura_calculada)
        self.atacando = True

        self.mensagem_sistema = f"Inimigo usou {golpe.nome}!"
        self.msg_extra = msg_efeito
        self.estado_atual = "ANIMANDO_INIMIGO"
        self.timer_espera = pg.time.get_ticks()

    def trocar_pokemon_auto(self):
        # Verifica se tem pokémon vivo disponível
        tem_pokemon_vivo = any(pkmn.esta_vivo() for pkmn in self.equipe)
        
        if tem_pokemon_vivo:
            # Abre menu de troca obrigatório
            self.troca_obrigatoria = True
            self.estado_atual = "MENU_TROCA"
            self.cursor_pos = 0
            self.max_opcoes = len(self.equipe)
            self.mensagem_sistema = "Escolha um Pokemon para trocar:"
            return True
        return False
    
    def trocar_inimigo_auto(self):
        for pkmn in self.enemy_equipe:
            if pkmn.esta_vivo():
                self.enemy_pkmn = pkmn
                self.visual_hp_enemy = float(self.enemy_pkmn.hp_atual)
                
                # Reseta posição para animação de entrada do novo inimigo
                self.anim_x_enemy = 800 
                
                self.mensagem_sistema = f"Inimigo enviou {pkmn.nome}!"

                if self.enemy_pkmn.nome not in progresso_pokedex:
                    progresso_pokedex[self.enemy_pkmn.nome] = "visto"

                self.estado_atual = "TROCA_ANIMACAO_INIMIGO"
                self.timer_espera = pg.time.get_ticks()

                return True
        return False

    def get_cor_hp(self, atual, maximo):
        pct = atual / maximo
        if pct > 0.5: return (0, 200, 0)
        if pct > 0.2: return (255, 200, 0)
        return (200, 0, 0)

    def get_type_modifier(self, ataque_tipo, defensor_tipo_str):
        tabela = {
            "Normal":   {"Pedra": 0.5, "Fantasma": 0.0, "Aco": 0.5},
            "Fogo":     {"Grama": 2.0, "Gelo": 2.0, "Inseto": 2.0, "Aco": 2.0, "Fogo": 0.5, "Agua": 0.5, "Pedra": 0.5, "Dragao": 0.5},
            "Agua":     {"Fogo": 2.0, "Terra": 2.0, "Pedra": 2.0, "Agua": 0.5, "Grama": 0.5, "Dragao": 0.5},
            "Eletrico": {"Agua": 2.0, "Voador": 2.0, "Eletrico": 0.5, "Grama": 0.5, "Dragao": 0.5, "Terra": 0.0},
            "Grama":    {"Agua": 2.0, "Terra": 2.0, "Pedra": 2.0, "Fogo": 0.5, "Grama": 0.5, "Veneno": 0.5, "Voador": 0.5, "Inseto": 0.5, "Dragao": 0.5, "Aco": 0.5},
            "Gelo":     {"Grama": 2.0, "Terra": 2.0, "Voador": 2.0, "Dragao": 2.0, "Fogo": 0.5, "Agua": 0.5, "Gelo": 0.5, "Aco": 0.5},
            "Lutador":  {"Normal": 2.0, "Gelo": 2.0, "Pedra": 2.0, "Aco": 2.0, "Veneno": 0.5, "Voador": 0.5, "Psiquico": 0.5, "Inseto": 0.5, "Fada": 0.5, "Fantasma": 0.0},
            "Veneno":   {"Grama": 2.0, "Fada": 2.0, "Veneno": 0.5, "Terra": 0.5, "Pedra": 0.5, "Fantasma": 0.5, "Aco": 0.0},
            "Terra":    {"Fogo": 2.0, "Eletrico": 2.0, "Veneno": 2.0, "Pedra": 2.0, "Aco": 2.0, "Grama": 0.5, "Inseto": 0.5, "Voador": 0.0},
            "Voador":   {"Grama": 2.0, "Lutador": 2.0, "Inseto": 2.0, "Eletrico": 0.5, "Pedra": 0.5, "Aco": 0.5},
            "Psiquico": {"Lutador": 2.0, "Veneno": 2.0, "Psiquico": 0.5, "Aco": 0.5, "Sombrio": 0.0},
            "Inseto":   {"Grama": 2.0, "Psiquico": 2.0, "Sombrio": 2.0, "Fogo": 0.5, "Lutador": 0.5, "Veneno": 0.5, "Voador": 0.5, "Fantasma": 0.5, "Aco": 0.5, "Fada": 0.5},
            "Pedra":    {"Fogo": 2.0, "Gelo": 2.0, "Voador": 2.0, "Inseto": 2.0, "Lutador": 0.5, "Terra": 0.5, "Aco": 0.5},
            "Fantasma": {"Psiquico": 2.0, "Fantasma": 2.0, "Sombrio": 0.5, "Normal": 0.0},
            "Dragao":   {"Dragao": 2.0, "Aco": 0.5, "Fada": 0.0},
            "Aco":      {"Gelo": 2.0, "Pedra": 2.0, "Fada": 2.0, "Fogo": 0.5, "Agua": 0.5, "Eletrico": 0.5, "Aco": 0.5},
            "Fada":     {"Lutador": 2.0, "Dragao": 2.0, "Sombrio": 2.0, "Fogo": 0.5, "Veneno": 0.5, "Aco": 0.5}
        }
        
        tipos_defensor = defensor_tipo_str.split('/')
        multiplicador_final = 1.0
        modificadores_ataque = tabela.get(ataque_tipo, {})

        for tipo in tipos_defensor:
            tipo = tipo.strip()
            val = modificadores_ataque.get(tipo, 1.0)
            multiplicador_final *= val
            
        return multiplicador_final

    def calcular_dano(self, atq, defe, golpe):
        self.atacando = False
        chance = random.randint(1, 100)
        # Se errou pela precisão do golpe
        if chance > golpe.precisao: 
            return 0, "Errou!"
        
        mult = self.get_type_modifier(golpe.tipo, defe.tipo)
        
        # Fórmula de dano
        nivel_factor = (2 * atq.nivel / 5) + 2
        stats_ratio = atq.atk / max(1, defe.defense)
        dano_base = ((nivel_factor * golpe.poder * stats_ratio) / 50) + 2
        
        dano_final = int(dano_base * mult)
        
        msg = ""
        if mult == 0:
            dano_final = 0
            msg = f"Nao afetou {defe.nome}..."
        elif mult > 1: 
            msg = "Foi super efetivo!"
        elif mult < 1: 
            msg = "Nao foi muito efetivo..."
        
        if mult > 0:
            dano_final = max(1, dano_final)
            
        return dano_final, msg
    
    def get_bezier_pos(self, t, p0, p1, p2):
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        return (x, y)
    
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
        elif self.visual_hp_enemy < self.enemy_pkmn.hp_atual: # Caso de cura ou troca
             self.visual_hp_enemy = self.enemy_pkmn.hp_atual
        
        if self.visual_hp_player > self.player_pkmn.hp_atual:
            self.visual_hp_player -= velocidade_animacao
            if self.visual_hp_player < self.player_pkmn.hp_atual: self.visual_hp_player = self.player_pkmn.hp_atual
        elif self.visual_hp_player < self.player_pkmn.hp_atual:
            self.visual_hp_player += velocidade_animacao
            if self.visual_hp_player > self.player_pkmn.hp_atual: self.visual_hp_player = self.player_pkmn.hp_atual

        agora = pg.time.get_ticks()
        
        # --- LÓGICA DO PULO ---
        self.offset_y_player = 0
        self.offset_y_enemy = 0
        
        if self.atacando:
            tempo_decorrido = agora - self.timer_espera
            duracao_pulo = 300 
            altura_pulo = self.altura_pulo   
            
            if tempo_decorrido < duracao_pulo:
                fator = math.sin((tempo_decorrido / duracao_pulo) * math.pi)
                
                if self.estado_atual == "ANIMANDO_PLAYER":
                    self.offset_y_player = -altura_pulo * fator
                    
                elif self.estado_atual == "ANIMANDO_INIMIGO":
                    self.offset_y_enemy = -altura_pulo * fator

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
                
                if self.tipo_batalha == "TREINADOR":
                    self.mensagem_sistema = f"{self.nome_inimigo} desafiou você!"
                else:
                    self.mensagem_sistema = f"Um {self.enemy_pkmn.nome} selvagem apareceu!"
                self.timer_espera = agora

        elif self.estado_atual == "MENSAGEM_INICIAL":
            if agora - self.timer_espera > 2500:
                self.estado_atual = "MENU_PRINCIPAL"
                self.mensagem_sistema = "O que voce vai fazer?"

        # --- ESTADO DE ANIMAÇÃO DE TROCA DO JOGADOR ---
        elif self.estado_atual == "TROCA_ANIMACAO":
            if self.anim_x_player < self.target_x_player:
                self.anim_x_player += 15
                if self.anim_x_player > self.target_x_player:
                    self.anim_x_player = self.target_x_player
            
            if self.anim_x_player == self.target_x_player:
                if agora - self.timer_espera > 1000:
                    # Se a troca foi em resposta à derrota do inimigo, trocar o inimigo
                    if self.troca_apos_derrota_inimigo:
                        self.troca_apos_derrota_inimigo = False  # Reseta flag
                        self.trocar_inimigo_auto()
                    else:
                        # Troca normal durante o turno, inimigo contra-ataca
                        self.contra_ataque_inimigo()

        # --- ESTADO DE ESPERA DA CAPTURA (SUSPENSE) ---
        elif self.estado_atual == "AGUARDANDO_CAPTURA":
            if agora - self.timer_espera > 1500:
                if self.captura_sucesso:
                    self.battle_over = True
                    self.vencedor = "CAPTURA"
                    self.mensagem_sistema = f"Gotcha! {self.enemy_pkmn.nome} foi capturado!"
                    self.equipe.append(self.enemy_pkmn)
                    self.estado_atual = "FIM_BATALHA" 
                else:
                    self.mensagem_sistema = self.msg_falha_captura
                    self.estado_atual = "ANIMANDO_PLAYER"
                    self.msg_extra = "" 
                    self.timer_espera = agora

        elif self.estado_atual == "ANIMANDO_PLAYER":
            if self.animacao_concluida():
                if self.msg_extra != "":
                    if agora - self.timer_espera > 1000: 
                        self.mensagem_sistema = self.msg_extra 
                        
                        if "quebrou" in self.msg_extra or "falhou" in self.msg_extra or "escapou" in self.msg_extra: 
                            self.contra_ataque_inimigo() 
                        
                        self.msg_extra = "" 
                        self.timer_espera = agora 
                
                elif agora - self.timer_espera > 1500: # Delay para ler mensagens
                    if not self.enemy_pkmn.esta_vivo():
                        # Lógica de Vitória / XP / Próximo Pokemon
                        
                        # Se for TREINADOR e tiver mais pokemons vivos na equipe inimiga
                        if self.tipo_batalha in ["TREINADOR", "TREINADOR_REVANCHE"] and any(p.esta_vivo() for p in self.enemy_equipe):
                             xp_ganho = self.enemy_pkmn.nivel * 15
                             self.player_pkmn.ganhar_xp(xp_ganho)
                             self.mensagem_sistema = f"Inimigo derrotado! +{xp_ganho} XP."
                             # Inicia animação de saída do pokemon derrotado
                             self.anim_x_enemy = self.target_x_enemy
                             self.estado_atual = "ANIMACAO_MORTE_INIMIGO"
                             self.timer_espera = agora
                        else:
                            # Vitória Definitiva
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

        elif self.estado_atual == "ANIMACAO_MORTE_INIMIGO":
            # Anima o inimigo saindo para a direita (igual à animação de troca)
            if self.anim_x_enemy < 800:
                self.anim_x_enemy += 15
            else:
                # Terminou a animação, agora espera para trocar
                self.estado_atual = "ESPERANDO_TROCA_INIMIGO"
                self.timer_espera = agora
        
        elif self.estado_atual == "ESPERANDO_TROCA_INIMIGO":
             if agora - self.timer_espera > 1000:
                 # Verifica o próximo pokémon do inimigo
                 proximo_inimigo = None
                 for pkmn in self.enemy_equipe:
                     if pkmn.esta_vivo():
                         proximo_inimigo = pkmn
                         break
                 
                 if proximo_inimigo:
                     # Conta quantos pokémons vivos o jogador tem
                     pokemons_vivos_jogador = sum(1 for pkmn in self.equipe if pkmn.esta_vivo())
                     
                     # Só pergunta se quer trocar se tiver mais de 1 pokémon vivo
                     if pokemons_vivos_jogador > 1:
                         self.mensagem_sistema = f"Próximo pokemon inimigo: {proximo_inimigo.nome}. Deseja trocar de pokemon?"
                         self.confirmar_troca_inimigo = True
                         self.cursor_confirmacao = 0
                         self.estado_atual = "CONFIRMACAO_TROCA_INIMIGO"
                     else:
                         # Só tem 1 pokémon vivo, pula direto para trocar o inimigo
                         self.trocar_inimigo_auto()
                 else:
                     # Não há próximo pokémon (não deveria acontecer, mas por segurança)
                     self.trocar_inimigo_auto()
        
        elif self.estado_atual == "TROCA_ANIMACAO_INIMIGO":
            # Anima o inimigo entrando da direita
            if self.anim_x_enemy > self.target_x_enemy:
                self.anim_x_enemy -= 15
                if self.anim_x_enemy < self.target_x_enemy: 
                    self.anim_x_enemy = self.target_x_enemy
            
            if self.anim_x_enemy == self.target_x_enemy:
                 if agora - self.timer_espera > 1000:
                     self.estado_atual = "MENU_PRINCIPAL"
                     self.mensagem_sistema = "O que você vai fazer?"
                     self.cursor_pos = 0

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
                        # Se trocou, o estado já foi mudado para TROCA_ANIMACAO pela função
                    else:
                        self.estado_atual = "MENU_PRINCIPAL"
                        self.cursor_pos = 0
                        self.max_opcoes = 3 
                        self.mensagem_sistema = "O que voce vai fazer?"

        # --- DESENHO HUD ---
        mostrar_hud = self.estado_atual not in ["ENTRADA_ANIMACAO", "MENSAGEM_INICIAL"]

        if mostrar_hud:
            # HUD Inimigo
            # Expande HUD se for batalha de treinador (para comportar as pokebolas)
            hud_height = 105 if self.tipo_batalha in ["TREINADOR", "TREINADOR_REVANCHE"] else 80
            pg.draw.rect(screen, (220, 220, 220), (50, 50, 300, hud_height), border_radius=8)
            
            # Sprites de pokebola indicando quantos pokemons o inimigo tem (se for treinador)
            # Posicionadas no topo do HUD
            offset_y = 0  # Offset para descer nome e HP quando há pokebolas
            if self.tipo_batalha in ["TREINADOR", "TREINADOR_REVANCHE"] and 'Pokebola' in self.sprites_balls:
                ball_sprite = self.sprites_balls['Pokebola']
                ball_size = 20  # Tamanho das pokebolas
                ball_sprite_small = pg.transform.scale(ball_sprite, (ball_size, ball_size))
                
                for i, p in enumerate(self.enemy_equipe):
                    bx = 60 + (i * 25)
                    by = 58  # No topo do HUD, acima do nome
                    
                    # Se morto, aplica filtro cinza
                    if not p.esta_vivo():
                        ball_gray = ball_sprite_small.copy()
                        ball_gray.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                        screen.blit(ball_gray, (bx, by))
                    else:
                        screen.blit(ball_sprite_small, (bx, by))
                
                offset_y = 25  # Desloca nome e HP para baixo
            
            nome_inimigo = f"{self.enemy_pkmn.nome} Lv.{self.enemy_pkmn.nivel}"
            screen.blit(self.font_big.render(nome_inimigo, True, (0,0,0)), (60, 55 + offset_y))
            
            pg.draw.rect(screen, (100,100,100), (60, 95 + offset_y, 200, 15))
            pct_enemy = self.visual_hp_enemy / self.enemy_pkmn.hp_max
            cor_enemy = self.get_cor_hp(self.visual_hp_enemy, self.enemy_pkmn.hp_max)
            pg.draw.rect(screen, cor_enemy, (60, 95 + offset_y, int(200 * pct_enemy), 15))

            # HUD Player
            pg.draw.rect(screen, (220, 220, 220), (450, 320, 320, 100), border_radius=8)
            nome_player = f"{self.player_pkmn.nome} Lv.{self.player_pkmn.nivel}"
            screen.blit(self.font_big.render(nome_player, True, (0,0,0)), (460, 330))
            screen.blit(self.font.render(f"HP: {int(self.visual_hp_player)}/{self.player_pkmn.hp_max}", True, (0,0,0)), (460, 370))
            
            pg.draw.rect(screen, (100,100,100), (600, 375, 150, 15))
            pct_player = self.visual_hp_player / self.player_pkmn.hp_max
            cor_player = self.get_cor_hp(self.visual_hp_player, self.player_pkmn.hp_max)
            pg.draw.rect(screen, cor_player, (600, 375, int(150 * pct_player), 15))
            
            # Sprites de pokebola indicando a equipe do jogador (dentro do HUD)
            if 'Pokebola' in self.sprites_balls:
                ball_sprite = self.sprites_balls['Pokebola']
                ball_size = 20  # Tamanho das pokebolas
                ball_sprite_small = pg.transform.scale(ball_sprite, (ball_size, ball_size))
                
                max_slots = 6  # Máximo de 6 pokémons
                for i in range(max_slots):
                    bx = 460 + (i * 25)
                    by = 395  # Dentro do HUD do jogador, abaixo da barra de HP
                    
                    if i < len(self.equipe):
                        # Tem pokémon neste slot
                        p = self.equipe[i]
                        if not p.esta_vivo():
                            # Pokémon morto - pokebola cinza
                            ball_gray = ball_sprite_small.copy()
                            ball_gray.fill((100, 100, 100), special_flags=pg.BLEND_MULT)
                            screen.blit(ball_gray, (bx, by))
                        else:
                            # Pokémon vivo - pokebola normal
                            screen.blit(ball_sprite_small, (bx, by))
                    else:
                        # Slot vazio - apenas contorno
                        pg.draw.circle(screen, (150, 150, 150), (bx + ball_size//2, by + ball_size//2), ball_size//2, 2)

        # --- SPRITES ---
        # Condição para esconder o inimigo durante a captura
        estados_escondido = ["ANIMACAO_BOLA_CHECK", "ANIMACAO_BOLA_RESULTADO"]
        inimigo_visivel = True
        if self.estado_atual in estados_escondido:
            inimigo_visivel = False
            
        if self.estado_atual == "FIM_BATALHA" and self.vencedor == "CAPTURA":
            inimigo_visivel = False
            
        # Também esconde inimigo enquanto espera o próximo aparecer
        if self.estado_atual == "ESPERANDO_TROCA_INIMIGO":
            inimigo_visivel = False
        
        # Mostra inimigo durante animação de morte para ele sair da tela
        if self.estado_atual == "ANIMACAO_MORTE_INIMIGO":
            inimigo_visivel = True

        if inimigo_visivel:
            # Inimigo
            rect_visivel_inimigo = self.enemy_pkmn.image.get_bounding_rect()
            pos_y_real_inimigo = 310 - rect_visivel_inimigo.bottom
            pos_inimigo = (self.anim_x_enemy - 10, pos_y_real_inimigo + self.offset_y_enemy) 
            screen.blit(self.enemy_pkmn.image, pos_inimigo)

        # Player
        rect_visivel_player = self.player_pkmn.back_image.get_bounding_rect()
        pos_y_real = 430 - rect_visivel_player.bottom
        pos_player = (self.anim_x_player, pos_y_real + self.offset_y_player ) 
        screen.blit(self.player_pkmn.back_image, pos_player)

        # --- MENU INFERIOR ---
        pg.draw.rect(screen, (30, 30, 80), (0, 430, 800, 170))
        pg.draw.rect(screen, (255, 255, 255), (0, 430, 800, 170), 4)
        
        screen.blit(self.font_msg.render(self.mensagem_sistema, True, (255, 255, 0)), (30, 450))

        # Opções de confirmação de troca após derrotar inimigo
        if self.estado_atual == "CONFIRMACAO_TROCA_INIMIGO":
            cor_padrao = (200, 200, 200)
            cor_select = (255, 255, 255)
            y_base = 520
            opcoes = ["SIM", "NAO"]
            x_base = 200
            spacing = 250
            
            for i, op in enumerate(opcoes):
                cor = cor_select if i == self.cursor_confirmacao else cor_padrao
                prefixo = "> " if i == self.cursor_confirmacao else "   "
                screen.blit(self.font_big.render(prefixo + op, True, cor), (x_base + (i * spacing), y_base))
        
        # Opções
        elif mostrar_hud and not self.battle_over:
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
                    pos_y = y_base + (row * 30) - 25
                    
                    screen.blit(self.font_big.render(prefixo + golpe.nome, True, cor), (pos_x, pos_y))

            elif self.estado_atual == "MENU_MOCHILA":
                x_base_cols = 50
                col_spacing = 400
                
                for i, nome_item in enumerate(self.itens_mochila):
                    cor = cor_select if i == self.cursor_pos else cor_padrao
                    prefixo = "> " if i == self.cursor_pos else "   "
                    
                    texto_final = nome_item
                    
                    if i > 0: 
                        qtd = self.inventario.get(nome_item, 0)
                        texto_final = f"{nome_item} x{qtd}"

                    col = i % 2
                    row = i // 2
                    pos_x = x_base_cols + (col * col_spacing)
                    pos_y = y_base + (row * 30) - 25
                    
                    screen.blit(self.font_big.render(prefixo + texto_final, True, cor), (pos_x, pos_y))

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
                    
                    pos_y = 490 + (row * 30) 

                    screen.blit(self.font_big.render(texto_pkmn, True, cor), (pos_x, pos_y))

            elif self.estado_atual == "ANIMACAO_BOLA_JOGADA":
                tempo_total = 1000
                t = (agora - self.bola_start_time) / tempo_total
                
                rect_inimigo = self.enemy_pkmn.image.get_bounding_rect()
                alvo_x = (self.anim_x_enemy - 10) + rect_inimigo.centerx
                self.bola_pos_alvo = (alvo_x, 285)

                if t > 1.0: 
                    t = 1.0
                    self.estado_atual = "ANIMACAO_BOLA_CHECK"
                    self.bola_start_time = agora
                    self.mensagem_sistema = "..." 
                
                p0 = (self.anim_x_player + 50, 400)      
                p2 = self.bola_pos_alvo                   
                p1 = ((p0[0] + p2[0]) / 2, p2[1] - 250)  
                pos_atual = self.get_bezier_pos(t, p0, p1, p2)
                
                if self.bola_img_atual:
                    angulo = t * 1080 * -1
                    img_rot = pg.transform.rotate(self.bola_img_atual, angulo)
                    rect_rot = img_rot.get_rect(center=pos_atual)
                    screen.blit(img_rot, rect_rot)

            elif self.estado_atual == "ANIMACAO_BOLA_CHECK":
                pos_final = self.bola_pos_alvo
                
                shake_x = 0
                if (agora // 100) % 2 == 0: 
                    shake_x = random.choice([-2, 2, 0])
                    
                pos_com_shake = (pos_final[0] + shake_x, pos_final[1])
                
                if self.bola_img_atual:
                    rect_final = self.bola_img_atual.get_rect(center=pos_com_shake)
                    screen.blit(self.bola_img_atual, rect_final)
                
                if agora - self.bola_start_time > 1500:
                    self.estado_atual = "ANIMACAO_BOLA_RESULTADO"
                    self.bola_start_time = agora
                    
                    if self.captura_sucesso:
                        self.bola_cor_filtro = (255, 255, 0) 
                        self.mensagem_sistema = f"Gotcha! {self.enemy_pkmn.nome} foi capturado!"
                        progresso_pokedex[self.enemy_pkmn.nome] = "capturado"
                    else:
                        self.bola_cor_filtro = (50, 50, 50) 
                        self.mensagem_sistema = "Ah não! Escapou!"

            elif self.estado_atual == "ANIMACAO_BOLA_RESULTADO":
                pos_final = self.bola_pos_alvo
                
                if self.bola_img_atual:
                    img_final = self.bola_img_atual.copy()
                    if self.bola_cor_filtro:
                        filtro = pg.Surface(img_final.get_size()).convert_alpha()
                        filtro.fill(self.bola_cor_filtro)
                        img_final.blit(filtro, (0,0), special_flags=pg.BLEND_MULT)

                    rect_final = img_final.get_rect(center=pos_final)
                    screen.blit(img_final, rect_final)
                
                if agora - self.bola_start_time > 1000:
                    if self.captura_sucesso:
                        self.equipe.append(self.enemy_pkmn)
                        self.battle_over = True
                        self.vencedor = "CAPTURA"
                        self.estado_atual = "FIM_BATALHA"
                    else:
                        self.estado_atual = "ANIMANDO_PLAYER"
                        self.timer_espera = agora
                        self.msg_extra = self.msg_falha_captura

        elif self.battle_over and self.estado_atual != "LEVEL_UP":
             screen.blit(self.font_msg.render("Pressione ESPACO para sair", True, (255, 255, 255)), (30, 540))
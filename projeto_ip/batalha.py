import pygame as pg
import random

# --- Classe para os Ataques ---
class Golpe:
    def __init__(self, nome, poder, tipo, precisao=100):
        self.nome = nome
        self.poder = poder
        self.tipo = tipo
        self.precisao = precisao

# --- Classe para os Pokémons ---
class Pokemon:
    def __init__(self, nome, nivel, tipo, hp, atk, defensa, speed, golpes):
        self.nome = nome
        self.nivel = nivel
        self.tipo = tipo
        self.hp_max = hp
        self.hp_atual = hp
        self.atk = atk
        self.defense = defensa
        self.speed = speed
        self.golpes = golpes  # Lista de objetos Golpe
        
    def esta_vivo(self):
        return self.hp_atual > 0

    def receber_dano(self, dano):
        self.hp_atual -= dano
        if self.hp_atual < 0: 
            self.hp_atual = 0

# --- Classe Principal que Controla a Lógica da Batalha ---
class BatalhaPokemon:
    def __init__(self, player_pkmn, enemy_pkmn, inventario):
        self.player_pkmn = player_pkmn
        self.enemy_pkmn = enemy_pkmn
        self.inventario = inventario
        self.turno = 1
        self.battle_over = False
        self.vencedor = None
        # Fonte simples para desenhar texto
        self.font = pg.font.SysFont("Arial", 20)

    # --- LÓGICA DE DANO ---
    def get_type_modifier(self, ataque_tipo, defensor_tipo):
        tabela = {
            "Fogo": {"Grama": 2.0, "Agua": 0.5, "Fogo": 0.5},
            "Agua": {"Fogo": 2.0, "Grama": 0.5, "Agua": 0.5},
            "Grama": {"Agua": 2.0, "Fogo": 0.5, "Grama": 0.5},
            "Normal": {} 
        }
        return tabela.get(ataque_tipo, {}).get(defensor_tipo, 1.0)

    def calcular_dano(self, atacante, defensor, golpe):
        # 1. Checa Precisão
        chance = random.randint(1, 100)
        if chance > golpe.precisao:
            return 0, "Errou!"

        # 2. Fórmula de Dano
        nivel_fator = (2 * atacante.nivel / 5) + 2
        ratio_atk_def = atacante.atk / defensor.defense
        base_dano = (nivel_fator * golpe.poder * ratio_atk_def / 50) + 2

        # 3. Modificadores
        stab = 1.5 if atacante.tipo == golpe.tipo else 1.0
        tipo_mult = self.get_type_modifier(golpe.tipo, defensor.tipo)
        random_mult = random.uniform(0.85, 1.0)

        dano_final = int(base_dano * stab * tipo_mult * random_mult)
        
        msg_extra = ""
        if tipo_mult > 1: msg_extra = "Super Efetivo!"
        elif tipo_mult < 1: msg_extra = "Não muito efetivo..."

        return max(1, dano_final), msg_extra

    # --- AÇÕES DO TURNO ---
    def turno_lutar(self, indice_golpe_player):
        if self.battle_over: return

        golpe_player = self.player_pkmn.golpes[indice_golpe_player]
        golpe_enemy = random.choice(self.enemy_pkmn.golpes)

        # Quem é mais rápido?
        player_first = self.player_pkmn.speed >= self.enemy_pkmn.speed

        primeiro = (self.player_pkmn, self.enemy_pkmn, golpe_player) if player_first else (self.enemy_pkmn, self.player_pkmn, golpe_enemy)
        segundo = (self.enemy_pkmn, self.player_pkmn, golpe_enemy) if player_first else (self.player_pkmn, self.enemy_pkmn, golpe_player)

        # Primeiro ataque
        self._executar_ataque(primeiro[0], primeiro[1], primeiro[2])
        
        # Segundo ataque (se ninguém desmaiou)
        if not self.battle_over:
            self._executar_ataque(segundo[0], segundo[1], segundo[2])

    def _executar_ataque(self, atacante, defensor, golpe):
        dano, msg = self.calcular_dano(atacante, defensor, golpe)
        
        if msg == "Errou!":
            print(f"{atacante.nome} errou o ataque!")
        else:
            defensor.receber_dano(dano)
            print(f"{atacante.nome} usou {golpe.nome}! Dano: {dano}. {msg}")

        if not defensor.esta_vivo():
            self.battle_over = True
            if defensor == self.player_pkmn:
                print("Você perdeu!")
            else:
                print("Você venceu!")

    def turno_usar_item(self, nome_item):
        if self.battle_over: return

        if nome_item not in self.inventario or self.inventario[nome_item] <= 0:
            print("Item indisponível!")
            return

        self.inventario[nome_item] -= 1
        print(f"Você usou {nome_item}!")

        if nome_item == "Poção" or nome_item == "Health Potion":
            cura = 20
            self.player_pkmn.hp_atual = min(self.player_pkmn.hp_max, self.player_pkmn.hp_atual + cura)
        
        elif nome_item == "Pokebola" or nome_item == "GreatBall":
            if random.choice([True, False]):
                print("Capturado!")
                self.battle_over = True
                return
            else:
                print("Escapou!")

        if not self.battle_over:
            golpe_enemy = random.choice(self.enemy_pkmn.golpes)
            self._executar_ataque(self.enemy_pkmn, self.player_pkmn, golpe_enemy)

    def turno_fugir(self):
        if self.battle_over: return False

        if self.player_pkmn.speed > self.enemy_pkmn.speed or random.choice([True, False]):
            print("Fugiu com sucesso!")
            self.battle_over = True
            return True
        else:
            print("Falha ao fugir!")
            golpe_enemy = random.choice(self.enemy_pkmn.golpes)
            self._executar_ataque(self.enemy_pkmn, self.player_pkmn, golpe_enemy)
            return False

    def desenhar(self, screen):
        screen.fill((30, 30, 30)) # Fundo Cinza Escuro

        # Info Inimigo
        pg.draw.rect(screen, (200, 200, 200), (50, 50, 250, 80))
        nome_ini = self.font.render(f"Inimigo: {self.enemy_pkmn.nome}", True, (0,0,0))
        hp_ini = self.font.render(f"HP: {self.enemy_pkmn.hp_atual}/{self.enemy_pkmn.hp_max}", True, (0,0,0))
        screen.blit(nome_ini, (60, 60))
        screen.blit(hp_ini, (60, 90))

        # Info Player
        pg.draw.rect(screen, (200, 200, 200), (450, 350, 250, 80))
        nome_ply = self.font.render(f"Você: {self.player_pkmn.nome}", True, (0,0,0))
        hp_ply = self.font.render(f"HP: {self.player_pkmn.hp_atual}/{self.player_pkmn.hp_max}", True, (0,0,0))
        screen.blit(nome_ply, (460, 360))
        screen.blit(hp_ply, (460, 390))

        # Menu de Opções
        pg.draw.rect(screen, (50, 50, 150), (0, 500, 800, 100))
        texto_instrucoes = self.font.render("1: Atacar | 2: Poção | 3: Fugir", True, (255, 255, 255))
        screen.blit(texto_instrucoes, (50, 530))
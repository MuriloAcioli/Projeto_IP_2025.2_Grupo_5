#bibliotecas do projeto
import pygame as pg
import random
import os

#modulos do jogo
from player import Player
from camera import Camera
from coletaveis import Pokebola, GreatBall, Pocao, Ultraball
from inventario import MenuInventario
from obstaculo import Obstaculo
from mato import Mato
from pokemon import Pokemon, criar_pokemon 
from batalha import BatalhaPokemon
from npc import NPC
from pokedex import POKEDEX,progresso_pokedex
from pokehealer import PokeHealer
from vitoria import exibir_vitoria
# from save import salvar_jogo_sistema, carregar_jogo_sistema, ler_info_save
from intro import definir_piso, exibir_intro, cena_professor, animacao_transicao, animacao_treinador
from game_over import exibir_game_over


#CONFIGURAÇÕES GERAIS

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 48 
FPS = 60
primeiro_encontro = True

som_ativo = True
volume_padrao = 0.5 
VOLUME_PADRAO = 0.5 

lista_pokemons_disponiveis = list(POKEDEX.keys())
lista_pokemons_comuns = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "comum"]
lista_pokemons_raros = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "raro"]
lista_pokemons_super_raros = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "super_raro"]
lista_pokemons_lendarios = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "lendario"]
lista_pokemons_iniciais = [nome for nome, dados in POKEDEX.items() if dados.get("raridade") == "inicial"]


#DADOS DO MAPA
MAPA_MATRIZ = [
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'B', 'T', 'G', 'M', 'M', '.', '.', '.', 'N', '.', '.', 'S', '.', 'T'],
    ['T', '.', 'P', '.', '.', '.', '.', '.', '.', 'B', '.', '.', 'T', '.', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'M', 'M', 'M', 'T', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'M', 'M', 'M', 'T', 'G', 'H', 'M', 'M', 'M', 'T', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'U', 'G', 'M', 'M', '.', '.', 'M', 'M', 'M', 'M', 'M', 'T', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', ',', 'T'],
    ['T', '.', 'M', 'M', 'M', '.', '.', '.', 'M', 'M', 'M', 'M', 'T', 'M', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'M', 'M', 'M', 'M', '.', '.', '.', 'M', 'M', 'M', 'G', 'T', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'M', 'M', 'M', 'M', '.', '.', '.', '.', 'M', 'T', 'T', 'T', '.', '.', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'H', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', 'T'],
    ['T', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', 'M', 'M', 'T', 'H', 'B', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '.', '.', 'T'],
    ['T', 'U', 'M', 'M', 'M', '.', '.', '.', '.', '.', 'M', 'M', 'T', 'T', '.', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '.', '.', 'T'],
    ['T', '.', 'M', 'T', '.', '.', '.', '.', '.', '.', 'T', 'B', 'G', 'T', 'M', 'M', 'T', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', 'H', '.', '.', '.', '.', '.', '.', '.', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'R', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', 'B', '.', '.', '.', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'B', '.', 'T'],
    ['T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'T'],
    ['T', 'H', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', '.', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', '.', '.', '.', 'T'],
    ['T', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'H', '.', 'M', 'M', 'M', 'M', 'M', 'T', 'M', '.', '.', 'T'],
    ['T', 'U', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'U', '.', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '.', '.', 'T'],
    ['T', '.', 'M', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'U', '.', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '.', '.', 'T'],
    ['T', '.', 'G', 'M', 'M', '.', '.', '.', '.', '.', '.', '.', 'T', 'H', '.', 'M', 'M', 'M', 'M', 'M', 'M', 'T', '.', '.', 'T'],
    ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],
]


#FUNÇÕES AUXILIARES
#lista para guardar posições [x, y] dos itens que já foram pegos
itens_coletados_ids = []

def carregar_mapa(mapa, grupo_obs, grupo_col, grupo_mato, grupo_npcs):
    #le a matriz do mapa e instancia os objetos nas posições corretas
    pos_player = (100, 100)
    path_professor = os.path.join(DIRETORIO_BASE, "assets/professor/professor_massa.png") 
    
    for row_index, row in enumerate(mapa):
        for col_index, letra in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            if letra == 'T':
                grupo_obs.add(Obstaculo(x, y))
            elif letra == 'B':
                grupo_col.add(Pokebola(x+15, y+15))
            elif letra == 'S': 
                healer = PokeHealer(x, y) 
                grupo_obs.add(healer)
                 
            elif letra == 'G':
                grupo_col.add(GreatBall(x+15, y+15))
            elif letra == 'H':
                grupo_col.add(Pocao(x+15, y+15))
            elif letra == 'M':
                grupo_mato.add(Mato(x, y)) 
            elif letra == 'P':
                pos_player = (x, y)  
            elif letra == 'N':
                try:
                    npc = NPC(x, y, path_professor, "Está pronto para derrotar a Equipe Manga Rosa?", tipo_npc="professor")
                    grupo_npcs.add(npc)
                    grupo_obs.add(npc) 
                except Exception as e:
                    print(f"Erro ao criar NPC: {e}")
            elif letra == 'R':
                try:
                    path_rival = os.path.join(DIRETORIO_BASE, "assets/professor/rival.png") 
                    npc = NPC(x, y, path_rival, "Você tem o que é preciso para me desafiar?", tipo_npc="rival")
                    grupo_npcs.add(npc)
                    grupo_obs.add(npc) 
                except Exception as e:
                    print(f"Erro ao criar NPC Rival: {e}")
            elif letra == 'U':
                grupo_col.add(Ultraball(x+15,y+15))
                
    largura_total = len(mapa[0]) * TILE_SIZE
    altura_total = len(mapa) * TILE_SIZE
    
    return largura_total, altura_total, pos_player


#SETUP INICIAL DO JOGO

pg.init()
pg.mixer.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("PokéCIn: A Ameaça do Mangue")

path_icon = os.path.join(DIRETORIO_BASE, "assets/icon/icon.png") 
imagem_icone = pg.image.load(path_icon) 

pg.display.set_icon(imagem_icone)
clock = pg.time.Clock()

#grupos de Sprites
grupo_obstaculos = pg.sprite.Group()
grupo_coletaveis = pg.sprite.Group()
grupo_mato = pg.sprite.Group()
grupo_npcs = pg.sprite.Group()

#carregamento do Mundo
map_w, map_h, player_pos = carregar_mapa(MAPA_MATRIZ, grupo_obstaculos, grupo_coletaveis, grupo_mato, grupo_npcs)

#inicialização do Player
try:
    path_down = os.path.join(DIRETORIO_BASE, "assets/mc/mc_down.png")
    path_left = os.path.join(DIRETORIO_BASE, "assets/mc/mc_left.png")
    path_up = os.path.join(DIRETORIO_BASE, "assets/mc/mc_up.png")
    path_right = os.path.join(DIRETORIO_BASE, "assets/mc/mc_right.png")
    
    protagonista = Player(player_pos[0], player_pos[1], path_down, path_left, path_up, path_right)
    player_group = pg.sprite.GroupSingle(protagonista)
except FileNotFoundError: 
    print("ERRO CRÍTICO: Imagens do player não encontradas.")
    exit()

#inicialização de Sistemas
menu_inv = MenuInventario()
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, map_w, map_h)

#gera o visual do chão
caminho_tileset = os.path.join(DIRETORIO_BASE, "assets/backgrounds/tileset.png")
fundo_grama = definir_piso(map_w, map_h, caminho_tileset)
esperando_confirmacao_load = False


#FLUXO DE INTRODUÇÃO

jogo_ativo = exibir_intro(screen, clock) 
nome_jogador = "Player"
inicial_escolhido = "Charmander" 

if jogo_ativo:
    jogo_ativo, nome_input, pokemon_input = cena_professor(screen, clock)
    
    if nome_input:
        nome_jogador = nome_input
    if pokemon_input:
        inicial_escolhido = pokemon_input
        
    print(f"Bem-vindo ao mangue, {nome_jogador}!")
    print(f"Seu inicial é: {inicial_escolhido}")
    lista_iniciais_fora_escolha = lista_pokemons_iniciais.copy()
    lista_iniciais_fora_escolha.remove(inicial_escolhido)
    
    if jogo_ativo:
        try: 
            pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3"))
            pg.mixer.music.set_volume(volume_padrao/5*2)
            pg.mixer.music.play(-1, fade_ms=2000)
        except: pass

#CRIAÇÃO DA EQUIPE COM O INICIAL ESCOLHIDO
equipe_jogador = []
pokemon_inicial = criar_pokemon(inicial_escolhido, 5) #cria Nível 5
progresso_pokedex[inicial_escolhido] = "capturado"
if pokemon_inicial:
    equipe_jogador.append(pokemon_inicial)
else:
    #fallback de segurança
    equipe_jogador.append(criar_pokemon("Charmander", 5))


#LOOP PRINCIPAL (GAME LOOP)


estado_jogo = "MUNDO"
sistema_batalha = None
modo_tela_cheia = False #controle da tela cheia
running = jogo_ativo 
path_sound = os.path.join(DIRETORIO_BASE, "assets/sfx/itemfound.wav")
rect_botao_som = pg.Rect(10,10,40,40)

mensagem_tela = None

while running:
    

    #ESTADO: MUNDO (Exploração)

    if estado_jogo == "MUNDO":
        
        #LOGICA DE UPDATE 
        
        #verifica se algum NPC está falando
        npc_falando_agora = None
        for npc in grupo_npcs:
            if npc.falando:
                npc_falando_agora = npc
                break
        
        #eventos
        for event in pg.event.get():

            if menu_inv.aberto:
                menu_inv.processar_input(event, protagonista.inventario, equipe_jogador,POKEDEX)

            if event.type == pg.QUIT: 
                running = False
            
            if event.type == pg.KEYDOWN:
                
                #SISTEMA DE TELA CHEIA (F11)
                if event.key == pg.K_F11:
                    modo_tela_cheia = not modo_tela_cheia 
                    if modo_tela_cheia:
                        screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
                    else:
                        screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

                #CONTROLES DE DIÁLOGO
                if npc_falando_agora:
                    #tecla f: Fecha o diálogo (se já tiver terminado)
                    if event.key == pg.K_f:
                        npc_falando_agora.interagir()
                    
                    #setas/A/D: Mudam a opção (Sim/Não)
                    elif event.key == pg.K_LEFT or event.key == pg.K_a:
                        npc_falando_agora.mudar_selecao(-1)
                    elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                        npc_falando_agora.mudar_selecao(1)
                    
                    #space: Confirma a escolha ou avança texto
                    elif event.key == pg.K_SPACE:
                        #se ainda não respondeu, processa a resposta
                        if not npc_falando_agora.respondeu:
                            npc_falando_agora.respondeu = True
                            if npc_falando_agora.indice_selecionado == 0: # Sim
                                
                                #VERIFICA TIPO DE NPC
                                if npc_falando_agora.tipo_npc == "rival":
                                    #RIVAL: Só pode batalhar se tiver insígnia
                                    tem_insignia = "Insígnia do Professor" in protagonista.inventario
                                    
                                    if not tem_insignia:
                                        npc_falando_agora.texto_atual = "Você ainda não provou seu valor.\nDerrote o Professor primeiro!"
                                        #nao fecha o diálogo, só muda o texto
                                    else:
                                        #pode batalhar
                                        npc_falando_agora.texto_atual = "Então vamos ver sua força!"
                                        npc_falando_agora.interagir() # Fecha diálogo
                                        
                                        #cria time do Rival (igual ao professor por enquanto)
                                        time_rival = []

                                        time_rival.append(criar_pokemon("Eevee*", 8))
                                        time_rival.append(criar_pokemon("Bellsprout", 8))
                                        time_rival.append(criar_pokemon("Clefairy", 10))
                                        time_rival.append(criar_pokemon("Porygon*", 10))
                                        time_rival.append(criar_pokemon("Articuno*", 12))
                                        time_rival.append(criar_pokemon("Moltres", 15))
                                        
                                        #filtra Nones caso erre o nome
                                        time_rival = [p for p in time_rival if p is not None] 
                                        
                                        inv_batalha = protagonista.inventario
                                        animacao_treinador(screen)
                                        estado_jogo = "BATALHA"
                                        
                                        #rival dá game over se perder
                                        sistema_batalha = BatalhaPokemon(
                                            equipe_jogador, 
                                            time_rival, 
                                            inv_batalha, 
                                            tipo_batalha="TREINADOR",
                                            inimigo_nome="Líder da Equipe Mangue Rosa",
                                        )
                                
                                elif npc_falando_agora.tipo_npc == "professor":
                                    #PROFESSOR: Lógica original
                                    tem_insignia = "Insígnia do Professor" in protagonista.inventario
                                    
                                    if tem_insignia:
                                        npc_falando_agora.texto_atual = "Uma revanche? Vamos lá!"
                                    else:
                                        npc_falando_agora.texto_atual = "Prepare-se! Não terei piedade."
                                    
                                    npc_falando_agora.interagir() #fecha diálogo para transição
                                    
                                    #cria o time do Professor
                                    time_professor = []

                                    time_professor.append(criar_pokemon(lista_iniciais_fora_escolha[0], 8))
                                    time_professor.append(criar_pokemon(lista_iniciais_fora_escolha[1], 8))
                                    time_professor.append(criar_pokemon("Abra", 7))
                                    time_professor.append(criar_pokemon("Pikachu", 8))
                                    time_professor.append(criar_pokemon("Lapras", 8))
                                    time_professor.append(criar_pokemon("Mewtwo", 9))
                                    
                                    #filtra Nones caso erre o nome
                                    time_professor = [p for p in time_professor if p is not None]

                                    inv_batalha = protagonista.inventario
                                    
                                    animacao_treinador(screen)
                                    estado_jogo = "BATALHA"
                                    
                                    #instancia com o modo TREINADOR ou TREINADOR_REVANCHE
                                    tipo_batalha = "TREINADOR_REVANCHE" if tem_insignia else "TREINADOR"
                                    sistema_batalha = BatalhaPokemon(
                                        equipe_jogador, 
                                        time_professor, 
                                        inv_batalha, 
                                        tipo_batalha=tipo_batalha,
                                        inimigo_nome="Professor Python"
                                    )

                            else: #nao
                                if npc_falando_agora.tipo_npc == "rival":
                                    npc_falando_agora.texto_atual = "Treine mais e volte quando estiver pronto."
                                else:
                                    npc_falando_agora.texto_atual = "Volte quando estiver pronto."
                        #se já respondeu, fecha
                        else:
                            npc_falando_agora.interagir()

                #CONTROLES DE MUNDO
                else:
                    #tecla E: Inventário
                    if event.key == pg.K_e:
                        menu_inv.alternar() 

                    #tecla Space: Coletar itens próximos e interagir
                    if event.key == pg.K_SPACE:
                        #Se tiver mensagem, limpa a mensagem
                        if mensagem_tela:
                            mensagem_tela = ""
                            
                        #se não for nada disso, é uma interação normal do jogo
                        else:
                            #tenta interagir com PokeHealer
                            area_interacao = protagonista.rect.inflate(10, 10)
                            healer_interagido = False
                            
                            for obs in grupo_obstaculos:
                                if isinstance(obs, PokeHealer) and area_interacao.colliderect(obs.rect):
                                    feedback = obs.curar_equipe(equipe_jogador,volume_padrao) 
                                    mensagem_tela = feedback
                                    healer_interagido = True
                                    break

                            #se não foi PokeHealer, tenta pegar item
                            if not healer_interagido:
                                item_pegado = False
                            
                                for item in grupo_coletaveis:
                                    if area_interacao.colliderect(item.rect):
                                        nome_item = item.nome_item 
                                        item.coletar(protagonista)
                                        itens_coletados_ids.append([item.rect.x, item.rect.y])
                                        mensagem_tela = f"Você pegou: {nome_item}"
                                        item_pegado = True

                                        try: 
                                            sfx_item = pg.mixer.Sound(os.path.join(DIRETORIO_BASE, "assets/sfx/itemfound.wav"))
                                            sfx_item.set_volume(volume_padrao)
                                            sfx_item.play()
                                        except: pass
                                        break
                                
                                #se não foi item nem PokeHealer, tenta NPC
                                if not item_pegado:
                                    hits_npc = pg.sprite.spritecollide(protagonista, grupo_npcs, False)
                                    if not hits_npc:
                                        area_busca = protagonista.rect.inflate(20, 20) 
                                        for npc in grupo_npcs:
                                            if area_busca.colliderect(npc.rect):
                                                npc.interagir()
                                                break
                                    else:
                                        hits_npc[0].interagir()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  #clique esquerdo
                    if rect_botao_som.collidepoint(event.pos):
                        som_ativo = not som_ativo  
                        
                        if som_ativo:
                            volume_padrao = VOLUME_PADRAO
                            pg.mixer.music.set_volume(volume_padrao/5*2)
                        else:
                            volume_padrao = 0
                            pg.mixer.music.set_volume(volume_padrao)

        #atualização do Mundo 
        if not npc_falando_agora and not menu_inv.aberto and not mensagem_tela:
            antigo_rect = protagonista.rect.copy()
            player_group.update()

            for obs in grupo_obstaculos:
                if isinstance(obs, PokeHealer) and obs.foi_curado: 
                    area_proximidade = obs.rect.inflate(TILE_SIZE * 1.5, TILE_SIZE * 1.5)
                    if not area_proximidade.colliderect(protagonista.rect):
                        obs.resetar_cura()
            
            #logica do Mato
            if protagonista.direction.magnitude() > 0:
                if pg.sprite.spritecollide(protagonista, grupo_mato, False):
                    if random.random() < 0.01: #chance de encontro
                        animacao_transicao(screen)
                        estado_jogo = "BATALHA"
 
                        #GERA O POKEMON NO MATO
                        raridade = random.randint(0, 100)
                        if raridade < 55:
                            pokemon_random = random.choice(lista_pokemons_comuns)
                            lvl_chao = 3; lvl_teto = 5
                        elif raridade < 85:
                            pokemon_random = random.choice(lista_pokemons_raros)
                            lvl_chao = 5; lvl_teto = 8
                        elif raridade < 98:
                            pokemon_random = random.choice(lista_pokemons_super_raros)
                            lvl_chao = 6; lvl_teto = 10
                        else:
                            lvl_chao = 50; lvl_teto = 50
                            pokemon_random = random.choice(lista_pokemons_lendarios)
                        
                        if primeiro_encontro:
                            shiny = random.randint(1,100) 
                            if shiny == 100:
                                nome_byte = "Byte*"
                            else:
                                nome_byte = "Byte"
                            inimigo_pokemon = criar_pokemon(nome_byte, random.randint(3,5))
                            primeiro_encontro = False
                        else:
                            shiny = random.randint(1,100) 
                            if shiny == 100:
                                pokemon_random += "*"
                            inimigo_pokemon = criar_pokemon(pokemon_random, random.randint(lvl_chao, lvl_teto))
                        
                        inv_batalha = protagonista.inventario if protagonista.inventario else {'Poção': 1, 'Pokebola': 1}

                        try:
                            #batalha selvagem padrão
                            sistema_batalha = BatalhaPokemon(equipe_jogador, inimigo_pokemon, inv_batalha, tipo_batalha="SELVAGEM", inimigo_nome=None)
                        except Exception as e:
                            print(f"ERRO AO INICIAR BATALHA: {e}")
                            estado_jogo = "MUNDO"

            #colisoes
            colisao_obs = pg.sprite.spritecollide(protagonista,grupo_obstaculos,False,collided=lambda spr1, spr2: spr1.hitbox.colliderect(spr2.hitbox)) 
            
            colisao_item = pg.sprite.spritecollide(protagonista, grupo_coletaveis, False, collided=lambda spr1, spr2: spr1.hitbox.colliderect(spr2.hitbox))
            if colisao_obs or colisao_item:
                protagonista.rect = antigo_rect

            #camera
            camera.update(protagonista.rect)


        #logica de desenho 
        screen.fill((0,0,0)) 
        screen.blit(fundo_grama, camera.apply_rect(fundo_grama.get_rect()))

        for item in grupo_mato: 
            screen.blit(item.image, camera.apply(item.rect))
        for parede in grupo_obstaculos: 
            screen.blit(parede.image, camera.apply(parede.rect))
        for item in grupo_coletaveis: 
            screen.blit(item.image, camera.apply(item.rect))

        for npc in grupo_npcs:
            screen.blit(npc.image, camera.apply(npc.rect))
        
        for sprite in player_group: 
            screen.blit(sprite.image, camera.apply(sprite.rect))

        menu_inv.desenhar(screen, protagonista.inventario, equipe_jogador,POKEDEX,progresso_pokedex)

        if menu_inv.aberto:
            pg.draw.rect(screen, (100,100,100), rect_botao_som, border_radius=5)
            pg.draw.rect(screen, (0,0,0), rect_botao_som, 2, border_radius=5)
            bx, by = rect_botao_som.x, rect_botao_som.y
            pontos_speaker = [(bx+10, by+15), (bx+10, by+25), (bx+20, by+25), (bx+30, by+35), (bx+30, by+5), (bx+20, by+15)]
            pg.draw.polygon(screen, (0,0,0), pontos_speaker)

            if not som_ativo:
                pg.draw.line(screen, (255,0,0), (bx+10, by+10), (bx+30, by+30), 4)
                pg.draw.line(screen, (255,0,0), (bx+30, by+10), (bx+10, by+30), 4)

        if npc_falando_agora:
            rect_fundo = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
            rect_interno = rect_fundo.inflate(-10, -10)
            
            pg.draw.rect(screen, (40, 40, 160), rect_fundo, border_radius=10) 
            pg.draw.rect(screen, (255, 255, 255), rect_interno, border_radius=10) 

            fonte = pg.font.SysFont("Arial", 22)
            linhas = npc_falando_agora.texto_atual.split('\n')
            y_texto = rect_interno.y + 20
            for linha in linhas:
                texto_surf = fonte.render(linha, True, (0, 0, 0))
                screen.blit(texto_surf, (rect_interno.x + 20, y_texto))
                y_texto += 30

            if running:
                pontos_seta = [
                    (rect_interno.right - 30, rect_interno.bottom - 20),
                    (rect_interno.right - 10, rect_interno.bottom - 20),
                    (rect_interno.right - 20, rect_interno.bottom - 10)
                ]
                pg.draw.polygon(screen, (200, 0, 0), pontos_seta)

            if not npc_falando_agora.respondeu:
                fonte_opcoes = pg.font.SysFont("Arial", 22, bold=True)
                cor_sim = (200, 0, 0) if npc_falando_agora.indice_selecionado == 0 else (0, 0, 0)
                cor_nao = (200, 0, 0) if npc_falando_agora.indice_selecionado == 1 else (0, 0, 0)
                sim_surf = fonte_opcoes.render("> Sim" if npc_falando_agora.indice_selecionado == 0 else "  Sim", True, cor_sim)
                nao_surf = fonte_opcoes.render("> Não" if npc_falando_agora.indice_selecionado == 1 else "  Não", True, cor_nao)

                screen.blit(sim_surf, (rect_interno.x + 50, rect_interno.y + 80))
                screen.blit(nao_surf, (rect_interno.x + 200, rect_interno.y + 80))


    #ESTADO: BATALHA

    elif estado_jogo == "BATALHA":
        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                running = False
            
            #input da Batalha
            if event.type == pg.KEYDOWN:
                if sistema_batalha and sistema_batalha.battle_over:
                    #se batalha acabou, Espaço para sair
                    if event.key == pg.K_SPACE:
                        #game over apenas se não for revanche
                        if sistema_batalha.vencedor == "INIMIGO":
                            #se for revanche, não dá game over
                            if sistema_batalha.tipo_batalha == "TREINADOR_REVANCHE":
                                mensagem_tela = "Você foi derrotado, mas pode tentar novamente!"
                                estado_jogo = "MUNDO"
                            else:
                                #batalha normal: game over
                                pg.mixer.music.set_volume(0.0)
                                print("GAME OVER")
                                exibir_game_over(screen,clock)
                                running = False
                        else:
                            #verifica se derrotou o professor e dá a insígnia
                            if sistema_batalha.tipo_batalha == "TREINADOR" and sistema_batalha.vencedor == "PLAYER":
                                if npc_falando_agora and npc_falando_agora.tipo_npc == "professor" and not npc_falando_agora.foi_derrotado:
                                    npc_falando_agora.foi_derrotado = True
                                    if "Insígnia do Professor" not in protagonista.inventario:
                                        protagonista.inventario["Insígnia do Professor"] = 1
                                        mensagem_tela = "Você recebeu a Insígnia do Professor!"

                                if npc_falando_agora.tipo_npc == "rival":
                                    mensagem_tela = f"DROGA! Seu {inicial_escolhido} quebrou o meu dedo! Agora vou ter que deixar o CIn em paz..."
                                    pg.mixer.music.set_volume(0.0)
                                    exibir_vitoria(screen,clock)
                                    running = False



                            elif sistema_batalha.tipo_batalha == "TREINADOR_REVANCHE" and sistema_batalha.vencedor == "PLAYER":
                                mensagem_tela = "Vitória na revanche! Você está cada vez mais forte!"
                            
                            estado_jogo = "MUNDO"
                        
                        #volta a música do mundo
                        if estado_jogo == "MUNDO":
                            try: 
                                pg.mixer.music.load(os.path.join(DIRETORIO_BASE, "assets/músicas/world_theme.mp3"))
                                pg.mixer.music.set_volume(volume_padrao)
                                pg.mixer.music.play(-1)
                            except: pass
                else:
                    if sistema_batalha: 
                        sistema_batalha.processar_input(event)

        if sistema_batalha: 
            sistema_batalha.desenhar(screen)

    #desenha a mensagem
    if mensagem_tela:
        rect_fundo = pg.Rect(20, SCREEN_HEIGHT - 160, SCREEN_WIDTH - 40, 140)
        rect_interno = rect_fundo.inflate(-10, -10)
        pg.draw.rect(screen, (40, 40, 160), rect_fundo, border_radius=10)
        pg.draw.rect(screen, (255, 255, 255), rect_interno, border_radius=10)
        fonte = pg.font.SysFont("Arial", 22)
        texto_surf = fonte.render(mensagem_tela, True, (0, 0, 0))
        screen.blit(texto_surf, (rect_interno.x + 20, rect_interno.y + 50))
        fonte_pequena = pg.font.SysFont("Arial", 16)
        aviso = fonte_pequena.render("[Space] para fechar", True, (100, 100, 100))
        screen.blit(aviso, (rect_interno.right - 150, rect_interno.bottom - 30))

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
import json, os
from pokemon import criar_pokemon
from datetime import datetime
import base64

# =============================================================================
# SISTEMA DE SAVE / LOAD
# =============================================================================
def salvar_jogo_sistema(player, equipe, nome_jogador,primeiro_encontro,lista_coletados):
    dados_do_save = {}

    # 1. Posição e Inventário
    dados_do_save["posicao_player"] = [player.rect.x, player.rect.y]
    dados_do_save["inventario"] = player.inventario
    dados_do_save["dados_primeiro_encontro"] = primeiro_encontro
    dados_do_save["nome_jogador"] = nome_jogador
    dados_do_save["tempo_do_save"] = datetime.now().strftime("%H:%M")
    dados_do_save["itens_coletados"] = lista_coletados
    # 2. Equipe Pokémon
    lista_pokemons_save = []
    for poke in equipe:
        dados_poke = {
            "nome": poke.nome,
            "nivel": poke.nivel,
            "xp_atual": poke.xp_atual,
            "hp_atual": poke.hp_atual,
            # Se quiser salvar golpes personalizados, adicione aqui
        }
        lista_pokemons_save.append(dados_poke)

    dados_do_save["equipe"] = lista_pokemons_save
    # ENCODING
    try:
        texto_json = json.dumps(dados_do_save) 
        dados_codificados = base64.b64encode(texto_json.encode('utf-8'))
        with open("savegame.dat", "wb") as arquivo:
            arquivo.write(dados_codificados)
        return "Jogo Salvo com Sucesso!"
    except Exception as e:
        print(e)
        return "Erro ao salvar jogo!"

def carregar_jogo_sistema(player, equipe, grupo_coletaveis, lista_coletados):
    if not os.path.exists("savegame.dat"): # Lembrar de mudar a extensão aqui também
        return "Nenhum save encontrado.", None

    try:
        with open("savegame.dat", "rb") as arquivo: # Modo de leitura BINÁRIA ("rb")
            dados_codificados = arquivo.read()
            
        # 1. Decodifica a sopa de letrinhas de volta para texto
        texto_json = base64.b64decode(dados_codificados).decode('utf-8')
        
        # 2. Carrega o JSON a partir do texto
        dados_carregados = json.loads(texto_json)   

        # 1. Restaurar Player
        player.rect.x = dados_carregados["posicao_player"][0]
        player.rect.y = dados_carregados["posicao_player"][1]
        player.inventario = dados_carregados["inventario"]
        novo_primeiro_encontro = dados_carregados.get("dados_primeiro_encontro", True)
        
        # 2. Restaurar Itens Coletados

        ids_salvos = dados_carregados.get("itens_coletados", [])
        
        lista_coletados.clear()
        lista_coletados.extend(ids_salvos)
        for item in grupo_coletaveis:
            if [item.rect.x, item.rect.y] in ids_salvos:
                item.kill()

        # 3. Restaurar Equipe
        equipe.clear() # Limpa a equipe atual
        
        for dados_poke in dados_carregados["equipe"]:
            # Recria o Pokémon usando sua fábrica
            novo_poke = criar_pokemon(dados_poke["nome"], dados_poke["nivel"])
            
            if novo_poke:
                novo_poke.xp_atual = dados_poke["xp_atual"]
                novo_poke.hp_atual = dados_poke["hp_atual"]
                equipe.append(novo_poke)
        
        return "Jogo Carregado!", novo_primeiro_encontro
    except Exception as e:
        print(e)
        return "Erro ao carregar o save."
    
def ler_info_save():
    if not os.path.exists("savegame.json"):
        return None, "Nenhum save encontrado."

    try:
        with open("savegame.json", "r") as arquivo:
            dados = json.load(arquivo)
            
        nome = dados.get("nome_jogador", "(Vazio)")
        qtd_poke = len(dados.get("equipe", [])) # .get é mais seguro caso a lista não exista
        hora = dados.get("tempo_do_save", "--:--")

        
        # O texto exatamente como você pediu
        msg = f"{nome}: POKEMONS COLETADOS:{qtd_poke} . HORA DO SAVE: {hora}"
        return True, msg
        
    except Exception:
        return False, "Save corrompido."
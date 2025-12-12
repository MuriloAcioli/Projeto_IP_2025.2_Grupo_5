
GOLPES_DB = {
    # Golpes de Dano Básico - DANO PADRAO, falta ajustar a precisão!!
    "Investida":        {"poder": 40, "tipo": "Normal",   "precisao": 100},
    "Brasas":           {"poder": 40, "tipo": "Fogo",     "precisao": 100},
    "Chicote":          {"poder": 45, "tipo": "Grama",    "precisao": 100},
    "Bolhas":           {"poder": 40, "tipo": "Agua",     "precisao": 100},
    "Arranhao":         {"poder": 40, "tipo": "Normal",   "precisao": 100},
    "Picada Venenosa":  {"poder": 15, "tipo": "Venenoso", "precisao": 100},
    "Ventania":         {"poder": 40, "tipo": "Voador",   "precisao": 100},
    "Ataque Rápido":    {"poder": 40, "tipo": "Normal",   "precisao": 100},
    "Choque do Trovão": {"poder": 40, "tipo": "Elétrico", "precisao": 100},
    "Bicada":           {"poder": 35, "tipo": "Voador",   "precisao": 100},
    "Envolver":         {"poder": 15, "tipo": "Normal",   "precisao": 90},
    "Tapa":             {"poder": 40, "tipo": "Normal",   "precisao": 100},

    # Golpes de Status - AJUSTAR O EFEITO!!
    "Tiro de Teia":     {"poder": 1,  "tipo": "Inseto",   "precisao": 95},  # Reduz velocidade
    "Rosnado":          {"poder": 1,  "tipo": "Normal",   "precisao": 100}, # Reduz ataque
    "Ataque de Areia":  {"poder": 1,  "tipo": "Terrestre","precisao": 100}, # Reduz precisão
    "Encarar":          {"poder": 1,  "tipo": "Normal",   "precisao": 100}, # Reduz defesa
    "Abanar o Rabo":    {"poder": 1,  "tipo": "Normal",   "precisao": 100}, # Reduz defesa
    "Canto": {"poder": 0, "tipo": "Normal", "precisao": 55},
    "Teletransporte": {"poder": 0, "tipo": "Psiquico", "precisao": 100},
    "Flash": {"poder": 0, "tipo": "Normal", "precisao": 100},
    "Focar Energia": {"poder": 0, "tipo": "Normal", "precisao": 100},
    "Endurecer": {"poder": 0, "tipo": "Normal", "precisao": 100},
    "Agilidade": {"poder": 0, "tipo": "Psiquico", "precisao": 100},
    "Onda de Trovao": {"poder": 0, "tipo": "Eletrico", "precisao": 90},
    "Barreira": {"poder": 0, "tipo": "Psiquico", "precisao": 100},
    "Recuperacao": {"poder": 0, "tipo": "Normal", "precisao": 100},
    "Refletir": {"poder": 0, "tipo": "Psiquico", "precisao": 100},
    "Ataque de Areia": {"poder": 0, "tipo": "Terra", "precisao": 100},
    "Rosnar": {"poder": 0, "tipo": "Normal", "precisao": 100},
    "Po do Sono": {"poder": 0, "tipo": "Grama", "precisao": 75},
    "Conversao": {"poder": 0, "tipo": "Normal", "precisao": 100},
    # Golpes de Água/Gelo
    "Jato D'Agua": {"poder": 40, "tipo": "Agua", "precisao": 100},
    "Raio de Gelo": {"poder": 90, "tipo": "Gelo", "precisao": 100},
    "Nevasca": {"poder": 110, "tipo": "Gelo", "precisao": 70},
    
    # Golpes Físicos/Normal
    "Pancada Corporal": {"poder": 85, "tipo": "Normal", "precisao": 100},
    "Investida": {"poder": 40, "tipo": "Normal", "precisao": 100},
    "Ataque Rapido": {"poder": 40, "tipo": "Normal", "precisao": 100},
    "Cabecada": {"poder": 70, "tipo": "Normal", "precisao": 100},
    "Pisar": {"poder": 65, "tipo": "Normal", "precisao": 100},
    "Estrondo Sonico": {"poder": 20, "tipo": "Normal", "precisao": 90}, # Dano fixo no original, aqui ajustado
    "Tri-Ataque": {"poder": 80, "tipo": "Normal", "precisao": 100},
    "Meteoro Veloz": {"poder": 60, "tipo": "Normal", "precisao": 100}, # Nunca erra
    "Mordida": {"poder": 60, "tipo": "Normal", "precisao": 100},
    "Enrolar": {"poder": 15, "tipo": "Normal", "precisao": 90},
    "Autodestruicao": {"poder": 200, "tipo": "Normal", "precisao": 100}, # Alto risco

    
    # Golpes Psíquicos
    "Psiquico": {"poder": 90, "tipo": "Psiquico", "precisao": 100},
    "Confusao": {"poder": 50, "tipo": "Psiquico", "precisao": 100},
    "Psirraio": {"poder": 65, "tipo": "Psiquico", "precisao": 100},
    
    # Golpes de Lutador
    "Golpe de Karate": {"poder": 50, "tipo": "Lutador", "precisao": 100},
    "Chute Baixo": {"poder": 50, "tipo": "Lutador", "precisao": 100}, # Dano por peso no original
    "Eremesso Sismico": {"poder": 40, "tipo": "Lutador", "precisao": 100}, # Dano fixo
    
    # Golpes de Pedra/Terra
    "Arremesso de Rocha": {"poder": 50, "tipo": "Pedra", "precisao": 90},
    "Magnitude": {"poder": 70, "tipo": "Terra", "precisao": 100}, # Variavel no original
    "Osso Clube": {"poder": 65, "tipo": "Terra", "precisao": 85},
    "Bonemerangue": {"poder": 50, "tipo": "Terra", "precisao": 90}, # Bate 2x no original
    
    # Golpes de Fogo
    "Brasas": {"poder": 40, "tipo": "Fogo", "precisao": 100},
    "Giro de Fogo": {"poder": 35, "tipo": "Fogo", "precisao": 85},
    "Lanca-Chamas": {"poder": 90, "tipo": "Fogo", "precisao": 100},
    
    # Golpes Elétricos
    "Choque do Trovao": {"poder": 40, "tipo": "Eletrico", "precisao": 100},
    "Trovao": {"poder": 110, "tipo": "Eletrico", "precisao": 70},
    
    # Golpes Voadores
    "Bicar": {"poder": 35, "tipo": "Voador", "precisao": 100},
    "Bico Broca": {"poder": 80, "tipo": "Voador", "precisao": 100},
    "Ataque do Ceu": {"poder": 140, "tipo": "Voador", "precisao": 90},
    
    # Golpes de Planta/Veneno
    "Chicote de Vinha": {"poder": 45, "tipo": "Grama", "precisao": 100},
    "Poluicao": {"poder": 30, "tipo": "Veneno", "precisao": 70},
    "Lama": {"poder": 65, "tipo": "Veneno", "precisao": 100},
    "Acido": {"poder": 40, "tipo": "Veneno", "precisao": 100},
    
    # Golpes de Status (Dano 0, focados em buff/debuff)

}
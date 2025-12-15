# PokéCIn: A ameaça do Mangue!

Jogo voltado ao mundo de pokemon com uma pitada de CIn, prove ao Professor Python, Ricardo Massa, que você é capaz de acabar. Jogo feito em python.


## Controles Básicos do Jogo
- **WASD:** Movimentação do personagem.
- **Tecla E:** Abrir/fechar/inventário.
- **Shift:** Para correr
- **Esc:** Para voltar
- **Espaço:** Para selecionar/interagir

##  Instalação
1. Clone o repositório:

   ```bash
   git clone https://github.com/MuriloAcioli/Projeto_IP_2025.2_Grupo_5.git
   ```

2. Instale as dependências:

   ```py
   pip install -r requirements.txt
   ```
3. Execute o jogo:

   ```py
   python main.py
   ```

##  Equipe

- **Arthur Maciel Costa Zanardi**
- **Felipe de Brito Komata**
- **Murilo Andrade Acioli**
- **Pedro Wellington Ferreira Felizola Lucena**
- **Artur Regis**
- **Rafaell Bezerra Saraiva**

```
PROJETO_IP_2025.2_GRUPO_5/
│
├── .gitignore          # Arquivos ignorados pelo Git (__pycache__)
├── README.md           # Documentação do projeto (Você está aqui!)
├── requirements.txt    # Lista de bibliotecas necessárias (pygame)
├── tutorial.txt        # Guia de uso
│
├── assets/             # RECURSOS DO JOGO (Imagens e Sons)
│   ├── backgrounds/    # Imagens de fundo (mapas, cenários de batalha)
│   ├── coletaveis/     # Sprites dos itens que ficam no chão
│   ├── intro_font/     # Fontes usadas na introdução/menus
│   ├── mc/             # Sprites do Personagem Principal (Main Character)
│   ├── músicas/        # Trilhas sonoras de fundo
│   ├── obstaculos/     # Imagens de objetos sólidos (árvores, pedras)
│   ├── pokemons/       # Sprites dos Pokémons (frente/costas)
│   ├── professor/      # Sprites do NPC Professor
│   └── sfx/            # Efeitos sonoros (ataques, coleta de itens)
│
├── main.py         # PONTO DE ENTRADA (Inicializa o jogo e o loop principal)
├── ataques.py      # Definição e lógica dos golpes
├── batalha.py      # Loop da batalha, turnos e lógica de combate
├── camera.py       # Controle da câmera (segue o player pelo mapa)
├── intro.py        # Telas de introdução e Menu Inicial
├── mato.py         # Lógica da grama alta (encontros aleatórios)
├── Obstaculo.py    # Classe para gerenciar colisões do cenário
├── pokehealer.py   # Lógica de cura (Centro Pokémon/Nurse)
├── coletaveis.py   # Lógica dos itens coletáveis
├── inventario.py   # Gerenciamento da mochila e itens do jogador
├── npc.py          # Comportamento de personagens não jogáveis
├── player.py       # Classe do Jogador (Movimentação, inputs)
├── pokedex.py      # Dados/Visualização dos Pokémons conhecidos
└── pokemon.py      # Classe base do Pokémon (status, vida, tipo)
```

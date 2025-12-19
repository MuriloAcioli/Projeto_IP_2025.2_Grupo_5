# PokéCIn: A Ameaça da Equipe Manga

> **Status do Projeto:** Concluído (2025.2)

O projeto **“PokéCIn: A Ameaça da Equipe Manga”** é um jogo 2D desenvolvido em **Python**, utilizando a biblioteca **PyGame**, para a disciplina de Introdução à Programação do curso de Ciência da Computação do Centro de Informática da UFPE (CIn-UFPE).

O jogo adapta o universo Pokémon para a realidade e cultura do CIn. Sua missão é provar ao **Professor Ricardo Massa** que você é capaz de impedir a **Equipe Manga Rosa** (baseada na Equipe Rocket), que ameaça destruir os computadores do centro após rumores maliciosos.

## Screenshots

<div align="center">
  <img width="795" height="594" alt="Captura de tela 2025-12-19 133032" src="https://github.com/user-attachments/assets/5797ce8e-5955-4d29-925c-fe7990262bc4" />
  <img width="400" alt="Gameplay 2" src="https://github.com/user-attachments/assets/90f85c18-f7e1-4b9c-9bdb-4ac4d8a063c9" />
  <img width="400" alt="Gameplay 3" src="https://github.com/user-attachments/assets/99fac0d7-c0f3-4921-870b-1c113f6249a9" />
  <img width="400" alt="Gameplay 4" src="https://github.com/user-attachments/assets/7b770ae6-5efb-4211-8422-2f4897b06e3e" />
  <img width="400" alt="Gameplay 5" src="https://github.com/user-attachments/assets/0b13d0a2-05ac-4348-afd7-e88dc91c7ccb" />
  <img width="799" height="591" alt="Captura de tela 2025-12-19 133100" src="https://github.com/user-attachments/assets/41238d4a-7010-49f0-9fcb-62f419c3300b" />
</div>

---

## Controles

| Tecla | Ação |
| :---: | :--- |
| **W, A, S, D** | Movimentação do personagem |
| **Shift** | Correr |
| **E** | Abrir/Fechar Inventário |
| **Espaço** | Selecionar / Interagir |
| **Esc** | Voltar / Menu de Pausa |

---

## Instalação e Execução

Pré-requisitos: Python instalado.

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/MuriloAcioli/Projeto_IP_2025.2_Grupo_5.git](https://github.com/MuriloAcioli/Projeto_IP_2025.2_Grupo_5.git)

##  Equipe

- **Arthur Maciel Costa Zanardi** - Responsável pela movimentação do player, geração de mundo, colisões, e estrutura geral do código, implementações de sprites.
- **Felipe de Brito Komata** - Responsável pelo Visual do jogo, Criações de sprites autorais, polimento do código.
- **Murilo Andrade Acioli** - Principal idealista do jogo, implementou lógica de pokemons, e da lógica base de batalhas.
- **Pedro Wellington Ferreira Felizola Lucena** - Level designer, responsável pela lógica dos coletaveis e organização da party de pokemons.
- **Artur Regis** - Desenvolveu a mecânica dos menus, lógica primitiva das classes pokemons e do menu de batalha.
- **Rafaell Bezerra Saraiva** - Responsável pelas mecânicas de spawn e captura de pokemons, batalhas de chefe, polimento geral de gameplay e correção de bugs.

## Arquitetura do Projeto

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
│   ├── icon/     # Fontes usadas na introdução/menus
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
├── batalha.py      # Loop da batalha, turnos e lógica de combatex
├── camera.py       # Controle da câmera (segue o player pelo mapa)
├── intro.py        # Telas de introdução e Menu Inicial
├── mato.py         # Lógica da grama alta (encontros aleatórios)
├── obstaculo.py    # Classe para gerenciar colisões do cenário
├── pokehealer.py   # Lógica de cura (Centro Pokémon/Nurse)
├── coletaveis.py   # Lógica dos itens coletáveis
├── inventario.py   # Gerenciamento da mochila e itens do jogador
├── npc.py          # Comportamento de personagens não jogáveis
├── player.py       # Classe do Jogador (Movimentação, inputs)
├── pokedex.py      # Dados/Visualização dos Pokémons conhecidos
├── pokemon.py      # Criação dos pokemons. Função de instanciar (criar) os pokemons.
├── vitoria.py      # Tela de vitória e seus elementos 
└── game_over.py      # Tela de Game Over e seus elementos
```

## Bibliotecas:

Pygame - Biblioteca base para criação de jogos em Python.<br>
Os - Foi usado para acessar os diretorios de forma padrão através do World_path.<br>
Random - gerar de maneira simples aleatoriedade.<br>
Math - Usado para simplificar cálculos mais complexos.<br>

## Conceitos aprendidos em aulas e usados no código:

Condicionais - usado durante todo o código para a parte de desenvolvimento lógico do jogo.<br>
Loops - usados nas batalhas, intro, menus e toda mecânica que há repetição.<br>
Listas - usado no inventário, na party de pokemon do player e de inimigos.<br>
Funções - usados em forma de métodos em classes e para carregar e desenhar cenas em geral.<br>
Tuplas - Usados principalmente por conta da sintaxe do pygame para passar valores de escala e posição.<br>
Dicíonarios - Usados na categorização de pokemon, inventário, lista de ataques e pokedex.<br>

## Desafios e erros:

## Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?

Desenvolver muitas mecânicas simultaneamente sobrecarregou a equipe. A solução foi priorizar funcionalidades essenciais em detrimento do polimento de recursos secundários.

## Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?

Gestão de Versão: A maior dificuldade inicial foi a adaptação ao Git e GitHub. O desenvolvimento começou fragmentado, exigindo a união manual de códigos e resolução complexa de conflitos. Com o tempo, a equipe adotou branches e merges, aumentando a eficiência.

## Quais as lições aprendidas durante o projeto?

Organização e destribuição de tarefas é essencial - é necessário organização extrema quando desenvolvendos softwares complexos, minimizando a ociosidade dos membros, até porque muitas mecânicas dependem de outras para serem desenvolvidas.

Comunicação constante e relatórios de desenvolvimentos são necessários - aconteceu de mais de um membro estar desenvolvendo a mesma feature, o que diminuiu nossa produtividade e gerou frustração no grupo. Após isso percebemos que é muito importante que todos estejam alinhados e saibam o que os outros estão fazendo e quando estão fazendo.

É preciso propósito em conjunto - acima de tudo, ter pessoas alinhadas e comprometidas a um objetivo em comum foi essencial, madrugamos inúmeras noites em equipe sem reclamar e o que era para ser obrigação, virou hobby, esse foi o fator principal para o sucesso do nosso trabalho.







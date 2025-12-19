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
## SCREENSHOTS

<img width="794" height="544" alt="Captura de tela 2025-12-18 123651" src="https://github.com/user-attachments/assets/99fac0d7-c0f3-4921-870b-1c113f6249a9" />


##  Equipe

- **Arthur Maciel Costa Zanardi** - Responsável pela movimentação do player, geração de mundo, colisões, e estrutura geral do código, implementações de sprites.
- **Felipe de Brito Komata** - Responsável pelo Visual do jogo, Criações de sprites autorais, polimento do código.
- **Murilo Andrade Acioli** - Principal idealista do jogo, implementou lógica de pokemons, e da lógica base de batalhas.
- **Pedro Wellington Ferreira Felizola Lucena** - Level designer, responsável pela lógica dos coletaveis e organização da party de pokemons.
- **Artur Regis** - Desenvolveu a mecânica dos menus, lógica primitiva das classes pokemons e do menu de batalha.
- **Rafaell Bezerra Saraiva** - Responsável pelas mecânicas de spawn e captura de pokemons, batalhas de chefe, polimento geral de gameplay e correção de bugs.

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

Bibliotecas:

Pygame - Biblioteca base para criação de jogos em Python.
Os - Foi usado para acessar os diretorios de forma padrão através do World_path.
Random - gerar de maneira simples aleatoriedade.
Math - Usado para simplificar cálculos mais complexos.

Conceitos aprendidos em aulas e usados no código:

Condicionais - usado durante todo o código para a parte de desenvolvimento lógico do jogo.
Loops - usados nas batalhas, intro, menus e toda mecânica que há repetição.
Listas - usado no inventário, na party de pokemon do player e de inimigos.
Funções - usados em forma de métodos em classes e para carregar e desenhar cenas em geral.
Tuplas - Usados principalmente por conta da sintaxe do pygame para passar valores de escala e posição.
Dicíonarios - Usados na categorização de pokemon, inventário, lista de ataques e pokedex.

Desafios e erros:

Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?

O maior erro foi desenvolver muitos mecânicas simultaneamente e deixar o polimento para o final, sobrecarregando os membros do grupo desnecessariamente. Lidamos pela força do braço, trabalhando até tarde e escolhendo mecânicas menos importantes para ficarem menos polidas.


Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?

Demora da maior parte do grupo a aprender a mexer com git e github. Inicialmente desenvolvemos tudo separadamente e tivemos que juntar todas as partes do código e lidar com conflitos manualmente. Próximo do final, o grupo já estava familiarizado com as ferramentas, e pode codar muito mais eficientemente, usando branches e merge.

Quais as lições aprendidas durante o projeto?

Organização e destribuição de tarefas é essencial - é necessário organização extrema quando desenvolvendos softwares complexos, minimizando a ociosidade dos membros, até porque muitas mecânicas dependem de outras para serem desenvolvidas.

Comunicação constante e relatórios de desenvolvimentos são necessários - aconteceu de mais de um membro estar desenvolvendo a mesma feature, o que diminuiu nossa produtividade e gerou frustração no grupo. Após isso percebemos que é muito importante que todos estejam alinhados e saibam o que os outros estão fazendo e quando estão fazendo.

É preciso propósito em conjunto - acima de tudo, ter pessoas alinhadas e comprometidas a um objetivo em comum foi essencial, madrugamos inúmeras noites em equipe sem reclamar e o que era para ser obrigação, virou hobby, esse foi o fator principal para o sucesso do nosso trabalho.



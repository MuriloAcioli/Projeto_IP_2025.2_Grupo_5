import pygame as pg

# Configurações básicas

class Player(pg.sprite.Sprite): # É boa prática herdar de sprite.Sprite
    def __init__(self, x, y, sprite_sheet_path_down, sprite_sheet_path_left,sprite_sheet_path_up,sprite_sheet_path_right):
        super().__init__()
        
        # 1. Carregar as imagens (Spritesheets)
        
        self.animations = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }

        self.inventario = {}

        img_down = pg.image.load(sprite_sheet_path_down).convert()
        img_left = pg.image.load(sprite_sheet_path_left).convert()
        img_up = pg.image.load(sprite_sheet_path_up).convert()
        img_right = pg.image.load(sprite_sheet_path_right).convert()
        
        img_down.set_colorkey((255, 255, 255))
        img_left.set_colorkey((255, 255, 255))
        img_up.set_colorkey((255, 255, 255))
        img_right.set_colorkey((255, 255, 255))

        # Função interna para recortar a spritesheet
        def recortar_frames(imagem, quantidade_frames):
            lista_frames = []
            frame_width = imagem.get_width() // quantidade_frames
            frame_height = imagem.get_height()
            
            for i in range(quantidade_frames):
                # Cria um recorte (rect) da imagem original
                corte = pg.Rect(i * frame_width, 0, frame_width, frame_height)
                # Pega a subsuperfície
                frame = imagem.subsurface(corte)
                lista_frames.append(frame)
            return lista_frames

        # Preenchendo as animações
        self.animations['down'] = recortar_frames(img_down, 4)
        self.animations['left'] = recortar_frames(img_left, 4)
        self.animations['right'] = recortar_frames(img_right, 4)
        self.animations['up'] = recortar_frames(img_up, 4)

        # 2. Configuração da Animação
        self.frame_index = 0
        self.animation_speed = 0.15 # Velocidade da troca de quadros
        self.status = 'down' # Estado inicial
        
        # 3. Configuração da Imagem Inicial
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.direction = pg.math.Vector2(0, 0) # Vetor de direção é melhor que x/y soltos

    def get_input(self):
            keys = pg.key.get_pressed()
            
            # --- LÓGICA DO SHIFT (CORRER) ---
            # Se Shift Esquerdo (LSHIFT) estiver apertado
            if keys[pg.K_LSHIFT]: 
                self.speed = 5           # Aumenta a velocidade
                self.animation_speed = 0.15 # (Opcional) Acelera a animação das pernas
            else:
                self.speed = 3            # Volta para velocidade normal
                self.animation_speed = 0.1 # Volta animação normal
            # -------------------------------

            # Reseta direção
            self.direction.x = 0
            self.direction.y = 0

            if keys[pg.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pg.K_d]:
                self.direction.x = 1
                self.status = 'right'
                
            if keys[pg.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pg.K_s]:
                self.direction.y = 1
                self.status = 'down'

    def animate(self):
        # Só anima se estiver se movendo
        if self.direction.magnitude() != 0:
            self.frame_index += self.animation_speed
            
            # Se o index passar do número de frames, volta pro 0 (loop)
            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0
        else:
            # Se estiver parado, mostra o primeiro frame (index 0) ou frame de "idle"
            self.frame_index = 0

        # Atualiza a imagem atual
        # O int() é necessário porque frame_index é float para controlar velocidade
        self.image = self.animations[self.status][int(self.frame_index)]

    def update(self):
        self.get_input()
        self.animate()
        
        # Movimentação normalizando o vetor (pra não andar mais rápido na diagonal)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

# --- Loop Principal para testar ---

""" Alteração """
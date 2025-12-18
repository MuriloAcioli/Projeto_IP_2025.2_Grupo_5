import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet_path_down, sprite_sheet_path_left,sprite_sheet_path_up,sprite_sheet_path_right):
        super().__init__()
        
        # tamanho do personagem
        self.ESCALA = 1.4  # 1.0 = Normal, 2.0 = Dobro do tamanho, etc.
        #self.primeiro_encontro = True
        #Carregar as imagens
        
        self.animations = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }

        self.inventario = {}

        # Carrega as folhas de sprite originais
        img_down = pg.image.load(sprite_sheet_path_down).convert()
        img_left = pg.image.load(sprite_sheet_path_left).convert()
        img_up = pg.image.load(sprite_sheet_path_up).convert()
        img_right = pg.image.load(sprite_sheet_path_right).convert()
        
        img_down.set_colorkey((255, 255, 255))
        img_left.set_colorkey((255, 255, 255))
        img_up.set_colorkey((255, 255, 255))
        img_right.set_colorkey((255, 255, 255))

        # Função interna para recortar e aumentar
        def recortar_frames(imagem, quantidade_frames):
            lista_frames = []
            frame_width = imagem.get_width() // quantidade_frames
            frame_height = imagem.get_height()
            
            for i in range(quantidade_frames):
                # Cria um recorte (rect) da imagem original
                corte = pg.Rect(i * frame_width, 0, frame_width, frame_height)
                
                # Pega a subsuperfície (o frame pequeno original)
                frame_original = imagem.subsurface(corte)
                
                novo_w = int(frame_width * self.ESCALA)
                novo_h = int(frame_height * self.ESCALA)
                
                # Criamos o frame aumentado
                frame_escalado = pg.transform.scale(frame_original, (novo_w, novo_h))
                
                # Adicionamos o frame grande na lista
                lista_frames.append(frame_escalado)
                
            return lista_frames

        # Preenchendo as animações (já virão aumentadas)
        self.animations['down'] = recortar_frames(img_down, 4)
        self.animations['left'] = recortar_frames(img_left, 4)
        self.animations['right'] = recortar_frames(img_right, 4)
        self.animations['up'] = recortar_frames(img_up, 4)

        #Configuração da Animação
        self.frame_index = 0
        self.animation_speed = 0.15 
        self.status = 'down' 
        
        #Configuração da Imagem Inicial
        self.image = self.animations[self.status][self.frame_index]
        
        #O rect vai pegar o tamanho da imagem já aumentada automaticamente
        self.rect = self.image.get_rect(topleft=(x, y))
        #self.rect.height = self.rect.height // 2
        #self.rect.bottom = y + self.image.get_height()
        self.hitbox = self.rect.inflate(0, -self.rect.height / 1.3)
        
        self.hitbox.bottom = self.rect.bottom
        self.speed = 5
        self.direction = pg.math.Vector2(0, 0) 
        
    def get_input(self):
            keys = pg.key.get_pressed()
            
            # logica da corrida (tecla SHIFT)
            if keys[pg.K_LSHIFT]: 
                self.speed = 6          # Aumentei um pouco a corrida já que o boneco cresceu
                self.animation_speed = 0.15 
            else:
                self.speed = 4          
                self.animation_speed = 0.1 

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
            
            if self.frame_index >= len(self.animations[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 0

        # Atualiza a imagem atual
        self.image = self.animations[self.status][int(self.frame_index)]

    def update(self):
        self.get_input()
        self.animate()
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        self.hitbox.midbottom = self.rect.midbottom

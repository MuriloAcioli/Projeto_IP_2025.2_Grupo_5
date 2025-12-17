import pygame as pg
import os

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))

class PokeHealer(pg.sprite.Sprite):
    """Representa um Centro Pokémon (PokeHealer) no mapa."""
    
    # Path para a imagem (você precisará de uma imagem, use um placeholder temporário se não tiver)
    # Exemplo: um bloco vermelho ou algo que simbolize a cura. 
    # Vou usar o Obstaculo como base visual por agora.
    
    def __init__(self, x, y, tile_size=48):
        super().__init__()
        
        # Tenta carregar uma imagem específica para o Healer
        try:
            path_imagem = os.path.join(DIRETORIO_BASE, "assets/obstaculos/pokehealer.png")
            self.image = pg.image.load(path_imagem).convert_alpha()
        except pg.error:
            # Fallback (usar um quadrado simples ou a imagem do Obstaculo se já carregada)
            print("AVISO: Imagem do PokeHealer não encontrada. Usando quadrado temporário.")
            self.image = pg.Surface((tile_size, tile_size))
            self.image.fill((255, 0, 0)) # Um bloco vermelho para cura
            
        self.image = pg.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()
        self.foi_curado = False # Flag para evitar cura repetida ao ficar parado
        
    def curar_equipe(self, equipe_jogador,volume_padrao):
        """Restaura HP e status de todos os Pokemons da equipe."""
        if self.foi_curado:
            return "A equipe já está curada."
            
        curados = 0
        for pokemon in equipe_jogador:
            # Restaura HP
            pokemon.hp_atual = pokemon.hp_max
            # Você pode adicionar lógica para curar status aqui (ex: envenenamento)
            # if pokemon.status != None: pokemon.status = None
            curados += 1
            
        if curados >= 0:
            self.foi_curado = True # Marca como curado
            
            sfx_heal = None
            try: 
                sfx_heal = pg.mixer.Sound(os.path.join(DIRETORIO_BASE, "assets/sfx/sfx_heal.wav"))
                sfx_heal.set_volume(volume_padrao)
            except: pass

            sfx_heal.play()

            return f"Sua equipe de {len(equipe_jogador)} Pokémons foi curada!"
        else:
            return "Você não tem Pokémons para curar!"
            
    def resetar_cura(self):
        """Reseta a flag 'foi_curado' para permitir curar novamente (ex: se o player sair e voltar)."""
        self.foi_curado = False
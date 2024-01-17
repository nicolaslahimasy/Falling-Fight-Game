import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('Character/tiles/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)


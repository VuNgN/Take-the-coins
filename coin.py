import pygame
import random

class Coin(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 165, 0))  # Orange
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(0, screen_height - self.rect.height)

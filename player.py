import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Yellow
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.check_boundary()

    def check_boundary(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface((50, 50))
        self.image.fill((139, 69, 19))  # Brown
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(0, screen_height - self.rect.height)
        self.dx = random.choice([-1, 1])  # Random initial direction
        self.dy = random.choice([-1, 1])  # Random initial direction
        self.speed_increase = 0.1
        self.time_since_speed_increase = 0
        self.time_since_duplication = 0

    def update(self, obstacles):
        FPS = 60
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.left < 0 or self.rect.right > self.screen_width:
            self.dx *= -1
        if self.rect.top < 0 or self.rect.bottom > self.screen_height:
            self.dy *= -1

        # Increase speed every 5 seconds
        self.time_since_speed_increase += 1 / FPS
        if self.time_since_speed_increase >= 5:
            self.speed_increase *= 1.5
            self.dx *= 1 + self.speed_increase
            self.dy *= 1 + self.speed_increase
            self.time_since_speed_increase = 0

        # Duplicate every 5 seconds
        self.time_since_duplication += 1 / FPS
        if self.time_since_duplication >= 5:
            new_obstacle = Obstacle(self.screen_width, self.screen_height)
            new_obstacle.rect.x = self.rect.x
            new_obstacle.rect.y = self.rect.y
            obstacles.add(new_obstacle)
            self.time_since_duplication = 0

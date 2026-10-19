import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet, speed):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(3):  # 3 frames d'animation
            img = spritesheet.get_image(i, 32, 32, 1.5, (0, 0, 0))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.counter = 0
    
    def update(self, scroll, SCREEN_WIDTH):
        self.rect.x -= self.speed
        self.rect.y += scroll
        
        # Animation
        self.counter += 1
        if self.counter >= 15:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
        
        # Supprimer si hors écran
        if self.rect.right < 0:
            self.kill()
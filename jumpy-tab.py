import pygame
import random
import os
import json
from pygame import mixer

# Initialisation
pygame.init()
mixer.init()

# Configuration
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy with Maps')
clock = pygame.time.Clock()
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Polices
font = pygame.font.SysFont('Arial', 20)
big_font = pygame.font.SysFont('Arial', 30)

# Variables du jeu
scroll = 0
score = 0
game_over = False
current_level = 1
max_levels = 3

# Classe Joueur
class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((30, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumping = False

    def update(self, platforms):
        # Gravité
        self.vel_y += 0.5
        if self.vel_y > 10:
            self.vel_y = 10

        # Mouvement vertical
        self.rect.y += self.vel_y

        # Collision avec les plateformes
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                if self.rect.bottom < platform.rect.centery:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = -15
                    self.jumping = False

        # Contrôles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Limites de l'écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Game over si tombe en bas
        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y - scroll))

# Classe Plateforme
class Platform:
    def __init__(self, x, y, width, is_moving=False):
        self.image = pygame.Surface((width, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_moving = is_moving
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        if self.is_moving:
            self.rect.x += self.move_direction * 2
            self.move_counter += 1
            if self.move_counter > 100:
                self.move_direction *= -1
                self.move_counter = 0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y - scroll))

# Classe Ennemi
class Enemy:
    def __init__(self, x, y):
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass  # Ajouter du mouvement si nécessaire

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y - scroll))

# Système de Maps
class MapSystem:
    def __init__(self):
        self.maps = {}
        self.load_maps()
    
    def load_maps(self):
        # Map 1 - Facile
        self.maps[1] = {
            "platforms": [
                {"x": 150, "y": 500, "width": 100, "moving": False},
                {"x": 300, "y": 400, "width": 80, "moving": False},
                {"x": 50, "y": 300, "width": 80, "moving": True},
                {"x": 200, "y": 200, "width": 100, "moving": False}
            ],
            "enemies": [
                {"x": 200, "y": 150}
            ],
            "player_start": {"x": 200, "y": 400}
        }

        # Map 2 - Moyenne
        self.maps[2] = {
            "platforms": [
                {"x": 100, "y": 550, "width": 80, "moving": False},
                {"x": 250, "y": 450, "width": 60, "moving": True},
                {"x": 50, "y": 350, "width": 70, "moving": False},
                {"x": 280, "y": 250, "width": 90, "moving": True},
                {"x": 100, "y": 150, "width": 80, "moving": False}
            ],
            "enemies": [
                {"x": 150, "y": 100},
                {"x": 300, "y": 200}
            ],
            "player_start": {"x": 200, "y": 450}
        }

        # Map 3 - Difficile
        self.maps[3] = {
            "platforms": [
                {"x": 50, "y": 500, "width": 70, "moving": True},
                {"x": 200, "y": 450, "width": 60, "moving": False},
                {"x": 300, "y": 380, "width": 50, "moving": True},
                {"x": 100, "y": 300, "width": 60, "moving": False},
                {"x": 250, "y": 220, "width": 70, "moving": True},
                {"x": 50, "y": 150, "width": 80, "moving": False}
            ],
            "enemies": [
                {"x": 200, "y": 100},
                {"x": 100, "y": 250},
                {"x": 300, "y": 350}
            ],
            "player_start": {"x": 200, "y": 400}
        }
    
    def get_map(self, level):
        return self.maps.get(level, self.maps[1])

# Initialisation des systèmes
map_system = MapSystem()
player = None
platforms = []
enemies = []

def load_level(level):
    global player, platforms, enemies, scroll
    
    # Réinitialiser
    platforms = []
    enemies = []
    scroll = 0
    
    # Charger la map
    current_map = map_system.get_map(level)
    
    # Créer les plateformes
    for plat_data in current_map["platforms"]:
        platforms.append(Platform(
            plat_data["x"], 
            plat_data["y"], 
            plat_data["width"], 
            plat_data["moving"]
        ))
    
    # Créer les ennemis
    for enemy_data in current_map["enemies"]:
        enemies.append(Enemy(
            enemy_data["x"], 
            enemy_data["y"]
        ))
    
    # Créer le joueur
    start_pos = current_map["player_start"]
    player = Player(start_pos["x"], start_pos["y"])

# Charger le premier niveau
load_level(current_level)

# Menu
def show_menu():
    screen.fill(BLACK)
    title = big_font.render("JUMPY ADVENTURE", True, WHITE)
    start = font.render("Appuyez sur ESPACE pour commencer", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))
    screen.blit(start, (SCREEN_WIDTH//2 - start.get_width()//2, 300))
    pygame.display.update()

# Boucle de jeu
running = True
in_menu = True

while running:
    clock.tick(FPS)
    
    # Menu
    if in_menu:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_menu = False
        continue
    
    # Jeu principal
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        # Mettre à jour le joueur
        game_over = player.update(platforms)
        
        # Mettre à jour les plateformes
        for platform in platforms:
            platform.update()
        
        # Mettre à jour le scroll
        if player.rect.y < SCROLL_THRESH:
            scroll = SCROLL_THRESH - player.rect.y
            player.rect.y = SCROLL_THRESH
        
        # Mettre à jour le score
        score = max(score, -player.rect.y)
        
        # Vérifier la fin du niveau
        if player.rect.y < -500:  # Atteint le haut de la map
            current_level += 1
            if current_level > max_levels:
                current_level = 1  # Reboucler
            load_level(current_level)
    
    # Dessin
    screen.fill(BLACK)
    
    # Dessiner les plateformes
    for platform in platforms:
        platform.draw(screen)
    
    # Dessiner les ennemis
    for enemy in enemies:
        enemy.draw(screen)
    
    # Dessiner le joueur
    player.draw(screen)
    
    # UI
    level_text = font.render(f"Niveau: {current_level}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(level_text, (10, 10))
    screen.blit(score_text, (10, 40))
    
    # Game over
    if game_over:
        over_text = big_font.render("GAME OVER", True, RED)
        restart_text = font.render("Appuyez sur R pour recommencer", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 200))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 250))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            score = 0
            load_level(current_level)
    
    pygame.display.update()

pygame.quit()
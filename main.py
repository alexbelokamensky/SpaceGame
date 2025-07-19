import pygame
import math
import os
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

original_player_image = pygame.image.load(os.path.join("rocket.png")).convert_alpha()
player_sprite = pygame.transform.scale(original_player_image, (75,75))

class Mob:
    def __init__(self, x, y, angle=0):
        self.pos = pygame.Vector2(x, y)
        self.angle = angle
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

    def update(self, dt):
        self.velocity += self.acceleration
        self.pos += self.velocity * dt

    def draw(self, surface, image):
        rotated_image = pygame.transform.rotate(image, -self.angle)
        rect = rotated_image.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(rotated_image, rect.topleft)

class Player(Mob):
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.angle -= 5
        if keys[pygame.K_d]:
            self.angle += 5
    
    def update(self, dt):
        self.acceleration = pygame.Vector2(math.sin(math.radians(self.angle)),-math.cos(math.radians(self.angle)))
        self.velocity += self.acceleration
        self.pos += self.velocity * dt

player = Player(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    screen.fill("black")

    player.handle_input()
    player.update(dt)
    player.draw(screen, player_sprite)

    pygame.display.flip()

pygame.quit()
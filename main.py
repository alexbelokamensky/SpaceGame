import pygame
import math
import os
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_rotation = 270
player_acceleration = pygame.Vector2(0,0)
player_speed = pygame.Vector2(0,0)

original_player_image = pygame.image.load(os.path.join("rocket.png")).convert_alpha()
player_sprite = pygame.transform.scale(original_player_image, (75,75))
player_sprite = pygame.transform.rotate(player_sprite, 90)

def player(x,y): 
    rotated_image = pygame.transform.rotate(player_sprite, player_rotation)
    rect = rotated_image.get_rect(center=(x, y))
    screen.blit(rotated_image, rect.topleft)
    player_mask = pygame.mask.from_surface(rotated_image)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    radians = math.radians(player_rotation)
    player_acceleration.x = -math.cos(radians)
    player_acceleration.y = math.sin(radians)

    player_speed.x += player_acceleration.x
    player_speed.y += player_acceleration.y

    player_pos.x += player_speed.x/20
    player_pos.y += player_speed.y/20

    player(player_pos.x, player_pos.y)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_rotation += 5
    if keys[pygame.K_d]:
        player_rotation -= 5

    if player_pos.x > 1280:
        player_pos.x = 0
    if player_pos.x < 0:
        player_pos.x = 1280
    if player_pos.y > 720:
        player_pos.y = 0
    if player_pos.y < 0:
        player_pos.y = 720

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
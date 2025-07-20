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

original_asteroid_image = pygame.image.load(os.path.join("asteroid.png")).convert_alpha()
asteroid_sprite = pygame.transform.scale(original_asteroid_image, (50, 50))

class Mob:
    def __init__(self, x, y, angle=0):
        self.pos = pygame.Vector2(x, y)
        self.angle = angle
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

    def update(self, dt):
        self.angle += 2
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

class Asteroid(Mob):
    def generate(self):
        match random.randrange(0, 3):
            case 0: 
                self.pos = pygame.Vector2(0, random.randrange(0, 720))
                self.acceleration = pygame.Vector2(random.uniform(0, 1), random.uniform(-1, 1))
            case 1: 
                self.pos = pygame.Vector2(1280, random.randrange(0, 720))
                self.acceleration = pygame.Vector2(random.uniform(-1, 0), random.uniform(-1, 1))
            case 2: 
                self.pos = pygame.Vector2(random.randrange(0,1280), 0)
                self.acceleration = pygame.Vector2(random.uniform(-1, 1), random.uniform(0, 1))
            case 3: 
                self.pos = pygame.Vector2(random.randrange(0,1280), 720)
                self.acceleration = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 0))
        print(f"{self.acceleration.x} {self.acceleration.y}")

    def clear(self):
        if self.pos.x > 1380 and self.pos.x < -100 and sepf.pos.y > 820 and self.pos.y < -100:
            return True
        return False

player = Player(screen.get_width() / 2, screen.get_height() / 2)
asteroid = Asteroid(0,0)
asteroid.generate()

asteroids = [asteroid]

frame_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000

    screen.fill("black")

    player.handle_input()
    player.update(dt)
    player.draw(screen, player_sprite)

    for asteroid in asteroids:
        asteroid.draw(screen, asteroid_sprite)
        asteroid.update(dt)
        
        if asteroid.clear():
            asteroids.remove(asteroid)

    frame_counter += 1
    if frame_counter == 90:
        frame_counter = 0
        asteroid = Asteroid(0, 0)
        asteroid.generate()
        asteroids.append(asteroid)
        print("generated")

    pygame.display.flip()

pygame.quit()
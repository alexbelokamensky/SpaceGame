import pygame
import math
import os
import random
import button

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.Font(None, 25)
clock = pygame.time.Clock()
running = True
main_menu = True
game_over = False
survival_game = None
dt = 0

lvl_sprite = pygame.image.load(os.path.join("lvl1.png")).convert_alpha()

original_player_image = pygame.image.load(os.path.join("rocket.png")).convert_alpha()
player_sprite = pygame.transform.scale(original_player_image, (75,75))

original_asteroid_image = pygame.image.load(os.path.join("asteroid.png")).convert_alpha()
asteroid_sprite = pygame.transform.scale(original_asteroid_image, (50, 50))

lvl_mask = pygame.mask.from_surface(lvl_sprite)
player_mask = pygame.mask.from_surface(player_sprite)
asteroid_mask = pygame.mask.from_surface(asteroid_sprite)

class Mob:
    def __init__(self, x, y, angle=0, image=None):
        self.pos = pygame.Vector2(x, y)
        self.angle = angle
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.original_image = image
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.angle += 2
        self.velocity += self.acceleration
        self.pos += self.velocity * dt

    def update_graphics(self):
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

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
        if self.pos.x > 1380 or self.pos.x < -100 or self.pos.y > 820 or self.pos.y < -100:
            return True
        return False

    def collides_with(self, other, radius_self, radius_other):
        return self.pos.distance_to(other.pos) < (radius_self + radius_other)

class GameState:
    MAIN_MENU = "main_menu"
    SURVIVAL = "survival"
    PARKING = "parking"
    GAME_OVER = "game_over"

class lvl:
    def __init__(self, image):
        self.pos = pygame.Vector2(0,0)
        self.image = image
        self.rect = self.image.get_rect(center=self.pos)
    
    def draw(self, surface, image):
        surface.blit(image, self.rect.center)

current_state = GameState.MAIN_MENU
level = lvl(lvl_sprite)
player = Player(screen.get_width() / 2, screen.get_height() / 2, image=player_sprite)
asteroid = Asteroid(0, 0, image=asteroid_sprite)
asteroid.generate()

asteroids = [asteroid]


main_menu_buttons = [
    button.Button(275, 200, 300, 100, "Survival", font, (0,128,255), (0,200,255), (255,255,255), lambda: change_state(GameState.SURVIVAL)),
    button.Button(675, 200, 300, 100, "Parking", font, (0,128,255), (0,200,255), (255,255,255), lambda: change_state(GameState.PARKING))
]
game_over_buttons = [
    button.Button(275, 400, 300, 100, "Restart", font, (200,0,0), (128,0,0), (255,255,255), lambda: change_state(GameState.MAIN_MENU)),
    button.Button(675, 400, 300, 100, "Main Menu", font, (200,0,0), (128,0,0), (255,255,255), lambda: change_state(GameState.MAIN_MENU))
]

def change_state(new_state):
    global current_state, asteroids, player
    current_state = new_state
    asteroids.clear()
    player = Player(screen.get_width()/2, screen.get_height()/2, image=player_sprite)

frame_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_state == GameState.MAIN_MENU:
        for btn in main_menu_buttons:
            btn.handele_event(event)
    elif current_state == GameState.GAME_OVER:
        for btn in game_over_buttons:
            btn.handele_event(event)
    dt = clock.tick(60) / 1000
    screen.fill("black")

    if current_state == GameState.MAIN_MENU:
        for btn in main_menu_buttons:
            btn.draw(screen)

    elif current_state == GameState.PARKING:
        player.handle_input()
        player.update(dt)
        player.update_graphics()
        player.draw(screen)
        level.draw(screen, lvl_sprite)
        offset = (level.pos.x - player.rect.x, level.pos.y - player.rect.y)
        if player_mask.overlap(lvl_mask, offset):
            current_state = GameState.GAME_OVER

    elif current_state == GameState.SURVIVAL:
        player.handle_input()
        player.update(dt)
        player.update_graphics()
        player.draw(screen)
        for asteroid in asteroids:
            asteroid.update_graphics()
            asteroid.draw(screen)
            asteroid.update(dt)

            offset = (int(asteroid.rect.left - player.rect.left), int(asteroid.rect.top - player.rect.top))
            if player.mask.overlap(asteroid.mask, offset):
                current_state = GameState.GAME_OVER
                
            if asteroid.clear():
                asteroids.remove(asteroid)

        frame_counter += 1
        if frame_counter == 30:
            frame_counter = 0
            asteroid = Asteroid(0, 0, image=asteroid_sprite)
            asteroid.generate()
            asteroids.append(asteroid)
            print(len(asteroids))

    elif current_state == GameState.GAME_OVER:
        for btn in game_over_buttons:
            btn.draw(screen)

    pygame.display.flip()

pygame.quit()
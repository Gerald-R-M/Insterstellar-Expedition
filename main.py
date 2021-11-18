# -------------------------------------------Interstellar Expedition---------------------------------------------------#
# -------------------------------------------Author: Gerald Monnecka---------------------------------------------------#
# ------------------------------------------------Version: 0.75--------------------------------------------------------#
# --------------Description: Move the yellow triangle with WASD and navigate your way through space!-------------------#
# ---------------------------------------------------------------------------------------------------------------------#
# -------------------------------What remains: Difficulty settings and obstacles.--------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
# ----------------------------Implement non-placeholder art assets and sound effects-----------------------------------#

import pygame
import os
import time
import random
pygame.font.init()

WIDTH = 750
HEIGHT = 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interstellar Expedition")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "red_ship.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "blue_ship.png"))
PURPLE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "purple_ship.png"))

# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "player_ship.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "red_laser.png"))
PURPLE_LASER = pygame.image.load(os.path.join("assets", "purple_laser.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "blue_laser.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "yellow_laser.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))

#Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 15

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objects):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objects:
                    if laser.collision(obj):
                        objects.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, GREEN, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "purple": (PURPLE_SPACE_SHIP, PURPLE_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("Arial", 25)
    lost_font = pygame.font.SysFont("Arial", 30)

    #TODO implement scoring

    enemies = []
    wave_length = 5 #TODO implement different wave lengths and speeds based on difficulties
    enemy_velocity = 3

    player_velocity = 8
    laser_velocity = 7

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WINDOW.blit(BG, (0, 0))
        # draw text
        #TODO draw player score text
        lives_text = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_text = main_font.render(f"Level: {level + 1}", 1, (255,255,255))

        WINDOW.blit(lives_text, (10, 10))
        WINDOW.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            lost_text = lost_font.render("Game Over!", 1, WHITE)
            #TODO print players score and if they got a high score
            WINDOW.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "purple", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0: # left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH: # right
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0: # up
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + 15 < HEIGHT: # down
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_velocity, enemies)

def main_menu():
    title_font = pygame.font.SysFont("Arial", 60)
    start_font = pygame.font.SysFont("Arial", 30)
    author_font = pygame.font.SysFont("Arial", 25)
    run = True
    while run:
        WINDOW.blit(BG, (0, 0))
        start_label = start_font.render("Press the mouse to begin...", 1, WHITE)
        title_label = title_font.render("Interstellar Expedition", 1, WHITE)
        author_label = author_font.render("By: Gerald Monnecka", 1, WHITE)
        WINDOW.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, 500))
        WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 200))
        WINDOW.blit(author_label, (WIDTH / 2 - author_label.get_width() / 2, 300))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
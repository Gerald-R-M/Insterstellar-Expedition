# -------------------------------------------Interstellar Expedition---------------------------------------------------#
# -------------------------------------------Author: Gerald Monnecka---------------------------------------------------#
# ------------------------------------------------Version: 1.00--------------------------------------------------------#
# -----------------------Description: Move your ship with WASD and navigate your way through space!--------------------#
# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

import pygame
import os
import time
import random
from pygame import mixer

mixer.init()

pygame.font.init()

WIDTH = 750
HEIGHT = 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interstellar Expedition")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets/art/red_ship.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets/art/blue_ship.png"))
PURPLE_SPACE_SHIP = pygame.image.load(os.path.join("assets/art/purple_ship.png"))

# Player image
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets/art/player_ship.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets/art/red_laser.png"))
PURPLE_LASER = pygame.image.load(os.path.join("assets/art/purple_laser.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets/art/blue_laser.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets/art/yellow_laser.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/art/background.png")), (WIDTH, HEIGHT))

# Audio
playerlaserSFX = pygame.mixer.Sound("assets/Sound & Music/Player_Laser.ogg")
enemylaserSFX = pygame.mixer.Sound("assets/Sound & Music/Enemy_Laser.ogg")
gameOverSFX = pygame.mixer.Sound("assets/Sound & Music/Game_Over.ogg")
explosionSFX = pygame.mixer.Sound("assets/Sound & Music/Ship_Explosion.ogg")
playerdamageSFX = pygame.mixer.Sound("assets/Sound & Music/Player_Damage.ogg")
lostlifeSFX = pygame.mixer.Sound("assets/Sound & Music/Lost_Life.ogg")

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 100, 0)
DARK_YELLOW = (200, 200, 0)
DARK_RED = (100, 0, 0)


# Global Difficulty Variables
lives = 0
enemy_velocity = 1000
points = 0
# Score tracking variables
score = 0
highscore = 0
# Variable to track if the game has been run once before in the current session
firsttry = True
# Variable to track if the player has beaten their previous high score
newscore = False
# Variable to track which difficulty the player has selected for repeat playthroughs
difficulty = -1 # default: -1, easy: 0, medium: 1, hard: 2

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Arial', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isover(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


# Buttons
easyButton = Button(GREEN, 50, 450, 150, 100, "Easy")
mediumButton = Button(YELLOW, 250, 450, 250, 100, "Medium")
hardButton = Button(RED, 550, 450, 150, 100, "Hard")
rulesButton = Button(PURPLE, 125, 300, 500, 100, "Rules/Controls")
playButton = Button(BLUE, 300, 600, 150, 100, "Play!")
backButton = Button(PURPLE, 75, 600, 600, 75, "Back to Main Menu")

def easymode():
    global lives
    global enemy_velocity
    global points
    global difficulty
    difficulty = 0
    lives = 15
    enemy_velocity = 2
    points = 100
    easyButton.color = DARK_GREEN
    mediumButton.color = YELLOW
    hardButton.color = RED


def mediummode():
    global lives
    global enemy_velocity
    global points
    global difficulty
    difficulty = 1
    lives = 10
    enemy_velocity = 3
    points = 200
    easyButton.color = GREEN
    mediumButton.color = DARK_YELLOW
    hardButton.color = RED


def hardmode():
    global lives
    global enemy_velocity
    global points
    global difficulty
    difficulty = 2
    lives = 5
    enemy_velocity = 4
    points = 300
    easyButton.color = GREEN
    mediumButton.color = YELLOW
    hardButton.color = DARK_RED


def rulescreen():
    run = True
    rules_font = pygame.font.SysFont("Arial", 25)
    rules1 = rules_font.render("You are traveling through space on an expedition when you", 1, WHITE)
    rules2 = rules_font.render("are suddenly under attack from alien lifeforms!", 1, WHITE)
    rules3 = rules_font.render("Take them down without letting too many get past you", 1, WHITE)
    rules4 = rules_font.render("and fly to take over your home planet!", 1, WHITE)
    rules5 = rules_font.render("Use WASD to move your ship!", 1, YELLOW)
    rules6 = rules_font.render("Press the space bar to fire!", 1, YELLOW)
    rules7 = rules_font.render("Watch out for enemy fire if you lose too much health you'll lose!", 1, RED)
    rules8 = rules_font.render("Letting enemies get past you will cost you lives", 1, RED)
    rules9 = rules_font.render("if you run out of lives you lose!", 1, RED)
    rules10 = rules_font.render("Aim to get the high score! You earn more points by", 1, BLUE)
    rules11 = rules_font.render("shooting down ships! The higher the difficulty", 1, BLUE)
    rules12 = rules_font.render("the more points you earn!", 1, BLUE)


    while run:

        WINDOW.blit(BG, (0, 0))
        WINDOW.blit(rules1, (WIDTH / 2 - rules1.get_width() / 2, 100))
        WINDOW.blit(rules2, (WIDTH / 2 - rules2.get_width() / 2, 125))
        WINDOW.blit(rules3, (WIDTH / 2 - rules3.get_width() / 2, 175))
        WINDOW.blit(rules4, (WIDTH / 2 - rules4.get_width() / 2, 200))
        WINDOW.blit(rules5, (WIDTH / 2 - rules5.get_width() / 2, 250))
        WINDOW.blit(rules6, (WIDTH / 2 - rules6.get_width() / 2, 275))
        WINDOW.blit(rules7, (WIDTH / 2 - rules7.get_width() / 2, 325))
        WINDOW.blit(rules8, (WIDTH / 2 - rules8.get_width() / 2, 350))
        WINDOW.blit(rules9, (WIDTH / 2 - rules9.get_width() / 2, 375))
        WINDOW.blit(rules10, (WIDTH / 2 - rules10.get_width() / 2, 425))
        WINDOW.blit(rules11, (WIDTH / 2 - rules11.get_width() / 2, 450))
        WINDOW.blit(rules12, (WIDTH / 2 - rules12.get_width() / 2, 475))

        backButton.draw(WINDOW, WHITE)

        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            if backButton.isover(pos):
                backButton.color = WHITE
            else:
                backButton.color = PURPLE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backButton.isover(pos):
                    run = False


def main_menu():
    title_font = pygame.font.SysFont("Arial", 60)
    author_font = pygame.font.SysFont("Arial", 25)
    selectmode_font = pygame.font.SysFont("Arial", 45)
    run = True
    mixer.music.load("assets/Sound & Music/Main_Menu.ogg")
    mixer.music.set_volume(0.1)
    mixer.music.play()
    modeselected = False
    while run:

        WINDOW.blit(BG, (0, 0))
        title_label = title_font.render("Interstellar Expedition", 1, RED)
        author_label = author_font.render("By: Gerald Monnecka", 1, BLUE)
        selectmode_label = selectmode_font.render("Select a Difficulty!", 1, WHITE)
        easyButton.draw(WINDOW, WHITE)
        mediumButton.draw(WINDOW, WHITE)
        hardButton.draw(WINDOW, WHITE)
        rulesButton.draw(WINDOW, WHITE)
        if modeselected:
            playButton.draw(WINDOW, WHITE)
        else:
            WINDOW.blit(selectmode_label, (WIDTH / 2 - selectmode_label.get_width() / 2, 600))
        WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 100))
        WINDOW.blit(author_label, (WIDTH / 2 - author_label.get_width() / 2, 200))

        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            global lives
            if easyButton.isover(pos):
                easyButton.color = WHITE
            else:
                if lives != 15:
                    easyButton.color = GREEN
                else:
                    easyButton.color = DARK_GREEN
            if mediumButton.isover(pos):
                mediumButton.color = WHITE
            else:
                if lives != 10:
                    mediumButton.color = YELLOW
                else:
                    mediumButton.color = DARK_YELLOW
            if hardButton.isover(pos):
                hardButton.color = WHITE
            else:
                if lives != 5:
                    hardButton.color = RED
                else:
                    hardButton.color = DARK_RED
            if rulesButton.isover(pos):
                rulesButton.color = WHITE
            else:
                rulesButton.color = PURPLE
            if playButton.isover(pos):
                playButton.color = WHITE
            else:
                playButton.color = BLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easyButton.isover(pos):
                    easymode()
                    modeselected = True
                if mediumButton.isover(pos):
                    mediummode()
                    modeselected = True
                if hardButton.isover(pos):
                    hardmode()
                    modeselected = True
                if rulesButton.isover(pos):
                    rulescreen()
                if playButton.isover(pos):
                    pygame.mixer.stop()
                    mixer.music.load("assets/Sound & Music/Game_Music.ogg")
                    mixer.music.set_volume(0.1)
                    mixer.music.play()
                    global score
                    score = 0
                    global points
                    if difficulty == 0:
                        lives = 15
                        points = 100
                    elif difficulty == 1:
                        lives = 10
                        points = 200
                    elif difficulty == 2:
                        lives = 5
                        points = 300
                    main()

    pygame.quit()


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
        return not (height >= self.y >= 0)

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
                if obj.health > 0:
                    playerdamageSFX.set_volume(0.1)
                    playerdamageSFX.play()
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            playerlaserSFX.set_volume(0.1)
            playerlaserSFX.play()
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
                        objdeath = Explosion(obj.x + obj.get_width() / 2, obj.y + obj.get_height() / 2)
                        explosion_group.add(objdeath)
                        explosionSFX.set_volume(0.5)
                        explosionSFX.play()
                        objects.remove(obj)
                        global score
                        score += points
                        global highscore
                        if score > highscore:
                            highscore = score
                            global newscore
                            newscore = True
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, GREEN, (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width() * (self.health / self.max_health),
            10))


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
        if self.cool_down_counter == 0 and self.y > 0:
            enemylaserSFX.set_volume(0.1)
            enemylaserSFX.play()
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        for num in range(1, 6):
            img = pygame.image.load(f"assets/art/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):

        explosion_speed = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


explosion_group = pygame.sprite.Group()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    FPS = 60
    level = 0
    main_font = pygame.font.SysFont("Arial", 25)
    lost_font = pygame.font.SysFont("Arial", 60)
    final_font = pygame.font.SysFont("Arial", 30)
    new_font = pygame.font.SysFont("Arial", 40)
    enemies = []
    wave_length = 5

    player_velocity = 9
    laser_velocity = 9

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WINDOW.blit(BG, (0, 0))
        global lives
        lives_text = main_font.render(f"Lives: {lives}", 1, WHITE)
        level_text = main_font.render(f"Level: {level}", 1, WHITE)
        score_text = main_font.render(f"Score: {score}", 1, WHITE)
        high_text = main_font.render(f"High Score: {highscore}", 1, WHITE)
        WINDOW.blit(lives_text, (10, 10))
        WINDOW.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
        WINDOW.blit(score_text, (10, 40))
        if not firsttry:
            WINDOW.blit(high_text, (10, 70))
            if newscore:
                high_text = main_font.render(f"High Score: {highscore}", 1, YELLOW)
                WINDOW.blit(high_text, (10, 70))

        for enemyobjs in enemies:
            enemyobjs.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            pygame.mixer.music.stop()
            lost_text = lost_font.render("Game Over!", 1, WHITE)
            final_text = final_font.render(f"Your final score was: {score} points",1,WHITE)
            new_text = new_font.render(f"Your new high score is: {highscore}!",1,YELLOW)
            WINDOW.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, 200))
            WINDOW.blit(final_text, (WIDTH / 2 - final_text.get_width() / 2, 300))
            if newscore and not firsttry:
                WINDOW.blit(new_text, (WIDTH / 2 - new_text.get_width() / 2, 400))

        explosion_group.draw(WINDOW)
        explosion_group.update()

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        global lives
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                global firsttry
                firsttry = False
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 3
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "purple", "blue"]))
                enemies.append(enemy)

                for enemy in enemies:
                    for enemy1 in enemies:
                        if collide(enemy, enemy1):
                            enemy.y -= 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0:  # left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH:  # right
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0:  # up
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemydeath = Explosion(enemy.x + enemy.get_width() / 2, enemy.y + enemy.get_height() / 2)
                explosion_group.add(enemydeath)
                explosionSFX.set_volume(0.5)
                explosionSFX.play()
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                lostlifeSFX.set_volume(0.1)
                lostlifeSFX.play()
                enemies.remove(enemy)

        player.move_lasers(-laser_velocity, enemies)



main_menu()

import pygame
import time
import random
from os import path

# Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Settings:
pygame.init()
pygame.mixer.init()  # initialize for sounds
WITDH = 600
HEIGTH = 800
screen = pygame.display.set_mode((WITDH, HEIGTH))
pygame.display.set_caption("Space Shooter !")
clock = pygame.time.Clock()
FPS = 144
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")


# Game Classes

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (120, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = int(WITDH / 2)
        self.rect.bottom = HEIGTH - 20
        self.speed_x = 0
        self.speed = 3
        self.last_bullet_shot = pygame.time.get_ticks()

    def shoot_bullet(self):
        """Create and shoot a bullet when the space is pressed."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_shot > 200:
            self.last_bullet_shot = current_time
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_bullets.add(bullet)
            all_sprites.add(bullet)

    def boundary(self):
        """ Boundary of the ship to the size of the screen"""
        if self.rect.right > WITDH:
            self.rect.right = WITDH
        if self.rect.left < 0:
            self.rect.left = 0

    def movement(self):
        """Ship's movement left and right"""
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_d]:
            self.speed_x = self.speed
        if keystate[pygame.K_a]:
            self.speed_x = -self.speed  # -8 pixels to the left
        if keystate[pygame.K_SPACE]:
            self.shoot_bullet()
        self.rect.x += self.speed_x

    def update(self, *args):
        self.movement()
        self.boundary()


class Meteor(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.meteor_img = meteor_image()
        self.image = random.choice(self.meteor_img)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WITDH - 30)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(1, 3)
        self.speed_x = random.randrange(-3, 3)

    def spawn_new_meteor(self):
        self.rect.x = random.randrange(0, WITDH - 30)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(1, 3)
        self.speed_x = random.randrange(-3, 3)

    def boundary(self):
        if self.rect.left > WITDH + 5 or self.rect.right < -5 or self.rect.top > HEIGTH + 5:
            self.spawn_new_meteor()

    def update(self, *args):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.boundary()


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):  # x and y represent the center of the ship
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(laser_img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = -10

    def update(self, *args):
        self.rect.y += self.speed_y

        if self.rect.bottom < 0:
            self.kill()


# Game Functions
def spawn_new_meteor():
    """Spawn a new meteor"""
    meteor = Meteor()
    all_meteors.add(meteor)
    all_sprites.add(meteor)


def get_image(filename, colorkey=None):
    """Upload and return an image"""
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(colorkey)
    return img


# Images:
background = pygame.image.load(path.join(img_folder, "background.png")).convert()
background_rect = background.get_rect()
player_img = get_image("spaceship.png", BLACK)
laser_img = get_image("laser.png", BLACK)


def meteor_image():
    meteor_img = []  # list to store the meteor images
    for meteor_large_grey_a in range(0, 9):
        img = get_image("large/a1000{}.png".format(meteor_large_grey_a), BLACK)
        meteor_img.append(img)
    for meteor_medium_grey_a in range(0, 9):
        img = get_image("medium/a1000{}.png".format(meteor_medium_grey_a), BLACK)
        meteor_img.append(img)
    for meteor_small_grey_a in range(0, 9):
        img = get_image("small/a1000{}.png".format(meteor_small_grey_a), BLACK)
        meteor_img.append(img)
    return meteor_img


# Game Sprites
all_sprites = pygame.sprite.Group()  # container for ALL the sprites
all_meteors = pygame.sprite.Group()  # Group all the meteors together
all_bullets = pygame.sprite.Group()  # Group all the bullets together
player = Player()
all_sprites.add(player)

for i in range(9):
    """Cretes 9 meteors."""
    spawn_new_meteor()

# Main Game Loop

running = True

while running:

    # Keep the game running at 6144 Fps
    clock.tick(FPS)

    # Check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update:
    all_sprites.update()

    # Check to see if any meteors hit the ship:
    meteor_collision = pygame.sprite.spritecollide(player, all_meteors, False)
    if meteor_collision:
        running = False

    # Check to see if the bullet hits a meteor:
    bullet_collision = pygame.sprite.groupcollide(all_meteors, all_bullets, True, True)
    for collision in bullet_collision:
        spawn_new_meteor()

    # Draw to the screen
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # Update after drawing everything to the screen:
    pygame.display.update()

pygame.quit()

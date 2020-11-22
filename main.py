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
score = 0
font_name = pygame.font.match_font("comicsansms")
DELAY = 300


# Game Classes

class Player(pygame.sprite.Sprite):
    """Attribute for the ship"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (80, 50))
        self.rect = self.image.get_rect()
        self.surface = self.image.get_width()
        self.radius = int(self.surface * .85 / 2)
        # pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.rect.centerx = int(WITDH / 2)
        self.rect.bottom = HEIGTH - 20
        self.speed_x = 0
        self.speed = 3
        self.last_bullet_shot = pygame.time.get_ticks()
        self.health = 100
        self.lives = 3
        self.hide_ship_timer = pygame.time.get_ticks()
        self.ship_is_hidden = False

    def hide_ship(self):
        """move the ship off the screen for a certain time"""
        self.hide_ship_timer = pygame.time.get_ticks()
        self.ship_is_hidden = True
        self.rect.centerx = int(WITDH/2)
        self.rect.y = HEIGTH + 100

    def shoot_bullet(self):
        """Create and shoot a bullet when the space is pressed."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_shot > DELAY:
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
        """Check if the ship is currently off the screen. Respawn after 1.5 seconds."""
        if self.ship_is_hidden and pygame.time.get_ticks() - self.hide_ship_timer > 3500:
            self.ship_is_hidden = False
            self.rect.centerx = int(WITDH/2)
            self.rect.bottom = HEIGTH-10
        self.movement()
        self.boundary()


class Meteor(pygame.sprite.Sprite):
    """Atrtributes for the Meteors"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.meteor_img = get_meteor_images()
        self.original_image = random.choice(self.meteor_img)  # original image use to rotate
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.surface = self.image.get_width()
        self.radius = int(self.surface * .85 / 2)
        self.rect.x = random.randrange(0, WITDH - self.surface)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(1, 3)
        self.speed_x = random.randrange(-3, 3)
        self.last_rotation = pygame.time.get_ticks()  # Keeps travks of time in milliseconds
        self.rotation_degree = 0  # initial degree of rotation
        self.rotation_speed = 5

    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_rotation > 20:
            # rotate the meteor
            self.last_rotation = current_time
            self.rotation_degree += self.rotation_speed
            self.image = pygame.transform.rotate(self.original_image, self.rotation_degree)
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.original_image, self.rotation_degree)
            self.rect = self.image.get_rect()
            # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
            self.rect.center = old_center

    def spawn_new_meteor(self):
        self.rect.x = random.randrange(0, WITDH - self.surface)
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
        self.rotate()


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


class Explosion(pygame.sprite.Sprite):

    def __init__(self, explosion_size, center):
        pygame.sprite.Sprite.__init__(self)
        self.explosion_size = explosion_size
        self.image = self.explosion_size[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_frame = pygame.time.get_ticks()
        self.current_frame = 0

    def update(self, *args):
        """After a certain amount of time, dsipay the next image"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame > 40:
            self.last_frame = current_time
            self.current_frame += 1
            if self.current_frame == len(self.explosion_size):
                """If the frame is egal to the len of the explosion size kill thr goup"""
                self.kill()
            else:
                old_center = self.rect.center
                self.image = self.explosion_size[self.current_frame]
                self.image = pygame.transform.scale(self.image, (200, 200))
                self.rect = self.image.get_rect()
                self.rect.center = old_center


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


def get_meteor_images():
    """
    list to store the meteors images
    :return: a list meteors images
    """
    meteors_sizes = ["large", "medium", "small"]  # list to store the sizes of the meteors
    img_path = "{}/a1000{}.png"
    return [get_image(img_path.format(size, j), BLACK) for size in meteors_sizes for j in range(0, 9)]


def message_to_screen(message, color, font_size, x, y):
    """Display messages to the screen"""
    font = pygame.font.SysFont(font_name, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)


# Explosion images

def laser_explosion():
    """
    When the bullet hits the meteor
    :return: a list of explosion images.
    """
    img_path = "spaceshipexplosionFile/00{}.png"
    return [get_image(img_path.format("0" + str(i)), WHITE) if i <= 9 else get_image(img_path.format(i), WHITE)
            for i in range(1, 28)]


def small_explosion():
    """
    When the meteor hit the ship
    :return: a list of explosion images.
    """
    img_path = "smallexplosionFile/00{}.png"
    return [get_image(img_path.format("0" + str(i)), WHITE) if i <= 9 else get_image(img_path.format(i), WHITE)
            for i in range(1, 12)]


def ship_explosion():
    img_path = "finalexplosionFile/00{}.png"
    return [get_image(img_path.format("0" + str(i)), WHITE) if i <= 9 else get_image(img_path.format(i), WHITE)
            for i in range(1, 79)]


# Images:
background = pygame.image.load(path.join(img_folder, "background.png")).convert()
background_rect = background.get_rect()
player_img = get_image("ships_blue.png", BLACK)
laser_img = get_image("laser_red.png", BLACK)

# Game Sprites
all_sprites = pygame.sprite.Group()  # container for ALL the sprites
all_meteors = pygame.sprite.Group()  # Group all the meteors together
all_bullets = pygame.sprite.Group()  # Group all the bullets together
player = Player()
all_sprites.add(player)

for _ in range(9):
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
    meteor_collision = pygame.sprite.spritecollide(player, all_meteors, True, pygame.sprite.collide_circle)
    for hit in meteor_collision:
        explosion = Explosion(small_explosion(), player.rect.center)
        all_sprites.add(explosion)
        player.health -= hit.radius * 2
        spawn_new_meteor()
        if player.health <= 0:
            final_explosion = Explosion(ship_explosion(), player.rect.center)
            all_sprites.add(final_explosion)
            player.hide_ship()
            player.health = 100
            player.lives -= 1

    # End the game if the player is out of lives and explosion images are done.
    if player.lives == 0 and final_explosion.alive():
        running = False

    # Check to see if the bullet hits a meteor:
    bullet_collision = pygame.sprite.groupcollide(all_meteors, all_bullets, True, True)
    for collision in bullet_collision:  # Collision loop in throw the list bullet_collision
        explosion = Explosion(laser_explosion(), collision.rect.center)
        all_sprites.add(explosion)
        spawn_new_meteor()
        score += 80 - collision.radius

    # Draw to the screen
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    message_to_screen("Score : " + str(score), RED, 24, int(WITDH / 2), 10)
    message_to_screen("Health : " + str(player.health), RED, 24, 50, 10)

    # Update after drawing everything to the screen:
    pygame.display.update()

pygame.quit()

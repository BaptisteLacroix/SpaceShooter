import pygame
import time
import random

# Colors:
WHITE = (255, 255, 255)
BLACk = (0, 0, 0)
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


# Game Classes

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = int(WITDH / 2)
        self.rect.bottom = HEIGTH - 10
        self.speed_x = 0
        self.speed = 3

    def shoot_bullet(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_bullets.add(bullet)
        all_sprites.add(bullet)

    def boundary(self):
        if self.rect.right > WITDH:
            self.rect.right = WITDH
        if self.rect.left < 0:
            self.rect.left = 0

    def movement(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_d]:
            self.speed_x = self.speed
        if keystate[pygame.K_a]:
            self.speed_x = -self.speed  # -8 pixels to the left
        self.rect.x += self.speed_x

    def update(self, *args):
        self.movement()
        self.boundary()


class Meteor(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WITDH - 30)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(1, 3)
        self.speed_x = random.randrange(-3, 3)

    def spawn_new_meteor(self):
        self.rect.x = random.randrange(0, WITDH - 30)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(1, 3 )
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
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = -10

    def update(self, *args):
        self.rect.y += self.speed_y

        if self.rect.bottom < 0:
            self.kill()


# Game Functions


# Game Sprites
all_sprites = pygame.sprite.Group()  # container for ALL the sprites
all_meteors = pygame.sprite.Group()  # Group all the meteors together
all_bullets = pygame.sprite.Group()  # Group all the bullets together
player = Player()
all_sprites.add(player)

for i in range(9):
    """Cretes 9 meteors."""
    meteor = Meteor()
    all_meteors.add(meteor)
    all_sprites.add(meteor)

# Main Game Loop

running = True

while running:

    # Keep the game running at 6144 Fps
    clock.tick(FPS)

    # Check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot_bullet()

    # Update:
    all_sprites.update()

    # Check to see if any meteors hit the ship:
    meteor_collision = pygame.sprite.spritecollide(player, all_meteors, False)
    if meteor_collision:
        running = False

    # Check to see if the bullet hits a meteor:
    bullet_collision = pygame.sprite.groupcollide(all_meteors, all_bullets, True, True)
    for collision in bullet_collision:
        meteor = Meteor
        all_meteors.add(meteor)
        all_sprites.add(meteor)

    # Draw to the screen
    screen.fill(BLACk)
    all_sprites.draw(screen)

    # Update after drawing everything to the screen:
    pygame.display.update()

pygame.quit()

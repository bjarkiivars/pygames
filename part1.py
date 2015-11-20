# coding: latin-1
# If you are commenting in icelandic you need the line above.
import pygame
import random


# If we want to use sprites we create a class that inherits from the Sprite class.
# Each class has an associated image and a rectangle.
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroid_image
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_image
        self.rect = self.image.get_rect()

# Lets load the game images and put them into variables
player_image = pygame.image.load('images/player_pad.png')
asteroid_image = pygame.image.load('images/green_ball.png')
missile_image = pygame.image.load('images/missile.png')
background_image =  pygame.image.load('images/space_background.jpg')

WHITE = (255, 255, 255)

SCORE = 100


pygame.init()

screen_width = 700
screen_height = 483
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
asteroid_list = pygame.sprite.Group()
# Group to hold missiles
missile_list = pygame.sprite.Group()
# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
rangeInt = random.randint(15,50)
for i in range(rangeInt):
    block = Asteroid()
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width - 20)
    block.rect.y = random.randrange(screen_height - 200)  # ekki láta asteroid-ana byrja of neðarlega

    asteroid_list.add(block)
    all_sprites_list.add(block)

# Create a player block
player = Player()
player.rect.x = 320
player.rect.y = 463
player.points = 0

all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0

allGoneOutOfScope = False

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
game_over = False

def isEnemeyVoilatingPlayerSpace(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
          return True
    else:
          return False


# -------- Main Program Loop -----------
# We need to check out what happens when the player hits the space bar in order to "shoot".
# A new missile is created and gets it's initial position in the "middle" of the player.
# Then this missile is added to the missile sprite-group and also to the all_sprites group.
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shot = Missile()
                shot.rect.x = player.rect.x + 30
                shot.rect.y = player.rect.y - 15
                missile_list.add(shot)
                all_sprites_list.add(shot)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        if player.rect.x < -60:
            player.rect.x = 700
        player.rect.x -= 5
    elif key[pygame.K_RIGHT]:
        if player.rect.x > 700:
            player.rect.x = - 60
        player.rect.x += 5

    #screen.fill((0, 0, 0))

    screen.blit(background_image, (0, 0))

    # Below is another good example of Sprite and SpriteGroup functionality.
    # It is now enough to see if some missile has collided with some asteroid
    # and if so, they are removed from their respective groups.
    # In other words:  A missile exploded and so did an asteroid.

    before_total_asteroids = len(asteroid_list)
    # See if the player block has collided with anything.
    pygame.sprite.groupcollide(missile_list, asteroid_list, True, True)
    after_total_asteroids = len(asteroid_list)
    if after_total_asteroids < before_total_asteroids:
        total_killed = before_total_asteroids - after_total_asteroids
        player.points += (SCORE * total_killed)

    # Checking if enemy has collided with the players rectangle
    for enemy in asteroid_list:
        if isEnemeyVoilatingPlayerSpace(enemy.rect.x, enemy.rect.y, player.rect):
            game_over = True

    score_text = 'Score: ' + str(player.points)
    text = font.render(score_text, True, WHITE)
    screen.blit(text, [5,0])

    # Only move and process game logic if the game isn't over.
    if not game_over:
        # Missiles move at a constant speed up the screen, towards the enemy
        for shot in missile_list:
            shot.rect.y -= 5

        # All the enemies move down the screen at a constant speed
        for block in asteroid_list:
            block.rect.y += 1
            if block.rect.y >= screen_height:
                allGoneOutOfScope = True
            else:
                allGoneOutOfScope = False

        if allGoneOutOfScope:
            game_over = True
            
        # Draw all the spites
        all_sprites_list.draw(screen)

    elif game_over:
        # font = pygame.font.Font(None, 36)
        # text = font.render("Hello There", 1, (255, 255, 255))
        # textpos = text.get_rect()
        # textpos.centerx = screen.get_rect().centerx
        # screen.blit(text, textpos)

        #If game over is true, draw game over
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])

    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()




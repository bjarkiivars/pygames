# coding: latin-1
import pygame
import random

# This Demo is based on: Program Arcade Games With Python and Pygame(Chapter 14) 
# Author: Paul Vincent Craven
#  http://programarcadegames.com/index.php?chapter=introduction_to_sprites
# Taken on: 23-10-2014

# Enemy klasinn erfir frá sprite klasanum sem er það rétta í stöðunni ef nota á mikið að
# sprætum í leikjum.  Klasinn er afskaplega einfaldur en fyrir utan að kalla á smiðinn
# í klasanum Sprite setur hann sína png-mynd og nær svo í "surface" til að staðsetja hana á.
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()

# Alveg eins og enemy klasinn nema hvað heitið er Player og myndin er ekki sú sama
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()

# Myndunum load-að og settar í breytur. ATH: Röðin á þessari aðgerð keur EKKI í veg
# fyrir að klasarnir geti notað breyturnar.
player_image = pygame.image.load('images/player_pad.png')
enemy_image = pygame.image.load('images/green_ball.png')

# The white color is used for the background
WHITE = (255, 255, 255)

pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# ---------- ATHUGIÐ,ATTENTION,ACHTUNG,ATTENZIONE:
# Næstu línur af kóða eru mjög mikilvægar.  Hérna er Sprite-klasa afleiddum klösum
# komið fyrir í grúppun.  Þetta er gert til að auðvelda "samskipti" / collision á milli
# Players og hóps af óvinum.
# This is a list of 'sprites' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(50):
    block = Enemy()
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width - 20)
    block.rect.y = random.randrange(screen_height - 20)

    block_list.add(block)
    all_sprites_list.add(block)

# Create a player block
player = Player()
# Setja upphafsstöðu
player.rect.x = 340
player.rect.y = 380
# Playerinn fer í spritegrúppuna sem geymir ALLA spræta(má ekki fara í óvinagrúppuna
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Höfum bara áhuga á að hreyfa playerinn til hægri og vinstri og notum "Wrap around" hegðun.
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        if player.rect.x < -60:
            player.rect.x = 700
        player.rect.x -= 5
    elif key[pygame.K_RIGHT]:
        if player.rect.x > 700:
            player.rect.x = - 60
        player.rect.x += 5

    screen.fill(WHITE)

    # Hérna kikkar Spriteklasinn virkilega inn og nú þurfum við ekki að skrifa
    # langann(og oft ljótan) collision detection kóða. spritecollide skilar dictonary.
    # Eins og þið hafið tekið eftir þá eru óvinirnir "drepnir" með snertingu við playerinn :-)
    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)

    # Allir óvinirnir færast niður skjáinn.
    for block in block_list:
        block.rect.y += 1

    # Check the list of collisions.
    # Score listinn útbúinn og prentaður út
    for block in blocks_hit_list:
        score += 1
        print(score)

    # Draw all the spites
    all_sprites_list.draw(screen)
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
pygame.quit()
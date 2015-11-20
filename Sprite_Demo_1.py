# coding: latin-1
import pygame
import random

# This Demo is based on: Program Arcade Games With Python and Pygame(Chapter 14) 
# Author: Paul Vincent Craven
#  http://programarcadegames.com/index.php?chapter=introduction_to_sprites
# Taken on: 23-10-2014

# Enemy klasinn erfir fr� sprite klasanum sem er �a� r�tta � st��unni ef nota � miki� a�
# spr�tum � leikjum.  Klasinn er afskaplega einfaldur en fyrir utan a� kalla � smi�inn
# � klasanum Sprite setur hann s�na png-mynd og n�r svo � "surface" til a� sta�setja hana �.
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()

# Alveg eins og enemy klasinn nema hva� heiti� er Player og myndin er ekki s� sama
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()

# Myndunum load-a� og settar � breytur. ATH: R��in � �essari a�ger� keur EKKI � veg
# fyrir a� klasarnir geti nota� breyturnar.
player_image = pygame.image.load('images/player_pad.png')
enemy_image = pygame.image.load('images/green_ball.png')

# The white color is used for the background
WHITE = (255, 255, 255)

pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# ---------- ATHUGI�,ATTENTION,ACHTUNG,ATTENZIONE:
# N�stu l�nur af k��a eru mj�g mikilv�gar.  H�rna er Sprite-klasa afleiddum kl�sum
# komi� fyrir � gr�ppun.  �etta er gert til a� au�velda "samskipti" / collision � milli
# Players og h�ps af �vinum.
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
# Setja upphafsst��u
player.rect.x = 340
player.rect.y = 380
# Playerinn fer � spritegr�ppuna sem geymir ALLA spr�ta(m� ekki fara � �vinagr�ppuna
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
    # H�fum bara �huga � a� hreyfa playerinn til h�gri og vinstri og notum "Wrap around" heg�un.
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

    # H�rna kikkar Spriteklasinn virkilega inn og n� �urfum vi� ekki a� skrifa
    # langann(og oft lj�tan) collision detection k��a. spritecollide skilar dictonary.
    # Eins og �i� hafi� teki� eftir �� eru �vinirnir "drepnir" me� snertingu vi� playerinn :-)
    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)

    # Allir �vinirnir f�rast ni�ur skj�inn.
    for block in block_list:
        block.rect.y += 1

    # Check the list of collisions.
    # Score listinn �tb�inn og prenta�ur �t
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
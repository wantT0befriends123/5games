import pygame
from os.path import join

from random import randint

# general setup
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 650
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('space shooter')
running = True

#surface
surf = pygame.Surface((100, 200))
surf.fill('orange')
x = 100

#! ------------------------------- import images ------------------------------ #
#import player image
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

#import star
star = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)] 

#import meteor
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

#import laser
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

direction = 0.1

while running:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw game
    display_surface.fill('darkgray')
    for pos in star_positions:
        display_surface.blit(star, pos)

    if player_rect.right > WINDOW_WIDTH-1:
        direction = -0.1 #go right
    elif player_rect.left < 1:
        direction = 0.1 #go left
    
    player_rect.left += direction #move player

    display_surface.blit(player_surf, player_rect) #display player
    display_surface.blit(meteor_surf, meteor_rect) #display meteor
    display_surface.blit(laser_surf, laser_rect) #display laser
    
    pygame.display.update()

pygame.quit()
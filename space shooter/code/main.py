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

#import player image
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (0,0))

star = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)] 

while running:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw game
    display_surface.fill('darkgray')
    for pos in star_positions:
        display_surface.blit(star, pos)

    display_surface.blit(player_surf, player_rect)
    pygame.display.update()

pygame.quit()
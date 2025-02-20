import pygame

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
player_surf = pygame.image.load('images/player.png')

while running:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw game
    display_surface.fill('darkgray')
    x += 1
    display_surface.blit(player_surf, (x, 150))
    pygame.display.update()

pygame.quit()
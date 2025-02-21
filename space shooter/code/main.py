import pygame
from os.path import join

from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha() #import image
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) #center player
        self.direction = pygame.math.Vector2() #direction as vector
        self.speed = 300 #speed
    
    def update(self, dt): #update player
        # pygame.mouse.get_pos() # of no use rn
        keys = pygame.key.get_pressed() # get all keys presed
        self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) # set x direction
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP]) #set y direction
        self.direction = self.direction.normalize() if self.direction else self.direction # normalize vector (prevent diagonal speedy boi)
        self.rect.center += self.direction * self.speed * dt # move player

        recent_keys = pygame.key.get_just_pressed() # get new key presses
        if recent_keys[pygame.K_SPACE]:
            print('fire laser') #TODO: fire laser

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

#! ------------------------------- general setup ------------------------------ #
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 900, 600 # window size
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('space shooter') # set caption
running = True # game loop
clock = pygame.time.Clock() # clock

# surface (test + useless)
# surf = pygame.Surface((100, 200))
# surf.fill('orange')
# x = 100

all_sprites = pygame.sprite.Group() # sprite group

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha() # import star image
for i in range(20): # add 20 stars
    Star(all_sprites, star_surf)
player = Player(all_sprites) # add player


#! ------------------------------- import images ------------------------------ #

#import meteor
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

#import laser
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

while running:
    dt = clock.tick() / 1000 # synce framerate

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update all sprites
    all_sprites.update(dt)

    # draw game
    display_surface.fill('darkgray')

    # draw all sprites
    all_sprites.draw(display_surface)

    # update display
    pygame.display.update()

pygame.quit()
import pygame
from os.path import join

from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha() #import image
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) #center player
        self.direction = pygame.math.Vector2() #direction as vector
        self.speed = 300 #speed

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 100

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self, dt): #update player
        # pygame.mouse.get_pos() # of no use rn
        keys = pygame.key.get_pressed() # get all keys presed
        self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) # set x direction
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP]) #set y direction
        self.direction = self.direction.normalize() if self.direction else self.direction # normalize vector (prevent diagonal speedy boi)
        self.rect.center += self.direction * self.speed * dt # move player

        recent_keys = pygame.key.get_just_pressed() # get new key presses
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 500

    def update(self, dt):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 2000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

#! ------------------------------- general setup ------------------------------ #
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 # window size
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('space shooter') # set caption
running = True # game loop
clock = pygame.time.Clock() # clock

# surface (test + useless)
# surf = pygame.Surface((100, 200))
# surf.fill('orange')
# x = 100

#! SPRITE GROUPS
all_sprites = pygame.sprite.Group() # sprite group
meteor_sprites = pygame.sprite.Group() # meteor group


#! IMPORT IMAGES
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha() # import laser image
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha() # import star image

for i in range(20): # add 20 stars
    Star(star_surf, all_sprites)
player = Player(all_sprites) # add player

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000 # synce framerate

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event. type == meteor_event:
            Meteor(meteor_surf, (randint(0, WINDOW_WIDTH), 0), (all_sprites, meteor_sprites))

    # update
    all_sprites.update(dt)
    meteor_sprites.update(dt)

    # draw game
    display_surface.fill('darkgray')
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
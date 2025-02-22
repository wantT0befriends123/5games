import pygame
from os.path import join

from random import randint, uniform
import random

#! ---------------------------------- classes --------------------------------- #

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha() #import image
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) #center player
        self.direction = pygame.math.Vector2() #direction as vector
        self.speed = 500 #speed

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

        # mask
        self.mask = pygame.mask.from_surface(self.image)

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
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
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

        self.original_surf = surf
        self.rotation_speed = random.choice([randint(-50,-20), randint(20,50)])
        self.rotation = 0
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
#! --------------------------------- functions -------------------------------- #

def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True,  (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)

    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20, 10).move(0, -8), 5, 10)

#! ------------------------------- general setup ------------------------------ #
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 # window size
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('space shooter') # set caption
running = True # game loop
clock = pygame.time.Clock() # clock

#! IMPORT
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha() # import laser image
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha() # import star image
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40) # font
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

#! SPRITES
all_sprites = pygame.sprite.Group() # sprite group
meteor_sprites = pygame.sprite.Group() # meteor group
laser_sprites = pygame.sprite.Group() # laser group

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

    #collisions
    collisions()

    # draw game
    display_surface.fill('#3a2e3f')
    display_score()
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()
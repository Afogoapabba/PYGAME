
from re import T
from sys import exit
from random import randint, choice
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Intro/graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Intro/graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Intro/graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('Intro/audio/jump.mp3')
        self.jump_sound.set_volume(0.1)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load('Intro/graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('Intro/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('Intro/graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('Intro/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(str(current_time), True, ('green'))
    score_rect = score_surf.get_rect(center=(350, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        return obstacle_list
    else:
        return []


def collision_check():
    if pygame.sprite.spritecollide(player.sprite, obstacles,False):
        return False
    else:
        return True

def player_animation():
    global player_index , player_surf

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.15
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_font = pygame.font.Font('Intro/font/Pixeltype.ttf', 50)  # Remove leading slash
game_active = True
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('Intro/audio/music.wav')
bg_music.set_volume(0.1)
# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacles = pygame.sprite.Group()


sky_surf = pygame.image.load('Intro/graphics/Sky.png').convert()
ground_surf = pygame.image.load('Intro/graphics/ground.png').convert()
# Obstacles


# Intro screen
player_stand = pygame.image.load('Intro/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)  # Scaled
player_stand_rect = player_stand.get_rect(center=(400, 200))
game_message = game_font.render('Press SPACE to start!', False, ('black'))
game_message_rect = game_message.get_rect(center=(400, 350))

game_name = game_font.render('Pixel Runner', False, ('green'))
game_name_rect = game_name.get_rect(center=(400, 100))

#  timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


#  event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    game_active = False
                    pygame.quit()
                    exit()
            # Obstacle spawn
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

 



    if game_active:
        bg_music.play(loops=-1)
        #  Background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()
        # score
        score = display_score()
# Collision

        game_active = collision_check() ################################################


# # Score
        display_score()
    else:
        # obstacle_rect_list.clear()
        obstacles.empty()
        player_gravity = 0
        score_message = game_font.render(f'Your score:{score} ', True, ('yellow'))
        score_message_rect = score_message.get_rect(center=(400, 50))
        # game over screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
        screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(60)


from re import T
from sys import exit
from random import randint, choice
import pygame
from player import Player
from obstacle import Obstacle


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
channel = pygame.mixer.Channel(0)
channel.set_volume(0.1)
channel.play(bg_music, loops=-1)


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

        game_active = collision_check() 


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

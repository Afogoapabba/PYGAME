
from sys import exit
import pygame


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = game_font.render(str(current_time), True, ('green'))
    score_rect = score_surface.get_rect(center=(350, 50))
    screen.blit(score_surface, score_rect)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_font = pygame.font.Font(
    'Intro/font/Pixeltype.ttf', 50)  # Remove leading slash
game_active = True
start_time = 0

sky_surface = pygame.image.load('Intro/graphics/Sky.png').convert()
ground_surface = pygame.image.load('Intro/graphics/ground.png').convert()

snail_surface = pygame.image.load(
    'Intro/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomleft=(600, 300))

player_surface = pygame.image.load(
    'Intro/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load(
    'Intro/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)  # Scaled
player_stand_rect = player_stand.get_rect(center=(400, 200))
game_message = game_font.render(
    'Press SPACE to start!', True, ('black'))
game_message_rect = game_message.get_rect(center=(400, 300))
game_name_rect = game_message.get_rect(center=(450, 100))
game_name = game_font.render('Pixel Runner', True, ('green'))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -7

                if event.key == pygame.K_ESCAPE:
                    game_active = False
                    pygame.quit()
                    exit()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        #  Background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
# Collision
        if player_rect.colliderect(snail_rect):
            game_active = False
            snail_rect.left = 800

# Player
        player_gravity += 0.2
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)
# Snail
        snail_rect.x -= 6
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)
        display_score()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_message, game_message_rect)
        screen.blit(game_name, game_name_rect)
    pygame.display.update()
    clock.tick(60)

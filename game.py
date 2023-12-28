
from sys import exit
import pygame


def display_score():
    current_time = pygame.time.get_ticks()
    score_surface = test_font.render(str(current_time), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(288, 50))
    screen.blit(score_surface, score_rect)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Intro/font/Pixeltype.ttf', 50)  # Remove leading slash
game_active = True

sky_surface = pygame.image.load('Intro/graphics/Sky.png').convert()
ground_surface = pygame.image.load('Intro/graphics/ground.png').convert()

snail_surface = pygame.image.load(
    'Intro/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomleft=(600, 300))

player_surface = pygame.image.load(
    'Intro/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))

    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    player_gravity += 0.2
    player_rect.y += player_gravity

    if player_rect.bottom >= 300:
        player_rect.bottom = 300

    display_score()

    pygame.display.update()
    clock.tick(60)

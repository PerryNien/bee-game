# To run this game, you need to have pygame installed: pip install pygame
# Then, you can run this file: python main.py
#
# I was unable to download the images for the game. I have used colored rectangles as placeholders.
# You can replace the placeholder graphics with your own images.
# To do this, you will need to load the images using pygame.image.load() and then draw them to the screen instead of the rectangles.

import pygame
import sys
import random

# Initialize Pygame
pygame.init()
mixer_initialized = False
try:
    pygame.mixer.init()
    mixer_initialized = True
except pygame.error:
    print("No audio device found, sounds will be disabled.")

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Player
player_img = pygame.image.load('assets/bee.png')
player_img = pygame.transform.scale(player_img, (50, 50))
player_rect = player_img.get_rect(center=(screen_width / 2, screen_height - 50))
player_speed = 5

# Bullet
bullet_size = 10
bullet_speed = 10
bullets = []

# Enemy
enemy_img = pygame.image.load('assets/honeycomb.png')
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
enemy_speed = 2
enemies = []
enemy_spawn_rate = 60  # Lower is faster
enemy_spawn_counter = 0

# Score
score = 0
font = pygame.font.Font(None, 36)

# Sound
if mixer_initialized:
    laser_sound = pygame.mixer.Sound('assets/laser-312360.mp3')
    explosion_sound = pygame.mixer.Sound('assets/explosion-312361.mp3')

# Game state
game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_rect.x + player_rect.width / 2 - bullet_size / 2
                bullet_y = player_rect.y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_size, bullet_size))
                if mixer_initialized:
                    laser_sound.play()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.x > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.x < screen_width - player_rect.width:
            player_rect.x += player_speed

        # Enemy spawning
        enemy_spawn_counter += 1
        if enemy_spawn_counter >= enemy_spawn_rate:
            enemy_spawn_counter = 0
            enemy_rect = enemy_img.get_rect()
            enemy_rect.x = random.randint(0, screen_width - enemy_rect.width)
            enemy_rect.y = -enemy_rect.height
            enemies.append(enemy_rect)

        # Movement
        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > screen_height:
                enemies.remove(enemy)

        # Collision detection
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    if mixer_initialized:
                        explosion_sound.play()
                    break

        for enemy in enemies:
            if player_rect.colliderect(enemy):
                if mixer_initialized:
                    explosion_sound.play()
                game_over = True
                break

    # Drawing
    screen.fill(black)
    screen.blit(player_img, player_rect)
    for bullet in bullets:
        pygame.draw.rect(screen, white, bullet)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    # Score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Game Over
    if game_over:
        game_over_text = font.render("Game Over", True, white)
        text_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(game_over_text, text_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

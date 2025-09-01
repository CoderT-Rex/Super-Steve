import sys
import pygame
import random
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from shot import Shot

def show_menu(screen, font):
    screen.fill("black")
    
    # Retro arcade style title with glow effect
    title_font = pygame.font.Font(None, 96)
    title_text = "SUPER STEVE"
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2 - 100
    
    # Create glow effect by drawing multiple outlines
    glow_colors = [(64, 0, 128), (128, 0, 255), (0, 255, 255)]  # Purple to cyan glow
    for i, color in enumerate(glow_colors):
        for dx in range(-3 + i, 4 - i):
            for dy in range(-3 + i, 4 - i):
                if dx != 0 or dy != 0:
                    glow_text = title_font.render(title_text, True, color)
                    glow_rect = glow_text.get_rect()
                    glow_rect.center = (center_x + dx, center_y + dy)
                    screen.blit(glow_text, glow_rect)
    
    # Draw main text on top
    main_text = title_font.render(title_text, True, "white")
    main_rect = main_text.get_rect()
    main_rect.center = (center_x, center_y)
    screen.blit(main_text, main_rect)
    
    # Display instructions
    instruction_text = font.render("Press 1 to start a new game", True, "white")
    instruction_rect = instruction_text.get_rect()
    instruction_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    screen.blit(instruction_text, instruction_rect)
    
    quit_text = font.render("Press 2 to quit", True, "white")
    quit_rect = quit_text.get_rect()
    quit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140)
    screen.blit(quit_text, quit_rect)
    
    pygame.display.flip()

def reset_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Shot.containers = (shots, updatable, drawable)

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    return updatable, drawable, asteroids, shots, player, asteroid_field

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    death_messages = [
        "Ran out of Monster Energy Drinks",
        "Should've studied more!",
        "Got 689 when you needed 700",
        "You failed ITF+?? That's for Babies!",
        "Need to do more flashcards",
        "Get on TryHackMe!",
        "Back to Jason Dion!",
        "Subnetting is hard.",
        "What's port 22 again?"
    ]
    
    game_state = "menu"  # "menu" or "playing"
    score = 0
    lives = 3
    death_message = ""
    message_timer = 0
    game_over_timer = 0
    
    updatable, drawable, asteroids, shots, player, asteroid_field = reset_game()
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_state = "playing"
                        score = 0
                        lives = 3
                        game_over_timer = 0
                        message_timer = 0
                        updatable, drawable, asteroids, shots, player, asteroid_field = reset_game()
                    elif event.key == pygame.K_2:
                        return
        
        if game_state == "menu":
            show_menu(screen, font)
        elif game_state == "playing":
            if message_timer > 0:
                message_timer -= dt
            
            if game_over_timer > 0:
                game_over_timer -= dt
                if game_over_timer <= 0:
                    game_state = "menu"
            
            if game_over_timer <= 0:
                updatable.update(dt)
            
            for asteroid in asteroids:
                if asteroid.collision(player):
                    lives -= 1
                    player.position.x = SCREEN_WIDTH / 2
                    player.position.y = SCREEN_HEIGHT / 2
                    player.rotation = 0
                    # Show random death message
                    death_message = random.choice(death_messages)
                    message_timer = 3.0  # Show message for 3 seconds
                    # Clear all asteroids when player loses a life
                    for asteroid_to_clear in asteroids:
                        asteroid_to_clear.kill()
                    if lives <= 0:
                        death_message = "Ran out of Vouchers!"
                        message_timer = 3.0
                        game_over_timer = 3.0
                    break

            for shot in shots:
                for asteroid in asteroids:
                    if asteroid.collision(shot):
                        shot.kill()
                        asteroid.split()
                        score += 5

            screen.fill("black")

            for obj in drawable:
                obj.draw(screen)
            
            score_text = font.render(f"Salary: ${score}", True, "white")
            score_rect = score_text.get_rect()
            score_rect.topright = (SCREEN_WIDTH - 10, 10)
            screen.blit(score_text, score_rect)
            
            lives_text = font.render(f"Vouchers: {lives}", True, "white")
            lives_rect = lives_text.get_rect()
            lives_rect.topleft = (10, 10)
            screen.blit(lives_text, lives_rect)
            
            # Display death message if active
            if message_timer > 0:
                message_text = font.render(death_message, True, "red")
                message_rect = message_text.get_rect()
                message_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                # Add black background for better readability
                bg_rect = message_rect.inflate(20, 10)
                pygame.draw.rect(screen, "black", bg_rect)
                pygame.draw.rect(screen, "white", bg_rect, 2)
                screen.blit(message_text, message_rect)

            pygame.display.flip()
        else:
            pygame.display.flip()
        
        dt = clock.tick(60)/1000

    print("Game Over")


if __name__ == "__main__":
    main()



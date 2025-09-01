import sys
import pygame
import random
import math
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
    
    # Display instructions - find the widest text to align all options
    option1_text = "Press 1 to start a new game"
    option2_text = "Press 2 to view high scores"
    option3_text = "Press 3 to quit"
    
    # Calculate alignment based on the longest text
    temp_text1 = font.render(option1_text, True, "white")
    temp_text2 = font.render(option2_text, True, "white")
    temp_text3 = font.render(option3_text, True, "white")
    
    max_width = max(temp_text1.get_width(), temp_text2.get_width(), temp_text3.get_width())
    left_align_x = (SCREEN_WIDTH - max_width) // 2
    
    instruction_text = font.render(option1_text, True, "white")
    instruction_rect = instruction_text.get_rect()
    instruction_rect.x = left_align_x
    instruction_rect.y = SCREEN_HEIGHT // 2 + 80
    screen.blit(instruction_text, instruction_rect)
    
    highscore_text = font.render(option2_text, True, "white")
    highscore_rect = highscore_text.get_rect()
    highscore_rect.x = left_align_x
    highscore_rect.y = SCREEN_HEIGHT // 2 + 120
    screen.blit(highscore_text, highscore_rect)
    
    quit_text = font.render(option3_text, True, "white")
    quit_rect = quit_text.get_rect()
    quit_rect.x = left_align_x
    quit_rect.y = SCREEN_HEIGHT // 2 + 160
    screen.blit(quit_text, quit_rect)
    
    pygame.display.flip()

def show_highscores(screen, font, high_scores):
    screen.fill("black")
    
    # Title
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("HIGH SCORES", True, "yellow")
    title_rect = title_text.get_rect()
    title_rect.center = (SCREEN_WIDTH // 2, 80)
    screen.blit(title_text, title_rect)
    
    # Display scores
    start_y = 150
    for i, (name, score) in enumerate(high_scores):
        score_text = font.render(f"{i+1:2d}. {name}: ${score:,}", True, "white")
        score_rect = score_text.get_rect()
        score_rect.centerx = SCREEN_WIDTH // 2
        score_rect.y = start_y + (i * 40)
        screen.blit(score_text, score_rect)
    
    # Instructions
    instruction_text = font.render("Press ESC to return to menu", True, "white")
    instruction_rect = instruction_text.get_rect()
    instruction_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()

def check_high_score(score, high_scores):
    """Check if score qualifies for high score board"""
    if len(high_scores) < 10:
        return True
    return score > high_scores[-1][1]

def add_high_score(name, score, high_scores):
    """Add new high score and keep list sorted"""
    high_scores.append((name, score))
    high_scores.sort(key=lambda x: x[1], reverse=True)
    if len(high_scores) > 10:
        high_scores.pop()

def show_name_entry(screen, font, score, current_name):
    screen.fill("black")
    
    # Title
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("NEW HIGH SCORE!", True, "yellow")
    title_rect = title_text.get_rect()
    title_rect.center = (SCREEN_WIDTH // 2, 150)
    screen.blit(title_text, title_rect)
    
    # Score
    score_text = font.render(f"Your Salary: ${score:,}", True, "white")
    score_rect = score_text.get_rect()
    score_rect.center = (SCREEN_WIDTH // 2, 220)
    screen.blit(score_text, score_rect)
    
    # Name entry
    name_prompt = font.render("Enter your name:", True, "white")
    name_rect = name_prompt.get_rect()
    name_rect.center = (SCREEN_WIDTH // 2, 280)
    screen.blit(name_prompt, name_rect)
    
    name_display = font.render(current_name + "_", True, "cyan")
    name_display_rect = name_display.get_rect()
    name_display_rect.center = (SCREEN_WIDTH // 2, 320)
    screen.blit(name_display, name_display_rect)
    
    # Instructions
    instruction_text = font.render("Press ENTER when done", True, "white")
    instruction_rect = instruction_text.get_rect()
    instruction_rect.center = (SCREEN_WIDTH // 2, 400)
    screen.blit(instruction_text, instruction_rect)
    
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
    
    # High score leaderboard
    high_scores = [
        ("Mike Chapel", 100000),
        ("Jason Dion", 90000),
        ("Professor Messer", 80000),
        ("Indian YouTube Guy", 75000),
        ("Luis Candelario", 50000),
        ("Kris Torres", 25000),
        ("Eli Hause", 20000),
        ("Brennan White", 15000),
        ("Jose Rico", 10000),
        ("Herminio Paez", 1)
    ]
    
    game_state = "menu"  # "menu", "playing", "highscores", or "name_entry"
    score = 0
    lives = 3
    death_message = ""
    message_timer = 0
    game_over_timer = 0
    player_name = ""
    total_time = 0  # For color cycling
    
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
                        game_state = "highscores"
                    elif event.key == pygame.K_3:
                        return
            elif game_state == "highscores":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"
            elif game_state == "name_entry":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name.strip():
                            add_high_score(player_name.strip(), score, high_scores)
                        game_state = "menu"
                        player_name = ""
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.unicode.isprintable() and len(player_name) < 20:
                        player_name += event.unicode
        
        if game_state == "menu":
            show_menu(screen, font)
        elif game_state == "highscores":
            show_highscores(screen, font, high_scores)
        elif game_state == "name_entry":
            show_name_entry(screen, font, score, player_name)
        elif game_state == "playing":
            total_time += dt
            
            if message_timer > 0:
                message_timer -= dt
            
            if game_over_timer > 0:
                game_over_timer -= dt
                if game_over_timer <= 0:
                    if check_high_score(score, high_scores):
                        game_state = "name_entry"
                    else:
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
                # Create neon glow effect with color cycling and pulsing
                center_x = player.position.x
                center_y = player.position.y - 80
                
                # Color cycling - cycle through hues over time
                hue_cycle = (total_time * 60) % 360  # Complete cycle every 6 seconds
                
                # Pulsing intensity - varies brightness
                pulse = (math.sin(total_time * 8) + 1) / 2  # Pulse between 0 and 1
                base_intensity = 0.7 + (pulse * 0.3)  # Between 0.7 and 1.0
                
                # Convert HSV to RGB for cycling colors
                def hsv_to_rgb(h, s, v):
                    h = h / 360.0
                    i = int(h * 6.0)
                    f = h * 6.0 - i
                    p = v * (1.0 - s)
                    q = v * (1.0 - s * f)
                    t = v * (1.0 - s * (1.0 - f))
                    i = i % 6
                    
                    if i == 0: r, g, b = v, t, p
                    elif i == 1: r, g, b = q, v, p
                    elif i == 2: r, g, b = p, v, t
                    elif i == 3: r, g, b = p, q, v
                    elif i == 4: r, g, b = t, p, v
                    elif i == 5: r, g, b = v, p, q
                    
                    return (int(r * 255), int(g * 255), int(b * 255))
                
                # Generate colors with varying intensities
                bright_color = hsv_to_rgb(hue_cycle, 1.0, base_intensity)
                glow_colors = [
                    hsv_to_rgb(hue_cycle, 1.0, base_intensity * 0.3),
                    hsv_to_rgb(hue_cycle, 1.0, base_intensity * 0.6),
                    hsv_to_rgb(hue_cycle, 1.0, base_intensity * 0.8)
                ]
                
                # Draw multiple outlines for glow effect
                for i, color in enumerate(glow_colors):
                    for dx in range(-2 + i, 3 - i):
                        for dy in range(-2 + i, 3 - i):
                            if dx != 0 or dy != 0:
                                outline_text = font.render(death_message, True, color)
                                outline_rect = outline_text.get_rect()
                                outline_rect.center = (center_x + dx, center_y + dy)
                                screen.blit(outline_text, outline_rect)
                
                # Draw bright main text on top
                main_text = font.render(death_message, True, bright_color)
                main_rect = main_text.get_rect()
                main_rect.center = (center_x, center_y)
                screen.blit(main_text, main_rect)

            pygame.display.flip()
        else:
            pygame.display.flip()
        
        dt = clock.tick(60)/1000

    print("Game Over")


if __name__ == "__main__":
    main()



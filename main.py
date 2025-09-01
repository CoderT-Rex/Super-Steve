import sys
import pygame
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import *
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    score = 0
    lives = 3

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

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        
        for asteroid in asteroids:
            if asteroid.collision(player):
                lives -= 1
                player.position.x = SCREEN_WIDTH / 2
                player.position.y = SCREEN_HEIGHT / 2
                player.rotation = 0
                if lives <= 0:
                    print("Game over!")
                    sys.exit()
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

        pygame.display.flip()
        
        dt = clock.tick(60)/1000

    print("Game Over")


if __name__ == "__main__":
    main()



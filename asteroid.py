from circleshape import CircleShape
import pygame
from constants import ASTEROID_MIN_RADIUS
import random

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        asteroid_num = random.randint(1, 10)
        self.original_image = pygame.image.load(f"asteroid{asteroid_num}.png").convert_alpha()
        scale_factor = (radius * 2) / max(self.original_image.get_width(), self.original_image.get_height())
        new_size = (int(self.original_image.get_width() * scale_factor), 
                    int(self.original_image.get_height() * scale_factor))
        self.original_image = pygame.transform.scale(self.original_image, new_size)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-100, 100)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, self.rotation)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)

    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rotation += self.rotation_speed * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2

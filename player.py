import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from shot import Shot

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.original_image = pygame.image.load("SuperSteve.png").convert_alpha()
        scale_factor = (PLAYER_RADIUS * 2) / max(self.original_image.get_width(), self.original_image.get_height())
        new_size = (int(self.original_image.get_width() * scale_factor), 
                    int(self.original_image.get_height() * scale_factor))
        self.original_image = pygame.transform.scale(self.original_image, new_size)
        self.image = self.original_image

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -self.rotation)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)   
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        
    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

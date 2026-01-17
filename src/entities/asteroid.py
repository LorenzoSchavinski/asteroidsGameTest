import pygame
from .circleshape import CircleShape
from ..config.constants import *
from ..utils.logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), self.radius, LINE_WIDTH)
        
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20,50)
            firstSplitDireciton = self.velocity.rotate(angle)
            secondSplitDireciton = self.velocity.rotate(-angle)
            newRadius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, newRadius)
            asteroid1.velocity = firstSplitDireciton * 1.2
            asteroid2 = Asteroid(self.position.x, self.position.y, newRadius)
            asteroid2.velocity = secondSplitDireciton * 1.2

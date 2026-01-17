import pygame
from ..config.constants import *
from ..entities.player import Player
from ..utils.logger import *
from ..entities.asteroid import Asteroid
from ..entities.asteroidfield import AsteroidField
import sys
from ..entities.shot import Shot 




def main():
    print("Starting Asteroids with pygame version: VERSION")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}" )
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Shot.containers = (drawable, updatable, shots)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    gameloop(screen, clock, dt, updatable, drawable, asteroids, shots, player)



    
def gameloop(screen, clock, dt, updatable, drawable, asteroids, shots, player): 
    while True:
        log_state()
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        drawGame(screen, drawable)
        checkDeath(asteroids, player)
        checkShotCollision(asteroids, shots)
        pygame.display.flip()
        dt = clock.tick(60)/1000.0
        #print(dt)


def drawGame(screen, drawable):
    for sprite in drawable:
        sprite.draw(screen)

def checkDeath(asteroids,player):
    for asteroid in asteroids:
        if asteroid.collides_with(player):
            log_event("Player hit")
            print("Game over!")
            sys.exit()

def checkShotCollision(asteroids, shots):
    for shot in shots:
        for asteroid in asteroids:
            if asteroid.collides_with(shot):
                log_event("asteroid_shot")
                shot.kill()
                asteroid.split()




if __name__ == "__main__":
    main()

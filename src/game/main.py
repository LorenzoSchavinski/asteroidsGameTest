import pygame
from ..config.constants import *
from ..entities.player import Player
from ..utils.logger import *
from ..entities.asteroid import Asteroid
from ..entities.asteroidfield import AsteroidField
import sys
from ..entities.shot import Shot 


startMenu = True
dt = 0
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
    gameloop(screen, clock, dt, updatable, drawable, asteroids, shots, player, startMenu)


def draw_text(text,font,text_col, x,y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def gameloop(screen, clock, dt, updatable, drawable, asteroids, shots, player, startMenu):
    buttonSelect = 0
    while startMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if buttonSelect == 1:
                        sys.exit()
                    startMenu = False
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    buttonSelect = 1 - buttonSelect
                    
        screen.fill("black")
        gameTitle(screen)
        button(screen)
        if buttonSelect == 0:
            pygame.draw.rect(screen, "yellow", (SCREEN_WIDTH* 1/2-50 , SCREEN_HEIGHT* 1/2-50, 125, 50), LINE_WIDTH)
        else:
            pygame.draw.rect(screen, "yellow", (SCREEN_WIDTH* 1/2-50 , SCREEN_HEIGHT* 1/2+50, 125, 50), LINE_WIDTH)
        pygame.display.flip()

    while True:
        log_state()
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        drawGame(screen, drawable)
        draw_text(f"Score: {player.score}", pygame.font.Font(None, 36), (255,255,255), 10, 10, screen)
        checkDeath(asteroids, player, screen)
        checkShotCollision(asteroids, shots, player)
        pygame.display.flip()
        dt = clock.tick(60)/1000.0
        #print(dt)


def gameTitle(screen):
    screen.fill("black")
    draw_text("Asteroid Game", pygame.font.Font(None, 60), (255,255,255), SCREEN_WIDTH* 1/2 - 130, SCREEN_HEIGHT* (1/8), screen)

def drawGame(screen, drawable):
    for sprite in drawable:
        sprite.draw(screen)

def checkDeath(asteroids,player, screen):
    for asteroid in asteroids:
        if asteroid.collides_with(player):
            log_event("Player hit")
            print("Game over!")
            print("Score :", player.score)
            endScreen(screen, player)

def endScreen(screen, player):
    screen.fill("black")
    draw_text("Game Over", pygame.font.Font(None, 60), (255,255,255), SCREEN_WIDTH* 1/2 - 100, SCREEN_HEIGHT* (1/8), screen)
    draw_text(f"Score: {player.score}", pygame.font.Font(None, 60), (255,255,255), SCREEN_WIDTH* 1/2 - 75, SCREEN_HEIGHT* 1/4, screen)
    draw_text("Press Space to Continue", pygame.font.Font(None, 45), (255,255,255), SCREEN_WIDTH* 1/2 -150 , SCREEN_HEIGHT* (1/2), screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #startMenu = True
                    main()


def checkShotCollision(asteroids, shots, player):
    for shot in shots:
        for asteroid in asteroids:
            if asteroid.collides_with(shot):
                log_event("asteroid_shot")
                shot.kill()
                player.score += asteroid.split()
                
def button(screen):
    start_coordinates = (SCREEN_WIDTH* 1/2-50 , SCREEN_HEIGHT* 1/2-50)
    end_coordinates = (SCREEN_WIDTH* 1/2-50 , SCREEN_HEIGHT* 1/2+50)
    start = pygame.Rect(start_coordinates, (125, 50))
    end = pygame.Rect(end_coordinates, (125, 50))
    pygame.draw.rect(screen, "white", start, LINE_WIDTH)
    draw_text("Start", pygame.font.Font(None, 36), (255,255,255),start_coordinates[0] + +35, start_coordinates[1] + 15, screen)
    pygame.draw.rect(screen, "white", end, LINE_WIDTH)
    draw_text("End", pygame.font.Font(None, 36), (255,255,255), end_coordinates[0] + 40, end_coordinates[1] + 15, screen)

    



if __name__ == "__main__":
    main()

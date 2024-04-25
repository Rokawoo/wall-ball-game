"""
Game: Ball and Paddle Bounce Game
Description: A Pygame-based game where the player controls a paddle to bounce a ball to prevent it from hitting a boundary. 
For detailed information, refer to the readme.txt file.

Author: Roka		
Development Period: May 7, 2023 - May 16, 2023
"""

import os
import random
import pygame
from Ball import Ball
from Paddle import Paddle
from Text import Text
from Boundary import Boundary

pygame.init()
pygame.mixer.init()

# Functions
def random_direction():
    return random.choice([-1, 1])

def trail(parent_ball, trail_ball, distance):
    x, y = parent_ball.get_loc()
    speedX = parent_ball.get_speedX()
    speedY = parent_ball.get_speedY()
    if speedX >= 0 and speedY >= 0:
        trail_ball.set_loc((x - distance, y - distance))
    elif speedX > 0 and speedY < 0:
        trail_ball.set_loc((x - distance, y + distance))
    elif speedX < 0 and speedY > 0:
        trail_ball.set_loc((x + distance, y - distance))
    elif speedX < 0 and speedY < 0:
        trail_ball.set_loc((x + distance, y + distance))
    trail_ball.draw(surface)

def ball_color_randomizer():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    ball.set_color((r, g, b))
    r, g, b = max(r - 100, 10), max(g - 100, 10), max(b - 100, 10)
    trailBall.set_color((r, g, b))
    r, g, b = max(r - 50, 1), max(g - 50, 1), max(b - 50, 1)
    trailBall2.set_color((r, g, b))

def draw_all():
    ball.draw(surface)
    paddle.draw(surface)
    boundary.draw(surface)
    scoreBoard.draw(surface)
    healthBoard.draw(surface)
    speedBoard.draw(surface)

def update_boards():
    scoreBoard.set_message(f"Score: {numHits}")
    healthBoard.set_message(f"Health: {health}")
    speedBoard.set_message(f"Speed: {abs(ball.get_speedX()):.2f}")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
grey = (150, 150, 150)
darkGrey = (75, 75, 75)

# Sounds
SOUND_PATH = 'Sounds'
bgMusic = pygame.mixer.Sound(os.path.join(SOUND_PATH, "bgMusic.MP3"))
pauseMusic = pygame.mixer.Sound(os.path.join(SOUND_PATH, "pauseMusic.MP3"))
meowSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "meow.MP3"))
bounceSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "bounce.MP3"))
hurtSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "lose.MP3"))
winSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "win.MP3"))
byeSound = pygame.mixer.Sound(os.path.join(SOUND_PATH, "bye.MP3"))

# Game Objects
surfaceWidth = 800
surfaceHeight = 600
surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))

paddle = Paddle(100, 15, white)
boundary = Boundary(0, 800, 10, red)
ball = Ball(400, 250, 15, white)

trailBall = Ball(ball.get_loc()[0], ball.get_loc()[1], 15, grey)
trailBall2 = Ball(ball.get_loc()[0], ball.get_loc()[1], 15, darkGrey)

scoreBoard = Text("Score: 0", 10, 60)
speedBoard = Text("Speed: 10", 10, 35)
healthBoard = Text("Health: 3", 10, 10)

# Messages
startMessage = Text("Press SPACE to Start", 280, 300)
pauseMessage = Text("Press SPACE to Continue", 245, 300)
quitMessage = Text("Press SPACE to Quit", 275, 300)
instructionMessage = Text("Get 30!!", 350, 275)
winMessage = Text("You Win!", 350, 275)
loseMessage = Text("You Lose", 350, 275)

# Game State
numHits = 0
health = 3

if __name__ == "__main__":
    meowSound.play(0)
    
    start = True
    lose = False
    win = False
    paused = True
    pauseMusicPlay = True
    running = True
    fpsClock = pygame.time.Clock()

    while running:
        surface.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if paused:
                    start = False
                    pauseMusic.stop()
                    winSound.stop()
                    bgMusic.play(-1)
                    pauseMusicPlay = False
                    paused = not lose and not paused
                    if lose:
                        pauseMusicPlay = True
                        running = False
        
        if paused:
            bgMusic.stop()
            if not pauseMusicPlay:
                if win:
                    winSound.play(0)
                else:
                    pauseMusic.play(-1)
                pauseMusicPlay = True
            
            if start:
                instructionMessage.draw(surface)
                startMessage.draw(surface)
                ball.set_speedX(ball.get_speedX() * random_direction())
                ball.set_speedY(ball.get_speedY() * random_direction())
            elif win:
                winMessage.draw(surface)
                pauseMessage.draw(surface)
            elif lose:
                loseMessage.draw(surface)
                quitMessage.draw(surface)
            else:
                pauseMessage.draw(surface)
            
            draw_all()
        
        else:      
            if ball.intersects(paddle):
                numHits += 1
                ball.set_speedY(-ball.get_speedY())
                ball.set_speedX(ball.get_speedX() * 1.05)
                ball.set_speedY(ball.get_speedY() * 1.05)
                update_boards()
                bounceSound.play(0)

            if ball.intersects(boundary):
                paused = True
                health -= 1
                ball.set_color(white)
                trailBall.set_color(grey)
                trailBall2.set_color(darkGrey)
                if health > 0:
                    numHits -= 5
                    if numHits < 0:
                        numHits = 0
                    ball.set_loc((396, 50))
                    ball.set_speedX(ball.get_speedX() / 1.15927 * random_direction())
                    ball.set_speedY(ball.get_speedY() / 1.15927)
                    if abs(ball.get_speedX()) < 10:
                        ball.set_speedX(10 * random_direction())
                    ball.set_speedY(10)
                    update_boards()
                hurtSound.play(0)

            if numHits >= 6:
                trail(ball, trailBall, -6)
            if numHits >= 12:
                trail(ball, trailBall2, 1)
                ball_color_randomizer()
            
            if numHits == 20:
                win = True
                paused = True
                
            if health <= 0:
                lose = True
                paused = True
                
            ball.move()
            draw_all()
        
        pygame.display.update()
        fpsClock.tick(30)
    
    bgMusic.stop()
    byeSound.play(0)
    pygame.time.delay(800)
    pygame.quit()
    exit()
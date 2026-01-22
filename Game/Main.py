"""Ball and Paddle Bounce Game - Optimized"""

import os
import sys
import random
import asyncio
import pygame

from Ball import Ball
from Text import Text

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (150, 150, 150)
DARK_GREY = (75, 75, 75)
BLACK = (0, 0, 0)

# Window chrome
TITLE_BAR_GREY = (45, 45, 45)
BORDER_GREY = (60, 60, 60)
BTN_CLOSE = (232, 77, 61)
BTN_MIN = (227, 187, 55)
BTN_MAX = (43, 185, 59)

# Game constants
GAME_W, GAME_H = 800, 600
TITLE_H, BORDER = 32, 1
WIN_W = GAME_W + BORDER * 2
WIN_H = GAME_H + TITLE_H + BORDER * 2
GAME_X, GAME_Y = BORDER, TITLE_H + BORDER

PADDLE_W, PADDLE_H, PADDLE_Y = 100, 15, 555
BOUND_H = 10
BOUND_Y = GAME_H - BOUND_H
BALL_R = 15

WIN_SCORE = 30
INIT_SPEED = 10
SPEED_MULT = 1.05
SPEED_DIV = 1.15927


async def main():
    pygame.init()
    
    if sys.platform == "emscripten":
        sound_path = "/data/data/game/assets/Sounds/"
    else:
        try:
            sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sounds") + os.sep
        except:
            sound_path = "Game/Sounds/"
    
    surface = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Wall and Ball")
    game_surf = pygame.Surface((GAME_W, GAME_H))
    
    pygame.mixer.init()
    
    # Pre-render title bar elements
    try:
        title_font = pygame.font.SysFont('Consolas', 16)
    except:
        title_font = pygame.font.Font(None, 20)
    title_text = title_font.render("C:\\Games\\WallAndBall.exe", True, (180, 180, 180))
    title_pos = ((WIN_W - title_text.get_width()) // 2, (TITLE_H - title_text.get_height()) // 1.5)
    btn_y = TITLE_H // 2
    
    current_music = None
    
    def play_audio(filename, loop=False):
        nonlocal current_music
        try:
            pygame.mixer.music.load(sound_path + filename)
            pygame.mixer.music.play(-1 if loop else 0)
            current_music = filename
        except Exception as e:
            print(f"Audio error ({filename}): {e}")
    
    def stop_audio():
        nonlocal current_music
        try:
            pygame.mixer.music.stop()
            current_music = None
        except:
            pass
    
    def play_effect(filename):
        nonlocal current_music
        try:
            pygame.mixer.music.load(sound_path + filename)
            pygame.mixer.music.play(0)
            current_music = filename
        except Exception as e:
            print(f"Effect error ({filename}): {e}")
    
    # Game objects
    paddle_rect = pygame.Rect((GAME_W - PADDLE_W) // 2, PADDLE_Y, PADDLE_W, PADDLE_H)
    bound_rect = pygame.Rect(0, BOUND_Y, GAME_W, BOUND_H)
    
    ball = Ball(400, 250, BALL_R, WHITE)
    trail1 = Ball(400, 250, BALL_R, GREY)
    trail2 = Ball(400, 250, BALL_R, DARK_GREY)
    
    # UI elements
    score_txt = Text("Score: 0", 10, 60)
    speed_txt = Text("Speed: 10", 10, 35)
    health_txt = Text("Health: 3", 10, 10)
    
    click_msg = Text("Click to Start", 320, 300)
    start_msg = Text("Press SPACE to Start", 280, 320)
    pause_msg = Text("Press SPACE to Continue", 245, 300)
    restart_msg = Text("Press SPACE to Restart", 265, 320)
    instr_msg = Text("Get 30!!", 350, 280)
    win_msg = Text("You Win!", 350, 280)
    lose_msg = Text("You Lose", 350, 280)
    
    # State
    hits = health = 0
    start = lose = win = paused = pause_music = audio_unlocked = False
    
    def rand_dir():
        return random.choice((-1, 1))
    
    def update_ui():
        score_txt.set_message(f"Score: {hits}")
        health_txt.set_message(f"Health: {health}")
        speed_txt.set_message(f"Speed: {abs(ball.get_speedX()):.2f}")
    
    def reset_colors():
        ball.set_color(WHITE)
        trail1.set_color(GREY)
        trail2.set_color(DARK_GREY)
    
    def rand_colors():
        r, g, b = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        ball.set_color((r, g, b))
        trail1.set_color((max(r - 100, 10), max(g - 100, 10), max(b - 100, 10)))
        trail2.set_color((max(r - 150, 1), max(g - 150, 1), max(b - 150, 1)))
    
    def reset_game():
        nonlocal hits, health, start, lose, win, paused, pause_music
        hits, health = 0, 3
        start, paused, pause_music = True, True, True
        lose, win = False, False
        ball.set_loc((400, 250))
        ball.set_speedX(INIT_SPEED)
        ball.set_speedY(INIT_SPEED)
        reset_colors()
        update_ui()
        stop_audio()
    
    def draw_chrome():
        surface.fill(BLACK)
        pygame.draw.rect(surface, TITLE_BAR_GREY, (0, 0, WIN_W, TITLE_H))
        pygame.draw.line(surface, BORDER_GREY, (0, TITLE_H), (WIN_W, TITLE_H), 1)
        pygame.draw.circle(surface, BTN_CLOSE, (12, btn_y), 6)
        pygame.draw.circle(surface, BTN_MIN, (32, btn_y), 6)
        pygame.draw.circle(surface, BTN_MAX, (52, btn_y), 6)
        surface.blit(title_text, title_pos)
    
    def update_paddle():
        paddle_rect.x = max(0, min(pygame.mouse.get_pos()[0] - GAME_X - PADDLE_W // 2, GAME_W - PADDLE_W))
    
    def draw_trail(parent, t, dist):
        px, py = parent.get_loc()
        sx, sy = parent.get_speedX(), parent.get_speedY()
        t.set_loc((px + (dist if sx < 0 else -dist), py + (dist if sy < 0 else -dist)))
        t.draw(game_surf)
    
    def ball_hits_paddle():
        bx, by = ball.get_loc()
        return pygame.Rect(bx - BALL_R, by - BALL_R, BALL_R * 2, BALL_R * 2).colliderect(paddle_rect) and ball.get_speedY() > 0
    
    def ball_hits_bound():
        return ball.get_loc()[1] + BALL_R >= BOUND_Y
    
    def draw_game():
        ball.draw(game_surf)
        update_paddle()
        pygame.draw.rect(game_surf, WHITE, paddle_rect)
        pygame.draw.rect(game_surf, RED, bound_rect)
        score_txt.draw(game_surf)
        health_txt.draw(game_surf)
        speed_txt.draw(game_surf)
    
    # Initialize state
    reset_game()
    audio_unlocked = False
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        draw_chrome()
        game_surf.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and not audio_unlocked:
                audio_unlocked = True
                play_effect("meow.mp3")
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and paused and audio_unlocked:
                if lose or win:
                    reset_game()
                    continue
                start = False
                stop_audio()
                play_audio("bgMusic.mp3", loop=True)
                pause_music = False
                paused = False
        
        if not running:
            break
        
        if not audio_unlocked:
            click_msg.draw(game_surf)
            draw_game()
        
        elif paused:
            if current_music == "bgMusic.mp3":
                stop_audio()
            
            if not pause_music:
                play_effect("win.mp3") if win else play_audio("pauseMusic.mp3", loop=True)
                pause_music = True
            
            if start:
                instr_msg.draw(game_surf)
                start_msg.draw(game_surf)
                ball.set_speedX(ball.get_speedX() * rand_dir())
                ball.set_speedY(ball.get_speedY() * rand_dir())
            elif win:
                win_msg.draw(game_surf)
                restart_msg.draw(game_surf)
            elif lose:
                lose_msg.draw(game_surf)
                restart_msg.draw(game_surf)
            else:
                pause_msg.draw(game_surf)
            
            draw_game()
        
        else:
            if ball_hits_paddle():
                hits += 1
                ball.set_speedY(-abs(ball.get_speedY()))
                ball.set_speedX(ball.get_speedX() * SPEED_MULT)
                ball.set_speedY(ball.get_speedY() * SPEED_MULT)
                ball.set_loc((ball.get_loc()[0], PADDLE_Y - 16))
                update_ui()
            
            if ball_hits_bound():
                paused = True
                health -= 1
                reset_colors()
                
                if health > 0:
                    hits = max(0, hits - 5)
                    ball.set_loc((396, 50))
                    spd = max(INIT_SPEED, abs(ball.get_speedX()) / SPEED_DIV)
                    ball.set_speedX(spd * rand_dir())
                    ball.set_speedY(INIT_SPEED)
                    update_ui()
                
                play_effect("lose.mp3")
            
            if hits >= 6:
                draw_trail(ball, trail1, -6)
            if hits >= 12:
                draw_trail(ball, trail2, 1)
                rand_colors()
            
            if hits >= WIN_SCORE:
                win, paused = True, True
            
            if health <= 0:
                lose, paused = True, True
            
            ball.move()
            draw_game()
        
        surface.blit(game_surf, (GAME_X, GAME_Y))
        pygame.display.update()
        clock.tick(30)
        await asyncio.sleep(0)
    
    pygame.quit()

asyncio.run(main())
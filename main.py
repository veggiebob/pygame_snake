import pygame, sys, text, random
from snake import *
from pygame.locals import *
pygame.init()

on = not 0
off = not 1


GAME_STATE = {
    'items': on,
    'growing': on,
    'speeding': on,
    'players': 1
}



WIDTH = 400
HEIGHT = 400
MINIMUM_WIDTH = 165
MINIMUM_HEIGHT = 115
TILE_DIM = 20
SNAKE_BORDER = 0.1 # 10%
def getCheckerboard (box, dims, color1=(255, 255, 255), color2=(0, 0, 0)):
    surf = pygame.Surface((box.w, box.h))
    bx = box.w/dims[0]
    by = box.h/dims[1]
    dbx = int(bx)+1
    dby = int(by)+1
    for i in range(dims[1]):
        for j in range(dims[0]):
            pygame.draw.rect(
                surf,
                color1 if i%2==j%2 else color2,
                (j * bx, i * by, dbx, dby),
                0
            )
    return surf
def ij_to_board_loc (i, j):
    global VIEW_BOX, BOX_SIZE
    return [VIEW_BOX.x + j * TILE_SIZE, VIEW_BOX.y + i * TILE_SIZE]
def doSetup ():
    global MIN_DIM, BORDER, BOX_SIZE, TILE_SIZE, DISPLAY, VIEW_BOX, CHECKERBOARD, cherry_display, cherries, scissors, scissors_display
    MIN_DIM = min(WIDTH, HEIGHT)
    BORDER = MIN_DIM * 0.05
    BOX_SIZE = MIN_DIM - BORDER * 2
    TILE_SIZE = BOX_SIZE / TILE_DIM
    VIEW_BOX = pygame.Rect(WIDTH/2-BOX_SIZE/2, HEIGHT/2-BOX_SIZE/2, BOX_SIZE, BOX_SIZE)
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    CHECKERBOARD = getCheckerboard(VIEW_BOX, [TILE_DIM, TILE_DIM], (0, 200, 200), (50, 230, 230))
    cherry_display = pygame.transform.scale(cherries, (int(TILE_SIZE), int(TILE_SIZE)))
    scissors_display = pygame.transform.scale(scissors, (int(TILE_SIZE), int(TILE_SIZE)))

pygame.display.set_caption("Snake")

DVORAK = True
arrow_keys = [[K_UP, K_LEFT, K_DOWN, K_RIGHT]]
number_keys = [[K_KP8, K_KP4, K_KP5, K_KP6]]
keySetups = arrow_keys + number_keys
if DVORAK:
    keySetups += [
        [K_COMMA, K_a, K_o, K_e],
    ]
else:
    keySetups += [
        [K_w, K_a, K_s, K_d]
    ]
fps = 120
game_clock = pygame.time.Clock()
txt = text.Text()
cherries = pygame.image.load('cherries.png')
cherry_display = pygame.Surface((cherries.get_width(), cherries.get_height()))
cherry_display.blit(cherries, (0, 0))
scissors = pygame.image.load('scissors.png')
scissors_display = pygame.Surface((scissors.get_width(), scissors.get_height()))
scissors_display.blit(scissors, (0, 0))

def gen_fruit():
    global fruit
    fruit.append([random.randint(0, TILE_DIM-1), random.randint(0, TILE_DIM-1)])
    for f in fruit:
        for fr in fruit:
            if f[0]==fr[0] and f[1]==fr[1] and f!=fr:
                fruit.remove(fr)
                break
def gen_cut():
    global cuts
    cuts.append([random.randint(0, TILE_DIM-1), random.randint(0, TILE_DIM-1)])
    for c in cuts:
        for cc in cuts:
            if c[0]==cc[0] and c[1]==cc[1] and c!=cc:
                cuts.remove(cc)
                break

def reset_game ():
    global game_update_frames, game_update_timer, snakes, paused, game_over, fruit, cut_update_frames, game_time, cherries, DISPLAY, cuts, fips
    DISPLAY.fill((255, 255, 255))
    game_update_frames = fps / 4  # wait how many frames before updating snake
    cut_update_frames = fps * 10 # number of frames per fruit generation
    game_time = 0 # game time in frames
    game_update_timer = 0 # timer for updating scren
    snakes = [Snake([0, i]) for i in range(GAME_STATE['players'])]
    fruit = []
    cuts = []
    paused = True
    game_over = False
    for _ in range(GAME_STATE['players']):
        gen_fruit()
        gen_cut()

doSetup()
reset_game()
while True:
    keys_pressed = []
    for e in pygame.event.get():
        if e.type==MOUSEBUTTONDOWN:
            print(WIDTH, HEIGHT)
            if game_over:
                reset_game()
                paused = False
            else:
                paused = not paused
                if not paused:
                    game_update_timer = 0
        elif e.type==KEYDOWN:
            k = e.key
            for i in range(GAME_STATE['players']):
                keys = keySetups[i]
                s = snakes[i]
                if k == keys[0]:
                    s.set_direction(0)
                elif k == keys[1]:
                    s.set_direction(1)
                elif k == keys[2]:
                    s.set_direction(2)
                elif k == keys[3]:
                    s.set_direction(3)
        elif e.type==VIDEORESIZE:
            WIDTH = max(e.w, MINIMUM_WIDTH)
            HEIGHT = max(e.h, MINIMUM_HEIGHT)
            doSetup()
            DISPLAY.fill((255, 255, 255), (0, 0, WIDTH, HEIGHT))
            game_update_timer = 0
        # elif e.type==VIDEOEXPOSE:
        #     print('hi')
        elif e.type==QUIT:
            pygame.quit()
            sys.exit()
    if not game_over:
        if game_update_timer%game_update_frames == 0 and not paused:
            pygame.draw.rect(DISPLAY, (200, 200, 200), VIEW_BOX)
            DISPLAY.blit(CHECKERBOARD, VIEW_BOX)
            iindex = -1
            all_dead = True
            add_fruit = False
            for snake in snakes:
                iindex += 1
                snake.move()
                h = snake.get_head()
                if h[0] < 0 or h[1] < 0 or h[0] >= TILE_DIM or h[1] >= TILE_DIM:
                    snake.die()
                fi = -1
                for f in fruit:
                    fi += 1
                    if h[0] == f[0] and h[1] == f[1]:
                        snake.eat_fruit(GAME_STATE['growing'])
                        fruit.remove(f)
                        add_fruit = True
                        if GAME_STATE['speeding']:
                            game_update_frames = max(int(game_update_frames*(0.9 + random.randint(0, 20)/20 * 0.1)), 1)
                            print('speed is now %d'%game_update_frames)
                if GAME_STATE['items']:
                    fi = -1
                    for c in cuts:
                        fi += 1
                        if h[0] == c[0] and h[1] == c[1]:
                            snake.cut()
                            cuts.remove(c)

                for s in snake.path:
                    p = ij_to_board_loc(s[0], s[1])
                    pygame.draw.rect(DISPLAY, (0, 100, 50),
                         (
                             p[0] + SNAKE_BORDER * TILE_SIZE,
                             p[1] + SNAKE_BORDER * TILE_SIZE,
                             TILE_SIZE - TILE_SIZE * SNAKE_BORDER * 2,
                             TILE_SIZE - TILE_SIZE * SNAKE_BORDER * 2
                         ), 0)

                if not snake.dead:
                    all_dead = not 1

            for snake in snakes:
                for s in snakes:
                    if s.check_bump_into(snake):
                        s.die()
                        if snake.check_bump_into(s):
                            snake.die()

            if all_dead:
                game_over = True
            if add_fruit:
                gen_fruit()
            for f in fruit:
                p = ij_to_board_loc(f[0], f[1])
                DISPLAY.blit(cherry_display, p)
            if GAME_STATE['items']:
                for c in cuts:
                    p = ij_to_board_loc(c[0], c[1])
                    DISPLAY.blit(scissors_display, p)

        if paused:
            txt.drawToSurface(DISPLAY, (WIDTH/2, HEIGHT/2), "||", 60, (200, 200, 200))

        if game_time % cut_update_frames == 0:
            gen_cut()
    else:
        DISPLAY.fill((200, 200, 200))
        txt.drawToSurface(DISPLAY, (WIDTH/2, HEIGHT/2), "GAME OVER", 60, (255, 0, 0))
    pygame.display.update()
    game_clock.tick(fps)
    game_update_timer += 1
    if not paused:
        game_time += 1

import random
import time
import sys
import pygame
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 800
BOARDSIZE = 20
BOARDWIDTH = 15
BOARDHEIGHT = 30
BLANK = '.'

MOVESIDEFREQ = 0.2
MOVEDOWNFREQ = 0.2

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOARDSIZE) / 600)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOARDSIZE) - 5

WHITE       = (255, 255, 255)
GGREEN      = ( 88, 100,   0)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
ORANGE      = (255, 140,   0)
LIGHTORANGE = (255, 165,   0)
GRAY        = (169, 169, 169)
LIGHTGRAY   = (211, 211, 211)
YELLOW      = (255, 215,   0)
LIGHTYELLOW = (255, 255,   0)
PINK        = (255,  20, 147)
LIGHTPINK   = (255, 105, 180)
BROWN       = (139,  69,  19)
LIGHTBROWN  = (160,  82,  45)

BOARDCOLOR  = GGREEN
BGCOLOR     = BLACK
TEXTCOLOR   = WHITE
COLORS      = (     BLUE,      BROWN,      GREEN,      PINK,     GRAY,      RED,      ORANGE,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTBROWN, LIGHTGREEN, LIGHTPINK,LIGHTGRAY, LIGHTRED, LIGHTORANGE, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS)

TEMPLATEWIDTH = 4
TEMPLATEHEIGHT = 4

INSTRUCTION1 = ('Press r for restart.')
INSTRUCTION2 = ('Press p for pause.')
INSTRUCTION3 = ('Press left, down, and right for move.')
INSTRUCTION4 = ('Press up for rotate.')
INSTRUCTION5 = ('Press space for end fall.')
INSTRUCTION6 = ('Press escape for quite.')
INSTRUCTION7 = ('Press m for mute.')
INSTRUCTION8 = ('Press n for unmute.')

SHAPE1 = [['.....',
           '.....',
           '.OO..',
           '.OO..',
           '.....']]

SHAPE2 = [['.....',
           '.....',
           '..OO.',
           '.OO..',
           '.....'],
          ['.....',
           '..O..',
           '..OO.',
           '...O.',
           '.....']]

SHAPE3 = [['.....',
           '.....',
           '.OO..',
           '..OO.',
           '.....'],
          ['.....',
           '..O..',
           '.OO..',
           '.O...',
           '.....']]

SHAPE4 = [['..O..',
           '..O..',
           '..O..',
           '..O..',
           '.....'],
          ['.....',
           '.....',
           'OOOO.',
           '.....',
           '.....']]

SHAPE5 = [['.....',
           '.O...',
           '.OOO.',
           '.....',
           '.....'],
          ['.....',
           '..OO.',
           '..O..',
           '..O..',
           '.....'],
          ['.....',
           '.....',
           '.OOO.',
           '...O.',
           '.....'],
          ['.....',
           '..O..',
           '..O..',
           '.OO..',
           '.....']]

SHAPE6 = [['.....',
           '...O.',
           '.OOO.',
           '.....',
           '.....'],
          ['.....',
           '..O..',
           '..O..',
           '..OO.',
           '.....'],
          ['.....',
           '.....',
           '.OOO.',
           '.O...',
           '.....'],
          ['.....',
           '.OO..',
           '..O..',
           '..O..',
           '.....']]

SHAPE7 = [['.....',
           '..O..',
           '.OOO.',
           '.....',
           '.....'],
          ['.....',
           '..O..',
           '..OO.',
           '..O..',
           '.....'],
          ['.....',
           '.....',
           '.OOO.',
           '..O..',
           '.....'],
          ['.....',
           '..O..',
           '.OO..',
           '..O..',
           '.....']]

BLOCKS = {'ONE'  : SHAPE1,
          'TWO'  : SHAPE2,
          'THREE': SHAPE3,
          'FOUR' : SHAPE4,
          'FIVE' : SHAPE5,
          'SIX'  : SHAPE6,
          'SEVEN': SHAPE7}

def main():
    global BASICFONT, BIGFONT, DISPLAYSURF, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 15)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 50)
    pygame.display.set_caption('TETRIS PUZZLE')

    show_text_screen('TETRIS PUZZLE')
    while True: 
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('kahoot.mp3')
        else:
            pygame.mixer.music.load('kahoot.mp3')
        pygame.mixer.music.play(-1, 0)
        run_game()
        pygame.mixer.music.stop()
        DISPLAYSURF.fill(BGCOLOR)
        show_text_screen('Game Over')

def run_game():
    board = get_blank_board()
    last_move_down_time = time.time()
    last_move_side_time = time.time()
    last_fall_time = time.time()
    moving_down = False 
    moving_left = False
    moving_right = False
    point = 0
    level, fall_freq = calc_level_and_fall_freq(point)

    falling_block = get_new_block()
    next_block = get_new_block()

    while True: 
        if falling_block == None:
            falling_block = next_block
            next_block = get_new_block()
            last_fall_time = time.time() 

            if not valid_position(board, falling_block):
                return 

        check_for_quit()
        for event in pygame.event.get(): 
            if event.type == KEYUP:
                if event.key == K_p:
                    pygame.mixer.music.stop()
                    show_text_screen(' ') 
                    pygame.mixer.music.play(-1, 0.0)           
                elif event.key == K_r:
                    board = []
                    for i in range(BOARDWIDTH):
                        board.append([BLANK] * BOARDHEIGHT)
                    run_game()
                elif event.key == K_m:
                    pygame.mixer.music.stop()
                elif event.key == K_n:
                    pygame.mixer.music.play()
                elif event.key == K_LEFT:
                    moving_left = False
                elif event.key == K_RIGHT:
                    moving_right = False
                elif event.key == K_DOWN:
                    moving_down = False

            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and valid_position(board, falling_block, adj_x=-1):
                    falling_block['x'] -= 1
                    moving_left = True
                    moving_right = False
                    last_move_side_time = time.time()

                elif (event.key == K_RIGHT) and valid_position(board, falling_block, adj_x=1):
                    falling_block['x'] += 1
                    moving_right = True
                    moving_left = False
                    last_move_side_time = time.time()

                elif (event.key == K_UP):
                    falling_block['rotation'] = (falling_block['rotation'] + 1) % len(BLOCKS[falling_block['shape']])
                    if not valid_position(board, falling_block):
                        falling_block['rotation'] = (falling_block['rotation'] - 1) % len(BLOCKS[falling_block['shape']])

                elif (event.key == K_DOWN):
                    moving_down = True
                    if valid_position(board, falling_block, adj_y=1):
                        falling_block['y'] += 1
                    last_move_down_time = time.time()

                elif event.key == K_SPACE:
                    moving_down = False
                    moving_left = False
                    moving_right = False
                    for i in range(1, BOARDHEIGHT):
                        if not valid_position(board, falling_block, adj_y=i):
                            break
                    falling_block['y'] += i - 1

        if (moving_left or moving_right) and time.time() - last_move_side_time > MOVESIDEFREQ:
            if moving_left and valid_position(board, falling_block, adj_x=-1):
                falling_block['x'] -= 1
            elif moving_right and valid_position(board, falling_block, adj_x=1):
                falling_block['x'] += 1
            last_move_side_time = time.time()

        if moving_down and time.time() - last_move_down_time > MOVEDOWNFREQ and valid_position(board, falling_block, adj_y=1):
            falling_block['y'] += 1
            last_move_down_time = time.time()

        if time.time() - last_fall_time > fall_freq:
            if not valid_position(board, falling_block, adj_y=1):
                add_to_board(board, falling_block)
                point += (remove_lines(board)*2)
                level, fall_freq = calc_level_and_fall_freq(point)
                falling_block = None
            else:
                falling_block['y'] += 1
                last_fall_time = time.time()

        DISPLAYSURF.fill(BGCOLOR)
        draw_board(board)
        draw_status(point, level)
        draw_next_block(next_block)
        if falling_block != None:
            draw_block(falling_block)
        instruction()
        
        pygame.display.update()
        FPSCLOCK.tick()

def instruction():
    instruction_surf = BASICFONT.render(INSTRUCTION1, True, TEXTCOLOR)
    instruction_rect = instruction_surf.get_rect()
    instruction_rect.topleft = (WINDOWWIDTH - 290, 200) 
    DISPLAYSURF.blit(instruction_surf, instruction_rect)

    instruction_surf = BASICFONT.render(INSTRUCTION2, True, TEXTCOLOR)
    instruction_rect = instruction_surf.get_rect()
    instruction_rect.topleft = (WINDOWWIDTH - 290, 230) 
    DISPLAYSURF.blit(instruction_surf, instruction_rect)

    instruction_surf = BASICFONT.render(INSTRUCTION3, True, TEXTCOLOR)
    instruction_rect = instruction_surf.get_rect()
    instruction_rect.topleft = (WINDOWWIDTH - 290, 260) 
    DISPLAYSURF.blit(instruction_surf, instruction_rect)

    instruction_surf = BASICFONT.render(INSTRUCTION4, True, TEXTCOLOR)
    instruction_rect = instruction_surf.get_rect()
    instruction_rect.topleft = (WINDOWWIDTH - 290, 290) 
    DISPLAYSURF.blit(instruction_surf, instruction_rect)

    instruction_surf = BASICFONT.render(INSTRUCTION5, True, TEXTCOLOR)
    instruction_rect = instruction_surf.get_rect()
    instruction_rect.topleft = (WINDOWWIDTH - 290, 320) 
    DISPLAYSURF.blit(instruction_surf, instruction_rect)

    instruction_surf = BASICFONT.render(INSTRUCTION6, True, TEXTCOLOR)
    instruction_rect = instruction_surf.get_rect()
    instruction_rect.topleft = (WINDOWWIDTH - 290, 350) 
    DISPLAYSURF.blit(instruction_surf, instruction_rect)

    instruction_surf = BASICFONT.render(INSTRUCTION7, True, TEXTCOLOR)
    instruction_rect = instruction_surf.get_rect()
    instruction_rect.topleft = (WINDOWWIDTH - 290, 380) 
    DISPLAYSURF.blit(instruction_surf, instruction_rect)

    instruction_surf = BASICFONT.render(INSTRUCTION8, True, TEXTCOLOR)
    instruction_rect = instruction_surf.get_rect()
    instruction_rect.topleft = (WINDOWWIDTH - 290, 410) 
    DISPLAYSURF.blit(instruction_surf, instruction_rect)
    
def make_text_objs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def check_for_key_press():
    check_for_quit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def show_text_screen(text):
    title_surf, title_rect = make_text_objs(text, BIGFONT, TEXTCOLOR)
    title_rect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(title_surf, title_rect)

    while check_for_key_press() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def check_for_quit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate() 
        pygame.event.post(event) 

def calc_level_and_fall_freq(point):
    level = int(point / 15) + 1
    fall_freq = 0.30 - (level * 0.02)
    return level, fall_freq

def get_new_block():
    shape = random.choice(list(BLOCKS.keys()))
    new_block = {'shape': shape,
                'rotation': random.randint(0, len(BLOCKS[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, 
                'color': random.randint(0, len(COLORS)-1)}
    return new_block

def add_to_board(board, block):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if BLOCKS[block['shape']][block['rotation']][y][x] != BLANK:
                board[x + block['x']][y + block['y']] = block['color']

def get_blank_board():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def on_board(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def valid_position(board, block, adj_x=0, adj_y=0):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            above_board = y + block['y'] + adj_y < 0
            if above_board or BLOCKS[block['shape']][block['rotation']][y][x] == BLANK:
                continue
            if not on_board(x + block['x'] + adj_x, y + block['y'] + adj_y):
                return False
            if board[x + block['x'] + adj_x][y + block['y'] + adj_y] != BLANK:
                return False
    return True

def complete_line(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def remove_lines(board):
    num_lines_removed = 0
    y = BOARDHEIGHT - 1 
    while y >= 0:
        if complete_line(board, y):
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pull_down_y] = board[x][pull_down_y-1]
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            num_lines_removed += 1
        else:
            y -= 1
    return num_lines_removed
       
def convert_pixel_coords(box_x, box_y):
    return (XMARGIN + (box_x * BOARDSIZE)), (TOPMARGIN + (box_y * BOARDSIZE))

def draw_box(box_x, box_y, color, pixel_x=None, pixel_y=None):
    if color == BLANK:
        return
    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convert_pixel_coords(box_x, box_y)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixel_x + 1, pixel_y + 1, BOARDSIZE - 1, BOARDSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixel_x + 1, pixel_y + 1, BOARDSIZE - 4, BOARDSIZE - 4))


def draw_board(board): 
    pygame.draw.rect(DISPLAYSURF, BOARDCOLOR, (XMARGIN, TOPMARGIN, BOARDSIZE * BOARDWIDTH, BOARDSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            draw_box(x, y, board[x][y])

def draw_status(point, level):
    point_surf = BASICFONT.render('Point: %s' % point, True, TEXTCOLOR)
    point_rect = point_surf.get_rect()
    point_rect.topleft = (WINDOWWIDTH - 590, 50)
    DISPLAYSURF.blit(point_surf, point_rect)

    level_surf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOWWIDTH - 590, 80)
    DISPLAYSURF.blit(level_surf, level_rect)

def draw_block(block, pixel_x=None, pixel_y=None):
    shape_draw = BLOCKS[block['shape']][block['rotation']]
    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convert_pixel_coords(block['x'], block['y'])

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shape_draw[y][x] != BLANK:
                draw_box(None, None, block['color'], pixel_x + (x * BOARDSIZE), pixel_y + (y * BOARDSIZE))

def draw_next_block(block):
    next_surf = BASICFONT.render('Next :', True, TEXTCOLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOWWIDTH - 450, 50)
    DISPLAYSURF.blit(next_surf, next_rect)
    draw_block(block, pixel_x = WINDOWWIDTH - 400, pixel_y = 50)

if __name__ == '__main__':
    main()

#code from https://inventwithpython.com/pygame/chapter7.html

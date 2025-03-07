import pygame
import numpy as np

pygame.init()

GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (40, 60, 255)
YELLOW = (255, 255, 0)
LIGHT_RED = (255, 50, 50)
LIGHT_YELLOW = (240, 240, 0)
large_font = pygame.font.SysFont('malgungothic', 72)
CELL_SIZE = 100
COLUMN_COUNT = 7
ROW_COUNT = 6
P1_WIN = 1
P2_WIN = 2
DRAW = 3
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

done = False
grid = np.zeros((ROW_COUNT, COLUMN_COUNT))
mouse_x, mouse_y = pygame.mouse.get_pos()

clock = pygame.time.Clock() 

def is_free_column_index(grid, column_index):
    if column_index < 0 or column_index > COLUMN_COUNT - 1:
        return False

    return grid[ROW_COUNT - 1][column_index] == 0

def get_free_row_index(grid, column_index):
    for row_index in range(ROW_COUNT):
        if grid[row_index][column_index] == 0:
            return row_index

def is_winner(grid, piece):
    for column_index in range(COLUMN_COUNT - 3):
        for row_index in range(ROW_COUNT):
            if grid[row_index][column_index] == piece and grid[row_index][column_index + 1] == piece and grid[row_index][column_index + 2] == piece and grid[row_index][column_index + 3] == piece:
                return True

    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT - 3):
            if grid[row_index][column_index] == piece and grid[row_index + 1][column_index] == piece and grid[row_index + 2][column_index] == piece and grid[row_index + 3][column_index] == piece:
                return True
    for column_index in range(COLUMN_COUNT - 3):
        for row_index in range(ROW_COUNT - 3):
            if grid[row_index][column_index] == piece and grid[row_index + 1][column_index + 1] == piece and grid[row_index + 2][column_index + 2] == piece and grid[row_index + 3][column_index + 3] == piece:
                return True

    for column_index in range(COLUMN_COUNT - 3):
        for row_index in range(3, ROW_COUNT):
            if grid[row_index][column_index] == piece and grid[row_index - 1][column_index + 1] == piece and grid[row_index - 2][column_index + 2] == piece and grid[row_index - 3][column_index + 3] == piece:
                return True

def is_grid_full(count):
    if count == 42:
        return True
    return  False



def runGame():
    game_over = 0
    turn = 0
    count = 0
    global done

    def reset():
        global game_over, turn, count, grid
        game_over = 0
        turn = 0
        count = 0
        grid = np.zeros((ROW_COUNT, COLUMN_COUNT))
        screen.fill(WHITE)
        runGame()


    while not done: 
        clock.tick(30) 
        screen.fill(WHITE) 

        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                done=True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                column_index = event.pos[0] // CELL_SIZE
                count += 1

                if turn == 0:
                    if is_free_column_index(grid, column_index):
                        row_index = get_free_row_index(grid, column_index)
                        grid[row_index][column_index] = 1

                        if is_winner(grid, 1):
                            game_over = P1_WIN
                        elif is_grid_full(count):
                            game_over = DRAW

                        turn += 1
                        turn %= 2

                elif turn == 1:    
                    if is_free_column_index(grid, column_index):
                        row_index = get_free_row_index(grid, column_index)
                        grid[row_index][column_index] = 2

                        if is_winner(grid, 2):
                            game_over = P2_WIN
                        elif is_grid_full(count):
                            game_over = DRAW

                        turn += 1
                        turn %= 2

        if game_over == 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()

        #그리기 함수
        width = 700
        pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, width, CELL_SIZE))
        if turn == 0:
            pygame.draw.circle(screen, RED, (mouse_x, CELL_SIZE // 2), CELL_SIZE // 2 - 5)
        else: 
            pygame.draw.circle(screen, YELLOW, (mouse_x, CELL_SIZE // 2), CELL_SIZE // 2 - 5)

        for column_index in range(COLUMN_COUNT):
            for row_index in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, pygame.Rect(column_index * CELL_SIZE, row_index * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, WHITE, (column_index * CELL_SIZE + CELL_SIZE // 2, row_index * CELL_SIZE + CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

        for column_index in range(COLUMN_COUNT):
            for row_index in range(ROW_COUNT):   
                if grid[row_index][column_index] == 1:
                    height = CELL_SIZE * (ROW_COUNT + 1)
                    pygame.draw.circle(screen, RED, (column_index * CELL_SIZE + CELL_SIZE // 2, height - (row_index * CELL_SIZE + CELL_SIZE // 2)), CELL_SIZE // 2 - 5)
                elif grid[row_index][column_index] == 2: 
                    height = CELL_SIZE * (ROW_COUNT + 1)
                    pygame.draw.circle(screen, YELLOW, (column_index * CELL_SIZE + CELL_SIZE // 2, height - (row_index * CELL_SIZE + CELL_SIZE // 2)), CELL_SIZE // 2 - 5)   

        if game_over > 0: 
            if game_over == P1_WIN:
                p1_win_image = large_font.render('빨강 Win', True, LIGHT_RED)
                screen.fill(GRAY)
                screen.blit(p1_win_image, p1_win_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
            elif game_over == P2_WIN:
                p2_win_image = large_font.render('노랑 Win', True, LIGHT_YELLOW)
                screen.fill(GRAY)
                screen.blit(p2_win_image, p2_win_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
            else:
                draw_image = large_font.render('무승부', True, BLACK)
                screen.fill(GRAY)
                screen.blit(draw_image, draw_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))

        pygame.display.update()
    

runGame()

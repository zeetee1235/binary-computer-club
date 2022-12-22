import pygame 
pygame.init() 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)
font = pygame.font.SysFont("malgungothic",80)
mark_font = pygame.font.SysFont(None, 320)
size = [600,600]
screen = pygame.display.set_mode(size)
turn = 0 
grid = [' ', ' ', ' ', 
        ' ', ' ', ' ', 
        ' ', ' ', ' ']
done = False
clock = pygame.time.Clock()


def is_valid_position(grid, position):
    if grid[position] == ' ':
        return True
    else:
        return False

def is_winner(grid, mark):
    if (grid[0] == mark and grid[1] == mark and grid[2] == mark) or \
        (grid[3] == mark and grid[4] == mark and grid[5] == mark) or \
        (grid[6] == mark and grid[7] == mark and grid[8] == mark) or \
        (grid[0] == mark and grid[3] == mark and grid[6] == mark) or \
        (grid[1] == mark and grid[4] == mark and grid[7] == mark) or \
        (grid[2] == mark and grid[5] == mark and grid[8] == mark) or \
        (grid[0] == mark and grid[4] == mark and grid[8] == mark) or \
        (grid[2] == mark and grid[4] == mark and grid[6] == mark):
        return True
    else:
        return False

def is_grid_full(grid):
    full = True
    for mark in grid:
        if mark == ' ':
            full = False 
            break
    return full

turn = 0 

def runGame():
    CELL_SIZE = 200
    COLUMN_COUNT = 3
    ROW_COUNT = 3
    X_WIN = 1
    O_WIN = 2
    DRAW = 3
    game_over = 0
    global done, turn, grid
    
    
    
    def reset():
        global done, turn, grid
        done = 0
        turn = 0
        grid = [' ', ' ', ' ', 
                ' ', ' ', ' ', 
                ' ', ' ', ' ']
        screen.fill(WHITE)
        for column_index in range(COLUMN_COUNT):
            for row_index in range(ROW_COUNT):
                rect = (CELL_SIZE * column_index, CELL_SIZE * row_index, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
        runGame()

    
    while not done:
        clock.tick(30)
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                done=True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if turn == 0:
                    column_index = event.pos[0] // CELL_SIZE
                    row_index = event.pos[1] // CELL_SIZE
                    position = column_index + 3 * row_index
                    
                    if is_valid_position(grid, position):
                        grid[position] = 'X'
                        
                        if is_winner(grid, 'X'):
                            print('X 가 이겼습니다.')
                            game_over = X_WIN 
                        
                        elif is_grid_full(grid):
                            print('무승부 입니다.')
                            game_over = DRAW 
                        turn += 1
                        turn = turn % 2
                
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                    reset()
                
                elif turn == 1:
                    if event.key == pygame.K_q:
                        position = 0
                    elif event.key == pygame.K_w:
                        position = 1
                    elif event.key == pygame.K_e:
                        position = 2
                    elif event.key == pygame.K_a:
                        position = 3
                    elif event.key == pygame.K_s:
                        position = 4
                    elif event.key == pygame.K_d:
                        position = 5
                    elif event.key == pygame.K_z:
                        position = 6
                    elif event.key == pygame.K_x:
                        position = 7
                    elif event.key == pygame.K_c:
                        position = 8
                
                    if is_valid_position(grid, position):
                            grid[position] = 'O'
                        
                            if is_winner(grid, 'O'):
                                print('O 가 이겼습니다.')
                                game_over = O_WIN 
                        
                            elif is_grid_full(grid):
                                print('무승부 입니다.')
                                game_over = DRAW 
                            turn += 1
                            turn = turn % 2
            
            
                

            for column_index in range(COLUMN_COUNT):
                
                for row_index in range(ROW_COUNT):
                    rect = (CELL_SIZE * column_index, CELL_SIZE * row_index, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, BLACK, rect, 1)
            
            for column_index in range(COLUMN_COUNT):
                
                for row_index in range(ROW_COUNT):
                    position = column_index + 3 * row_index
                    mark = grid[position]
                    
                    if mark == 'X':
                        X_image = mark_font.render('{}'.format('X'), True, RED)
                        screen.blit(X_image, (CELL_SIZE * column_index + 10, CELL_SIZE * row_index + 10)) 
                    
                    elif mark == 'O':
                        O_image = mark_font.render('{}'.format('O'), True, GREEN)
                        screen.blit(O_image, (CELL_SIZE * column_index + 10, CELL_SIZE * row_index + 10)) 
            
            if not game_over: 
                pass
            
            else:
                if game_over == X_WIN:
                    screen.fill(WHITE)
                    txt1 = font.render('승리',True,RED)
                    screen.blit(txt1, (220,220))
                    
                    
                elif game_over == O_WIN:
                    screen.fill(WHITE)
                    txt2 = font.render('패배',True,GREEN)
                    screen.blit(txt2, (220,220))
                    
                    
                else:
                    screen.fill(WHITE)
                    txt3 = font.render('무승부',True,GRAY)
                    screen.blit(txt3, (190,220))
                    

                    
            pygame.display.update()


            
runGame()

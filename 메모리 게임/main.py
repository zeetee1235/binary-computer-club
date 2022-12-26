import random, pygame, sys 
from pygame.locals import *
pygame.init()

FPS = 30 
WINDOWWIDTH = 1200
WINDOWHEIGHT = 960
REVEALSPEED = 8 
BOXSIZE = 100 
GAPSIZE = 10 
BOARDWIDTH = 5
BOARDHEIGHT = 4 
assert (BOARDWIDTH*BOARDHEIGHT)%2==0, "Board Needs To have an even Number of boxes for pairs of matches."
XMARGIN = int((WINDOWWIDTH -(BOARDWIDTH*(BOXSIZE+GAPSIZE)))/2)
YMARGIN = int((WINDOWHEIGHT -(BOARDHEIGHT*(BOXSIZE+GAPSIZE)))/2)
large_font = pygame.font.SysFont('malgungothic', 50)
very_large_font = pygame.font.SysFont('malgungothic', 200)
chance = 15
chance2 = chance

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
LIGHTBLACK = (50, 50, 50)
BLACK = (0, 0, 0)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
DARKBGCOLOR = LIGHTBGCOLOR
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK,DISPLAYSURF, chance, chance2
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Chans Memory Puzzle")
    mousex = 0 
    mousey = 0 
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False) 
    firstSelection = None 
    chance_str = chance
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)
    
    while True: 
        mouseClicked = False 
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard,revealedBoxes)
        

        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit() 
            
            elif event.type == MOUSEMOTION:
                mousex,mousey == event.pos 
            
            elif event.type == MOUSEBUTTONUP:
                mousex,mousey = event.pos 
                mouseClicked = True 
        
        boxx, boxy = getBoxAtPixel(mousex,mousey)
        
        if boxx != None and boxy != None :
            
            if not revealedBoxes[boxx][boxy]: 
                drawHighlightBox(boxx,boxy) 
            
            if not revealedBoxes[boxx][boxy] and mouseClicked: 
                revealBoxesAnimation(mainBoard,[(boxx,boxy)]) 
                revealedBoxes[boxx][boxy] = True 
                
                if firstSelection == None : 
                    firstSelection = (boxx,boxy)
                    
                    if chance == 0:
                        gameLoseAnimation(mainBoard)
                        pygame.time.wait(2000)
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGameAnimation(mainBoard)
                        chance = 5###
                
                else: 
                    icon1shape,icon1color = getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1])
                    icon2shape,icon2color = getShapeAndColor(mainBoard,boxx,boxy)
                    
                    if chance == 0:
                        gameLoseAnimation(mainBoard)
                        pygame.time.wait(2000)
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGameAnimation(mainBoard)
                        chance = chance2
                    
                    
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000) 
                        coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False 
                        revealedBoxes[boxx][boxy] = False  
                        chance = chance - 1
                    
                    elif hasWon(revealedBoxes): 
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGameAnimation(mainBoard)
                    
                    
                    firstSelection = None 

        pygame.display.update()
        FPSCLOCK.tick(FPS)

#열린 상자에 대한 데이터 구조만들기
def generateRevealedBoxesData(val): 
    revealedBoxes = []   
    
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val]*BOARDHEIGHT)
    
    return revealedBoxes #revealedBoxes[x][y]가 된다. 

def getRandomizedBoard():
    icons = []
    
    for color in ALLCOLORS:
        
        for shape in ALLSHAPES:
            icons.append((shape,color))
    
    random.shuffle(icons)
    numIconsUsed = int(BOARDWIDTH*BOARDHEIGHT/2) 
    icons = icons[:numIconsUsed] * 2 
    random.shuffle(icons)

    board = []
    
    for x in range(BOARDWIDTH):
        column=[]
        
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] 
        
        board.append(column)
    return board 

def splitIntoGroupsOf(groupSize,theList):
    result = []
    
    for i in range(0,len(theList),groupSize):
        result.append(theList[i:i+groupSize])
    
    return result

def leftTopCoordsOfBox(boxx,boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE )+ YMARGIN
    
    return (left, top)

def getBoxAtPixel(x,y):
    
    for boxx in range(BOARDWIDTH):
        
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx,boxy)
            boxRect = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
            
            if boxRect.collidepoint(x,y): 
                
                return (boxx,boxy)
    
    return (None,None)

def drawIcon(shape,color,boxx,boxy):
    quarter = int(BOXSIZE*0.25) #syntactic sugar
    half = int(BOXSIZE*0.5) 

    left,top = leftTopCoordsOfBox(boxx,boxy)
    
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board,boxx,boxy): 
    #x,y 위치의 아이콘 형태의 값은 board[x][y][0]
    #x,y 위치의 아이콘 색의 값은 board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board,boxes,coverage):
    
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0],box[1])
        pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape,color,box[0],box[1])
        
        if coverage>0: 
            pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,coverage,BOXSIZE))
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board,boxesToReveal):
    
    for coverage in range(BOXSIZE,(-REVEALSPEED)-1,-REVEALSPEED):
        drawBoxCovers(board,boxesToReveal,coverage)

def coverBoxesAnimation(board,boxesToCover):
    
    for coverage in range(0,BOXSIZE+REVEALSPEED,REVEALSPEED):
        drawBoxCovers(board,boxesToCover,coverage)

def drawBoard(board,revealed):
    
    for boxx in range(BOARDWIDTH):
        
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx,boxy)
            
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
            
            else:
                shape, color = getShapeAndColor(board,boxx,boxy)
                drawIcon(shape,color,boxx,boxy)
    global chance
    chance_str = str(chance)
    chance_text = large_font.render('남은기회:', True, BLACK)
    chance_text2 = large_font.render(chance_str, True, BLACK)
    DISPLAYSURF.blit(chance_text, (0,0))
    DISPLAYSURF.blit(chance_text2, (215,0))
    
    

def drawHighlightBox(boxx,boxy):
    left,top = leftTopCoordsOfBox(boxx,boxy)
    pygame.draw.rect(DISPLAYSURF,HIGHLIGHTCOLOR,(left-5,top-5,BOXSIZE+10,BOXSIZE+10),4)

def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    
    for x in range(BOARDWIDTH):
        
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8,boxes)
    
    drawBoard(board,coveredBoxes)
    
    for boxGroup in boxGroups:
        revealBoxesAnimation(board,boxGroup)
        coverBoxesAnimation(board,boxGroup)
    
def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    DISPLAYSURF.fill(BGCOLOR)
    
    for i in range(10):
        color1,color2 = color2,color1 
        DISPLAYSURF.fill(color1)
        win_image = large_font.render('성공', True, RED)
        DISPLAYSURF.blit(win_image, win_image.get_rect(centerx=WINDOWWIDTH // 2 - 10, centery=200))
        drawBoard(board,coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)
        
    DISPLAYSURF.fill(BGCOLOR)
        
def gameLoseAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = DARKBGCOLOR
    color2 = BGCOLOR
    DISPLAYSURF.fill(BGCOLOR)
    
    for i in range(10):
        color1,color2 = color2,color1 
        DISPLAYSURF.fill(color1)
        lose_image = large_font.render('실패', True, BLACK)
        DISPLAYSURF.blit(lose_image, lose_image.get_rect(centerx=WINDOWWIDTH // 2 - 10, centery=200))
        drawBoard(board,coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)
        
    DISPLAYSURF.fill(BGCOLOR)

def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == '__main__':
    main()

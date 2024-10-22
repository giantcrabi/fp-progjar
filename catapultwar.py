import random, pygame, sys, socket, json, os
from pygame.locals import *

server_address = ('127.0.0.1', 5027)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

FPS = 30
WINDOWWIDTH = 1600
WINDOWHEIGHT = 900
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 15
BOARDHEIGHT = 15
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

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

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

FIREBOMB = 'firebomb'
CROSSBOMB = 'crossbomb'
NAPALM = 'napalm'
GUILLOTINE = 'guillotine'
ROCKET = 'rocket'
BENTENG = 'benteng'
NONE = 'none'

POWERUPS = ((FIREBOMB, 8), (CROSSBOMB, 8), (NAPALM, 5), (GUILLOTINE, 3), (ROCKET, 3))

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption('Catapult War')

    pygame.mixer.music.load('music/background.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1, 0.0)
    
    musicCastle = inisialisasiMusicEffect()

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    lifePlayer1, lifePlayer2, kesempatanTembak1 = getInitVar()
    jumlahBenteng1 = 5
    kena1 = 0
    powerPlayer1 = ''

    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(mainBoard, revealedBoxes)
    pygame.display.update()

    while True:
        mouseClicked = False
        
        lifePlayer1 = getLifePlayer1()
        if(getBoard() != []):
            mainBoardTemp = getBoard()
            if mainBoard != mainBoardTemp:
                mainBoard = mainBoardTemp
                revealedBoxes = generateRevealedBoxesData(False)
                
        
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        drawBentengSendiri(lifePlayer1)
        drawBentengLawan(lifePlayer2)
        myTurn = myTurnHere()

        
        if myTurn:
            drawTurn("YOUR TURN")
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True

            if jumlahBenteng1 > 0:
                boxx, boxy = getBoxAtPixel(mousex, mousey)
                if boxx != None and boxy != None:
                    if not revealedBoxes[boxx][boxy]:
                        drawHighlightBox(boxx, boxy)
                    if not revealedBoxes[boxx][boxy] and mouseClicked:
                        jumlahBenteng1 -= 1
                        mainBoard[boxx][boxy] = BENTENG
                        revealedBoxes[boxx][boxy] = True
                        drawIcon(BENTENG, boxx, boxy)
                        musicCastle.play()
            if jumlahBenteng1 == 0:
                sendBoard(mainBoard)
                jumlahBenteng1 -= 1
            else:
                if kesempatanTembak1 != 0:
                    boxx, boxy = getBoxAtPixel(mousex, mousey)
                    if boxx != None and boxy != None:
                        if not revealedBoxes[boxx][boxy]:
                            drawHighlightBox(boxx, boxy)
                        if not revealedBoxes[boxx][boxy] and mouseClicked:
                            powerPlayer1, kena1  = fireCatapult(mainBoard,revealedBoxes,boxx,boxy,powerPlayer1)
                            lifePlayer2 = sendKena(kena1)
                            kesempatanTembak1 -= 1
                
        elif myTurn == 0:
            kesempatanTembak1 = getKesempatanTembak1()
            drawTurn("ENEMY TURN")
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True
                
        if lifePlayer2 <= 0:
            DISPLAYSURF.fill(NAVYBLUE)
            drawKemenangan()
            pygame.time.wait(3000)
            client_socket.close()
            pygame.quit()
            sys.exit(0)

        if lifePlayer1 <= 0:
            DISPLAYSURF.fill(GRAY)
            drawKekalahan()
            pygame.time.wait(3000)
            client_socket.close()
            pygame.quit()
            sys.exit(0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawKemenangan():
    winFont = pygame.font.Font('freesansbold.ttf', 80)
    gameSurf = winFont.render('CONGRATULATIONS', True, WHITE)
    winSurf = winFont.render('YOU WIN!!!', True, WHITE)
    gameRect = gameSurf.get_rect()
    winRect = winSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH/2, 500)
    winRect.midtop = (WINDOWWIDTH/2, gameRect.height + 50 + 45)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(winSurf, winRect)
    pygame.display.update()


def drawKekalahan():
    winFont = pygame.font.Font('freesansbold.ttf', 80)
    gameSurf = winFont.render('SORRY', True, WHITE)
    winSurf = winFont.render('YOU LOSE :(', True, WHITE)
    gameRect = gameSurf.get_rect()
    winRect = winSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH/2, 500)
    winRect.midtop = (WINDOWWIDTH/2, gameRect.height + 50 + 45)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(winSurf, winRect)
    pygame.display.update()


def myTurnHere():
    client_socket.send('turn')
    receive = int(client_socket.recv(10))
    return receive


def getInitVar():
    client_socket.send('init')
    receive = client_socket.recv(1024)
    parsed_data = json.loads(receive)
    return parsed_data[0], parsed_data[1], parsed_data[2]


def getLifePlayer1():
    client_socket.send('LP')
    receive = int(client_socket.recv(1024))
    return receive


def getKesempatanTembak1():
    client_socket.send('KT')
    receive = int(client_socket.recv(1024))
    return receive


def sendKena(kena):
    client_socket.send('SK')
    pygame.time.wait(5)
    client_socket.send(str(kena))
    receive = int(client_socket.recv(1024))
    return receive


def sendBoard(board):
    client_socket.send('MB')
    pygame.time.wait(5)
    databuffer = json.dumps(board)
    client_socket.send(databuffer)


def getBoard():
    client_socket.send('CB')
    receive = client_socket.recv(16384)
    board = json.loads(receive)
    return board


def drawBentengSendiri(score):
    scoreSurf = BASICFONT.render('Benteng Player: %d' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 400, 75)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    
def drawTurn(score):
    scoreSurf = BASICFONT.render('%s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 400, 140)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawBentengLawan(score):
    scoreSurf = BASICFONT.render('Benteng Lawan: %d' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 400, 105)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def inisialisasiMusicEffect():
    musicCastle = pygame.mixer.Sound('music/buildCastle.ogg')
    #castleDestroy = pygame.mixer.Sound('')
    #catapultFire = pygame.mixer.Sound('')

    return musicCastle


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(NONE)
        board.append(column)

    powerups = []
    for items in POWERUPS:
        for i in range(items[1]):
            powerups.append(items[0])

    random.shuffle(powerups)

    while(len(powerups) != 0):
        xcoord = random.randint(0, BOARDWIDTH - 1)
        ycoord = random.randint(0, BOARDHEIGHT - 1)
        if board[xcoord][ycoord] == NONE:
            board[xcoord][ycoord] = powerups[0]
            del powerups[0]
        else:
            continue

    return board

def fireCatapult(board, revealedBoxes, boxx, boxy, powerup):
    boxes = []
    boxes.append((boxx, boxy))
    revealedBoxes[boxx][boxy] = True
    powerPlayer1=''
    kena1 = 0
    if board[boxx][boxy] != NONE and board[boxx][boxy] != BENTENG:
        powerPlayer1 = board[boxx][boxy]
    if board[boxx][boxy] == BENTENG:
        kena1 += 1
    if(powerup == FIREBOMB):
        powerPlayer1 = ''
        boxes = []
        boxes.append((boxx, boxy))
        revealedBoxes[boxx][boxy] = True

        if(boxx - 1 >= 0 and not revealedBoxes[boxx - 1][boxy]):
            boxes.append((boxx - 1, boxy))
            revealedBoxes[boxx - 1][boxy] = True
            if board[boxx - 1][boxy] != NONE and board[boxx - 1][boxy] != BENTENG:
                powerPlayer1 = board[boxx - 1][boxy]
            if board[boxx - 1][boxy] == BENTENG:
                kena1 += 1
        if(boxx + 1 < BOARDWIDTH and not revealedBoxes[boxx + 1][boxy]):
            boxes.append((boxx + 1, boxy))
            revealedBoxes[boxx + 1][boxy] = True
            if board[boxx + 1][boxy] != NONE and board[boxx + 1][boxy] != BENTENG:
                powerPlayer1 = board[boxx + 1][boxy]
            if board[boxx + 1][boxy] == BENTENG:
                kena1 += 1
        if(boxy - 1 >= 0 and not revealedBoxes[boxx][boxy - 1]):
            boxes.append((boxx, boxy - 1))
            revealedBoxes[boxx][boxy - 1] = True
            if board[boxx][boxy - 1] != NONE and board[boxx][boxy - 1] != BENTENG:
                powerPlayer1 = board[boxx][boxy - 1]
            if board[boxx][boxy - 1] == BENTENG:
                kena1 += 1
        if(boxy + 1 < BOARDHEIGHT and not revealedBoxes[boxx][boxy + 1]):
            boxes.append((boxx, boxy + 1))
            revealedBoxes[boxx][boxy + 1] = True
            if board[boxx][boxy + 1] != NONE and board[boxx][boxy + 1] != BENTENG:
                powerPlayer1 = board[boxx][boxy + 1]
            if board[boxx][boxy + 1] == BENTENG:
                kena1 += 1

    if(powerup == CROSSBOMB):
        powerPlayer1 = ''
        boxes = []
        boxes.append((boxx, boxy))
        revealedBoxes[boxx][boxy] = True

        if(boxx - 1 >= 0 and boxy - 1 and not revealedBoxes[boxx - 1][boxy - 1]):
            boxes.append((boxx - 1, boxy - 1))
            revealedBoxes[boxx - 1][boxy - 1] = True
            if board[boxx - 1][boxy - 1] != NONE and board[boxx - 1][boxy - 1] != BENTENG:
                powerPlayer1 = board[boxx - 1][boxy - 1]
            if board[boxx - 1][boxy - 1] == BENTENG:
                kena1 += 1
        if(boxx + 1 < BOARDWIDTH and boxy + 1 < BOARDHEIGHT and not revealedBoxes[boxx + 1][boxy + 1]):
            boxes.append((boxx + 1, boxy + 1))
            revealedBoxes[boxx + 1][boxy + 1] = True
            if board[boxx + 1][boxy + 1] != NONE and board[boxx + 1][boxy + 1] != BENTENG:
                powerPlayer1 = board[boxx + 1][boxy + 1]
            if board[boxx + 1][boxy + 1] == BENTENG:
                kena1 += 1
        if(boxy - 1 >= 0 and boxx + 1 < BOARDWIDTH and not revealedBoxes[boxx + 1][boxy - 1]):
            boxes.append((boxx + 1, boxy - 1))
            revealedBoxes[boxx + 1][boxy - 1] = True
            if board[boxx + 1][boxy - 1] != NONE and board[boxx + 1][boxy - 1] != BENTENG:
                powerPlayer1 = board[boxx + 1][boxy - 1]
            if board[boxx + 1][boxy - 1] == BENTENG:
                kena1 += 1
        if(boxy + 1 < BOARDHEIGHT and boxx - 1 >= 0 and not revealedBoxes[boxx - 1][boxy + 1]):
            boxes.append((boxx - 1, boxy + 1))
            revealedBoxes[boxx - 1][boxy + 1] = True
            if board[boxx - 1][boxy + 1] != NONE and board[boxx - 1][boxy + 1] != BENTENG:
                powerPlayer1 = board[boxx - 1][boxy + 1]
            if board[boxx - 1][boxy + 1] == BENTENG:
                kena1 += 1

    if(powerup == NAPALM):
        powerPlayer1 = ''
        boxes = []
        boxes.append((boxx, boxy))
        revealedBoxes[boxx][boxy] = True

        if(boxx - 1 >= 0 and boxy - 1 and not revealedBoxes[boxx - 1][boxy - 1]):
            boxes.append((boxx - 1, boxy - 1))
            revealedBoxes[boxx - 1][boxy - 1] = True
            if board[boxx - 1][boxy - 1] != NONE and board[boxx - 1][boxy - 1] != BENTENG:
                powerPlayer1 = board[boxx - 1][boxy - 1]
            if board[boxx - 1][boxy - 1] == BENTENG:
                kena1 += 1
        if(boxx + 1 < BOARDWIDTH and boxy + 1 < BOARDHEIGHT and not revealedBoxes[boxx + 1][boxy + 1]):
            boxes.append((boxx + 1, boxy + 1))
            revealedBoxes[boxx + 1][boxy + 1] = True
            if board[boxx + 1][boxy + 1] != NONE and board[boxx + 1][boxy + 1] != BENTENG:
                powerPlayer1 = board[boxx + 1][boxy + 1]
            if board[boxx + 1][boxy + 1] == BENTENG:
                kena1 += 1
        if(boxy - 1 >= 0 and boxx + 1 < BOARDWIDTH and not revealedBoxes[boxx + 1][boxy - 1]):
            boxes.append((boxx + 1, boxy - 1))
            revealedBoxes[boxx + 1][boxy - 1] = True
            if board[boxx + 1][boxy - 1] != NONE and board[boxx + 1][boxy - 1] != BENTENG:
                powerPlayer1 = board[boxx + 1][boxy - 1]
            if board[boxx + 1][boxy - 1] == BENTENG:
                kena1 += 1
        if(boxy + 1 < BOARDHEIGHT and boxx - 1 >= 0 and not revealedBoxes[boxx - 1][boxy + 1]):
            boxes.append((boxx - 1, boxy + 1))
            revealedBoxes[boxx - 1][boxy + 1] = True
            if board[boxx - 1][boxy + 1] != NONE and board[boxx - 1][boxy + 1] != BENTENG:
                powerPlayer1 = board[boxx - 1][boxy + 1]
            if board[boxx - 1][boxy + 1] == BENTENG:
                kena1 += 1
        if(boxx - 1 >= 0 and not revealedBoxes[boxx - 1][boxy]):
            boxes.append((boxx - 1, boxy))
            revealedBoxes[boxx - 1][boxy] = True
            if board[boxx - 1][boxy] != NONE and board[boxx - 1][boxy] != BENTENG:
                powerPlayer1 = board[boxx - 1][boxy]
            if board[boxx - 1][boxy] == BENTENG:
                kena1 += 1
        if(boxx + 1 < BOARDWIDTH and not revealedBoxes[boxx + 1][boxy]):
            boxes.append((boxx + 1, boxy))
            revealedBoxes[boxx + 1][boxy] = True
            if board[boxx + 1][boxy] != NONE and board[boxx + 1][boxy] != BENTENG:
                powerPlayer1 = board[boxx + 1][boxy]
            if board[boxx + 1][boxy] == BENTENG:
                kena1 += 1
        if(boxy - 1 >= 0 and not revealedBoxes[boxx][boxy - 1]):
            boxes.append((boxx, boxy - 1))
            revealedBoxes[boxx][boxy - 1] = True
            if board[boxx][boxy - 1] != NONE and board[boxx][boxy - 1] != BENTENG:
                powerPlayer1 = board[boxx][boxy - 1]
            if board[boxx][boxy - 1] == BENTENG:
                kena1 += 1
        if(boxy + 1 < BOARDHEIGHT and not revealedBoxes[boxx][boxy + 1]):
            boxes.append((boxx, boxy + 1))
            revealedBoxes[boxx][boxy + 1] = True
            if board[boxx][boxy + 1] != NONE and board[boxx][boxy + 1] != BENTENG:
                powerPlayer1 = board[boxx][boxy + 1]
            if board[boxx][boxy + 1] == BENTENG:
                kena1 += 1

    if(powerup == GUILLOTINE):
        powerPlayer1 = ''
        boxes = []
        boxes.append((boxx, boxy))
        revealedBoxes[boxx][boxy] = True
        boxx1 = boxx - 1
        boxx2 = boxx + 1
        while boxx1 >=0:
           if not revealedBoxes[boxx1][boxy]:
                boxes.append((boxx1, boxy))
                revealedBoxes[boxx1][boxy] = True
                if board[boxx1][boxy] != NONE and board[boxx1][boxy] != BENTENG:
                    powerPlayer1 = board[boxx1][boxy]
                if board[boxx1][boxy] == BENTENG:
                    kena1 += 1
           boxx1 -= 1
        while boxx2 < BOARDWIDTH:
           if not revealedBoxes[boxx2][boxy]:
                boxes.append((boxx2, boxy))
                revealedBoxes[boxx2][boxy] = True
                if board[boxx2][boxy] != NONE and board[boxx2][boxy] != BENTENG:
                    powerPlayer1 = board[boxx2][boxy]
                if board[boxx2][boxy] == BENTENG:
                    kena1 += 1
           boxx2 += 1
    if(powerup == ROCKET):
        powerPlayer1 = ''
        boxes = []
        boxes.append((boxx, boxy))
        revealedBoxes[boxx][boxy] = True
        boxy1 = boxy - 1
        boxy2 = boxy + 1
        while boxy1 >=0:
           if not revealedBoxes[boxx][boxy1]:
                boxes.append((boxx, boxy1))
                revealedBoxes[boxx][boxy1] = True
                if board[boxx][boxy1] != NONE and board[boxx][boxy1] != BENTENG:
                    powerPlayer1 = board[boxx][boxy1]
                if board[boxx][boxy1] == BENTENG:
                    kena1 += 1
           boxy1 -= 1
        while boxy2 < BOARDWIDTH:
           if not revealedBoxes[boxx][boxy2]:
                boxes.append((boxx, boxy2))
                revealedBoxes[boxx][boxy2] = True
                if board[boxx][boxy2] != NONE and board[boxx][boxy2] != BENTENG:
                    powerPlayer1 = board[boxx][boxy2]
                if board[boxx][boxy2] == BENTENG:
                    kena1 += 1
           boxy2 += 1
    
    revealBoxesAnimation(board, boxes)
    return powerPlayer1, kena1


def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy) 

    if shape == BENTENG:
        DISPLAYSURF.blit(pygame.image.load('gambar/benteng.png'),(left,top))
    elif shape == FIREBOMB:
        DISPLAYSURF.blit(pygame.image.load('gambar/firebomb.png'),(left,top))
    elif shape == CROSSBOMB:
        DISPLAYSURF.blit(pygame.image.load('gambar/crossbomb.png'),(left,top))
    elif shape == NAPALM:
        DISPLAYSURF.blit(pygame.image.load('gambar/napalm.png'),(left,top))
    elif shape == GUILLOTINE:
        DISPLAYSURF.blit(pygame.image.load('gambar/guillotine.png'),(left,top))
    elif shape == ROCKET:
        DISPLAYSURF.blit(pygame.image.load('gambar/rocket.png'),(left,top))


def getShape(board, boxx, boxy):
    return board[boxx][boxy]


def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape = getShape(board, box[0], box[1])
        drawIcon(shape, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape = getShape(board, boxx, boxy)
                drawIcon(shape, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


if __name__ == '__main__':
    while True:
        ready = client_socket.recv(1024)
        if(ready == 'NOT'):
            print "Waiting for Player 2..."
        elif(ready == 'OK'):
            print "Game Started!!!"
            main()
            break

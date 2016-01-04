import SocketServer
import random, pygame, sys, json
from pygame.locals import *

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
LUCKY = 'lucky'
SUPERLUCKY = 'superlucky'
BENTENG = 'benteng'
NONE = 'none'

POWERUPS = ((FIREBOMB, 5), (CROSSBOMB, 5), (NAPALM, 3), (GUILLOTINE, 2), (ROCKET, 2), (LUCKY, 5), (SUPERLUCKY, 3))

lifePlayer1 = 5
lifePlayer2 = 5
sisaLife1 = 5
sisaLife2 = 5
kena1 = 0
kena2 = 0
kesempatanTembak1 = 3
kesempatanTembak2 = 3
board1 = []
board2 = []

class MyTCPHandler(SocketServer.StreamRequestHandler):
    timeout = 60
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            print "{} wrote:".format(self.client_address[0])
            print self.data
            if(self.data == 'init'):
                self.initVar()
            elif(self.data == 'LP2'):
                self.sendLifePlayer2()
            elif(self.data == 'SK'):
                self.getKena()
            elif(self.data == 'MB'):
                self.getBoard()

    def initVar(self):
        datalist = [lifePlayer1,kesempatanTembak1]
        databuffer = json.dumps(datalist)
        self.request.send(databuffer)

    def sendLifePlayer2(self):
        self.request.send(str(sisaLife2))

    def getKena(self):
        global kena1
        global sisaLife2
        kena1 = int(self.request.recv(1024).strip())
        sisaLife2 = sisaLife2 - kena1
        self.sendLifePlayer2()

    def getBoard(self):
        global board1
        receive = self.request.recv(4096)
        board1 = json.loads(receive)
        print board1

if __name__ == "__main__":
    HOST, PORT = "localhost", 5002

    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "Got keyboard interrupt, shutting down"
        server.shutdown()
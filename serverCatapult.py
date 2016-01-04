import SocketServer
import random, pygame, sys, json, random, threading
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

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class MyTCPHandler(SocketServer.StreamRequestHandler):
    timeout = 60
    lifePlayer1 = 5
    lifePlayer2 = 5
    sisaLife1 = lifePlayer1
    sisaLife2 = lifePlayer1
    kena1 = 0
    kena2 = 0
    kesempatanTembak1 = 3
    kesempatanTembak2 = 3
    board1 = []
    board2 = []
    turn = random.randint(1,2)

    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            self.cur_thread = threading.current_thread()
            if(self.data == ''):
                break
            response = "{}: {}".format(self.cur_thread.name, self.data)
            print response
            """
            print "{} wrote:".format(self.client_address[0])
            print self.data
            """
            if(self.data == 'init'):
                self.initVar()
            elif(self.data == 'LP'):
                self.sendLifePlayer(self.lifePlayer1)
            elif(self.data == 'FI'):
                self.sendKesempatanTembak(self.kesempatanTembak1)
            elif(self.data == 'SK'):
                self.getKena()
            elif(self.data == 'MB'):
                self.getBoard()


    def initVar(self):
        datalist = [self.lifePlayer1,self.lifePlayer2,self.kesempatanTembak1]
        databuffer = json.dumps(datalist)
        self.request.send(databuffer)

    def sendLifePlayer(self,lifePlayer):
        self.request.send(str(lifePlayer))

    def sendKesempatanTembak(self,kesempatanTembak):
        self.request.send(str(kesempatanTembak))

    def getKena(self):
        self.kena1 = int(self.request.recv(1024).strip())
        self.sisaLife2 = self.sisaLife2 - self.kena1
        self.sendLifePlayer(self.sisaLife2)

    def getBoard(self):
        receive = self.request.recv(8192)
        self.board1 = json.loads(receive)
        print self.board1

if __name__ == "__main__":
    HOST, PORT = "localhost", 5002

    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler )
    ip, port = server.server_address

    try:
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever())
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print "Server loop running in thread:", server_thread.name

    except KeyboardInterrupt:
        print "Got keyboard interrupt, shutting down"
        server.shutdown()
        server.server_close()
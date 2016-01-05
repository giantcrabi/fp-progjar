import SocketServer
import random, pygame, sys, json, threading, math
from pygame.locals import *


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
cekturn = 1
shot = 0


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class MyTCPHandler(SocketServer.StreamRequestHandler):
    timeout = 1000
    def handle(self):
        global lifePlayer1, lifePlayer2, sisaLife1, sisaLife2, kena1, kena2, kesempatanTembak1, kesempatanTembak2, board1, board2, cekturn, shot
        print "{} connected".format(self.client_address)
        if(threading.activeCount() < 3):
            self.request.send('NOT')
        while True:
            if(threading.activeCount() == 3):
                self.request.send('OK')
                break
        while True:
            self.data = self.request.recv(1024).strip()
            self.cur_thread = threading.current_thread()

            if(self.data == ''):
                print "{} disconnected".format(self.client_address)
                break
            
            if(self.data == 'init'):
                self.initVar()
            elif(self.data == 'LP'):
                if self.cur_thread.name == "Thread-1":
                    self.sendLifePlayer(sisaLife1)
                elif self.cur_thread.name == "Thread-2":
                    self.sendLifePlayer(sisaLife2)
            elif(self.data == 'KT'):
                if self.cur_thread.name == "Thread-1":
                    self.sendKesempatanTembak(kesempatanTembak1)
                elif self.cur_thread.name == "Thread-2":
                    self.sendKesempatanTembak(kesempatanTembak1)
            elif(self.data == 'SK'):
                if self.cur_thread.name == "Thread-1":
                    kena1, sisaLife2 = self.getKena(kena1, sisaLife2)
                elif self.cur_thread.name == "Thread-2":
                    kena2, sisaLife1 = self.getKena(kena2, sisaLife1)
            elif(self.data == 'MB'):
                if self.cur_thread.name == "Thread-1":
                    board1 = self.getBoard(board1)
                elif self.cur_thread.name == "Thread-2":
                    board2 = self.getBoard(board2)
            elif(self.data == 'CB'):
                if self.cur_thread.name == "Thread-1":
                    self.sendBoard(board1)
                elif self.cur_thread.name == "Thread-2":
                    self.sendBoard(board2)
            elif(self.data == 'turn'):
                if self.cur_thread.name == "Thread-1" and cekturn % 2 != 0:
                    self.turn(1)
                elif self.cur_thread.name == "Thread-1" and cekturn % 2 == 0:
                    self.turn(0)
                elif self.cur_thread.name == "Thread-2" and cekturn % 2 != 0:
                    self.turn(0)
                elif self.cur_thread.name == "Thread-2" and cekturn % 2 == 0:
                    self.turn(1)

            if(cekturn == 3 and board1 != [] and board2 != []):
                board1, board2 = board2, board1
                cekturn += 2

    def turn(self, i):
        self.request.send(str(i))

    def initVar(self):
        global lifePlayer1, lifePlayer2, kesempatanTembak1
        datalist = [lifePlayer1,lifePlayer2,kesempatanTembak1]
        databuffer = json.dumps(datalist)
        self.request.send(databuffer)

    def sendLifePlayer(self,lifePlayer):
        self.request.send(str(lifePlayer))

    def sendKesempatanTembak(self,kesempatanTembak):
        self.request.send(str(kesempatanTembak))

    def getKena(self,kena,sisaLife):
        global cekturn, shot
        kena = int(self.request.recv(1024).strip())
        sisaLife = sisaLife - kena
        self.sendLifePlayer(sisaLife)
        shot += 1
        if(shot == 3):
            cekturn += 1
            shot = 0
        return kena, sisaLife

    def getBoard(self,board):
        global cekturn
        receive = self.request.recv(16384)
        board = json.loads(receive)
        cekturn += 1
        return board

    def sendBoard(self,board):
        databuffer = json.dumps(board)
        self.request.send(databuffer)


if __name__ == "__main__":
    HOST, PORT = "localhost", 5027

    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler )
    ip, port = server.server_address

    try:
        server_thread = threading.Thread(target=server.serve_forever())
        server_thread.daemon = True
        server_thread.start()

    except KeyboardInterrupt:
        print "Got keyboard interrupt, shutting down"
        server.shutdown()
        server.server_close()

import PodSixNet
import PodSixNet.Channel as pc
import PodSixNet.Server as ps
from time import sleep

class clientChannel(pc.Channel):
    def Network(self, data):
        print data

class gameServer(ps.Server):
    channelClass = clientChannel

    def Connected(self, channel, addr):
        print "New Connection: ", channel

print "Starting Server on Localhost"
gameServe = gameServer()

while True:
    gameServe.Pump()
    sleep(0.01)



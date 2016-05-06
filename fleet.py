import random
import sys

class Fleet:
    def __init__(self, flyTime):
        self.currentFlightTime = 0
        self.flytime = flyTime

        #generamos in id aleatorio para la flota diferente de 0
        self.fleetID = random.randrange(1,sys.maxint,1)
from planet import *

class SpyReport:
    def __init__(self, msgID, nombre, flotas, defensas, recursos, botinPosible, galaxy, system, planetPosition):
        self.msgID = msgID
        self.flotas = flotas
        self.defensas = defensas
        self.recursos = recursos
        self.botinPosible = int((recursos*botinPosible)/100)
        self.navesPequenasNecesarias = int(self.botinPosible/5000)+1
        self.navesGrandesNecesarias = int(self.botinPosible/25000)+1
        self.galaxy = galaxy
        self.system = system
        self.planetPosition = planetPosition
        self.nombre = nombre

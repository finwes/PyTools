import globalConstants
import time
import generalTools
import seleniumTools
import threading

from fleet import Fleet
from spaceship import Spaceship

class FleetControl:
    def __init__(self, driver):
        #debemos inicializar las estructuras de naves y sondas
        self.sondasEspionaje = []
        self.navesPequenasDeCarga = []
        self.navesGrandesDeCarga = []
        self.flotas = []

        self.driver = driver

        #cargamos la configuracion necesaria
        self.tiempoVueloSondas = int(globalConstants.config.getAttribute("tiempoVueloSondas"))

        #vamos a la pantalla de Flota para ver cuantas naves de cada tipo tenemos disponigles y cuantos slots de flota quedan libres para ser utilizados
        generalTools.navigateTo("Flota", self.driver)
        sondasDisponibles = int(seleniumTools.getElementByXPath(self.driver, 10, ".//*[@id='button210']//span[@class='level']").text)
        navesGrandesDisponibles = int(seleniumTools.getElementByXPath(self.driver, 10, ".//*[@id='button203']//span[@class='level']").text)
        navesPequenasDisponibles = int(seleniumTools.getElementByXPath(self.driver, 10, ".//*[@id='button202']//span[@class='level']").text)

        textoFlotas = seleniumTools.getElementByXPath(self.driver, 10, ".//*[@id='slots']//span[contains(text(),'Flotas')]/..").text
        textoFlotas = textoFlotas[textoFlotas.find(":")+1:len(textoFlotas)]
        self.flotasUtilizadas = int(textoFlotas[0:textoFlotas.find("/")])
        self.flotasTotales = int(textoFlotas[textoFlotas.find("/")+1:len(textoFlotas)])

        #inicializamos la lista de sondas
        for i in range(0,sondasDisponibles):
            self.sondasEspionaje.append(Spaceship())

        #inicializamos la lista de naves grandes y pequenas de carga
        #De momento no se calcula el tiempo de vuelo de la nave. Mas adelante seria interesante calcular los tiempos reales de vuelo y asi poder ajustar bien cuando vuelven las naves y lanzar ataques nuevos. De momento hacemos que cuando se lanza una nave estara fuera 2 horas
        for i in range(0,navesGrandesDisponibles):
            self.navesGrandesDeCarga.append(Spaceship())

        for i in range(0,navesPequenasDisponibles):
            self.navesPequenasDeCarga.append(Spaceship())

        # inicializamos el thread de clase que controlara si la sonda esta en la base o volando y los tiempos de vuelo
        threading.Thread(target=self.flyControlThread).start()

        print "Control de flotas inicializado correctamente"

    def selectShipsForFleet(self, numNaves, listaNaves, fleetID):

        navesSelecionadas = 0
        for nave in listaNaves:
            if navesSelecionadas>=numNaves:
                break

            if nave.fleetID == 0:
                nave.fleetID = fleetID
                navesSelecionadas+=1

        if navesSelecionadas<numNaves:
            raise Exception('No se han podido seleccionar todas las naves para la flota')


    def sendFleet(self, numNavesPequenasCarga, numNavesGrandeCarga, numSondaEspionaje):
        if (numNavesPequenasCarga == 0 or self.shipsAvailable(numNavesPequenasCarga, self.navesPequenasDeCarga)) and (numNavesGrandeCarga == 0 or self.shipsAvailable(numNavesGrandeCarga, self.navesGrandesDeCarga)) and (numSondaEspionaje == 0 or self.shipsAvailable(numSondaEspionaje, self.sondasEspionaje)):
            #tenemos suficientes naves para lanzar la flota calculamos el tiempo de vuelo de la flota y creamos la flota
            tiempoVueloFlota = self.tiempoVueloSondas
            if numNavesGrandeCarga>0 or numNavesPequenasCarga>0:
                #Si enviamos naves de carga ponemos como tiempo de vuelo 2 horas. Mas adelante seria importante calcular el tiempo real de vuelo de la flota
                tiempoVueloFlota = 7200

            flota = Fleet(tiempoVueloFlota)

            #seleccionamos las naves de la flota
            self.selectShipsForFleet(numNavesPequenasCarga, self.navesPequenasDeCarga, flota.fleetID)
            self.selectShipsForFleet(numNavesGrandeCarga, self.navesGrandesDeCarga, flota.fleetID)
            self.selectShipsForFleet(numSondaEspionaje, self.sondasEspionaje, flota.fleetID)

            #incrementamos el numero de flotas en uso
            self.flotasUtilizadas+=1

            #finalmente anadimos la flota a la lista de flotas (lanzamos la flota a volar)
            self.flotas.append(flota)

        else:
            #no hay naves para lanzar la flota. Indicamos el error
            raise Exception('No hay naves suficientes para lanzar la flota.')

    def waitForSpyProbes(self):
        sondasVolando = True
        while sondasVolando:
            sondasVolando = False
            for sonda in self.sondasEspionaje:
                if sonda.fleetID!=0:
                    sondasVolando = True
                    break
            if sondasVolando:
                #esperamos a que lleguen a destino
                time.sleep(1)

    #devuelve True si tenemos numNaves listas para ser enviadas de la lista pasada por parametro
    def shipsAvailable(self, numNaves, listaNaves):
        result = False
        numNavesDisponibles = 0
        for nave in listaNaves:
            if nave.fleetID==0:
                numNavesDisponibles += 1
        if numNavesDisponibles>=numNaves:
            result = True
        return result

    #devuelve True si tenemos numsondas listas para ser enviadas
    def probeAvailable(self, numsondas):
        return self.shipsAvailable(numsondas, self.sondasEspionaje)

    #devuelve True si tenemos numNaves navesGrandesDeCarga listas para ser enviadas
    def navesGrandesAvailable(self, numNaves):
        return self.shipsAvailable(numNaves, self.navesGrandesDeCarga)

    #devuelve True si tenemos numNaves navesPequenasDeCarga listas para ser enviadas
    def navesPequenasAvailable(self, numNaves):
        return self.shipsAvailable(numNaves, self.navesPequenasDeCarga)

    #devuelve True si tenemos suficientes naves dispobibles para lanzar la flota pasada por parametro
    def fleetAvailable (self, numSondas, numPeques, numGrandes):
        return self.probeAvailable(numSondas) and self.navesGrandesAvailable(numGrandes) and self.navesPequenasAvailable(numPeques)

    #devuelve True si tenemos al menos un espacio de flota disponible
    def espacioFlotaDisponible(self):
        return self.flotasUtilizadas<self.flotasTotales


    def flyControlThread(self):
        while(globalConstants.running):
            #comprobamos el estado de vuelo de todas las flotas
            for flota in self.flotas:
                flota.currentFlightTime += 1
                if flota.currentFlightTime >= flota.flytime:
                    # La flota ya ha volado todo el tiempo por lo que la flota ha vuelto a base y acabamos el vuelo de la misma y de todas la naves que la componen
                    flota.currentFlightTime = 0

                    #Marcamos todas las naves de la flota como libres para poder formar parte de una nueva flota
                    for sonda in self.sondasEspionaje:
                        if sonda.fleetID == flota.fleetID:
                            sonda.fleetID = 0

                    for naveGrandeDeCarga in self.navesGrandesDeCarga:
                        if naveGrandeDeCarga.fleetID == flota.fleetID:
                            naveGrandeDeCarga.fleetID = 0

                    for navePequenaDeCarga in self.navesPequenasDeCarga:
                        if navePequenaDeCarga.fleetID == flota.fleetID:
                            navePequenaDeCarga.fleetID = 0

                    #marcamos el id de flota a 0 para luego eliminarlo de la lista facilmente
                    flota.fleetID = 0

                    #Decrementamos el numero de flotas utilizadas
                    self.flotasUtilizadas-=1

            #sacamos de la lista de flotas todas las que ya han vuelto a casa (fleetID == 0)
            self.flotas = [x for x in self.flotas if x.fleetID>0]

            # esperamos un segundo y volveremos a actualizar el vuelo de las naves si fuese necesario
            time.sleep(1)
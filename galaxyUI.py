import time
import globalConstants
import random

from planet import *
from generalTools import *
from seleniumTools import *
from generalTools import *
from spaceship import Spaceship
from selenium.common.exceptions import StaleElementReferenceException

class GalaxyUI:

    def __init__(self, driver):
        #inicializamos el driver
        self.driver = driver

        #Navegamos a galaxia. Para seguir utilizando el objeto no deberemos navegar fuera de esta pantalla hasta que hallamos acabado o se producira un error no controlado
        self.goToGalaxy()

        print "API de galaxia inicializada"

    def goToGalaxy(self):
        navigateTo("Galaxia", self.driver)

        #cargamos configuraciones necesarias
        self.numeroDeSodasPorEspionaje = int(globalConstants.config.getAttribute("sondasPorEspiojane"))

        #inicializamos galaxia y sistema actual
        self.galaxyElement = getElementByXPath(self.driver, 10, ".//*[@id='galaxy_input']")
        self.systemElement = getElementByXPath(self.driver, 10, ".//*[@id='system_input']")
        self.galaxy = int(self.galaxyElement.get_attribute("value"))
        self.system = int(self.systemElement.get_attribute("value"))

    #clickamos el boton 'Vamos' para actualizar la galaxia
    def goGalaxy(self):
        try:
            getElementByXPath(self.driver, 10, ".//*[@id='galaxyHeader']//div[contains(text(),'Vamos')]").click()
        except StaleElementReferenceException:
            #Si intentamos buscar demasiado rapido la tabla se modifica con ajax y se genera un error asi que debemos volver a intentarlo
            self.goGalaxy()

    #devuelve True si la galaxia todavia se esta cargando
    def isGalaxyLoading(self):
        galaxyLoadingElement = getElementByXPath(self.driver, 10, ".//*[@id='galaxyLoading']")
        return galaxyLoadingElement.is_displayed()


    def waitGalaxyToLoad(self):
        #Esperamos hasta que la galaxia deje de cargarse o hayan pasado 10 segundos
        segundosEsperando = 0
        while self.isGalaxyLoading():
            segundosEsperando += 1
            time.sleep(1)
            if (segundosEsperando>=10):
                break

        if segundosEsperando >= 10:
            #El cliente nos ha desconectado. Debemos volver a conectar e ir a la galaxia que estabamos procesando antes de poder seguir con el espionage
            print "[AVISO] El cliente ha finalizado la sesion. Se procede a logear de nuevo"

            #pulsamos el boton salir
            getElementByXPath(self.driver, 10, ".//*[@id='bar']//a[contains(text(),'Salir')]").click()

            #relogeamos
            reLogin(self.driver)

            print "[AVISO] Se ha relogeado correctamente"

            #vamos a la galaxia por la que nos habiamos quedado
            galaxiaDestino = self.galaxy
            sistemaDestino = self.system
            self.goToGalaxy()
            self.updateGalaxy(sistemaDestino, galaxiaDestino)

            print "[AVISO] El sistema se ha recuperado y continua el espionaje por donde lo habia dejado"


    #navegamos a un sistema y a una galaxia concreta
    def updateGalaxy(self,system, galaxy):

        galaxiaActual = int(self.galaxyElement.get_attribute("value"))
        sistemaActual = int(self.systemElement.get_attribute("value"))

        self.galaxy = galaxy
        self.system = system

        if (galaxy == galaxiaActual and system == sistemaActual+1):
            #Solo ha cambiado el sistema uno arriba. Nos movemos utilizando la flecha del cliente. Moverse rellenando el formulario y pulsando VAMOS cada vez genera que se desconecte el cliente.
            getElementByXPath(self.driver, 10, ".//span[@onclick='submitOnKey(39);']").click()
        elif (galaxy == galaxiaActual and system == sistemaActual-1):
            #Solo ha cambiado el sistema uno abajo. Nos movemos utilizando la flecha del cliente. Moverse rellenando el formulario y pulsando VAMOS cada vez genera que se desconecte el cliente.
            getElementByXPath(self.driver, 10, ".//span[@onclick='submitOnKey(37);']").click()
        else:
            #Ha cambiado mas que solo un sistema por lo que nos movemos rellenando el formulario
            self.galaxyElement.send_keys(str(galaxy))
            self.systemElement.send_keys(str(system))
            self.goGalaxy()

        #esperamos que se cargue la nueva galaxia
        self.waitGalaxyToLoad()

    #nos movemos un sistema para arriba en el universo
    def systemUp(self):
        sistemaActualizado = False
        logPrinted = False
        while not sistemaActualizado:
            #Solo actualizamos el sistema si tenemos espacio de flota y sondas para realizar otro espionaje. Si cambiamos de sistema sin posibilidad de espiar, el cliente nocarga los botones necesarios para lanzar el espionaje
            if globalConstants.fleetControl.espacioFlotaDisponible() and globalConstants.fleetControl.probeAvailable(self.numeroDeSodasPorEspionaje):
                #primero incrementamos el sistema teniendo en cuenta que podemos cambiar de galaxia haciendolo
                self.system+=1
                if (self.system>499):
                    self.system = 1
                    self.galaxy += 1
                    if (self.galaxy>7):
                        self.galaxy = 1

                #ahora que tenemos seleccionada la galaxia y el sistema, navegamos hasta ellos
                self.updateGalaxy(self.system, self.galaxy)
                sistemaActualizado = True
            else:
                #esperamos 1 segundo a que vuelvan nuestras flotas
                if logPrinted == False:
                    print "No hay sondas o espacio de flota suficiente para realizar el espionaje. Esperando que las sondas vuelvan a la base."
                    logPrinted = True
                time.sleep(1)

    #nos movemos un sistema para abajo en el universo
    def systemDown(self):
        sistemaActualizado = False
        logPrinted = False
        while not sistemaActualizado:
            #Solo actualizamos el sistema si tenemos espacio de flota y sondas para realizar otro espionaje. Si cambiamos de sistema sin posibilidad de espiar, el cliente nocarga los botones necesarios para lanzar el espionaje
            if globalConstants.fleetControl.espacioFlotaDisponible() and globalConstants.fleetControl.probeAvailable(self.numeroDeSodasPorEspionaje):
                #primero incrementamos el sistema teniendo en cuenta que podemos cambiar de galaxia haciendolo
                self.system-=1
                if (self.system<1):
                    self.system = 499
                    self.galaxy -= 1
                    if (self.galaxy<1):
                        self.galaxy = 7

                #ahora que tenemos seleccionada la galaxia y el sistema, navegamos hasta ellos
                self.updateGalaxy(self.system, self.galaxy)
                sistemaActualizado = True
            else:
                #esperamos 1 segundo a que vuelvan nuestras flotas
                if logPrinted == False:
                    print "No hay sondas o espacio de flota suficiente para realizar el espionaje. Esperando que las sondas vuelvan a la base."
                    logPrinted = True
                time.sleep(1)

    #comprueba el estado de las sondas y si hay suficientes las lanza contra el planeta indicado. Es precondicion que el cliente se encuentre en el sistema del planeta que se pretende espiar
    def spyPlanet(self, planet):
        planetaEspiado = False
        logPrinted = False

        while not planetaEspiado:
            #primero debemos saber si tenemos sondas suficientes disponibles y espacio de flotas para poder lanzarlas
            if globalConstants.fleetControl.espacioFlotaDisponible() and globalConstants.fleetControl.probeAvailable(self.numeroDeSodasPorEspionaje):
                #podemos lanzar la flota
                globalConstants.fleetControl.sendFleet(0,0,self.numeroDeSodasPorEspionaje)

                #solo falta clickar el boton de espiar del planeta para enviar las sondas
                getElementByXPath(self.driver, 10, ".//*[@id='galaxytable']//td[contains(text(),'"+planet.name+"')]/..//a[contains(@class, 'espionage')]").click()
                print "[ESPIONAJE] Planeta espiado:",
                printPlanet(planet)
                planetaEspiado = True
                #despues de espiar un planeta esperamos entre 1 y 2 segundos para dejar tiempo al cliente (popups, etc)
                time.sleep(random.randrange(1,2,1))
            else:
                #esperamos 1 segundo a que las sondas vuelvan y a tener espacio de flota para poder enviarlas
                if logPrinted == False:
                    print "No hay sondas o espacio de flota suficiente para realizar el espionaje. Esperando que las sondas vuelvan a la base."
                    logPrinted = True
                time.sleep(1)

    #Del sistema actual espia la lista de planetas inactivos con un ranking igual o inferior al pasado por parametro dentro del radio configurado. Devuelve la lista de planetas espiados.
    def spyInactive(self, minRanking):
        try:
            listaPlanetas = []
            #recorremos la tabla de galaxia
            TablaGalaxia = getElementByXPath(self.driver, 10, "//*[@id='galaxytable']/tbody")
            planetas = TablaGalaxia.find_elements_by_xpath("tr")

            for index, planeta in enumerate(planetas):
                infosPlaneta = planeta.find_elements_by_xpath("td")
                if infosPlaneta[3].text != '':
                    if ("(I)" in infosPlaneta[7].text or "(i)" in infosPlaneta[7].text):
                        #debemos saber el ranking del player para decidir si queremos spiarlo o no. Buscammos el popup que contiene esta informacion
                        infoUser = infosPlaneta[7].find_elements_by_xpath("a")[0].get_attribute("rel")
                        #print ""+str(self.galaxy)+":"+str(self.system)+" "+infoUser
                        rank = int(getElementByXPath(self.driver, 10, ".//*[@id='"+infoUser+"']//li[@class='rank']/a").get_attribute('innerHTML'))
                        if (rank<=minRanking):
                            #el planeta esta inactivo y cumple que esta en un ranking igual o inferior al pasado por parametro. Lo espiamos y anadimos a la lista de planetas espiados.
                            planetaAEspiar = Planet(self.galaxy, self.system, index+1, infosPlaneta[7].text, infosPlaneta[3].text, rank)
                            self.spyPlanet(planetaAEspiar)
                            listaPlanetas.append(planetaAEspiar)
        except StaleElementReferenceException:
            #Si intentamos buscar demasiado rapido la tabla se modifica con ajax y se genera un error asi que debemos volver a intentarlo
            self.findInactivos(minRanking)

        return listaPlanetas

    #Recorremos la galaxia y la vamos espiando segun los criterios de configuracion
    def spyGalaxy(self):

        print "Espiando galaxia..."

        #cargamos las configuraciones necesarias para realizar el espionaje
        radioEspionaje = int(globalConstants.config.getAttribute("radioEspionaje"))
        numeroDeSodasPorEspionaje = int(globalConstants.config.getAttribute("sondasPorEspiojane"))
        minRankEspionaje = int(globalConstants.config.getAttribute("minRankEspionaje"))

        #exploramos la galaxia en el radio configurado
        self.spyInactive(minRankEspionaje)

        #exploramos hacia arriba
        for i in range(0, int(radioEspionaje), 1):
            self.systemUp()
            self.spyInactive(minRankEspionaje)


        #volvemos al sistema de nuestro planeta -1
        self.goToGalaxy()

        #exploramos hacia abajo
        for i in range(0, radioEspionaje, 1):
            self.systemDown()
            self.spyInactive(minRankEspionaje)

        print "[ESPIONAJE] Se ha FINALIZADO el espionaje de la galaxia con exito."

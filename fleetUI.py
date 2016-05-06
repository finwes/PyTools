import globalConstants
import time

from generalTools import *

class FleetUI:

    def __init__(self, driver):
        #inicializamos el driver
        self.driver = driver

        #Navegamos a galaxia. Para seguir utilizando el objeto no deberemos navegar fuera de esta pantalla hasta que hallamos acabado o se producira un error no controlado
        self.goToFleet()

        print "API de flota inicializada"

    def goToFleet(self):
        navigateTo("Flota", self.driver)

    def sendFleet(self, numSondas, numNavesPeques, numNavesGrandes, galaxy, system, planetPosition):
        #primero seteamos las naves que componen la flota

        #sondas
        if numSondas>0:
            getElementByXPath(self.driver, 10, ".//*[@id='ship_210']").send_keys(str(numSondas))
        #navesPeques
        if numNavesPeques>0:
            getElementByXPath(self.driver, 10, ".//*[@id='ship_202']").send_keys(str(numNavesPeques))
        #navesGrandes
        if numNavesGrandes>0:
            getElementByXPath(self.driver, 10, ".//*[@id='ship_203']").send_keys(str(numNavesGrandes))

        #clickamos continuar
        time.sleep(1)
        getElementByXPath(self.driver, 10, ".//*[@id='continue']").click()

        #configuramos el planeta destino de la flota
        time.sleep(1)
        sendKeysByXPath(self.driver, 10, ".//*[@id='galaxy']", str(galaxy))
        sendKeysByXPath(self.driver, 10, ".//*[@id='system']", str(system))
        sendKeysByXPath(self.driver, 10, ".//*[@id='position']", str(planetPosition))

        #clickamos continuar
        time.sleep(1)
        getElementByXPath(self.driver, 10, ".//*[@id='continue']").click()

        #seleccionamos como mision atacar
        time.sleep(1)
        getElementByXPath(self.driver, 10, ".//*[@id='missionButton1']").click()

        #lanzamos la flota
        time.sleep(1)
        getElementByXPath(self.driver, 10, ".//*[@id='start']").click()

        #la flota ya esta en el aire pero debemos notificarlo al control de flotas del Bot para que la contavilice
        globalConstants.fleetControl.sendFleet(numNavesPeques, numNavesGrandes, numSondas)

        print "[ATAQUE] Se ha enviado una flota en ataque compuesta por "+str(numSondas+numNavesPeques+numNavesGrandes)+" naves al planeta ["+str(galaxy)+":"+str(system)+":"+str(planetPosition)+"]"

        time.sleep(1)

    #se lanzan ataques contra los planetas de la lista de reports pasada por parametro con el tipo de nave pasado por parametro. 0 Naves pequenas decarga, 1 Naves grandes de carga
    def attack(self, spyReportList, shipType):
        #solo se iran lanzando ataques mientras tengamos naves suficientes y espacios de flota para hacerlo
        print "Se inicia el proceso de ATAQUE a granjas"

        for spyReport in spyReportList:
            navesGrandesNecesarias = 0
            navesPequesNecesarias = 0
            if shipType == 0:
                navesPequesNecesarias = spyReport.navesPequenasNecesarias
            else:
                navesGrandesNecesarias = spyReport.navesGrandesNecesarias

            if globalConstants.fleetControl.espacioFlotaDisponible() and globalConstants.fleetControl.fleetAvailable(0,navesPequesNecesarias,navesGrandesNecesarias):
                #si tenemos espacio de flota y naves suficientes como para lanzar la flota la lanzamos
                self.sendFleet(0, navesPequesNecesarias, navesGrandesNecesarias, spyReport.galaxy, spyReport.system, spyReport.planetPosition)

        print "El ATAQUE a granjas a acabado con exito"
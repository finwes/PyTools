import time
import random
import globalConstants

from seleniumTools import *
from generalTools import *
from spyReport import SpyReport

class MessagesUI:

    def __init__(self, driver):
        #inicializamos el driver
        self.driver = driver

        #cargamos configuraciones necesarias
        self.numeroDeSodasPorEspionaje = int(globalConstants.config.getAttribute("sondasPorEspiojane"))

        #inicializamos las listas de mensajes
        self.spyReports = []

        #Navegamos a galaxia. Para seguir utilizando el objeto no deberemos navegar fuera de esta pantalla hasta que hallamos acabado o se producira un error no controlado
        self.goToMessages()

        print "Se inicializa el sistema de gestion de mensajes"


    def goToMessages(self):

        #vamos a la pantalla de mensajes
        getElementByXPath(self.driver, 10, ".//*[@id='message-wrapper']/a[contains(@class, 'messages')]").click()

    #devuelve True si los mensajes todavia se estan cargando
    def areMessagesLoading(self):
        galaxyLoadingElement = getElementByXPath(self.driver, 10, ".//img[contains(@class,'ajax_load_img')]")
        return galaxyLoadingElement.is_displayed()

    def waitToLoad(self, tabName):
        #Esperamos hasta que se carguen los mensajes o hayan pasado 10 segundos
        segundosEsperando = 0
        while self.areMessagesLoading():
            segundosEsperando += 1
            time.sleep(1)
            if (segundosEsperando>=10):
                break

        if segundosEsperando >= 10:
            #El cliente nos ha desconectado. Debemos volver a conectar e ir a la pantalla de mensajes que queriamos ir

            #pulsamos el boton salir
            getElementByXPath(self.driver, 10, ".//*[@id='bar']//a[contains(text(),'Salir')]").click()

            #relogeamos
            reLogin(self.driver)

            #vamos a la pantalla de mensajes que queriramos ir
            self.goToMessages()
            self.goToTab(tabName)


    def goToTab(self, tabName):
        getElementByXPath(self.driver, 10, ".//div[@class='tab_ctn']//a[contains(text(), '"+tabName+"')]").click()
        self.waitToLoad(tabName)

    #parsea un report de espionaje y devuelve el objeto con la informacion que contiene
    def parseSpyReport(self, mensaje):
        msgID = int(mensaje.get_attribute("data-msg-id"))

        textoFlotas = getElementByXPath(mensaje, 10, ".//span[contains(text(),'Flotas')]").text.replace(".","")
        flotas = int (textoFlotas[textoFlotas.find(":")+1:len(textoFlotas)])

        textoDefensas = getElementByXPath(mensaje, 10, ".//span[contains(text(),'Defensa')]").text.replace(".","")
        defensas = int (textoDefensas[textoDefensas.find(":")+1:len(textoDefensas)])

        textoRecursos = getElementByXPath(mensaje, 10, ".//span[contains(text(),'Recursos')]").text.replace(".","")
        recursos = int (textoRecursos[textoRecursos.find(":")+1:len(textoRecursos)])

        textoBotin = getElementByXPath(mensaje, 10, ".//span[contains(text(),'Bot')]").text.replace(".","")
        botin = int (textoBotin[textoBotin.find(":")+1:len(textoBotin)-1])

        textoPlaneta = getElementByXPath(mensaje, 10, ".//a[@class='txt_link']").text
        textoPlaneta = textoPlaneta[textoPlaneta.find("[")+1:len(textoPlaneta)-1]

        galaxia = textoPlaneta[0:textoPlaneta.find(":")]
        textoPlaneta = textoPlaneta[textoPlaneta.find(":")+1:len(textoPlaneta)]
        sistema = textoPlaneta[0:textoPlaneta.find(":")]
        posicionPlaneta = textoPlaneta[textoPlaneta.find(":")+1:len(textoPlaneta)]

        return SpyReport(msgID, flotas, defensas, recursos, botin, galaxia, sistema, posicionPlaneta)

    def refreshSpyReport(self, idReport):
        reportRefrescado = False
        logPrinted = False
        while not reportRefrescado:
            #primero debemos saber si tenemos sondas suficientes disponibles y espacio de flotas para poder lanzarlas
            if globalConstants.fleetControl.espacioFlotaDisponible() and globalConstants.fleetControl.probeAvailable(self.numeroDeSodasPorEspionaje):
                #podemos lanzar la flota de sondas
                globalConstants.fleetControl.sendFleet(0,0,self.numeroDeSodasPorEspionaje)

                #solo falta clickar el boton de espiar del planeta para enviar las sondas
                getElementByXPath(self.driver, 10, ".//li[@data-msg-id='"+str(idReport)+"']//a[contains(@onclick, 'sendShipsWithPopup')]").click()
                #despues de espiar un planeta esperamos entre 1 y 2 segundos para dejar tiempo al cliente (popups, etc)
                time.sleep(1)
                #Ahora borramos el repor antiguo
                getElementByXPath(self.driver, 10, ".//li[@data-msg-id='"+str(idReport)+"']//a[@class = 'fright']").click()
                #esperamos 1 segundo
                time.sleep(1)
                reportRefrescado = True

                print "[ESPIONAJE] Se han lanzado sondas para refrescar el report y se ha borrado el report antiguo con id "+str(idReport)

            else:
                #esperamos 1 segundo a que las sondas vuelvan y a tener espacio de flota para poder enviarlas
                if logPrinted == False:
                    print "No hay sondas o espacio de flota suficiente para realizar el espionaje. Esperando que las sondas vuelvan a la base."
                    logPrinted = True
                time.sleep(1)

    def refreshSpyReports(self):

        print "Se procede a lanzar nuevos espionajes contra todos los planetas espiados anteriormente"

        self.goToTab("Espionaje")
        for report in self.spyReports:
            self.refreshSpyReport(report.msgID)

        #esperamos que vuelvan todas las sondas que todavia esten volando
        print "Esperando que vuelvan las sondas para analizar los nuevos reports (90 secs aprox)..."
        globalConstants.fleetControl.waitForSpyProbes()

        #recargamos la pantalla para que aparezcan los nuevos reports
        self.goToMessages()
        self.goToTab("Espionaje")

        #recargamos la lista de reports con los nuevos reports
        self.populateSpyReports()

    #elimina todos los reports que no son utiles de la lista de msgs
    def deleteNonUsefulMsgs(self):
        #Eliminamos los reports de espionajes que nos han hecho a nosotros. Solo nos interesan los que nosotros hemos enviado

        print "Se eliminan los mensajes que no son reports de espionaje o de planetas destruidos"

        mensajes = self.driver.find_elements_by_xpath(".//span[contains(text(),'Acci')]//..//a[@class='fright']")
        mensajes.extend(self.driver.find_elements_by_xpath(".//span[contains(text(),'destruido')]//..//a[@class='fright']"))
        for mensaje in mensajes:
            if mensaje.is_displayed():
                mensaje.click()
                time.sleep(1)

    def populateSpyReports(self):

        print "Se procede a parsear la lista de reports de espionaje"

        self.goToTab("Espionaje")
        self.spyReports = []

        #Antes de empezar a parsear los mensajes de espionaje, eliminamos los posibles espionajes que nos hayan hecho a nosotors
        self.deleteNonUsefulMsgs()

        mensajes = self.driver.find_elements_by_xpath(".//li[not(contains(@class,'no_msg'))][contains(@class,'msg')]")
        for mensaje in mensajes:
            if mensaje.is_displayed():
                spyReport = self.parseSpyReport(mensaje)
                self.spyReports.append(spyReport)

        #ordenamos la lista de reports segun el botin disponible en cada planeta
        self.spyReports.sort(key=lambda x: x.botinPosible, reverse=True)

        print "Todos los reports de espionaje han sido parseados correctamente"

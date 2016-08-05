import globalConstants
import generalTools
import os

from galaxyUI import *
from generalTools import *
from seleniumTools import *
from selenium import webdriver
from messagesUI import *
from fleetUI import *
from galaxyUI import *

#Esta funcion realiza todo lo necesario para espiar la galaxia segun las configuraciones
def spyGalaxy(driver):
    #inicializamos la galaxia
    galaxia = GalaxyUI(driver)
    #espiamos
    galaxia.spyGalaxy()

#Esta funcion realiza todo lo necesario para atacar a las granjas (lista de reports de espionajes en la lista de mensajes)
def atacarGranjas(driver, refrescarReports):
    #Atacar granjas
    messages = MessagesUI(driver)
    messages.populateSpyReports()

    if refrescarReports:
        #refrescamos los reports que tengamos con nuevos espionajes
        messages.refreshSpyReports()

    #Ya tenemos reports con datos nuevos y ordenados de mas recursos a menos. Ahora podemos lanzar los ataques contra las granjas.
    fleetUI = FleetUI(driver)

    #lanzamos los ataques
    tipoNaves = int(globalConstants.config.getAttribute("tipoNavesAtaques"))
    fleetUI.attack(messages.spyReports, tipoNaves)

# Esta funcion reconfigura el Bot en base a las naves y configuraciones de ogame que tengamos
def refreshConfig(driver):
    # Navegamos por el cliente de Ogame para obtener la informacion necesaria de configuracion (Numero de sondas que se envian al espiar, naves pequenas de carga y naves grandes de carga)

    #Recuperamos el numero de sondas que enviamos al espiar
    getElementByXPath(driver, 10, ".//*[@id='bar']//a[contains(text(),'Opciones')]").click()
    getElementById(driver,10,"tabGeneral").click()
    getElementByXPath(driver, 10, ".//*[@id='two']//label[contains(text(),'Sondas de espionaje')]/..").click()
    numeroDeSondasElement = getElementByXPath(driver, 10, ".//*[@id='two']//input[@name='spio_anz']")
    globalConstants.config.setAttribute("sondasPorEspiojane", numeroDeSondasElement.get_attribute("value"))

    #Grabamos la nueva configuracion
    globalConstants.config.save()

    print "Configuracion automatica actualizada correctamente"

def login(server, login, password):
    globalConstants.server = server
    globalConstants.login = login
    globalConstants.password = password

    #recuperamos el driver
    if os.name=='posix':
        #Driver para linux
        driver = webdriver.Chrome("./browserDrivers/chromedriver")
    else:
        #Driver para windows
        driver = webdriver.Chrome("./browserDrivers/chromedriver.exe")
    #driver = webdriver.Firefox()

    driver.maximize_window()
    driver.get("https://es.ogame.gameforge.com/")

    #realizamos el login a la aplicacion
    reLogin(driver)

    print "Se ha realizado el LOGIN correctamente"

    #devolvemos el driver
    return driver

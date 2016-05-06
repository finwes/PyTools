import globalConstants
import time

from seleniumTools import *
from selenium.webdriver.support.select import Select

def navigateTo(menuName, driver):
    getElementByXPath(driver, 10, ".//*[@id='links']//a[span='"+menuName+"']").click()

def printPlanet(planeta):
    print "["+str(planeta.galaxy)+":"+str(planeta.system)+":"+str(planeta.position)+"] "+planeta.name + " - "+planeta.user + " ("+str(planeta.rank)+")"

def printPlanets(listaPlanetas):
    for planeta in listaPlanetas:
        printPlanet(planeta)

def goToPlanet(name, driver):
    try:
        planetXpath = ".//*[@id='planetList']//a[span='"+name+"']"
        planeta = getElementByXPath(driver, 10, planetXpath)
        planeta.click()
    except Exception:
        raise Exception('No se encuentra el planeta con nombre '+name+'. Revise la configuracion del BOT.')

def checkLogin(driver):
    #Buscamos la lista de planetas, si no la encontramos es que el login ha fallado y podemos lanzar la excepcion correspondiente
    try:
        planetXpath = ".//*[@id='planetList']"
        planeta = getElementByXPath(driver, 10, planetXpath)
        return True
    except Exception:
        raise Exception('Login o Password incorrectos')

def reLogin(driver):

    serverFieldElement =  getElementById(driver, 10, "serverLogin")
    loginFieldElement = getElementById(driver, 10, "usernameLogin")
    passFieldElement = getElementById(driver, 10, "passwordLogin")
    loginButtonElement = getElementById(driver, 10, "loginSubmit")

    if not serverFieldElement.is_displayed():
        getElementById(driver, 10, "loginBtn").click()

    try:
        Select(serverFieldElement).select_by_visible_text(globalConstants.server)
    except Exception:
        raise Exception('El servidor '+globalConstants.server+' no existe. Reintentelo con un servidor valido.')
    loginFieldElement.clear()
    loginFieldElement.send_keys(globalConstants.login)

    passFieldElement.clear()
    passFieldElement.send_keys(globalConstants.password)

    loginButtonElement.click()

    checkLogin(driver)

    #Despues de logear vamos directamente al planeta que se tenga configurado ya que el resto de funcionalidades se haran desde este planeta
    goToPlanet(globalConstants.config.getAttribute("nombrePlaneta"), driver)

    time.sleep(1)

import globalConstants
import oGameTools
import sys

from spaceship import *
from fleetControl import *
from messagesUI import *
from fleetUI import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

def main():

    #inicializamos las variables Globales
    globalConstants.init()

    try:

        if len(sys.argv) == 7:
            server = sys.argv[1]
            login = sys.argv[2]
            password = sys.argv[3]
            espiarGalaxia = sys.argv[4]=='1'
            atacarGranjas = sys.argv[5]=='1'
            refrescarConfiguracion = sys.argv[6]=='1'

            print "Iniciando procesos de OgameBOT"
            #Obtenemos el driver que utilizaremos para el resto de funcionalidades
            #driver = oGameTools.login("Antares", "zan", "01630163")
            driver = oGameTools.login(server, login, password)

            if refrescarConfiguracion:
                oGameTools.refreshConfig(driver)

            if espiarGalaxia or atacarGranjas:

                #Inicializamos el control de flotas (sin el control de flotas inicializado nada funciona)
                globalConstants.fleetControl = FleetControl(driver)

                if espiarGalaxia:
                    oGameTools.spyGalaxy(driver)

                if atacarGranjas:
                    oGameTools.atacarGranjas(driver, True)


            globalConstants.running = False
            print "Todos los procesos han acabado correctamente."
        else:
            print "Error en el uso del BOT:"
            print "USO: python main.py server login password espiarGalaxia atacarGranjas refrescarConfiguracion"
            print "En donde:"
            print " server: Server de la cuenta Ogame"
            print " longin: Login de la cuenta Ogame"
            print " password: Password de la cuenta Ogame"
            print " espiarGalaxia: 0 si no se quiere espiar la galaxia, 1 si se quiere espiar la galaxia"
            print " atacarGranjas: 0 si no se quiere atacar las granjas, 1 si se quiere atacar las granjas"
            print " refrescarConfiguracion: 0 si no se quiere refrescar la configuracion automatica, 1 si se quiere refrescar la configuracion automatica"
    except Exception as error:
        print('Se ha producido un error: ' + error.message)
        globalConstants.running = False

if __name__ == "__main__": main()





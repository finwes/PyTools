import time
from selenium.webdriver.support.ui import WebDriverWait

def getElementById(elementFrom, timeout, id):
    reintentos = 0
    element = None
    conseguido = False
    excepcion = None
    while not conseguido and reintentos<3:
        try:
            element = WebDriverWait(elementFrom, timeout).until(lambda elementFrom: elementFrom.find_element_by_id(id))
            conseguido = True
            reintentos+=1
        except Exception as error:
            print "ERROR: Al recuperar un elemento. Reintento: "+str(reintentos)
            excepcion = error
            reintentos+=1
            #Esperamos 2 segundos para ver si le da tiempo al cliente a cargar el elemento que ha fallado en cargar
            time.sleep(2)
    if not conseguido:
        raise excepcion
    return element

def getElementByXPath(elementFrom, timeout, XPath):
    reintentos = 0
    element = None
    conseguido = False
    excepcion = None
    while not conseguido and reintentos<3:
        try:
            element = WebDriverWait(elementFrom, timeout).until(lambda elementFrom: elementFrom.find_element_by_xpath(XPath))
            conseguido = True
            reintentos+=1
        except Exception as error:
            print "ERROR: Al recuperar un elemento. Reintento: "+str(reintentos)
            excepcion = error
            reintentos+=1
            #Esperamos 2 segundos para ver si le da tiempo al cliente a cargar el elemento que ha fallado en cargar
            time.sleep(2)
    if not conseguido:
        raise excepcion
    return element

def sendKeysByXPath(elementFrom, timeout, XPath, keys):
    reintentos = 0
    element = None
    conseguido = False
    excepcion = None
    while not conseguido and reintentos<3:
        try:
            element = getElementByXPath(elementFrom, timeout, XPath)
            element.clear()
            element.send_keys(keys)
            conseguido = True
            reintentos+=1
        except Exception as error:
            print "ERROR: Al enviar teclas a un elemento. Reintento: "+str(reintentos)
            excepcion = error
            reintentos+=1
            #Esperamos 2 segundos para ver si le da tiempo al cliente a cargar el elemento que ha fallado en cargar
            time.sleep(2)
    if not conseguido:
        raise excepcion
    return element

def getElementsByXPath(elementFrom, timeout, XPath):
    reintentos = 0
    elements = None
    conseguido = False
    excepcion = None
    while not conseguido and reintentos<3:
        try:
            elements = WebDriverWait(elementFrom, timeout).until(lambda elementFrom: elementFrom.find_elements_by_xpath(XPath))
            conseguido = True
            reintentos+=1
        except Exception as error:
            print "ERROR: Al recuperar un elemento. Reintento: "+str(reintentos)
            excepcion = error
            reintentos+=1
            #Esperamos 2 segundos para ver si le da tiempo al cliente a cargar el elemento que ha fallado en cargar
            time.sleep(2)
    if not conseguido:
        raise excepcion
    return elements

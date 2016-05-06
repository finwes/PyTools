from selenium.webdriver.support.ui import WebDriverWait

def getElementById(elementFrom, timeout, id):
    return WebDriverWait(elementFrom, timeout).until(lambda elementFrom: elementFrom.find_element_by_id(id))

def getElementByXPath(elementFrom, timeout, XPath):
    return WebDriverWait(elementFrom, timeout).until(lambda elementFrom: elementFrom.find_element_by_xpath(XPath))

def sendKeysByXPath(elementFrom, timeout, XPath, keys):
    element = getElementByXPath(elementFrom, timeout, XPath)
    element.clear()
    element.send_keys(keys)

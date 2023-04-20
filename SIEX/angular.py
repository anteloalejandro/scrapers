from time import sleep
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By

# Drivers para chrome y otros navegadores basados en chromium
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

# Drivers para Edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager as EdgeDriverManager

# Drivers para firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


# VARIABLES
url = 'https://www3.sede.fega.gob.es/bdcsixpor/mantenimiento-de-tablas'

list_selector =     '.menu_hijos'
link_selector =     'p-panelmenusub .p-menuitem'
boton_selector =    'app-boton-exportar button'
cerrar_selector =   'p-dialog button.p-dialog-header-close'

class AngularSpider(scrapy.Spider):
    name = 'angular_spider'
    start_urls = [ url ]

    # Inicializar webdriver
    def __init__(self):

        ## Firefox
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service = service)

        ## Chromium (sin testear)
        # service = ChromeService(ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(service = service)

        ## Edge (sin testear)
        # service = EdgeService(EdgeDriverManager().install())
        # self.driver = webdriver.Edge(service = service)

        ## Chromium (sin testear)
        # service = ChromeService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        # self.driver = webdriver.Chrome(service = service)

        ## Brave (sin testear)
        # service = ChromeService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
        # self.driver = webdriver.Chrome(service = service)

        # if (profile):
        #     profile.set_preference("browser.download.folderList", 2)
        #     profile.set_preference("browser.download.dir", '<ruta a la carpeta de descarga>')

    # Ejecutar el código principal por cada una de las URLs
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    # Devuelve WebElements. Reintenta periódicamente si no los encuentra.
    def find(self, selector, parent = None):
        max_tries = 20
        sleep_time = .05
        element = parent
        if (element == None): element = self.driver

        elements = element.find_elements(By.CSS_SELECTOR, selector)
        while (len(elements) == 0 and max_tries > 0):
            max_tries -= 1
            print('\n\n Could not find any elements, trying again \n\n')
            sleep(sleep_time)
            element.find_elements(By.CSS_SELECTOR, selector)

        return elements

    # Devuleve o un WebElement o None si no existe
    def findOne(self, selector, parent = None):
        elements = self.find(selector, parent)
        if len(elements) > 0:
            return elements[0]
        else:
            return None

    # Recorre la página y ejecuta el código principal
    def parse(self, response):
        self.driver.get(response.url)

        sleep(1)
        elements = self.find(list_selector)
        for element in elements:
            element.click()
            links = self.find(link_selector, element)

            for link in links:
                link.click()

                boton = self.findOne(boton_selector)
                if (boton): boton.click()

                cerrar = self.findOne(cerrar_selector)
                if (cerrar): cerrar.click()

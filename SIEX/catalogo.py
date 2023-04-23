from time import sleep
import os
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
from selenium.webdriver.firefox.options import Options as FirefoxOptions


# VARIABLES
url = 'https://www3.sede.fega.gob.es/bdcsixpor/mantenimiento-de-tablas'

list_selector =         '.menu_hijos'
list_name_selector =    '.p-menuitem-text'
link_selector =         'p-panelmenusub .p-menuitem'
boton_selector =        'app-boton-exportar button'
cerrar_selector =       'p-dialog button.p-dialog-header-close'

class CatalogoSpider(scrapy.Spider):
    name = 'catalogo_spider'
    start_urls = [ url ]
    last_file_list = []

    # Inicializar webdriver
    def __init__(self):

        # Directorio de descarga
        script_name = os.path.basename(os.path.splitext(__file__)[0])
        self.download_dir = os.path.dirname(__file__) + '/downloads/' + script_name
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)

        # Configuración de firefox
        firefox_options = FirefoxOptions()
        if firefox_options:
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.dir", self.download_dir)

        # Firefox
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service = service, options=firefox_options)

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

    # Ejecutar el código principal por cada una de las URLs
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    # Devuelve WebElements. Reintenta periódicamente si no los encuentra.
    def find(self, selector, parent = None):
        max_tries = 20
        sleep_time = .05
        element = parent if parent else self.driver

        elements = element.find_elements(By.CSS_SELECTOR, selector)
        while (len(elements) == 0 and max_tries > 0):
            max_tries -= 1
            print('\n\n No se han encontrado elementos, intentando de nuevo \n\n')
            sleep(sleep_time)
            element.find_elements(By.CSS_SELECTOR, selector)

        if max_tries <= 0: print('\n\n Intentos máximos superados \n\n')

        return elements

    # Devuleve un WebElement o None si no existe
    def findOne(self, selector, parent = None):
        elements = self.find(selector, parent)
        return elements[0] if len(elements) > 0 else None

    def moveLast(self, dir):
        max_tries = 100
        sleep_time = .5

        # Directorio en el que se guardará
        target_dir = self.download_dir + '/' + dir
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        # Sacar archivos en la carpeta de descargas
        files = []
        last_file = ''

        found_file = False

        while max_tries > 0:
            max_tries -= 1
            sleep(sleep_time)

            # Obtener lista de ficheros
            files = [f for f in os.listdir(self.download_dir) if os.path.isfile(os.path.join(self.download_dir, f))]
            files.sort(key = lambda x: os.stat(self.download_dir + '/' + x).st_mtime)

            # Comprobar si se ha descargado
            last_file = files[len(files) - 1]
            if last_file not in self.last_file_list:
                found_file = True
                break

        # Si no se ha descargado, para
        if not found_file:
            self.last_file_list = files
            return False

        # Borrar archivo de la lista antes de guardarla
        files.remove(last_file)
        self.last_file_list = files

        # Mover archivo
        old_path = self.download_dir + '/' + last_file
        new_path = target_dir + '/' + last_file
        os.rename(old_path, new_path)

        return True


    # Recorre la página y ejecuta el código principal
    def parse(self, response):
        self.driver.get(response.url)

        sleep(1)
        elements = self.find(list_selector)
        for element in elements:
            nameElement = self.findOne(list_name_selector, element)
            name = nameElement.text if nameElement else 'no_name'
            element.click()
            links = self.find(link_selector, element)

            for link in links:
                link.click()

                boton = self.findOne(boton_selector)
                if (boton):
                    boton.click()
                    self.moveLast(name)

                cerrar = self.findOne(cerrar_selector)
                if (cerrar): cerrar.click()

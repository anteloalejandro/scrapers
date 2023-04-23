from time import sleep
from platform import system
from os.path import join
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

system = system()
browser_paths = {
    'brave': {
        'Linux': '/usr/bin/brave-browser',
        'Windows': "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe",
        'MacOS': '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    },
    'chromium': {
        'Linux': '/usr/bin/chromium-browser',
        'Windows': 'C:/Users/'+os.getlogin()+'/AppData/Local/Chromium/Application/chrome.exe',
        'MacOS': '/Applications/Chromium Browser.app/Contents/MacOS/Chromium Browser'
    }
}

parent_selector =       'p-panelmenu'
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
    def __init__(self, browser):

        # Directorio de descarga
        script_name = os.path.basename(os.path.splitext(__file__)[0])
        self.download_dir = join(join(os.path.dirname(__file__), 'downloads' ), script_name)
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)

        # Configuración de firefox
        firefox_options = FirefoxOptions()
        if firefox_options:
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.dir", self.download_dir)

        # Configuración de chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        })

        # Configuración de Edge
        edge_options = webdriver.EdgeOptions()
        edge_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        })

        # Firefox
        if (browser == 'firefox'):
            service = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service = service, options=firefox_options)
        # Chrome (sin testear)
        elif (browser == 'chrome'):
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service = service, chrome_options=chrome_options)
        # Edge (sin testear)
        elif (browser == 'edge'):
            service = EdgeService(EdgeDriverManager().install())
            self.driver = webdriver.Edge(service = service, options=edge_options)
        # Chromium (sin testear)
        elif (browser == 'chromium'):
            service = ChromeService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            chromium_paths = browser_paths.get('chromium')
            if chromium_paths:
                chromium_install = chromium_paths.get(str(system))
                chrome_options.binary_location = chromium_install if chromium_install else ''
            self.driver = webdriver.Chrome(service = service, chrome_options=chrome_options)
        # Brave (sin testear)
        elif (browser == 'brave'):
            service = ChromeService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
            brave_paths = browser_paths.get('brave')
            if brave_paths:
                brave_install = brave_paths.get(str(system))
                chrome_options.binary_location = brave_install if brave_install else ''
            self.driver = webdriver.Chrome(service = service, chrome_options=chrome_options)
        else:
            raise ValueError('Navegador no soportado')


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
        target_dir = join(self.download_dir, dir)
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
            files = [f for f in os.listdir(self.download_dir) if os.path.isfile(join(self.download_dir, f))]
            files.sort(key = lambda x: os.stat(join(self.download_dir, x)).st_mtime)

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
        old_path = join(self.download_dir, last_file)
        new_path = join(target_dir, last_file)
        # En Linux/Unix mover sobreescribe, en Windows no
        if os.path.isfile(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)

        return True


    # Recorre la página y ejecuta el código principal
    def parse(self, response):
        self.driver.get(response.url)

        # Evitar página de error 404 cuando el navegador es lento
        sleep(1)
        while self.driver.current_url != response.url:
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

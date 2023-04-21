# Descripción

Scrapers hechos en python.

## Scrapers disponibles

### catalogo

Ruta: `SIEX/catalogo.py`.

Obtiene todos los CSVs automáticamente del sitio web <https://www3.sede.fega.gob.es/bdcsixpor/mantenimiento-de-tablas>.

Descarga los archivos en `SIEX/downloads/catalogo`.

# Dependencias

- `python3`
- `scrapy`
- `selenium`
- `webdriver-manager`
- Uno de los siguienes navegadores:
	- Firefox
	- Chromium (sin testear)
	- Chrome (sin testear)
	- Brave (sin testear)
	- Edge (sin testear)

# Instalación

**Instalar Python**  
<https://www.python.org/>

**Instalar Dependencias**  
```sh
pip install scrapy selenium webdriver-manager
```

**Instalar Firefox (u otro navegador soportado)**  
<https://www.mozilla.org/es-ES/firefox/new/>

_Si se pretende usar los scripts con alguno de los navegadores no soportados, será necesario modificar el código fuente para que algunos de ellos funcionen_

# Uso

```sh
python3 main.py {scraper}
```

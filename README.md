# Descripción

Scrapers hechos en python.

## Scrapers disponibles

- SIEX/catalogo: Obtiene todos los CSVs automáticamente del sitio web <https://www3.sede.fega.gob.es/bdcsixpor/mantenimiento-de-tablas>

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

**Instalar Firefox (u otro navegador soportado)* 

# Uso

```sh
python3 main.py {scraper}
```

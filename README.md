# Scrapping-Inmobiliaria
Se trata de un proyecto personal para practicar Web Scrapping. El proyecto consta de varias partes: extracción y depuración de datos, analisis y visualización, e informe.

# Descripción
El archivo "extraccion_datos_granada_depurados.py" es un algoritmo que se encarga de obtener datos del portal inmobiliario YaEncontre concretamente de una ciudad (Granada). 
Además, está configurado para que descarte aquellos anuncios repetidos, obteniendo una base de datos con los registros filtrados y con un formato de datos concreto.
Variables:
id, enlace_anuncio, titulo, barrio, precio, número habitaciones, número de baños, metros cuadrados. 
Además de variables dicotomicas binomiales (sí o no):
aire acondicionado, balcon, calefacción, garaje, piscina, chimenea, trastero, jardín y terraza.

Se han utilizado las siguientes librerias:
BeautifulSoup
requests
csv

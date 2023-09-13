from bs4 import BeautifulSoup
import requests
import re


# ---------------------------------------------------------
# VARIABLES
#---------------------------------------------------------
# 1. Obtener el HTML
URL_BASE = 'https://www.yaencontre.com/venta/casas/granada'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

# 2. "Parsear" ese HTML
soup1 = BeautifulSoup(html_obtenido, "html.parser")

type(soup1)

# EXTRAER CADA ANUNCIO
# EXTRAER DATOS DE LAS CASAS
divs = soup1.find_all('div', class_='content')

# Variables auxiliares
contador_anuncios = 1
pagina = 1

# LISTAS
enlaces_anuncios = []
casas = []
titulo = ''
barrios = []
barrio = ''
precios = []
precio = ''

#Propiedades de la casa
ids = []
habitaciones = []
habitacion = ''
banos = []
bano = ''
m_cuad = []
metros = ''

# Equipamiento de la casa (Categoricos Binomiales)
#Aire acondicionado
aires = []
aire = ''
#Balcón
balcones = []
balcon = ''
#Calefacción
calefacciones = []
calefaccion = ''
#Garaje
garajes = []
garaje = ''
#Piscina
piscinas = []
piscina = ''
#Chimenea
chimeneas = []
chimenea = ''
#Trastero
trasteros = []
trastero = ''
#Jardín
jardines = []
jardín = ''
#Terraza
terrazas = []
terraza = ''

# Comprobador de anuncios repetidos
anuncio_repetido = False

# Obtener el número total de páginas
paginas = int(soup1.find('div', class_='paginator').find_all('a')[-1].text)

# Iterar sobre las páginas
while pagina <= paginas:
    if pagina == 1:
                # Obtener la URL de la página actual
        URL_PAGINA = URL_BASE

        # Obtener el HTML de la página actual
        pedido_obtenido = requests.get(URL_PAGINA)
        html_obtenido = pedido_obtenido.text

        # Parsear el HTML de la página actual
        soup2 = BeautifulSoup(html_obtenido, "html.parser")

        # Extraer los datos de los artículos de la página actual
        for div in soup2.find_all('div', class_='content'):
            if (div.h3 is not None):
                # Obtener la URL del anuncio
                enlace = div.h3.a['href']
                enlaces_anuncios.append(enlace)

                # EXTRACIÓN DE DATOS DEL PROPIO ANUNCIO
                # 1. Obtener el HTML
                URL_ANUNCIO = URL_PAGINA.replace('/venta/casas/granada', '') + enlace
                anuncio_obtenido = requests.get(URL_ANUNCIO)
                html_anuncio_obtenido = anuncio_obtenido.text

                # 2. "Parsear" ese HTML
                soup2 = BeautifulSoup(html_anuncio_obtenido, "html.parser")

                type(soup2)

                # 3. EXTRAER DATOS DEL ANUNCIO
                if not casas or (len(casas) < 1):
                    main_anuncio = soup2.find('main', class_='details-info')
                    if main_anuncio:
                        # 1- Extraer título
                        titulo = main_anuncio.h1.get_text(strip=True)
                        # 2- Extraer barrio
                        div_barrio = main_anuncio.find('div', class_='details-address')
                        barrio = div_barrio.get_text(strip=True)
                        # 3- Extraer precio
                        section_details_header = main_anuncio.find('section', class_='details-header-info')
                        div_info_header = section_details_header.find('div', class_='info-header')
                        div_price = div_info_header.find('div', class_='price-wrapper')
                        precio = div_price.span.get_text(strip=True).replace(' €', '').replace('.', '')
                        # 4- Extraer habitaciones
                        div_icon_group = section_details_header.find('div', class_='iconGroup')
                        if (div_icon_group is not None):
                            div_icon_room = div_icon_group.find('div', class_='icon-room')
                            if div_icon_room is not None:  
                                habitacion = div_icon_room.span.get_text(strip=True)
                            # 5- Baños
                            div_icon_bath = div_icon_group.find('div', class_='icon-bath')
                            if div_icon_bath is not None:
                                bano = div_icon_bath.span.get_text(strip=True)
                            # 6- Metros cuadrados
                            div_icon_meter = div_icon_group.find('div', class_='icon-meter')
                            if div_icon_bath is not None:
                                metros = div_icon_group.find('div', class_='icon-meter').span.get_text(strip=True).replace(' m²', '').replace('.', '')

                            # 7- Equipamiento
                            section_equipamiento = main_anuncio.find('section', class_='separator', id='sticky-bar-limit-desktop')
                            if (section_equipamiento is not None):
                                equipamiento_texto = section_equipamiento.get_text(strip=True)
                                #7.1 - Comprobar si hay Aire Acondicionado
                                aire = "Sí" if "Aire acondicionado" in equipamiento_texto else "No"
                                #7.2 - Comprobar si hay Balcón
                                balcon = "Sí" if "Balcón" in equipamiento_texto else "No"
                                #7.3 - Comprobar si hay Calefacción
                                calefaccion = "Sí" if "Calefacción" in equipamiento_texto else "No"
                                #7.4 - Comprobar si hay Garaje
                                garaje = "Sí" if "Garaje" in equipamiento_texto else "No"
                                #7.5 - Comprobar si hay Piscina
                                piscina = "Sí" if "Piscina" in equipamiento_texto else "No"
                                #7.6 - Comprobar si hay Chimenea
                                chimenea = "Sí" if "Chimenea" in equipamiento_texto else "No"
                                #7.7 - Comprobar si hay Trastero
                                trastero = "Sí" if "Trastero" in equipamiento_texto else "No"
                                #7.8 - Comprobar si hay Jardín
                                jardin = "Sí" if "Jardín" in equipamiento_texto else "No"
                                #7.9 - Comprobar si hay Terraza
                                terraza = "Sí" if "Terraza" in equipamiento_texto else "No"

                            # Guardar datos e imprimir por consola
                            print(f'{contador_anuncios}- titulo: {titulo:<15} | barrio: {barrio} | precio: {precio} | \n'
                                f'habitaciones: {habitacion} | baños: {bano} | metros cuadrados: {metros} | aire: {aire} | \n'
                                f'balcon: {balcon} | calefacción: {calefaccion} | garaje: {garaje} | piscina: {piscina} | \n'
                                f'chimenea: {chimenea} | trastero: {trastero} | jardin: {jardin} | terraza: {terraza}')
                            ids.append(contador_anuncios)
                            casas.append(titulo)
                            barrios.append(barrio)
                            precios.append(precio)
                            habitaciones.append(habitacion)
                            banos.append(bano)
                            m_cuad.append(metros)
                            aires.append(aire)
                            balcones.append(balcon)
                            calefacciones.append(calefaccion)
                            garajes.append(garaje)
                            piscinas.append(piscina)
                            chimeneas.append(chimenea)
                            trasteros.append(trastero)
                            jardines.append(jardin)
                            terrazas.append(terraza)  

                            contador_anuncios += 1

                else:
                    anuncio_repetido = False
                    main_anuncio = soup2.find('main', class_='details-info')
                    if main_anuncio:
                        # 1- Extraer título
                        titulo = main_anuncio.h1.get_text(strip=True)
                        # 2- Extraer barrio
                        div_barrio = main_anuncio.find('div', class_='details-address')
                        barrio = div_barrio.get_text(strip=True)
                        # 3- Extraer precio
                        section_details_header = main_anuncio.find('section', class_='details-header-info')
                        div_info_header = section_details_header.find('div', class_='info-header')
                        div_price = div_info_header.find('div', class_='price-wrapper')
                        precio = div_price.span.get_text(strip=True).replace(' €', '').replace('.', '')
                        # 4- Extraer habitaciones
                        div_icon_group = section_details_header.find('div', class_='iconGroup')
                        if (div_icon_group is not None):
                            div_icon_room = div_icon_group.find('div', class_='icon-room')
                            if div_icon_room is not None:  
                                habitacion = div_icon_room.span.get_text(strip=True)
                            # 5- Baños
                            div_icon_bath = div_icon_group.find('div', class_='icon-bath')
                            if div_icon_bath is not None:
                                bano = div_icon_bath.span.get_text(strip=True)
                            # 6- Metros cuadrados
                            div_icon_meter = div_icon_group.find('div', class_='icon-meter')
                            if div_icon_bath is not None:
                                metros = div_icon_group.find('div', class_='icon-meter').span.get_text(strip=True).replace(' m²', '').replace('.', '')

                            # 7- Equipamiento
                            section_equipamiento = main_anuncio.find('section', class_='separator', id='sticky-bar-limit-desktop')
                            if (section_equipamiento is not None):
                                equipamiento_texto = section_equipamiento.get_text(strip=True)
                                #7.1 - Comprobar si hay Aire Acondicionado
                                aire = "Sí" if "Aire acondicionado" in equipamiento_texto else "No"
                                #7.2 - Comprobar si hay Balcón
                                balcon = "Sí" if "Balcón" in equipamiento_texto else "No"
                                #7.3 - Comprobar si hay Calefacción
                                calefaccion = "Sí" if "Calefacción" in equipamiento_texto else "No"
                                #7.4 - Comprobar si hay Garaje
                                garaje = "Sí" if "Garaje" in equipamiento_texto else "No"
                                #7.5 - Comprobar si hay Piscina
                                piscina = "Sí" if "Piscina" in equipamiento_texto else "No"
                                #7.6 - Comprobar si hay Chimenea
                                chimenea = "Sí" if "Chimenea" in equipamiento_texto else "No"
                                #7.7 - Comprobar si hay Trastero
                                trastero = "Sí" if "Trastero" in equipamiento_texto else "No"
                                #7.8 - Comprobar si hay Jardín
                                jardin = "Sí" if "Jardín" in equipamiento_texto else "No"
                                #7.9 - Comprobar si hay Terraza
                                terraza = "Sí" if "Terraza" in equipamiento_texto else "No"
                    
                    # Guardar en un "string" el anuncio que se esta extrayendo actualmente
                    anuncio_actual_str = (
                        f'{titulo}_{barrio}_{precio}_'
                        f'{habitacion}_{bano}_{metros}_'
                        f'{aire}_{balcon}_{calefaccion}_'
                        f'{garaje}_{piscina}_{chimenea}_'
                        f'{trastero}_{jardin}_{terraza}'
                    )

                    # Recorremos cada elemento de cada lista en la posición i para obtener el "string" del anuncio que ya tenemos guardado
                    for i in range(len(casas)):
                        # Añadir anuncio a anuncios unicos
                        anuncio_guardado_str = (
                                f'{casas[i]}_{barrios[i]}_{precios[i]}_'
                                f'{habitaciones[i]}_{banos[i]}_{m_cuad[i]}_'
                                f'{aires[i]}_{balcones[i]}_{calefacciones[i]}_'
                                f'{garajes[i]}_{piscinas[i]}_{chimeneas[i]}_'
                                f'{trasteros[i]}_{jardines[i]}_{terrazas[i]}'
                            )
    
                        # Verifica si el anuncio ya existe en el conjunto de anuncios
                        if anuncio_guardado_str == anuncio_actual_str:
                            anuncio_repetido = True
                            break
                        else:
                            anuncio_repetido = False

                    # En caso de que el anuncio no este repetido se guardará el actual, si no, no
                    if anuncio_repetido == False:
                        # Guardar datos e imprimir por consola
                        print(f'{contador_anuncios}- titulo: {titulo:<15} | barrio: {barrio} | precio: {precio} | \n'
                            f'habitaciones: {habitacion} | baños: {bano} | metros cuadrados: {metros} | aire: {aire} | \n'
                            f'balcon: {balcon} | calefacción: {calefaccion} | garaje: {garaje} | piscina: {piscina} | \n'
                            f'chimenea: {chimenea} | trastero: {trastero} | jardin: {jardin} | terraza: {terraza}')
                        ids.append(contador_anuncios)
                        casas.append(titulo)
                        barrios.append(barrio)
                        precios.append(precio)
                        habitaciones.append(habitacion)
                        banos.append(bano)
                        m_cuad.append(metros)
                        aires.append(aire)
                        balcones.append(balcon)
                        calefacciones.append(calefaccion)
                        garajes.append(garaje)
                        piscinas.append(piscina)
                        chimeneas.append(chimenea)
                        trasteros.append(trastero)
                        jardines.append(jardin)
                        terrazas.append(terraza)  

                        contador_anuncios += 1

        pagina += 1                

    elif pagina > 1:
        # Obtener la URL de la página actual (A PARTIR DE LA 2)
        URL_PAGINA = URL_BASE + '/pag-' + str(pagina)

        # Obtener el HTML de la página actual
        pedido_obtenido = requests.get(URL_PAGINA)
        html_obtenido = pedido_obtenido.text

        # Parsear el HTML de la página actual
        soup2 = BeautifulSoup(html_obtenido, "html.parser")

        # Extraer los datos de los artículos de la página actual
        for div in soup2.find_all('div', class_='content'):
            if (div.h3 is not None):
                # Obtener la URL del anuncio
                enlace = div.h3.a['href']
                enlaces_anuncios.append(enlace)
                

                # EXTRACIÓN DE DATOS DEL PROPIO ANUNCIO
                # 1. Obtener el HTML
                URL_ANUNCIO = URL_PAGINA.replace('/venta/casas/granada/pag-', '').replace(str(pagina), '') + enlace
                anuncio_obtenido = requests.get(URL_ANUNCIO)
                html_anuncio_obtenido = anuncio_obtenido.text

                # 2. "Parsear" ese HTML
                soup3 = BeautifulSoup(html_anuncio_obtenido, "html.parser")

                type(soup3)

                # 3. EXTRAER DATOS DEL ANUNCIO
                anuncio_repetido = False
                main_anuncio = soup3.find('main', class_='details-info')
                
                if main_anuncio:
                    # 1- Extraer título
                    titulo = main_anuncio.h1.get_text(strip=True)
                    # 2- Extraer barrio
                    div_barrio = main_anuncio.find('div', class_='details-address')
                    barrio = div_barrio.get_text(strip=True)
                    # 3- Extraer precio
                    section_details_header = main_anuncio.find('section', class_='details-header-info')
                    div_info_header = section_details_header.find('div', class_='info-header')
                    div_price = div_info_header.find('div', class_='price-wrapper')
                    precio = div_price.span.get_text(strip=True).replace(' €', '').replace('.', '')
                    # 4- Extraer habitaciones
                    div_icon_group = section_details_header.find('div', class_='iconGroup')
                    if (div_icon_group is not None):
                        div_icon_room = div_icon_group.find('div', class_='icon-room')
                        if div_icon_room is not None:  
                            habitacion = div_icon_room.span.get_text(strip=True)
                        # 5- Baños
                        div_icon_bath = div_icon_group.find('div', class_='icon-bath')
                        if div_icon_bath is not None:
                            bano = div_icon_bath.span.get_text(strip=True)
                        # 6- Metros cuadrados
                        div_icon_meter = div_icon_group.find('div', class_='icon-meter')
                        if div_icon_bath is not None:
                            metros = div_icon_group.find('div', class_='icon-meter').span.get_text(strip=True).replace(' m²', '').replace('.', '')

                        # 7- Equipamiento
                        section_equipamiento = main_anuncio.find('section', class_='separator', id='sticky-bar-limit-desktop')
                        if (section_equipamiento is not None):
                            equipamiento_texto = section_equipamiento.get_text(strip=True)
                            #7.1 - Comprobar si hay Aire Acondicionado
                            aire = "Sí" if "Aire acondicionado" in equipamiento_texto else "No"
                            #7.2 - Comprobar si hay Balcón
                            balcon = "Sí" if "Balcón" in equipamiento_texto else "No"
                            #7.3 - Comprobar si hay Calefacción
                            calefaccion = "Sí" if "Calefacción" in equipamiento_texto else "No"
                            #7.4 - Comprobar si hay Garaje
                            garaje = "Sí" if "Garaje" in equipamiento_texto else "No"
                            #7.5 - Comprobar si hay Piscina
                            piscina = "Sí" if "Piscina" in equipamiento_texto else "No"
                            #7.6 - Comprobar si hay Chimenea
                            chimenea = "Sí" if "Chimenea" in equipamiento_texto else "No"
                            #7.7 - Comprobar si hay Trastero
                            trastero = "Sí" if "Trastero" in equipamiento_texto else "No"
                            #7.8 - Comprobar si hay Jardín
                            jardin = "Sí" if "Jardín" in equipamiento_texto else "No"
                            #7.9 - Comprobar si hay Terraza
                            terraza = "Sí" if "Terraza" in equipamiento_texto else "No"

                    #Anuncio actual
                    anuncio_actual_str = (
                        f'{titulo}_{barrio}_{precio}_'
                        f'{habitacion}_{bano}_{metros}_'
                        f'{aire}_{balcon}_{calefaccion}_'
                        f'{garaje}_{piscina}_{chimenea}_'
                        f'{trastero}_{jardin}_{terraza}'
                    )

                    # Recorremos el conjunto de anuncios y obtenemos un anuncio
                    for i in range(len(casas)):
                        # Añadir anuncio a anuncios unicos
                        anuncio_guardado_str = (
                                f'{casas[i]}_{barrios[i]}_{precios[i]}_'
                                f'{habitaciones[i]}_{banos[i]}_{m_cuad[i]}_'
                                f'{aires[i]}_{balcones[i]}_{calefacciones[i]}_'
                                f'{garajes[i]}_{piscinas[i]}_{chimeneas[i]}_'
                                f'{trasteros[i]}_{jardines[i]}_{terrazas[i]}'
                            )
    
                        # Verifica si el anuncio ya existe en el conjunto de anuncios únicos
                        if anuncio_guardado_str == anuncio_actual_str:
                            anuncio_repetido = True
                            break
                        else:
                            anuncio_repetido = False
                        
                    if anuncio_repetido == False:
                        # Guardar datos e imprimir por consola
                        print(f'{contador_anuncios}- titulo: {titulo:<15} | barrio: {barrio} | precio: {precio} | \n'
                            f'habitaciones: {habitacion} | baños: {bano} | metros cuadrados: {metros} | aire: {aire} | \n'
                            f'balcon: {balcon} | calefacción: {calefaccion} | garaje: {garaje} | piscina: {piscina} | \n'
                            f'chimenea: {chimenea} | trastero: {trastero} | jardin: {jardin} | terraza: {terraza}')
                        ids.append(contador_anuncios)
                        casas.append(titulo)
                        barrios.append(barrio)
                        precios.append(precio)
                        habitaciones.append(habitacion)
                        banos.append(bano)
                        m_cuad.append(metros)
                        aires.append(aire)
                        balcones.append(balcon)
                        calefacciones.append(calefaccion)
                        garajes.append(garaje)
                        piscinas.append(piscina)
                        chimeneas.append(chimenea)
                        trasteros.append(trastero)
                        jardines.append(jardin)
                        terrazas.append(terraza)  

                        contador_anuncios += 1  
        pagina += 1                

        # Obtener de nuevo el numero de páginas
        paginas = int(soup2.find('div', class_='paginator').find_all('a')[-1].text)

# ALMACENAR DATOS DE LOS PRODUCTOS
import csv

# Insertar un encabezada (OMITIR EN ESTE CASO)
ids.insert(0, "ids")
casas.insert(0, "casas")
barrios.insert(0, "barrios")
precios.insert(0, "precios")
habitaciones.insert(0, "habitaciones")
banos.insert(0, "baños")
m_cuad.insert(0, "metros cuadrados")
aires.insert(0, "aire acondicionado")
balcones.insert(0, "balcón")
calefacciones.insert(0, "calefacción")
garajes.insert(0, "garaje")
piscinas.insert(0, "piscina")
chimeneas.insert(0, "chimenea")
trasteros.insert(0, "trastero")
jardines.insert(0, "jardín")
terrazas.insert(0, "terraza")
enlaces_anuncios.insert(0, "enlace")
# Guardar datos en un archivo .csv
with open('datos_casas_granada.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=',')  # Cambiar el delimitador a punto y coma
    for ids, casas, barrios, precios, habitaciones, banos, m_cuad, aires, balcones, calefacciones, garajes, piscinas, chimeneas, trasteros, jardines, terrazas, enlaces_anuncios in zip(
        ids, casas, barrios, precios, habitaciones, banos, m_cuad, aires, balcones, calefacciones, garajes, piscinas, chimeneas, trasteros, jardines, terrazas, enlaces_anuncios):
        w.writerow([ids, casas, barrios, precios, habitaciones, banos, m_cuad, aires, balcones, calefacciones, garajes, piscinas, chimeneas, trasteros, jardines, terrazas, enlaces_anuncios])

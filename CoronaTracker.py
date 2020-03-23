# Importaciones:
import requests
import time
from bs4 import BeautifulSoup

# URLs de donde extraeremos los datos:
url_world = "https://www.worldometers.info/coronavirus/"
url_region = "https://www.worldometers.info/coronavirus/country/spain/"

# Función get_corona_data que usa BeautifulSoup para extraer los datos de Internet:
def get_corona_data(url):

    try:

        response = requests.get(url)

    except:

        array_data = {"Error": "Connection error!"}

    # Extraemos y guardamos en un archivo la página:
    soup = BeautifulSoup(response.text, "html.parser")

    # Creamos un array que guarde fallecimientos, infectados, recuperados y errores:
    array_data = {"Deaths": 0, "Infect": 0, "Recove": 0, "Error": "None"}

    line = 1
    data = 0

    # Recorremos todos los <div> de la página buscando el que se llame "maincounter-number":
    for a_divtag in soup.findAll('div'):

        divattrs = a_divtag.attrs
        line += 1

        # Busca aquellos <div> que contengan atributos:
        if (a_divtag.has_attr('class')):

            dClass = divattrs['class'][0]

            # Si la clase se llama "maincounter-number":
            if (dClass == 'maincounter-number'):

                ccount = 0

                for child in a_divtag.children:

                    ccount += 1

                    if (ccount == 2):

                        statnum = child.string.strip()

                data += 1

                # Recorremos los atributos del <div> que incluyen Infectados, Fallecidos y Recuperados:
                if (data == 1):

                    array_data['Infect'] = statnum

                elif (data == 2):

                    array_data['Deaths'] = statnum

                elif (data == 3):

                    array_data['Recove'] = statnum

    return array_data

if __name__ == '__main__':

    while True:

        errors = 0

        # Obtener los datos globales:
        world_corona_cases = get_corona_data(url_world)

        if (world_corona_cases["Error"] != "None"):
            errors += 1

        # Obtener los datos por pais:
        region_corona_cases = get_corona_data(url_region)

        if (region_corona_cases["Error"] != "None"):
            errors += 1

        # Si no hay errores mostramos los datos:
        if (errors == 0):

            print("Casos mundiales: " + str(world_corona_cases["Infect"]))
            print("Muertes mundiales: " + str(world_corona_cases["Deaths"]))
            print("Recuperados mundiales: " + str(world_corona_cases["Recove"]))

            print("Casos España: " + str(region_corona_cases["Infect"]))
            print("Muertes España: " + str(region_corona_cases["Deaths"]))
            print("Recuperados España: " + str(region_corona_cases["Recove"]))

        # Actualizamos cada 60 segundos:
        time.sleep(60)

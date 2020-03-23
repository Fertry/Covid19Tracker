# Importaciones:
import requests
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
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

# Función contador:
def contador():

    errors = 0
    numbers = {"DW": 0, "IW": 0, "RW": 0, "DR": 0, "IR": 0, "RR": 0}

    # Obtener los datos globales:
    world_corona_cases = get_corona_data(url_world)

    if (world_corona_cases["Error"] != "None"):

        errors += 1

    # Obtener los datos por pais:
    region_corona_cases = get_corona_data(url_region)

    if (region_corona_cases["Error"] != "None"):

        errors += 1

    # Si no hay errores mostramos los datos (los guardamos en un diccionario para la interfaz):
    if (errors == 0):

        numbers["IW"] = str(world_corona_cases["Infect"])
        numbers["DW"] = str(world_corona_cases["Deaths"])
        numbers["RW"] = str(world_corona_cases["Recove"])

        numbers["IR"] = str(region_corona_cases["Infect"])
        numbers["DR"] = str(region_corona_cases["Deaths"])
        numbers["RR"] = str(region_corona_cases["Recove"])

        return numbers

        # Prints para ver los datos en cosola (debug):
        #print("Casos mundiales: " + str(world_corona_cases["Infect"]))
        #print("Muertes mundiales: " + str(world_corona_cases["Deaths"]))
        #print("Recuperados mundiales: " + str(world_corona_cases["Recove"]))

        #print("Casos España: " + str(region_corona_cases["Infect"]))
        #print("Muertes España: " + str(region_corona_cases["Deaths"]))
        #print("Recuperados España: " + str(region_corona_cases["Recove"]))

# Clase Interfaz de tipo BoxLayout que mostrará los datos:
class Interfaz(BoxLayout):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.dw_label = Label()
        self.add_widget(self.dw_label)
        self._update()
        # Actualiza cada 60 segundos:
        self._sheduler = Clock.schedule_interval(self._update, 60)

    def _update(self, dt=None):

        d = contador()
        self.dw_label.text = (
            f'Infectados a nivel global: {d["IW"]}\nFallecimientos a nivel global: {d["DW"]}\nRecuperados a nivel global: {d["RW"]}\n'
            f'Infectados a nivel regional: {d["IR"]}\nFallecimientos a nivel regional: {d["DR"]}\nRecuperados a nivel regional: {d["RR"]}\n'
            )

# Clase MyApp que ejecuta Interfaz:
class MyApp(App):
    
    def build(self):

        return Interfaz()

# Bucle principal:
if __name__ == '__main__':

    # Llamamos a la clase MyApp que hace display de Interfaz
    MyApp().run()

from urllib.request import urlopen
import numpy
import pandas as pd
import json
import math

url = "https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2900.0-6000.0&condition=used&category=MLM9761"
response = urlopen(url)
data_json = json.loads(response.read())
totalpublicaciones = int(data_json["paging"]["total"])
pos = 0
grafica_title = numpy.array([])
grafica_link = numpy.array([])
grafica_price = numpy.array([])
grafica_envio = numpy.array([])


for posicion in range(math.ceil(totalpublicaciones / 50)):

    url = "https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2900.0-6000.0&condition=used&category=MLM9761&offset=" + str(pos)
    response = urlopen(url)
    data_json = json.loads(response.read())
    totalpublicaciones = int(data_json["paging"]["total"])
    pos = pos + 50

    for titulos in data_json["results"]:
        grafica_title = numpy.append(grafica_title, titulos["title"])
        grafica_price = numpy.append(grafica_price, titulos["price"])
        grafica_link = numpy.append(grafica_link, titulos["permalink"])
        if titulos["shipping"]["free_shipping"]:
            grafica_envio = numpy.append(grafica_envio, "Envio gratis")
        else:
            grafica_envio = numpy.append(grafica_envio, "Sin envio gratis")

grafica_list = pd.DataFrame({
        'Grafica': grafica_title,
        'Precio': grafica_price,
        'Enlace': grafica_link,
        'Envio': grafica_envio
    })
print(grafica_list)

# grafica_list.to_csv(r'C:/Users/Jonathan/Desktop/ebay_webscrapping-master/' + str(accion) + '.csv', index=False, header=True)
# + time.strftime("%d.%m.%Y-%H.%M.%S")

import tkinter as tk
from tkinter import ttk
from pandastable import Table
from urllib.request import urlopen
import json
import math
import pandas as pd
import time
import glob
import os
import numpy

directorio = os.getcwd()

def chequeo(accion):
    url = "https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2300.0-6200.0&condition=used&category=MLM9761"
    response = urlopen(url)
    data_json = json.loads(response.read())
    totalpublicaciones = int(data_json["paging"]["total"])
    pos = 0
    grafica_title = numpy.array([])
    grafica_link = numpy.array([])
    grafica_price = numpy.array([])
    grafica_envio = numpy.array([])
    for posicion in range(math.ceil(totalpublicaciones / 50)):

        url = "https://api.mercadolibre.com/sites/MLM/search?sort=price_asc&price=2300.0-6200.0&condition=used&category=MLM9761&offset=" + str(pos)
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
    grafica_list.to_csv(r""+ directorio +'/' + str(accion) + '.csv', index=False, header=True)
    return grafica_list


def comparar():
    # Crear una ventana secundaria.
    ventana_secundaria = tk.Toplevel()
    ventana_secundaria.title("Ventana secundaria")
    ventana_secundaria.config(width=300, height=200)
    chequeo('comparaciones/comparator')
    list_of_files = glob.glob(directorio +'/comparaciones/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    latest_file = latest_file.replace(directorio +"/comparaciones\\", "")
    df1 = pd.read_csv('./base.csv', sep=',', header=None)
    df2 = pd.read_csv('./comparaciones/' + latest_file, sep=',', header=None)

    df_diff = pd.concat([df1.iloc[:, 0], df2.iloc[:, 0]]).drop_duplicates(keep=False)

    diferencias = numpy.array(df_diff)
    tb1N = numpy.array(df1)
    tb2N = numpy.array(df2)
    df3G = numpy.array([])
    df3P = numpy.array([])
    df3E = numpy.array([])
    df3S = numpy.array([])
    diff = numpy.setdiff1d(tb2N[:, 0], tb1N[:, 0])
    for i in range(len(tb2N)):
        for j in range(len(diff)):
            if numpy.array_equal(tb2N[i - 1, 0], diff[j - 1]):
                df3G = numpy.append(df3G, tb2N[i - 1, 0])
                df3P = numpy.append(df3P, tb2N[i - 1, 1])
                df3E = numpy.append(df3E, tb2N[i - 1, 2])
                df3S = numpy.append(df3S, 'nuevo')

    bolsita_list = pd.DataFrame({
        'Grafica': df3G,
        'Precio': df3P,
        'Enlace': df3E,
        'Status': df3S
    })
    print("Antes de if")
    if os.path.exists(directorio +"/comparaciones/comparator.csv"):
        os.remove(directorio +"/comparaciones/comparator.csv")
    bolsita_list.to_csv(r""+ directorio + '/comparaciones/comparacion de' + time.strftime("%d.%m.%Y-%H.%M.%S") + '.csv', index=False, header=True)
    df = bolsita_list
    Table(ventana_secundaria, dataframe=df, showtoolbar=True, showstatusbar=True).show()


def nuevo_archivo_base():
    tabla = tk.Toplevel()
    tabla.title("Tabla")
    df = chequeo("base")
    df.to_csv(r""+ directorio + '/respaldos/base de ' + time.strftime("%d.%m.%Y-%H.%M.%S") + '.csv', index=False, header=True)
    # df = grafica_list
    Table(tabla, dataframe=df, showtoolbar=True, showstatusbar=True).show()


def producto_del_dia():
    tabla = tk.Toplevel()
    tabla.title("Tabla")
    df = chequeo("base")
    df.to_csv(r""+ directorio + '/respaldos/base de ' + time.strftime("%d.%m.%Y-%H.%M.%S") + '.csv', index=False, header=True)
    # df = grafica_list
    Table(tabla, dataframe=df, showtoolbar=True, showstatusbar=True).show()


# Crear la ventana principal.
ventana_principal = tk.Tk()
ventana_principal.geometry("400x400")
ventana_principal.columnconfigure(0, weight=1)
ventana_principal.columnconfigure(1, weight=1)
ventana_principal.title("Ventana principal")
label = ttk.Label(text="Elige Opción a realizar")
boton_base = ttk.Button(
    ventana_principal,
    text="Crear nuevo archivo base",
    command=nuevo_archivo_base
)
boton_comparar = ttk.Button(
    ventana_principal,
    text="Comparar nuevos productos",
    command=comparar
)
boton_productos_del_dia = ttk.Button(
    ventana_principal,
    text="Comparar nuevos productos",
    command=producto_del_dia
)
label.grid(column=0, row=0, sticky=tk.EW, padx=5, pady=5)
boton_base.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
boton_comparar.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
ventana_principal.mainloop()

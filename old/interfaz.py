import shutil
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import glob
import os
import numpy
from sys import exit

clear = lambda: os.system('cls')

clear()
print("-------------------------------------------------------------------------------------------------")
print("Elige Opción a realizar - ()")
print("1 - Crear nuevo archivo base")
print("2 - Comparar archivo base con nuevos productos")
print("-------------------------------------------------------------------------------------------------")
# input
opcion = int(input())
z = 0


def chequeo(accion):
    driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe')

    driver.get(
        "https://computacion.mercadolibre.com.mx/componentes-pc-tarjetas-video/usado/_OrderId_PRICE_PriceRange_2900-6000_NoIndex_True")
    grafica_title = numpy.array([])
    grafica_link = numpy.array([])
    grafica_price = numpy.array([])
    page = BeautifulSoup(driver.page_source, 'html.parser')
    pg_amount = page.find('li', attrs={'class': 'andes-pagination__page-count'}).text.replace("de ", "")

    for i in range(0, int(pg_amount) - 1):
        pos = (i + 1) * 50 + 1
        driver.get("https://computacion.mercadolibre.com.mx/componentes-pc-tarjetas-video/usado/_Desde_" + str(
            pos) + "_OrderId_PRICE_PriceRange_2900-6000_NoIndex_True")
        page = BeautifulSoup(driver.page_source, 'html.parser')

        for grafica in page.findAll('li', attrs={'class': 'ui-search-layout__item'}):
            title = grafica.find('h2', attrs={'class': 'ui-search-item__title'})
            grafica_title = numpy.append(grafica_title, title.text)
            link = grafica.find('a', attrs={'class': 'ui-search-item__group__element ui-search-link'})
            grafica_link = numpy.append(grafica_link, link['href'])
            price = grafica.find('span', attrs={'class', 'price-tag-fraction'})
            grafica_price = numpy.append(grafica_price, price.text)

    grafica_list = pd.DataFrame({
        'Grafica': grafica_title,
        'Precio': grafica_price,
        'Enlace': grafica_link
    })
    grafica_list.to_csv(r'C:/Users/Jonathan/Desktop/ebay_webscrapping-master/' + str(accion) + '.csv', index=False, header=True)
    # + time.strftime("%d.%m.%Y-%H.%M.%S")
    driver.quit()


if opcion == 1 or opcion == 2:
    if opcion == 1:
        clear()
        print("1 - Crear nuevo archivo base")
        chequeo('base')
        print("Desea respaldar el anterior? s/n")
        option = str(input())
        if option == 's' or option == 'n':
            if option == 's':
                shutil.copy2('C:/Users/Jonathan/Desktop/ebay_webscrapping-master/base.csv', 'C:/Users/Jonathan/Desktop/ebay_webscrapping-master/respaldos/base de ' + time.strftime("%d.%m.%Y-%H.%M.%S") + '.csv')
            if option == 'n':
                exit(0)
        else:
            exit(0)

    if opcion == 2:
        clear()
        print("2 - Comparar archivo base con nuevos productos")
        chequeo('comparaciones/comparator')
        list_of_files = glob.glob('C:/Users/Jonathan/Desktop/ebay_webscrapping-master/comparaciones/*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file = latest_file.replace("C:/Users/Jonathan/Desktop/ebay_webscrapping-master/comparaciones\\", "")
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
        if os.path.exists("./comparaciones/comparator.csv"):
            os.remove("./comparaciones/comparator.csv")
        else:
            print("The file does not exist")
        bolsita_list.to_csv(r'C:/Users/Jonathan/Desktop/ebay_webscrapping-master/comparaciones/' + time.strftime("%d.%m.%Y-%H.%M.%S") + '.csv', index=False, header=True)
        list_of_files = glob.glob('C:/Users/Jonathan/Desktop/ebay_webscrapping-master/comparaciones/*.csv')
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file = latest_file.replace("C:/Users/Jonathan/Desktop/ebay_webscrapping-master/comparaciones\\", "")
        os.startfile('C:/Users/Jonathan/Desktop/ebay_webscrapping-master/comparaciones/' + latest_file)
        print("Desea conservar? s/n")
        option = str(input())
        if option == 's' or option == 'n':
            if option == 's':
                if os.path.exists('C:/Users/Jonathan/Desktop/ebay_webscrapping-master/comparaciones/' + latest_file):
                    os.remove('C:/Users/Jonathan/Desktop/ebay_webscrapping-master/comparaciones/' + latest_file)
                else:
                    print("The file does not exist")
            if option == 'n':
                exit(0)

else:
    print("A donde vas perra")

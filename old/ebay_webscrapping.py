from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import glob
import os
import numpy
from sys import exit

driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe')

driver.get("https://computacion.mercadolibre.com.mx/componentes-pc-tarjetas-video/usado/_OrderId_PRICE_PriceRange_2900-6000_NoIndex_True")
grafica_title = []
grafica_link = []
grafica_price = []

page = BeautifulSoup(driver.page_source,'html.parser')
pg_amount = page.find('li', attrs={'class':'andes-pagination__page-count'}).text.replace("de ", "")



for i in range(0, int(pg_amount)-1):
   pos = (i+1)*50+1
   driver.get("https://computacion.mercadolibre.com.mx/componentes-pc-tarjetas-video/usado/_Desde_"+ str(pos) +"_OrderId_PRICE_PriceRange_2900-6000_NoIndex_True")
   page = BeautifulSoup(driver.page_source,'html.parser')

   for grafica in page.findAll('li', attrs={'class':'ui-search-layout__item'}):
        title = grafica.find('h2', attrs={'class':'ui-search-item__title'})
        grafica_title.append(title.text)
        link = grafica.find('a', attrs={'class':'ui-search-item__group__element ui-search-link'})
        grafica_link.append(link['href'])

        price = grafica.find('span',attrs={'class','price-tag-fraction'})
        grafica_price.append(price.text)
grafica_list = pd.DataFrame({
                            'Grafica':grafica_title,
                            'Precio':grafica_price,
                            'Enlace': grafica_link
                         })
grafica_list.to_csv(r'C:/Users/Jonathan/Desktop/ebay_webscrapping-master/listas/'+ time.strftime("%d.%m.%Y-%H.%M.%S") +'.csv', index=None, header=True)
list_of_files = glob.glob('C:/Users/Jonathan/Desktop/ebay_webscrapping-master/listas/*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
mocho = latest_file.split("C:/Users/Jonathan/Desktop/ebay_webscrapping-master/listas\\")
arr = glob.glob('C:/Users/Jonathan/Desktop/ebay_webscrapping-master/listas/*.csv')
arr.sort()
if len(glob.glob('./listas/*.csv')) >= 2:
   result = arr[-2]
else :
   result = arr[0]
x = result.split("C:/Users/Jonathan/Desktop/ebay_webscrapping-master/listas\\")
last_file = str(mocho[-1])
penultimo = str(x[-1])
df1 = pd.read_csv('./listas/'+penultimo)
df2 = pd.read_csv('./listas/'+last_file)



df_diff = pd.concat([df1.iloc[: , 0],df2.iloc[: , 0]]).drop_duplicates(keep=False)

prueba = numpy.array(df_diff)
tb1N = numpy.array(df1)
tb2N = numpy.array(df2)


df1N = pd.DataFrame(tb1N,
     columns=['Grafica', 'Precio', 'Enlace'])
df2N = pd.DataFrame(tb2N,
     columns=['Grafica', 'Precio', 'Enlace'])

j = 0

bolsita = []
for i in prueba:
   if df1N.loc[df1N['Grafica'] == prueba[j]].size != 0:
      tempo = df1N.loc[df1N['Grafica'] == prueba[j]]
      bolsita.append(tempo)
      bolsita.append("Vendido")
   if df2N.loc[df2N['Grafica'] == prueba[j]].size != 0:
      tempo = df2N.loc[df2N['Grafica'] == prueba[j]]
      bolsita.append(tempo)
      bolsita.append("Nuevo")
   j = j+1


diferencias = pd.DataFrame({
                            'Bolsita':bolsita,
                         })


diferencias.to_csv(r'C:/Users/Jonathan/Desktop/ebay_webscrapping-master/nuevo/'+ time.strftime("%d.%m.%Y-%H.%M.%S") +'.csv', index=None, header=True)
driver.quit()
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
'''Es necesario instalar los siguientes librerias
1: pip install requests
py -2 nombre_archivo.py
py -2 h.py

El acceso es en el siguiente link:
http://104.239.158.49:8080/odk3
usuario: l.vargas Hackaton2017
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''

import os
import getpass
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import xlsxwriter
import time
from time import sleep
import datetime

import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns

# Obtener la fecha y hora del sistema
sisFecha = time.strftime('%Y%m%d')
sisHora = time.strftime('%H_%M')
fechaHora = '_' + sisFecha + '_' + sisHora

# Obtener la ruta del directorio en el cual se ejecuta el script
cwd = os.getcwd()

try:
	nombreExcel = 'odk_' + fechaHora + '.xlsx'
	workbook = xlsxwriter.Workbook(nombreExcel)
	nombrehoja = 'odk' +  fechaHora
	worksheet = workbook.add_worksheet(nombrehoja)
except:
	print '\nNo se pudo crear el archivo'
	exit()


######### Abrir la pagina web #########

url = 'http://104.239.158.49:8080/odk3' 
browser = webdriver.Chrome()
try:
	browser.get(url)
except:
	print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'

# Para retrasar la ejecucion
time.sleep(15)
rows = browser.find_elements_by_xpath('//*[@id="submission_table"]/tbody/tr')
total_rows = len(rows)
print '\nSe encontraron un total de', total_rows - 1, 'registros \n'

time.sleep(2)

listMarca = list()
listSemillas = list()
listFacilidad = list() 
countRow = 0
for row in rows:
	#print "cols length"
	col = len(row.find_elements(By.TAG_NAME, "td"))
	countCol = 0
	for n in xrange(1, col):
		colData = row.find_elements(By.TAG_NAME, "td")[n]
		colDataText = colData.text
		print colDataText
		worksheet.write(countRow, countCol, colDataText)
	
		if countRow != 0 and countCol == 11:
			listMarca.append(colDataText)
		elif countRow != 0 and countCol == 13:
			listSemillas.append(colDataText)
		elif countRow != 0 and countCol == 14:
			listFacilidad.append(colDataText)
		
		countCol = countCol + 1
		
	countRow = countRow + 1

workbook.close()

listSemillasDat = np.array(listSemillas).astype(np.int)
# print listSemillasDat

listFacilidadDat = np.array(listFacilidad).astype(np.int)
# print listFacilidadDat

listMarcaDat = np.array(listMarca).astype(np.str)
# print listMarcaDat

df = pd.DataFrame({'NumeroSemillas': listSemillasDat, 'GradoFacilidad': listFacilidadDat, 'Marca': listMarcaDat})
print df

plt.figure(1)
plt.subplot(211)

## Plot Facilidad
sns.boxplot(y = 'Marca', x = 'GradoFacilidad', data = df, whis = np.inf, palette = 'vlag')
sns.swarmplot(y = 'Marca', x = 'GradoFacilidad', data = df, size = 2, color = '.3', linewidth = 0)

plt.subplot(212)

## Plot Semillas
sns.boxplot(y = 'Marca', x = 'NumeroSemillas', data = df, whis = np.inf, palette = 'vlag')
sns.swarmplot(y = 'Marca', x = 'NumeroSemillas', data = df, size = 2, color = '.3', linewidth = 0)

plt.show()


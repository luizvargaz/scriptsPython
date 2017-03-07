#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# NOTA IMPORTANTE

# C:\Python35\Scripts\pip.exe install selenium
# pip.exe install selenium

# Mover el archivo chromedriver.exe al directorio donde se encuentra el scrit a ejecutar
# https://sites.google.com/a/chromium.org/chromedriver/downloads
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import xlsxwriter

cwd = os.getcwd() # Obtener la ruta del directorio en el cual se ejecuta el script, para posteriormente crear la carpeta con el nombre del hub, en donde se almacenaran las bitacoras

nmFile= raw_input('Escribe el nombre del archivo que contiene las urls: ')
nnwFile= raw_input('Escribe el nombre del archivo para guardar las nuevas urls: ')

# Crear el nuevo directorio
#hub = raw_input("\nEscribe el nombre de la carpeta: ")
#directory = os.getcwd() + '\\' + hub 
#if not os.path.exists(directory):
#    os.makedirs(directory)

# Abrir el archivo con las URLs
if len(nmFile) < 1:
	nameFile = 'url.txt'
else:
	exit() 
try:
	urls = open(nameFile)
except:
    print 'File cannot be opened', urls
    exit()

# Creal en archivo de Excel para guardar las neuvas urls
if len(nmFile) < 1:
	NwNameFile = 'newUrl.xlsx'
else:
	exit() 
try:
	workbook = xlsxwriter.Workbook('newUrl.xlsx')
	worksheet = workbook.add_worksheet()
except:
    print 'The excel workbook cannot be created'
    exit()
	
# Abrir la pagina con selenium
browser = webdriver.Chrome()
try:
	browser.get('https://bitly.com/')
except:
	print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'

# Crear cada nueva URL y guardarla en un archivo de excel
conteo = 0
for url in urls: # Leer cada linea del archivo con las urls 
	line = url.rstrip() # Eliminar los espeacios a la derecha de cada linea que se lee
	print '\nAbriendo la url: ', line
	
	element = browser.find_element_by_id('shorten_url')
	element.send_keys(line)

	time.sleep(2)

	ventana = browser.find_element_by_id('shorten_btn')
	ventana.click()

	time.sleep(2)
	texto = browser.find_element_by_class_name('short-url').text

	print 'La nueva url es: ', texto
	
	# obtener los primeros 255 caracteres de la linea de texto
	nwLine = line[1:255]
	
	# Escribir las urls en el archivo excel
	worksheet.write(conteo, 0, nwLine)
	worksheet.write(conteo, 1, texto)
	
	conteo = conteo + 1

workbook.close()

print "\nDone!!"
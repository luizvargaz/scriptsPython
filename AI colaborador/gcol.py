# https://cran.r-project.org/web/packages/RSelenium/vignettes/RSelenium-basics.html#injecting-javascript-synchronously
# py -2 gcol.py

import os
import time
import getpass
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import xlsxwriter

# Directorio downloads para cambiar los nombres de archivos
dirname = os.path.expanduser('~\Downloads') # Obtener la ruta del directorio de descargas
cwd = os.getcwd() # Obtener la ruta del directorio en el cual se ejecuta el script, para posteriormente crear la carpeta con el nombre del hub, en donde se almacenaran las bitacoras

# Nombre de usuario y contrasena
#name = raw_input("Enter your username: ")
#psw = getpass.getpass("Enter your password: ") 

browser = webdriver.Chrome()
try:
	browser.get('http://bem.cimmyt.org/Default.aspx')
except:
	print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'

# Cerrar la ventana emergente
ventana = browser.find_element_by_id('btnSalir')
ventana.click()

# Ingresar el nombre de usuario y contrasena
username = browser.find_element_by_id('LoginUser_UserName') #http://www.thetaranights.com/login-to-a-website-using-selenium-python-python-selenium-example/
password = browser.find_element_by_id('LoginUser_Password')
#username.send_keys(name)
#password.send_keys(psw)
username.send_keys('l.vargas@cgiar.org')
password.send_keys('ESparky86')

# Click en el boton de usuario y contrasena
elem = browser.find_element_by_id('LoginUser_LoginButton') # http://www.allwebdevhelp.com/javascript/js-help-tutorials.php?i=76945
elem.send_keys(Keys.RETURN)

# Creal en archivo de Excel para guardar las neuvas urls

try:
	workbook = xlsxwriter.Workbook('colaborador.xlsx')
	worksheet = workbook.add_worksheet()
except:
    print 'The excel workbook cannot be created'
    exit()

# Abrir el reporte
try:
	bitacoras = open('bit.txt')
except:
    print 'File cannot be opened', fh
    exit()

conteo = 0

for bitacora in bitacoras:
	
	line = bitacora.rstrip()
	print '\nDescargando la bitacora: ', line
		
	worksheet.write(conteo, 0, bitacora)
	
	url = 'http://bem.cimmyt.org/bitacora/Default.aspx?EditMode=DetailsExtension&id=' + bitacora
	try:
		browser.get(url)
	except:
		print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'
		worksheet.write(conteo, 1, "ERROR")
	
	try:
		colaborador = browser.find_element_by_id('MainContent_ctl00_lblColaborador').text
		worksheet.write(conteo, 1, colaborador)
	except:
		print '\n #### No se puede encontrar el elemento #### \n'
		worksheet.write(conteo, 1, "ERROR")
				
	print 'Productor: ', colaborador
	
	conteo = conteo + 1
	print '\nSe han descargado ', conteo, ' registros'
	
workbook.close()

print "\nDone!!"




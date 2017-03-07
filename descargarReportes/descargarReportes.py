#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# NOTA IMPORTANTE

# C:\Python35\Scripts\pip.exe install selenium
# pip.exe install selenium

# Mover el archivo chromedriver.exe al directorio donde se encuentra el scrit a ejecutar
# https://sites.google.com/a/chromium.org/chromedriver/downloads
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# https://cran.r-project.org/web/packages/RSelenium/vignettes/RSelenium-basics.html#injecting-javascript-synchronously
import os
import time
import getpass
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Directorio downloads para cambiar los nombres de archivos
dirname = os.path.expanduser('~\Downloads') # Obtener la ruta del directorio de descargas
cwd = os.getcwd() # Obtener la ruta del directorio en el cual se ejecuta el script, para posteriormente crear la carpeta con el nombre del hub, en donde se almacenaran las bitacoras

# Crear el nuevo directorio
hub = raw_input("\nEnter the hub's name: ")
directory = os.getcwd() + '\\' + hub 
if not os.path.exists(directory):
    os.makedirs(directory)
	
# Nombre de usuario y contrasena
name = raw_input("Enter your username: ")
psw = getpass.getpass("Enter your password: ") 

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
username.send_keys(name)
password.send_keys(psw)
#username.send_keys('l.vargas@cgiar.org')
#password.send_keys('ESparky86')

# Click en el boton de usuario y contrasena
elem = browser.find_element_by_id('LoginUser_LoginButton') # http://www.allwebdevhelp.com/javascript/js-help-tutorials.php?i=76945
elem.send_keys(Keys.RETURN)

# Abrir el reporte
try:
	bitacoras = open('bitacoras.txt')
except:
    print 'File cannot be opened', fh
    exit()

for bitacora in bitacoras:
	# fname = raw_input("Enter para abrir archivo (done para salir):")
	#if fname == "done":
	#	break
	line = bitacora.rstrip()
	print '\nDescargando la bitacora: ', line
	
	url = 'http://bem.cimmyt.org/bitacora/ImprimirUtilidad.aspx?&conDatos=true&idCicloAgronomico=' + bitacora + '&idTipoReporte=0'
	try:
		browser.get(url)
	except:
		print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'
	
	# Desplegar el menu de opciones patra exportar el reporte
	time.sleep(2)
	try:
		browser.execute_script("document.getElementById('ReportViewer1_ctl05_ctl04_ctl00_ButtonLink').click()") # http://stackoverflow.com/questions/7794087/running-javascript-in-selenium-using-python
	except:
		print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'
		
	# Exportar el reporte en formato PDF
	time.sleep(2)
	try:
		browser.find_element_by_xpath("//*[@id='ReportViewer1_ctl05_ctl04_ctl00_Menu']/div[3]/a").click()
	except:
		print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'
	
	# Leer los nombre de los archivos contenidos en el directorio de descargas
	time.sleep(4)
	directorio = os.listdir(dirname)
			
	# Renombrar el archivo descargado y moverlo a un nuevo directorio 
	for archivo in directorio:
		if archivo == 'RENTABILIDAD_DETALLADA.pdf':
			oldNombre = dirname + '\\' + archivo
			nombre = directory + '\\' + line + '.pdf'
			#print nombre
			#print 'EL nombre anterior es: ', oldNombre
			try:
				nuevoNombre = os.rename(oldNombre, nombre)		
				#print "Nombre anterior: ", archivo, " Nuevo nombre", nuevoNombre
				print 'La bitacora ', line, ' se ha guardado correctamente \n'
			except:
				print 'La bitacora ya existe\n'
			time.sleep(1)
print "\nDone!!"



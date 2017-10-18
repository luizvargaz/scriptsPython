#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# NOTA IMPORTANTE

## Es necesario instalar los siguientes librerias
# 2. Instalar el pip de python: https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip
# 1. pip install urllib
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import time
import urllib
import xlsxwriter
#import xlwt
from linereader import getline # Read a specific line in a text file


cwd = os.getcwd() # Obtener la ruta del directorio en el cual se ejecuta el script, para posteriormente crear la carpeta con el nombre del hub, en donde se almacenaran las bitacoras

# Crear la carpeta
while True:
	carpeta = raw_input('\nEscribe el nombre de la carpeta para almacenar los archivos: ')
	if len(carpeta) < 1:
		print("El nombre no puede estar vacio, ententa nuevamente")
		continue
	else:
		# Crear el directorio para alamacenar las imagenes
		dirCarp = cwd + '\\' + carpeta  
		if not os.path.exists(dirCarp):
			os.makedirs(dirCarp)
		#we're happy with the value given.
        #we're ready to exit the loop.
		break
		
# Crear el archivo Excel 

	# nomArchivo = nombreArchivo + '_' + idFila + '.xlsx'
try:

	#workbook = xlwt.Workbook() 
	#sheet = workbook.add_sheet('emas.xlsx') 

	workbook = xlsxwriter.Workbook('emas_.xlsx')
	worksheet = workbook.add_worksheet('a')
except:
	print '\nNo se pudo crear el archivo'
	exit()

conteo = 1
nCelda = 1

while conteo <= 3000:
	nombre = dirCarp + '//' + 'id_' + str(conteo) + '.txt'
	print conteo
	
	url = 'http://smn.cna.gob.mx/tools/GUI/EMAS_reporte_v2.php?id=' + str(conteo)	+ '&formato=txt&tipo=24h' 

	try:
		
		#fullfilename = os.path.join(dirCarp, nombre)
		#urllib.urlretrieve(url, fullfilename)
		urllib.urlretrieve(url, nombre)
		mensaje = 'Existe'
		#print mensaje
		
	except:
	
		print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'
		mensaje = 'No existe'
		print mensaje
	
	# abrir el archivo recien descargado	
	if mensaje == 'Existe':
		
		red = getline(nombre, 2)
		puntos = red.find(':')
		red = red[puntos:]
		red = red[1:len(red)]
		red = red.strip()
		
		estacion = getline(nombre, 3)
		puntos = estacion.find(':')
		estacion = estacion[puntos:]
		estacion = estacion[1:len(estacion)]
		estacion = estacion.strip()
		
		ubicacion = getline(nombre, 4)
		puntos = ubicacion.find(':')
		ubicacion = ubicacion[puntos:]
		ubicacion = ubicacion[1:len(ubicacion)]
		ubicacion = ubicacion.strip()
		
		latitud = getline(nombre, 5)
		puntos = latitud.find(':')
		latitud = latitud[puntos:]
		latitud = latitud[1:len(latitud)]
		latitud = latitud.strip()
		
		longitud = getline(nombre, 6)
		puntos = longitud.find(':')
		longitud = longitud[puntos:]
		longitud = longitud[1:len(longitud)]
		longitud = longitud.strip()
		
		altitud = getline(nombre, 7)
		puntos = altitud.find(':')
		altitud = altitud[puntos:]
		altitud = altitud[1:len(altitud)]
		altitud = altitud.strip()
		
		#print red
		print estacion
		print ubicacion
		#print latitud
		#print longitud
		#print altitud
		
		lenEst = len(estacion)
		print 'Len: ', lenEst
		
		if lenEst > 1:
		
			# si es la primera fila se escriben los encabezados 
			if nCelda == 1:
			
				#sheet.write(0, 1, 'Estacion')
				
				worksheet.write('A1', 'Red')
				worksheet.write('B1', 'Estacion')
				worksheet.write('C1', 'Ubicacion')
				worksheet.write('D1', 'Latitud (N)')
				worksheet.write('E1', 'Longitud (O)')
				worksheet.write('F1', 'Altitud')
				worksheet.write('G1', 'ID')
				
			nCelda = nCelda + 1
			
			#sheet.write(0, nCelda, red)
			
			# Escribir los datos en las celdas
			celdaRed = 'A' + str(nCelda)
			worksheet.write(celdaRed, red)
			
			celdaEst = 'B' + str(nCelda)
			worksheet.write(celdaEst, estacion)
			
			celdaUb = 'C' + str(nCelda)
			worksheet.write(celdaUb, ubicacion)
			
			celdaLa = 'D' + str(nCelda)
			worksheet.write(celdaLa, latitud)
			
			celdaLo = 'E' + str(nCelda)
			worksheet.write(celdaLo, longitud)
			
			celdaAl = 'F' + str(nCelda)
			worksheet.write(celdaAl, altitud)
			
			celdaUrl = 'G' + str(nCelda)
			worksheet.write(celdaUrl, url)
		
	conteo = conteo + 1
	
#workbook.save('emas.xlsx')	
workbook.close()


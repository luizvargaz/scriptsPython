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
nFila = 1

while conteo <= 2000:
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
			
			## Contar las filas que contienen los datos
			
			numLineas = sum(1 for line in open(nombre))
			print 'Numero de lineas: ', numLineas
			
			if numLineas > 9:
			
				conteoLineas = 0
				
				for linea in open(nombre):
				
					if conteoLineas > 9:
					
						# si es la primera fila se escriben los encabezados 
						if nFila == 1:
						
							#sheet.write(0, 1, 'Estacion')
							
							worksheet.write('A1', 'Red')
							worksheet.write('B1', 'Estacion')
							worksheet.write('C1', 'Ubicacion')
							worksheet.write('D1', 'Latitud (N)')
							worksheet.write('E1', 'Longitud (O)')
							worksheet.write('F1', 'Altitud')
							worksheet.write('G1', 'ID')
							worksheet.write('H1', 'AAAA/MM/DD')
							worksheet.write('I1', 'HH:MM')
							worksheet.write('J1', 'Direccion de rafaga (grados)')
							worksheet.write('K1', 'Direccion del Viento (grados)')
							worksheet.write('L1', 'Humedad relativa (%)')
							worksheet.write('M1', 'Precipitacion (mm)')
							worksheet.write('N1', 'Radiacion Solar (W/m2)')
							worksheet.write('O1', 'Rapidez de rafaga (km/h)')
							worksheet.write('P1', 'Rapidez de viento (km/h)')
							worksheet.write('Q1', 'Temperatura del Aire (C)')
							worksheet.write('R1', 'Presion Atmosferica   ')
							
						nFila = nFila + 1			
						
						#linea = linea.split()
						fecha = linea.split()[0]
						hora = linea.split()[1]
						dirRafaga = linea.split()[2]
						dirViento = linea.split()[3]
						humedadRelativa = linea.split()[4]
						precipitacion = linea.split()[5]
						radiacion = linea.split()[6]
						rapidezRafaga = linea.split()[7]
						rapidezViento = linea.split()[8]
						temperaturaAire = linea.split()[9]
						presionAtmosferica = linea.split()[10]
						
						# Escribir los datos en las celdas
						celdaRed = 'A' + str(nFila)
						worksheet.write(celdaRed, red)
						
						celdaEst = 'B' + str(nFila)
						worksheet.write(celdaEst, estacion)
						
						celdaUb = 'C' + str(nFila)
						worksheet.write(celdaUb, ubicacion)
						
						celdaLa = 'D' + str(nFila)
						worksheet.write(celdaLa, latitud)
						
						celdaLo = 'E' + str(nFila)
						worksheet.write(celdaLo, longitud)
						
						celdaAl = 'F' + str(nFila)
						worksheet.write(celdaAl, altitud)
						
						celdaUrl = 'G' + str(nFila)
						worksheet.write(celdaUrl, url)						
																	
						celdaFecha = 'H' + str(nFila)
						worksheet.write(celdaFecha, fecha)
						
						celdaHora = 'I' + str(nFila)
						worksheet.write(celdaHora, hora)
						
						celdaDirRafaga = 'J' + str(nFila)
						worksheet.write(celdaDirRafaga, dirRafaga)
						
						celdaDirViento = 'K' + str(nFila)
						worksheet.write(celdaDirViento, dirViento)
						
						celdaHumedadRelativa = 'L' + str(nFila)
						worksheet.write(celdaHumedadRelativa, humedadRelativa)
						
						celdaPrecipitacion = 'M' + str(nFila)
						worksheet.write(celdaPrecipitacion, precipitacion)
						
						celdaRadiacion = 'N' + str(nFila)
						worksheet.write(celdaRadiacion, radiacion)
											
						celdaRapidezRafaga = 'O' + str(nFila)
						worksheet.write(celdaRapidezRafaga, rapidezRafaga)
						
						celdaRapidezViento = 'P' + str(nFila)
						worksheet.write(celdaRapidezViento, rapidezViento)
						
						celdaTemperaturaAire = 'Q' + str(nFila)
						worksheet.write(celdaTemperaturaAire, temperaturaAire)
						
						celdaPresionAtmosferica = 'R' + str(nFila)
						worksheet.write(celdaPresionAtmosferica, presionAtmosferica)
						
						print '----------------------'
						print fecha
						print hora
						print dirRafaga
						print dirViento
						print humedadRelativa
						print precipitacion
						print radiacion
						print rapidezRafaga
						print rapidezViento
						print temperaturaAire
						print presionAtmosferica
						
					conteoLineas = conteoLineas + 1
			####### obtener los datos de cada celda
			
			#red = getline(nombre, 10)
			#column1 = red.split()
			#print column1
			
			
	conteo = conteo + 1
	
#workbook.save('emas.xlsx')	
workbook.close()


### cORREGIR EL ORDEN EN QUE SE ESCRIBEN LOS DATOS, POR QUE NO COINCIDEN LOS ID DE CELDA
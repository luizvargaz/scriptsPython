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
import csv
import time

# Obtener la fecha y hora
sisFecha = time.strftime('%Y%m%d')
sisHora = time.strftime('%H_%M')
fechaHora = '_' + sisFecha + '_' + sisHora

# Obtener la ruta del directorio en el cual se ejecuta el script, para posteriormente crear la carpeta con el nombre del hub, en donde se almacenaran las bitacoras
cwd = os.getcwd()

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
	nombreExcel = 'emas_' + fechaHora + '.xlsx'
	workbook = xlsxwriter.Workbook(nombreExcel)
	worksheet = workbook.add_worksheet('a')
except:
	print '\nNo se pudo crear el archivo'
	exit()

conteo = 1
nCelda = 1
nFila = 1

while conteo <= 1500:

	nombre = dirCarp + '//' + 'id_' + str(conteo) + fechaHora +'.txt'
	
	print '--------------------------------------------'
	print 'Probando la estacion ', conteo
	
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
		
		lenEst = len(estacion)
		
		if lenEst > 1:
			
			print 'Descargando datos de la estacion ',estacion
			## Contar las filas que contienen los datos
			
			numLineas = sum(1 for line in open(nombre))
			print 'Numero de lineas: ', numLineas
			
			if numLineas > 9:
			
				conteoLineas = 0
				
				### ^^^^^^^^^^^^^^
				#for linea in open(nombre):
					
				lineas = csv.reader(open(nombre), delimiter='\t', skipinitialspace = True)
				
				for linea in lineas:
				
					if conteoLineas > 9:
					
						conteoColumna = 1
						
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
																
						for columna in linea:
						
							#print 'columna', columna
							
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
		
							
							if conteoColumna == 1:
								
								fecha = columna.split()[0]							
								celdaFecha = 'H' + str(nFila)
								worksheet.write(celdaFecha, fecha)
								
								hora = columna.split()[1]
								celdaHora = 'I' + str(nFila)
								worksheet.write(celdaHora, hora)
																
							elif conteoColumna == 2:
								celdaDirRafaga = 'J' + str(nFila)
								worksheet.write(celdaDirRafaga, columna)
							
							elif conteoColumna == 3:
								celdaDirViento = 'K' + str(nFila)
								worksheet.write(celdaDirViento, columna)
								
							elif conteoColumna == 4:
								celdaHumedadRelativa = 'L' + str(nFila)
								worksheet.write(celdaHumedadRelativa, columna)
							
							elif conteoColumna == 5:
								celdaPrecipitacion = 'M' + str(nFila)
								worksheet.write(celdaPrecipitacion, columna)
							
							elif conteoColumna == 6:
								celdaRadiacion = 'N' + str(nFila)
								worksheet.write(celdaRadiacion, columna)
							
							elif conteoColumna == 7:
								celdaRapidezRafaga = 'O' + str(nFila)
								worksheet.write(celdaRapidezRafaga, columna)
							
							elif conteoColumna == 8:
								celdaRapidezViento = 'P' + str(nFila)
								worksheet.write(celdaRapidezViento, columna)
							
							elif conteoColumna == 9:
								celdaTemperaturaAire = 'Q' + str(nFila)
								worksheet.write(celdaTemperaturaAire, columna)
							
							elif conteoColumna == 10:
								celdaPresionAtmosferica = 'R' + str(nFila)
								worksheet.write(celdaPresionAtmosferica, columna)

							conteoColumna = conteoColumna + 1
							
						nFila = nFila + 1
							
				
					conteoLineas = conteoLineas + 1
			
			
			
	conteo = conteo + 1
print '\n......Guardando el archivo'
workbook.close()

print '\n^^^^^^^^^ El proceso se ha concluido con exito ^^^^^^^^^^^^^^^^^^'




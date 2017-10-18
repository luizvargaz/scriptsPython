#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Luis Vargas Rojas
# luizvargaz@hotmail.com
# 06 de abril de 2017
# NOTA IMPORTANTE

## Es necesario instalar los siguientes librerias
# 2. Instalar el pip de python: https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip
# 1. instalar las librerias necesarias, ejemplo: pip install urllib

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
import re
import time
from time import sleep
import datetime

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#Escribir la hora diaria de ejecucion del script
# Formato Las primeras dos cifras indican las horas, las siguentes dos indican los minutos y las ultimas dos son los segundos
horaEjecucion = '094200'
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Ejecuta el codigo de acuerdo a la hora programada
while True:
	hora = time.strftime('%H%M%S')
	if hora == horaEjecucion:

		# Obtener la fecha y hora
		sisFecha = time.strftime('%Y%m%d')
		sisHora = time.strftime('%H_%M')
		fechaHora = '_' + sisFecha + '_' + sisHora

		# Obtener la ruta del directorio en el cual se ejecuta el script
		cwd = os.getcwd()

		# Crear la carpeta para almacenar los archivos
		dirCarp = cwd + '\\' + 'emas' +  fechaHora
		if not os.path.exists(dirCarp):
			os.makedirs(dirCarp)
				
		# Crear el archivo Excel 
		try:

			#workbook = xlwt.Workbook() 
			#sheet = workbook.add_sheet('emas.xlsx') 
			nombreExcel = 'emas_' + fechaHora + '.xlsx'
			workbook = xlsxwriter.Workbook(nombreExcel)
			nombrehoja = 'emas' +  fechaHora
			worksheet = workbook.add_worksheet(nombrehoja)
		except:
			print '\nNo se pudo crear el archivo'
			exit()

		conteo = 1
		nCelda = 1
		nFila = 1

		while conteo <= 2:
			
			# Para retrasar la ejecucion 
			time.sleep(25)
			
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
				
				
				# Validar que la estacion contiene datos
				lenEst = len(estacion)
				
				if lenEst > 1:
					
					print 'Descargando datos de la estacion ',estacion
					## Contar las filas que contienen los datos
					
					numLineas = sum(1 for line in open(nombre))
					print 'Numero de lineas: ', numLineas
					
					# si es mayor a 9 contiene datos 
					if numLineas > 9:
					
						### ^^^^^^^^^^^^^^
						#for linea in open(nombre):
							
						lineas = csv.reader(open(nombre), delimiter='\t', skipinitialspace = True)
						
						conteoLineas = 0
						## Leer cada linea del archivo
						for linea in lineas:
							
							if conteoLineas == 8:
								
								# Leer los encabezados eliminar los caracteres expeciales y almecenarlos en una lista
								listaEncabezados = list() 
								for encabezado in linea:
									nEncabezado = re.sub('[^a-zA-Z0-9\n\.]', '', encabezado)
									print nEncabezado
									listaEncabezados.append(nEncabezado)
								#print listaEncabezados
								
								try:
									ccDirRafaga = listaEncabezados.index('Direccinderfagagrados')
								except:
									ccDirRafaga = -1
								#print 'ccDirRafaga ', ccDirRafaga
								
								try:
									ccDirViento = listaEncabezados.index('DireccindelVientogrados')
								except:
									ccDirViento = -1
								#print 'ccDirViento ', ccDirViento				
								
								try:
									ccHumedadRelativa = listaEncabezados.index('Humedadrelativa')
								except:
									ccHumedadRelativa = -1
								#print 'ccHumedadRelativa ', ccHumedadRelativa 
								
								try:
									ccPrecipitacion = listaEncabezados.index('Precipitacinmm')
								except:
									ccPrecipitacion = -1
								#print 'ccPrecipitacion ', ccPrecipitacion
								
								try:
									ccRadiacion = listaEncabezados.index('RadiacinSolarWm')
								except:
									ccRadiacion = -1
								#print 'ccRadiacion ', ccRadiacion
								
								try:
									ccRapidezRafaga = listaEncabezados.index('Rapidezderfagakmh')
								except:
									ccRapidezRafaga = -1
								#print 'ccRapidezRafaga ', ccRapidezRafaga
									
								try:
									ccRapidezViento = listaEncabezados.index('Rapidezdevientokmh')
								except:
									ccRapidezViento = -1
								#print 'ccRapidezViento ', ccRapidezViento
														
								try:
									ccTemperaturaAire = listaEncabezados.index('TemperaturadelAireC')
								except:
									ccTemperaturaAire = -1
								#print 'ccTemperaturaAire ', ccTemperaturaAire
										
								try:
									ccPresionAtmosferica = listaEncabezados.index('PresinAtmosfrica')
								except:
									ccPresionAtmosferica = -1
								#print 'ccPresionAtmosferica ', ccPresionAtmosferica
											
				
							# Omitir las primeras 8 lineas que contienen los datos de la estacion y encabezados
							if conteoLineas > 8:
							
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
								
								# obtener la fecha y hora
								columnaFechaHora = linea[0]
							
								fecha =columnaFechaHora.split()[0]							
								celdaFecha = 'H' + str(nFila)
								worksheet.write(celdaFecha, fecha)
										
								hora = columnaFechaHora.split()[1]
								celdaHora = 'I' + str(nFila)
								worksheet.write(celdaHora, hora)
								
								# Validar las columnas con datos y escribir el valor cuando lo tengan
								
								if ccDirRafaga > 0:
									DirRafaga = linea[ccDirRafaga]
									celdaDirRafaga = 'J' + str(nFila)
									worksheet.write(celdaDirRafaga, DirRafaga)
								
								if ccDirViento > 0:
									DirViento = linea[ccDirViento]
									celdaDirViento = 'K' + str(nFila)
									worksheet.write(celdaDirViento, DirViento)
								
								if ccHumedadRelativa > 0:
									HumedadRelativa = linea[ccHumedadRelativa]
									celdaHumedadRelativa = 'L' + str(nFila)
									worksheet.write(celdaHumedadRelativa, HumedadRelativa)
								
								if ccPrecipitacion > 0:
									Precipitacion = linea[ccPrecipitacion]
									celdaPrecipitacion = 'M' + str(nFila)
									worksheet.write(celdaPrecipitacion, Precipitacion)
									
								if ccRadiacion > 0:
									Radiacion = linea[ccRadiacion]
									celdaRadiacion = 'N' + str(nFila)
									worksheet.write(celdaRadiacion, Radiacion)
								
								if ccRapidezRafaga > 0:
									RapidezRafaga = linea[ccRapidezRafaga]
									celdaRapidezRafaga = 'O' + str(nFila)
									worksheet.write(celdaRapidezRafaga, RapidezRafaga)
								
								if ccRapidezViento > 0:
									RapidezViento = linea[ccRapidezViento]
									celdaRapidezViento = 'P' + str(nFila)
									worksheet.write(celdaRapidezViento, RapidezViento)
								
								if ccTemperaturaAire > 0:
									TemperaturaAire = linea[ccTemperaturaAire]
									celdaTemperaturaAire = 'Q' + str(nFila)
									worksheet.write(celdaTemperaturaAire, TemperaturaAire)
								
								if ccPresionAtmosferica > 0:
									PresionAtmosferica = linea[ccPresionAtmosferica]
									celdaPresionAtmosferica = 'R' + str(nFila)
									worksheet.write(celdaPresionAtmosferica, PresionAtmosferica)
									
							conteoLineas = conteoLineas + 1
					
			conteo = conteo + 1
		print '\n......Guardando el archivo'
		workbook.close()

		print '\n^^^^^^^^^ El proceso se ha concluido con exito ^^^^^^^^^^^^^^^^^^'

	if time.strftime('%M%S') == '1000':
	
		hor = horaEjecucion[0:2]
		min = horaEjecucion[2:4]
		sec = horaEjecucion[4:6]
		
		horaCompleta = hor + ':' + min + ':' + sec
		inicioHora= datetime.datetime.strptime(horaCompleta, '%H:%M:%S')
		
		tiempoRest = time.strftime('%H:%M:%S')
		finHora = datetime.datetime.strptime(tiempoRest, '%H:%M:%S')
		
		tiempoRest = inicioHora - finHora
		
		print '\nFaltan ', tiempoRest, ' para la siguiente descarga...'
		time.sleep(1)



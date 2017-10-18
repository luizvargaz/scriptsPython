#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# NOTA IMPORTANTE

## Es necesario instalar los siguientes librerias
# 1: pip install requests

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

import os
import xlsxwriter
import urllib
import requests
from requests.auth import HTTPDigestAuth
import time
from time import sleep

#############
#############
#############

# Obtener la lista de archivos en el directorio
cwd = os.getcwd() 
listaArchivos = os.listdir(cwd)
print '\n La lista de archivos es: ', listaArchivos
time.sleep(1)

# Obtener la lista de archivos en formato txt. Estos contienen las URL con la imagen a descargar 
archivosTxt = list()
for archivo in listaArchivos:
	if archivo.endswith(".txt"):
		archivosTxt.append(archivo)
		
print '\n Los archivos txt a leer son: ', archivosTxt
time.sleep(1)

idFila = 'test'

for arcTxt in archivosTxt:
	num_lines = sum(1 for line in open(arcTxt))
	print '\nEl archivo ', arcTxt, ' tiene ', num_lines, ' lineas'
	
	###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
	# Crear el archivo Excel
	txt = arcTxt.find('.txt')
	nombreArchivo = arcTxt[:txt]
	nombreArchivo = nombreArchivo.strip()
	
	nomArchivo = nombreArchivo + '_' + idFila + '.xlsx'
	try:
		workbook = xlsxwriter.Workbook(nomArchivo)
		worksheet = workbook.add_worksheet(idFila)
	except:
		print '\nNo se pudo crear el archivo'
		exit()
	
	# Abrir el primer archivo 
	try:
		num_lines = sum(1 for line in open(arcTxt))
		lineas = open(arcTxt)
	except:
		print '\nNO SE PUDO ABRIR EL ARCHIVO'
		workbook.close()
		exit()
	
	
	nCelda = 1
	countNumber = 1
	count = 1
	
	for linea in lineas: # Leer cada linea del archivo con las urls 
		######### Descargar la imagen #########
		print ('--------------------------------------------')
		#print '\n	Descargando la foto ', countNumber, ' de ', num_lines
		#print '\n	Trabajando con el archivo ', arcTxt
		
		# Extraer los caracteres de la tercer columna que corresponden al ID, se aislan de acuerdo a las tabulaciones
		espacio1 = linea.find('\t')
		linea1 = linea[espacio1+1:] # Para quitar el primer Tab se suma el numero 1
		espacio2 = linea1.find('\t')
		linea2 = linea1[espacio2:]
		
		uuid = linea2.find('uuid')
		print 'Codigo: ', uuid
		
		# Obtener el ID de usuario
		if uuid == 1:
			idUsuario = linea2.strip()
			idUsuario = idUsuario[5:43]
		else:
			idUsuario = linea2.strip()
			
		print '\n	Usuario: ', idUsuario
		
		# si es la primera fila se escriben los encabezados 
		if nCelda == 1:
			worksheet.write('A1', 'instanceID')
			worksheet.write('B1', 'Link')
			worksheet.write('C1', 'Imagen')
		
		# sumar el numero de celda
		nCelda = nCelda + 1
		
		# Escribir el ID
		celdaID = 'A' + str(nCelda)
		idUs = 'uuid:' + idUsuario
		worksheet.write(celdaID, idUs)
		
		count = count + 1
		countNumber = countNumber + 1
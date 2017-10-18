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
#from openpyxl import load_workbook

# Obtener la ruta del directorio en el cual se ejecuta el script
cwd = os.getcwd() 

######### Obtener los datos necesarios que ingresa el usuario #########

# Crear la carpeta
while True:
	carpeta = raw_input('\nEscribe el nombre de la carpeta: ')
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

# Obtener el dato de fila
while True:
	idFila = raw_input('\nEscribe un ID para la fila: ')
	if len(idFila) < 1:
		print("El nombre no puede estar vacio, ententa nuevamente")
		continue
	else:
		#we're happy with the value given.
        #we're ready to exit the loop.
		break
		
# Crear el archivo Excel
while True:
	idArchivo = raw_input('\nEscribe el nombre del archivo: ')
	# Crear el archivo de excel
	nomArchivo = idArchivo + '_' + idFila + '.xlsx'
	if len(idArchivo) < 1:
		print("El nombre no puede estar vacio, ententa nuevamente")
		continue
	else:
		#we're happy with the value given.
        #we're ready to exit the loop.
		try:
			workbook = xlsxwriter.Workbook(nomArchivo)
			worksheet = workbook.add_worksheet(idFila)
		except:
			print '\nNo se pudo crear el archivo'
			exit()
		break

try:
	num_lines = sum(1 for line in open('url_1.txt'))
	lineas = open('url_1.txt')
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
	print '\n	Descargando la foto ', countNumber, ' de ', num_lines
	
	espacio = [' ']
	uuid = linea.find('uuid')
	
	# Obtener el ID de usuario
	idUsuario = linea[uuid:]
	idUsuario = idUsuario.strip()
	idUsuario = idUsuario[7:43]
	# print '\n	Usuario: ', idUsuario
	
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
		
	# Revisar si tiene URL la linea 
	if any(i in linea for i in 'http'):
		print('\n	Tiene URL')
		
		# Obtener la url
		http = linea.find('http')
		url = linea[http:]
		url = url.strip() # Eliminar los espacios a la derecha de cada linea que se lee
		lenUrl = len(url) - 42
		url = url[0:lenUrl]
		url = url.strip()
		#print '\nAbriendo la url: ', url
		
		# Escribir el link
		celdaURL = 'B' + str(nCelda)
		worksheet.write(celdaURL, url)
		
		# Obtener el estado
		estado = linea[:http]
		estado = estado.strip()
		# print '\n	Estado: ', estado
	
		# construir el nombre del archivo
		nameIm = carpeta + '\\' + estado + '_' + idUsuario + '_' + idFila +  '.jpg'
		print '\n 	Nombre archivo: ' + nameIm
		
		# Construir url
		#imgUrl = 'http://104.239.158.49:8080/view/binaryData?blobKey=PIMAF-TECN04-SEPT%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2FPIMAF-TECN-04FormatoVisita-SEPT%5B%40key%3Duuid%3Aa14d2ef0-d2f0-4a21-b1d3-45126999faab%5D%2FSEC3%3AFotografia1'
		#print imgUrl
		
		#Descargar la imagen
		try:
			url_img = requests.get(url, auth = HTTPDigestAuth('admin', 'CIMMYTodk'), timeout = 5) 
			f = open(nameIm, 'wb') 
			f.write(url_img.content) 
			f.close()
			
			######### Crear el link en el archivo excel #########
			url_format = workbook.add_format({
				'font_color': 'blue',
				'underline':  1
			})
		
			# Crear el link a la imagen
			link = cwd + '\\' + nameIm	
			celdaUrl = 'C' + str(nCelda)
			worksheet.write_url(celdaUrl, link, url_format, 'Ver imagen')
		
		except:
			celdaUrl = 'C' + str(nCelda)
			worksheet.write(celdaUrl, 'No se pudo abrir la pagina')
			print '\n #### No se puede abrir la pagina, comprueba tu coneccion a internet #### \n'
		
	else:
		
		print('\n NO TIENE URL')
		# Obtener el estado
		estado = linea[:uuid]
		estado = estado.strip()
		#print '\n	Estado: ', estado
		
		# Escribir el link
		url = ' '
		celdaURL = 'B' + str(nCelda)
		worksheet.write(celdaURL, url)	
	
	count = count + 1
	countNumber = countNumber + 1
	
	
workbook.close()
	
	#print link
	# Link to a Folder.
	#worksheet.write_url('A1', link, url_format, 'Foto')
	
	#Open an xlsx for reading
	#workbook = load_workbook(filename = nomArchivo)
	#print 'El archivo es: ', workbook
	#Get the current Active Sheet
	#worksheet = workbook.get_active_sheet()
	#print 'La hoja es: ', worksheet
	
	#link = cwd + '\\' + carpeta + '\\' + estado + '_' + idUsuario + '_' + idFila +  '.jpg' 
	
	#print link
	
	#worksheet.cell(row=1, column=1).value = '=HYPERLINK("{}", "{}")'.format(link, "Link Name")
	#worksheet.cell('A1').value = '=HYPERLINK("http://www.google.com","Click Me")'
	
	
	
	#workbook.save(nomArchivo)




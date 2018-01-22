# Para construir el PDF
import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, legal, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, PageBreak, Table, TableStyle 
from reportlab.lib.styles import getSampleStyleSheet

#import codecs # para codificacion de caracteres
import csv
import os

# Para obtener las dimensiones de la imagen
import pygame

# obtener el directorio donde se ejecuta el script
cwd = os.getcwd() 

# Para descargar la imagen
import urllib
import requests
from requests.auth import HTTPDigestAuth
import time
from time import sleep

# Usuario y pwd en servidor ODK
usuario = 'l.vargas'
pwd = 'ODK'

# Escribir las variables de titulo etc
titulo = 'REPORTE DE VISITA'
subtitulo = 'PROAGRO 2017'
nombreArchivo = 'TECN_04_FormatoVisita.csv'
nformato = 'VSSC' ## abreviacion del formato

#Definir los estilos para el documento
estiloTabla = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
					   ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
					   ('VALIGN',(0,0),(0,-1),'TOP'),
					   ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
					   ('ALIGN',(0,-1),(-1,-1),'CENTER'),
					   ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
					   ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
					   ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
					   ('BOX', (0,0), (-1,-1), 0.25, colors.black),
					   ])
styles = getSampleStyleSheet() 
styleNormal = styles['Normal']
styleHeading = styles['Heading1']
styleHeading2 = styles['Heading2'] 
styleHeading.alignment = 1 # centre text (TA_CENTRE) 

#Configure style and word wrap
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'

# Importar datos de archivo con una lista
with open (nombreArchivo, 'rb') as csvfile:
	reader = csv.reader(csvfile)
	lista = list(reader)
	
encabezados = lista[0]

conteo = 1
for numRregistro in range(1,len(lista)):
	
	print '\n >>>> Creando el reporte ', conteo, ' de ', len(lista)-1
	
	reg1 = lista[numRregistro]
	
	#Recorrer cada registro y almacenar los encabezados y enlaces de imagenes. Descartar los registros vacios
	registros = list()
	encabezado = list()
	enlaces = list()
	encabezadoEnlaces = list()
	data = list()
	registrosVacios = list()
	
	conteoRegistros = 0
	
	for line in reg1:
		#print line
		
		#Validar registros vacios
		if line == '':
			registrosVacios.append(line)	
		
		elif encabezados[conteoRegistros].startswith('Estado en el que llevara a cabo su servicio'):
			estado = line
			
		elif encabezados[conteoRegistros].startswith('Nombre del Productor'):
			productor = line
			
		elif encabezados[conteoRegistros].startswith('Nombre del tecnico'):
			tecnico = line
			
		elif encabezados[conteoRegistros].startswith('Nombre de su formador'):
			formador = line	
			
		elif line.startswith('http'):
			enlaces.append(line)
			encabezadoEnlaces.append(encabezados[conteoRegistros])
			
		else:
			registros.append(line)
			encabezado.append(encabezados[conteoRegistros])
			
			data.append([str(encabezados[conteoRegistros]), str(line)])
		
		conteoRegistros = conteoRegistros + 1
		
	#print '#### \nNumero de registros vacios', len(registrosVacios)
	
	#print 'Enlaces', encabezadoEnlaces
	
	#almacenar el Id del registro
	idEncRegistro = encabezado.index('instanceID')
	idReg = registros[idEncRegistro]
	idRegistro  = idReg[5:]
	
	# Crear los directorios 
	directorioEstado = cwd + '\\' + estado 
	if not os.path.exists(directorioEstado):
		os.makedirs(directorioEstado)

	directorioFormador = directorioEstado + '\\' + formador 
	if not os.path.exists(directorioFormador):
		os.makedirs(directorioFormador)
		
	directorioTecnico = directorioFormador + '\\' + tecnico 
	if not os.path.exists(directorioTecnico):
		os.makedirs(directorioTecnico)
		
	directorioImagenes = directorioTecnico + '\\' + 'Imagenes' 
	if not os.path.exists(directorioImagenes):
		os.makedirs(directorioImagenes)
	
	# Descargar las imagenes
	
	conteoEnlace = 0
	
	listaNombresFotos = list()
	
	for enlace in enlaces:
		conteoEnlace = conteoEnlace + 1
		nombreImagen = directorioImagenes + '\\' + idRegistro + '_' + str(conteoEnlace) + '.png'
		print '        Descargando la foto ', conteoEnlace, ' de ', len(enlaces)
		
		try:
			url_img = requests.get(enlace, auth = HTTPDigestAuth(usuario, pwd), timeout = 5) 
			f = open(nombreImagen, 'wb') 
			f.write(url_img.content) 
			f.close()
			listaNombresFotos.append(nombreImagen)
					
		except:
			print '\n #### No se puede abrir la pagina, comprueba tu conexion a internet #### \n'
			listaNombresFotos.append('NA')
			continue
			
	print 'Lista nombres fotos: ', len(listaNombresFotos)
	print 'Encabezados: ', len(encabezadoEnlaces)
	
	#<<<<<<<<<<<< Construir el documento PDF >>>>>>>>>>>>>>
	# Construir la tabla para crear el documento
 	
	data2 = [[Paragraph(cell, s) for cell in row] for row in data]
	t = Table(data2)
	t.setStyle(estiloTabla)

	elements = []

	# formato del archivo
	nombreArchivo = directorioTecnico + '\\' + 'PROAGRO-' + nformato + '-' + estado + '-' + formador + '-' + tecnico + '-' + productor + '_' + str(conteo) + '.pdf'
	conteo = conteo + 1
	archivo_pdf = SimpleDocTemplate(nombreArchivo, pagesize = letter, rightMargin = 40, leftMargin = 40, topMargin = 40, bottomMargin = 28)


	#Send the data and build the file
	elements.append(Paragraph(titulo, styleHeading)) 
	elements.append(Paragraph(subtitulo, styleHeading2))
	elements.append(Paragraph('Nombre del productor: ' + productor, styleNormal))
	elements.append(Paragraph('Nombre del estado: ' + estado, styleNormal))
	elements.append(Paragraph('Nombre del tecnico: ' + tecnico, styleNormal))
	elements.append(Paragraph('Nombre del formador: ' + formador, styleNormal))
	elements.append(Spacer(inch, .25*inch))
	elements.append(t)
	elements.append(PageBreak()) 
	elements.append(Paragraph('Evidencia fotografica', styleHeading2))
	elements.append(Spacer(inch, .25*inch))
	
	conteoEncabezados = 0
	for enc in encabezadoEnlaces:
		#print enc
		elements.append(Paragraph(enc, styleNormal))
		#elements.append(Image(listaNombresFotos[conteoEncabezados], 6*inch, 4*inch))
		
		img = pygame.image.load(listaNombresFotos[conteoEncabezados])
		width = img.get_width()
		height = img.get_height()
		
		if width > height:
			elements.append(Image(listaNombresFotos[conteoEncabezados], 7*inch, 3.93803011943915*inch))
			
		else:
			elements.append(Image(listaNombresFotos[conteoEncabezados], 2.21544017451571*inch, 3.93803011943915*inch))
			
		elements.append(Spacer(inch, .25*inch)) 
		conteoEncabezados = conteoEncabezados + 1
	
	archivo_pdf.build(elements)
	print '        ****\nSe ha guardado el reporte en: ', nombreArchivo
	
	
	#<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>
		
# py -2 test.py	
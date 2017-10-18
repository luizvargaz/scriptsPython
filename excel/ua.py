import os
import xlsxwriter

dirArchivos = raw_input('\nEscribe el nombre directorio que contiene los archivos: ')
nuevoArchivo = raw_input('\nEscribe el nombre del archivo que se va a crear: ')
extension = '.xlsx'

dirname = os.getcwd()
directorioExcel = dirname + '\\' + dirArchivos
archivosDirectorio = os.listdir(directorioExcel)

lista = list()

count = 0 
for archivo in archivosDirectorio:
	if fnmatch.fnmatch(archivo, '*.xlsx'):
		print archivo
	else:
		continue
	lista.append(archivo)
#print lista

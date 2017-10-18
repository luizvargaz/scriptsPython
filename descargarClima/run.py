import time
import datetime
from datetime import datetime

horPro = '080000'

while True:
	hora = time.strftime('%H%M%S')
	if hora == '141300':
		print 'La ultima hora es ', hora
		print 'es la hora'
		break
	
	else:
		print 'minuto ', time.strftime("%H:%M:%S.%f")
		hor = horPro[0:2]
		print hor
		min = horPro[2:4]
		print min
		sec = horPro[4:6]
		print sec
		horaCompleta = hor + ':' + min + ':' + sec
		inicioHora= datetime.datetime.strptime(horaCompleta, '%H:%M:%S')
		print 'nhorPro ', inicioHora
		
		tiempoRest = time.strftime('%H:%M:%S')
		finHora = datetime.datetime.strptime(tiempoRest, '%H:%M:%S')
		print 'Hora: ', finHora
		
		
		tiempoRest = inicioHora - finHora
		#print 'Hora: ', int(hora)
		#print 'tiempo: ', int(time.strftime('%H%M%S'))
		print tiempoRest
	
	time.sleep(10)
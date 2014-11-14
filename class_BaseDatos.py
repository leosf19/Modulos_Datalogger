# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import datetime
import os.path
import glob 

"""
day_count: cantidad de dias que hay que registrar
day_sync: cantidad de veces que envia los datos en el dia.
"""


class BaseDatos:
	"""Se encarga del manejo de almacenamiento de los datos recibidos. 
	Guarda los datos en archivos de la manera fecha.log en la carpeta
	/logs. Los registros los hace de la siguiente manera:
	hora CodigoPlaca CodigoSensor Valor"""	
	
	#Variable global para definir la cantidad de dias que registro datos
	global day_count
	
	# Constructor de la clase	
	# Variables:
	#			Ndays -> cantidad de dias que solicita PROCESAMIENTO registrar
	def __init__(self,Ndays):
			self.day_count = Ndays
	
	
	# Almacenamiento de datos en la base de datos
	# Variables: 
	#		values[N]-> valores sensados enviados por procesamiento"""
	def storeData(self, values, sensor_code, board_code):
			
						
			# Generacion de archivo nvo o apertura del existente
			daily_reg = self.createFile()
			
			## Generacion de hora para guardar en archivo
			ts = time.time()
			date_log = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S') #usado para guardar el nombre del archivo diario.log
			#datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			
			#Escritura del archivo
			daily_reg.write(date_log + " - ")	
			daily_reg.write(board_code + " ")
			daily_reg.write(sensor_code + " ")
			daily_reg.write(values + " ")
			daily_reg.write('\r\n')
			
			daily_reg.close()
			
			#Si se guardo correctamente aviso a unidad de procesamiento	
			self.storeDone()
				
	# Crea el archivo de escritura diario "fecha.log"
	# Si no esta creado por ser la primera vez lo crea. Si esta creado
	# busca el ultimo archivo modificado y lo devuelve. Si se alcanza
	# el limite de archivos establecido se borra el mas viejo.			
	def createFile(self):
			
			path = "/home/leo/Documentos/PPS-TESIS/TESIS/logs"
			
			# Verifico si el path para almacenar datos existe, sino la creo
			if not os.path.exists(path):
				os.makedirs(path)
				#f = open(filepath, "a")
			
			## Generacion de fecha para el nombre del archivo
			now = time.time()
			date_reg = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d')
			
			# Verifico si se alcanzo el limite de .log establecido y borro
			# el archivo mas viejo correspondiente
			logCounter = len(glob.glob1(path,"*.log"))
			print self.day_count
			if logCounter == self.day_count:
				# 86400 = 1 dia
				age = int(self.day_count)*86400
				for file in os.listdir(path):
					#now = time.time()
					filepath = os.path.join(path, file)
					modified = os.stat(filepath).st_mtime
					if modified < now - age:
						if os.path.isfile(filepath):
							os.remove(filepath)
							print 'Deleted: %s (%s)' % (file, modified)
				
			
			else:
				# Si no hay ningun archivo .log creado, crearlo (primera vez)
				logCounter = len(glob.glob1(path,"*.log"))
				if logCounter == 0:
					print "No hay archivos .log"
					## Apertura de archivo para escritura
					#filepath = os.path.join(path, date_reg +'.log')
					daily_reg = open(path+'/'+date_reg+'.log','a+')
					print daily_reg
					return daily_reg
			
				# Si hay archivos creados tomar el ultimo si esta dentro del dia
				else:
					print "Existe el archivo"
					max_mtime = 0
					for dirname,subdirs,files in os.walk(path):
						for fname in files:
							full_path = os.path.join(dirname, fname)
							mtime = os.stat(full_path).st_mtime
							if mtime > max_mtime:
								max_mtime = mtime ## fecha del ultimo archivo modificado (formato epoch)
								max_dir = dirname
								max_file = fname ## este es el nombre del ultimo archivo modificado
							
								# Guardo la fecha del ultimo archivo modificado
								#time_last_file = time.strftime('%Y-%m-%d', time.localtime(max_mtime)) 
								time_last_file = datetime.datetime.fromtimestamp(max_mtime).strftime('%Y-%m-%d')
								#+ datetime.timedelta(days=1)
								#print time_last_file
							
								# Fecha actual del sistema
								now_time = datetime.date.today() 
								#print now_time
							
								# Verifico que archivo este dentro del dia sino debo crear uno nuevo
								# %H:%M:%S
							
								if now_time == time_last_file:
									return max_file #archivo dentro del dia
								
							else:
								
								#daily_reg = open(date_reg + ".log" ,"a+") #	archivo en dia nuevo
								daily_reg = open(path+'/'+date_reg+'.log','a+')
								return daily_reg
			    
			
			"""# Imprime todos los archivos con extension .log en el path
			for root, dirs, files in os.walk(path):
				for file in files:
					if file.endswith('.log'):
						print file"""
			
	
	def storeDone(self):
		print "Guardado en archivo correcto!"
	
	#def getReport(self):
		
########################################################################			
			
x = BaseDatos(5)
#valores = str(33)+ " " + str(41.3)+ " " +str(51.1)
#valores2 = str(61)+ " " + str(82.4)+ " " +str(33)
valores=([33.3, 43, 51.1])
for i in range(len(valores)):
	x.storeData(str(valores[i]), "Vb5/12", "P01")
	#time.sleep(10)
#x.storeData(valores2)

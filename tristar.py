# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import serial
import os
import Queue


class TristarTS60(object):
	
	class Sensor(object):
		'''
		Permite crear un sensor. Parametros:
		Nombre / Valor / Parametros (pensado para despues)
		'''
		def __init__(self,name):
			self.name = name
			#self.value = value
			self.q = Queue.Queue() # Cola donde va a guardar los datos que va pidiendo cada sensor
			
			self.q.put(21)
	
		# Devuelve el nombre del sensor	
		def getName(self):
			return self.name
	
		# Modifica el nombre del sensor	
		def setName(self,newname):
			self.name=newname
	
		# Devuelve el valor medido
		def getValue(self):
			return self.q.get()
			# Aca deberia hacer una llamada al metodo mas abstracto "sensar(name)"
			# donde acorde al nombre del sensor que lo llama pide de la cola de ese sensor
			# el valor 
	
	
	
	''' Permite generar los sensores que contenga este equipo particular,
	utilizando una lista definida con sus nombres.
	'''
	def __init__(self):
		
		# Ver: http://snipplr.com/view/35983/
		
		# Contiene los nombres de los sensores de este equipo
		self.nombreSensores = ['V_bat','V_pan', 'I_carga','I_load', 'T_equipo', 'T_bat']
		
		# Contiene los objetos sensores que se van a crear
		self.listaSensores=[]
		
		#for nombre in self.ListaSensores:
		#	simplelist = [TristarTS60.Sensor(nombre)]
		
		# Genero un array de objetos sensores
		for i in range(len(self.nombreSensores)):
			self.listaSensores.append(TristarTS60.Sensor(self.nombreSensores[i]))
		
		# Imprimo el nombre de cada sensor
		for i in range(len(self.listaSensores)):
			print self.listaSensores[i].getName()
		
		self.listaSensores[1].setName("Cambiado")
		print self.listaSensores[1].getName()
		
		#sensor=TristarTS60.Sensor('V_bat')
		#print sensor.getName()

	def ListarSensores(self):
		return self.nombreSensores
	
	# Me devuelve el valor que tenga un sensor particular. Es importante
	# no olvidar que en realidad los objetos sensores ya se crearon, uso
	# el nombre o la posición de la lista que es lo que le mando para poder
	# identificar ese sensor particular
	def Sensar(self, posicion):
		print "Sensor :",self.listaSensores[posicion].getName()
		if not self.listaSensores[posicion].q.empty(): 
			valor = self.listaSensores[posicion].q.get()
			print "Valor: ",valor
			return valor
		else:
			valor = self.ReadRegisters(self.listaSensores[posicion].getName())
			print "Tengo que llamar a ReadRegisters()"
		
	#def Encolar()
			
	'''#################################################################
	Se encarga de crear la conectividad serial
	###################################################################'''
	def StartSerial(self):
		sp = serial.Serial()
		sp.port = self.ScanSerialPorts()
		sp.baudrate = 9600
		sp.parity = serial.PARITY_NONE
		sp.bytesize = serial.EIGHTBITS
		sp.stopbits = serial.STOPBITS_TWO
		
		sp.open()
		return sp
		
	'''#################################################################
	 Busca los nombres de dispositivos seriales que hay en el sistema
	 ##################################################################'''	
	def ScanSerialPorts(self):
		# Variable para la ruta al directorio
		path = "/dev/serial/by-id/"
		
		# Lista todos los archivos en ese directorio
		lstDir = os.listdir(path)
		
		serialDevice =''.join(path)
		serialDevice += serialDevice.join(lstDir)
		
		# El nombre del dispositivo serial
		return serialDevice 
	
	'''#################################################################
	Lectura de la trama de datos (holding registers)
	###################################################################'''
	def readRegisters(self,sensor_name):
		# Mapea un nombre de sensor con una funcion para devolver el valor
		options = {'V_bat' : getBatVF,
					'V_batSVF' : getBatSVF,
					'V_pan' : getArrayLVF,
					'I_carga' : getChargingCurrentF,
					'I_load' : getLoadCurrentF,
					'V_batVSF' : getBatVSF,
					'T_equipo' : getHeatsinkTemp,
					'T_bat' : getBattTemp,
					'None' : getChargeRegVR}
		
		sp=self.StartSerial()
		
		out = '' # la uso para almacenar la trama recibida
		
		### Solicitud de lectura de Holding Registers ###
		sp.write("010300080009040e".decode('hex'))
		time.sleep(1)
		'''Hacerlo con inwaiting porque si leo por una cierta cantidad de bytes
		en algunas ocasiones no llega la trama entera'''
		while sp.inWaiting() > 0:
			out += sp.read(1)
		#out = sp.readline(21) # haciendolo de esta forma evito los ultimos 2 bytes que son CRC (total=23bytes)
		print out.encode('hex'),'\n'    
		
		sp.flushInput()
		sp.close()
		
		# Devuelve el valor del sensor pedido. El resto de los valores 
		# sacados de la trama los mando a las colas de cada sensor
		for key, value in sorted(options.items(),key=lambda x: x[1]):
			if 	key == sensor_name :
				# Pedido de valor de sensor dado
				dato = options[sensor_name](out)
			else:
				# Encolo resto de los valores de los sensores	
				#Encolar(options[sensor_name](out)) 
				print "Habilitar encolar"
		
		return dato
		
	'''################################################################
	Permite obtener el voltaje de bateria filtrado
	###################################################################
	'''	
	def getBatVF(self,trama):	
				
		# Decodificacion de trama recibida
		adc_vb_f=int(trama[3:5].encode('hex'),16) # Convierto de string hexa a int
		adc_vb_f= adc_vb_f*96.667*pow(2,-15)# Obtengo el valor decimal
		print "Battery voltage, filtered= %.2f" %adc_vb_f

		return adc_vb_f
		
		'''################################################################
	Permite obtener el voltaje de bateria sensado y filtrado
	###################################################################'''	
	def getBatSVF(self,trama):	
		
		# Decodificacion de trama recibida
		adc_vs_f=int(trama[3:5].encode('hex'),16)
		adc_vs_f = adc_vs_f*96.667*pow(2,-15)
		print "Battery sense voltage, filtered= %.2f" %adc_vs_f
	
		return adc_vs_f
		
		'''################################################################
	Permite obtener el voltaje del panel solar filtrado
	###################################################################'''	
	def getArrayLVF(self,trama):	
		
		# Decodificacion de trama recibida
		# Point Addr = 4011
		# Tension del panel solar
		adc_vx_f=int(trama[3:5].encode('hex'),16)
		adc_vx_f = adc_vx_f*139.15*pow(2,-15)
		print "Array/Load voltage, filtered= %.2f" %adc_vx_f
	
		return adc_vx_f
		
		'''################################################################
	Permite obtener la corriente de carga filtrada
	###################################################################'''	
	def getChargingCurrentF(self,trama):	
		sp=self.CreateSerial()
		sp.flushInput()
		
		out = '' # la uso para almacenar la trama recibida
		
		### Lectura de Holding Register 4012 ###
		sp.write("0103000b0001f5c8".decode('hex'))
		time.sleep(1)
		while sp.inWaiting() > 0:
			out += sp.read(1)
		print out.encode('hex'),'\n'
		
		# Decodificacion de trama recibida
		adc_ipv_f=int(out[3:5].encode('hex'),16)
		adc_ipv_f = adc_ipv_f*66.667*pow(2,-15)
		print "Charging current, filtered= %.2f" %adc_ipv_f
		
		sp.close()
		
		return adc_ipv_f

	'''################################################################
	Permite obtener la corriente de consumo filtrada (cuando hay carga conectada)
	###################################################################'''	
	def getLoadCurrentF(self,trama):	
		
		# Decodificacion de trama recibida
		adc_iload_f=int(trama[3:5].encode('hex'),16)
		adc_iload_f = adc_iload_f*316.67*pow(2,-15)
		print "Load current, filtered= %.2f" %adc_iload_f
		
		return adc_iload_f
		
		'''################################################################
	Permite obtener el voltaje de la bateria filtrado bajo
	###################################################################'''	
	def getBatVSF(self,trama):	
		
		# Decodificacion de trama recibida
		Vb_f=int(trama[3:5].encode('hex'),16)
		Vb_f = Vb_f*96.667*pow(2,-15)
		print "Battery voltage, slow filter= %.2f V" %Vb_f
	
		return Vb_f
		
		'''################################################################
	Permite obtener la temperatura del radiador del controlador de carga
	###################################################################'''	
	def getHeatsinkTemp(self,trama):	
	
		# Decodificacion de trama recibida
		T_hs=int(trama[3:5].encode('hex'),16)
		print "Heatsink temperature= ", T_hs

		return T_hs
		
		'''################################################################
	Permite obtener la temperatura de la bateria
	###################################################################'''	
	def getBattTemp(self,trama):	
		sp=self.CreateSerial()
		sp.flushInput()
		
		out = '' # la uso para almacenar la trama recibida
		
		### Lectura de Holding Register 4016 ###
		sp.write("0103000f0001b409".decode('hex'))
		time.sleep(1)
		while sp.inWaiting() > 0:
			out += sp.read(1)
		print out.encode('hex'),'\n'
		
		# Decodificacion de trama recibida
		T_batt=int(out[3:5].encode('hex'),16)
		print "Battery temperature= ",T_batt
		
		sp.close()
		
		return T_batt
		
		'''################################################################
	Permite obtener el voltaje de referencia del regulador de carga
	###################################################################'''	
	def getChargeRegVR(self,trama):	
		sp=self.CreateSerial()
		sp.flushInput()
		
		out = '' # la uso para almacenar la trama recibida
		
		### Lectura de Holding Register 4017 ###
		sp.write("01030010000185cf".decode('hex'))
		time.sleep(1)
		while sp.inWaiting() > 0:
			out += sp.read(1)
		print out.encode('hex'),'\n'
		
		# Decodificacion de trama recibida
		V_ref=int(out[3:5].encode('hex'),16)
		V_ref =V_ref*96.667*pow(2,-15)
		print "Charge regulator reference voltage= %.2f" %V_ref
		
		sp.close()
		
		return V_ref
		

		
if __name__ == "__main__":
	
	nombreSensores2=[] # la uso para saber que sensores hay o tiene TRistar
	x=TristarTS60() # Creacion de un objeto tristar
	#print x.listaSensores[3]
	nombreSensores2 = x.ListarSensores() # le pido que me de el nombre de los sensores que contiene
	print nombreSensores2 # imprimo los nombres de sensore 
	x.Sensar(nombreSensores2.index('V_bat')) # le pido al sensor V_bat que me de su valor
	x.Sensar(nombreSensores2.index('V_bat'))
	'''	
	x=ChargeCtrlConnection()
	
	#x.readRegisters()
	x.getBatVF()
	x.getBatSVF()
	x.getArrayLVF()
	x.getChargingCurrentF()
	x.getLoadCurrentF()
	x.getBatVSF()
	x.getHeatsinkTemp()
	x.getBattTemp()
	x.getChargeRegVR()
	'''

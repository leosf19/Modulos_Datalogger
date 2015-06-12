# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import serial
import os
import Queue
from sensor import *


class SensorTristarTS60(object):
	
	
	def __init__(self):
		
		# Ver: http://snipplr.com/view/35983/
		
		# Contiene los nombres de los sensores de este equipo
		#self.nombreSensores = ['V_bat','V_pan', 'I_carga','I_load', 'T_equipo', 'T_bat']
		self.nombreSensores=[]
		
		# Contiene los objetos sensores que se van a crear
		self.listaSensores=[sensV_Bat('V_bat'),sensV_pan('V_pan'),sensI_carga('I_carga'),sensI_load('I_load'),sensT_equipo('T_equipo'),sensT_bat('T_bat')]
		
		# Imprimo el nombre de cada sensor
		#for i in range(len(self.listaSensores)):
		#	print self.listaSensores[i].getName()
		
		
	'''Devuelve una lista de los nombres de sensores presentes
	'''
	def ListarSensores(self):
		for i in range(len(self.listaSensores)):
			self.nombreSensores.append(self.listaSensores[i].getName())
		
		return self.nombreSensores
	
	
	# Me devuelve el valor que tenga un sensor particular. Es importante
	# no olvidar que en realidad los objetos sensores ya se crearon, uso
	# el nombre o la posición de la lista que es lo que le mando para poder
	# identificar ese sensor particular
	def Sensar(self,nombre):
		# Recorro el array de sensores hasta encontrar para el cual se
		# solicita el valor y guardo su posicion
		for i in range(len(self.listaSensores)):
			if self.listaSensores[i].getName()==nombre:
				pos = i
		
		# Pido el valor en su cola, sino hago una lectura de registros		
		if not self.listaSensores[pos].getValue()=="No-value":
			return self.listaSensores[i].getValue()
		else:
			return self.readRegisters(nombre)
		
			
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
		options = {'V_bat' : self.getBatVF,
					'V_batSVF' : self.getBatSVF,
					'V_pan' : self.getArrayLVF,
					'I_carga' : self.getChargingCurrentF,
					'I_load' : self.getLoadCurrentF,
					'V_batVSF' : self.getBatVSF,
					'T_equipo' : self.getHeatsinkTemp,
					'T_bat' : self.getBattTemp,
					'None' : self.getChargeRegVR}
		
		################################################################
		# Inicializa el serial y sus configuraciones
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
		
		#print type(out)
				
		sp.flushInput()
		sp.close()
		#################################################################
		
		# Recorro el array de objeto sensores y cuando encuentro el nombre del
		# sensor que estoy pidiendo llamo a su funcion y devuelvo el dato.
		# Para el caso en que no es el sensor que pido, guardo su valor
		# en la cola del sensor correspondiente
		for i in range(len(self.listaSensores)):
			if self.listaSensores[i].getName() == sensor_name:
				print "Trama ",out.encode('hex')
				dato = options[sensor_name](out)
				# Le seteo el valor en 0 de manera que cuando lo pida de nuevo
				# sepa que tenga que pedir el dato sino se va a dar cuenta que
				# tiene un valor y va a quedar en un bucle ahi
				self.listaSensores[i].setValue(0)
			else:
				self.listaSensores[i].setValue(options[self.listaSensores[i].getName()](out))
		
		'''		
		# Devuelve el valor del sensor pedido. El resto de los valores 
		# sacados de la trama los mando a las colas de cada sensor
		for key, value in sorted(options.items(),key=lambda x: x[1]):
			if 	key == sensor_name :
				# Pedido de valor de sensor dado
				dato = options[sensor_name](out)
			else:
				# Encolo resto de los valores de los sensores	
				#Encolar(options[sensor_name](out)) 
				Encolar(self.listaSensores,nombre)
				print "Habilitar encolar"
		'''
		return dato
		
	'''################################################################
	Permite obtener el voltaje de bateria filtrado
	###################################################################
	'''	
	def getBatVF(self,trama):	
		print trama.encode('hex'),'\n'
		#print type(trama)
		# Decodificacion de trama recibida
		adc_vb_f=int(trama[3:5].encode('hex'),16) # Convierto de string hexa a int
		adc_vb_f= adc_vb_f*96.667*pow(2,-15)# Obtengo el valor decimal
		print "Battery voltage, filtered= %.2f" %adc_vb_f

		return float(adc_vb_f)
		
		'''################################################################
	Permite obtener el voltaje de bateria sensado y filtrado
	###################################################################'''	
	def getBatSVF(self,trama):	
		print trama.encode('hex'),'\n'
		# Decodificacion de trama recibida
		adc_vs_f=int(trama[3:5].encode('hex'),16)
		adc_vs_f = adc_vs_f*96.667*pow(2,-15)
		print "Battery sense voltage, filtered= %.2f" %adc_vs_f
	
		return adc_vs_f
		
		'''################################################################
	Permite obtener el voltaje del panel solar filtrado
	###################################################################'''	
	def getArrayLVF(self,trama):	
		print trama.encode('hex'),'\n'
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
		print trama.encode('hex'),'\n'
		# Decodificacion de trama recibida
		adc_ipv_f=int(trama[3:5].encode('hex'),16)
		adc_ipv_f = adc_ipv_f*66.667*pow(2,-15)
		print "Charging current, filtered= %.2f" %adc_ipv_f

		return adc_ipv_f

	'''################################################################
	Permite obtener la corriente de consumo filtrada (cuando hay carga conectada)
	###################################################################'''	
	def getLoadCurrentF(self,trama):	
		print trama.encode('hex'),'\n'
		# Decodificacion de trama recibida
		adc_iload_f=int(trama[3:5].encode('hex'),16)
		adc_iload_f = adc_iload_f*316.67*pow(2,-15)
		print "Load current, filtered= %.2f" %adc_iload_f
		
		return adc_iload_f
		
		'''################################################################
	Permite obtener el voltaje de la bateria filtrado bajo
	###################################################################'''	
	def getBatVSF(self,trama):	
		print trama.encode('hex'),'\n'
		# Decodificacion de trama recibida
		Vb_f=int(trama[3:5].encode('hex'),16)
		Vb_f = Vb_f*96.667*pow(2,-15)
		print "Battery voltage, slow filter= %.2f V" %Vb_f
	
		return Vb_f
		
		'''################################################################
	Permite obtener la temperatura del radiador del controlador de carga
	###################################################################'''	
	def getHeatsinkTemp(self,trama):	
		print trama.encode('hex'),'\n'
		# Decodificacion de trama recibida
		T_hs=int(trama[3:5].encode('hex'),16)
		print "Heatsink temperature= ", T_hs

		return T_hs
		
		'''################################################################
	Permite obtener la temperatura de la bateria
	###################################################################'''	
	def getBattTemp(self,trama):	
		print trama.encode('hex'),'\n'
		# Decodificacion de trama recibida
		print trama[3:5].encode('hex')
		T_batt=int(trama[3:5].encode('hex'),16)
		print "Battery temperature= ",T_batt
		
		return T_batt
		
		'''################################################################
	Permite obtener el voltaje de referencia del regulador de carga
	###################################################################'''	
	def getChargeRegVR(self,trama):	
		print trama.encode('hex'),'\n'
		# Decodificacion de trama recibida
		V_ref=int(trama[3:5].encode('hex'),16)
		V_ref =V_ref*96.667*pow(2,-15)
		print "Charge regulator reference voltage= %.2f" %V_ref

		return V_ref
		

'''		
if __name__ == "__main__":
	
	nombreSensores2=[] # la uso para saber que sensores hay o tiene TRistar
	x=SensorTristarTS60() # Creacion de un objeto tristar
	#print x.listaSensores[3]
	nombreSensores2 = x.ListarSensores() # le pido que me de el nombre de los sensores que contiene
	print "Listado de sensores: ",nombreSensores2 # imprimo los nombres de sensore 
	#x.Sensar('V_bat')
	#x.Sensar(nombreSensores2.index('V_bat')) # le pido al sensor V_bat que me de su valor
	#x.Sensar(nombreSensores2.index('V_bat'))
	
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

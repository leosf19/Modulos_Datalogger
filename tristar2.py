# -*- coding: utf-8 -*-
#!/usr/bin/python
import time, datetime
import serial
import os
import Queue
from sensor import *

''' Esta es la clase generica que va a contener a las clases de abajo.
Es la clase padre
'''
class TristarTS60(object):
	
	global tiempoInicial
	global tiempoTranscurrido 
	
	def __init__(self,name):
		
		self.name = name
		
		self.tiempoInicial = time.time()
		# Diccionario que va a tener los ultimos valores de los sensores,
		# que pida por puerto serial al equipo, siendo mas facil ingresar
		# mediante el uso de la key
		self.valorSensor = { 'TS60-V_bat' : 0,
								'TS60-V_pan' : 0,
								'TS60-I_carga' : 0,
								'TS60-I_load' : 0,
								'TS60-T_equipo' : 0,
								'TS60-T_bat' : 0}
		
	def getName(self):
		return self.name
	
	def getValor(self,nombre_sensor):
		# Verifico si el tiempo transcurrido en segs es mucho (> 1 min)
		self.tiempoTranscurrido = time.time()-self.tiempoInicial
		#tiempoTranscurrido = tiempoTranscurrido / 60
		print "tiempoInicial: ", self.tiempoInicial
		print "tiempoTranscurrido: ",self.tiempoTranscurrido
		print self.valorSensor
		self.tiempoInicial = self.tiempoTranscurrido
		
		if self.tiempoTranscurrido < 36000: # paso mas de 1 segundo
			return self.valorSensor[nombre_sensor]
		else:
			self.readRegisters()
			return self.valorSensor[nombre_sensor]
			
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
	def readRegisters(self):
		
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
		
		# Point Addr = 4009 -> Vbat
		adc_vb_f=int(out[3:5].encode('hex'),16) # Convierto de string hexa a int
		adc_vb_f= adc_vb_f*96.667*pow(2,-15)# Obtengo el valor decimal
		print "Battery voltage, filtered= %.2f" %adc_vb_f
	
		# Point Addr = 4010
		adc_vs_f=int(out[5:7].encode('hex'),16)
		adc_vs_f = adc_vs_f*96.667*pow(2,-15)
		print "Battery sense voltage, filtered= %.2f" %adc_vs_f
	
		# Point Addr = 4011
		# Tension del panel solar
		adc_vx_f=int(out[7:9].encode('hex'),16)
		adc_vx_f = adc_vx_f*139.15*pow(2,-15)
		print "Array/Load voltage, filtered= %.2f" %adc_vx_f
	
		# Point Addr = 4012
		adc_ipv_f=int(out[9:11].encode('hex'),16)
		adc_ipv_f = adc_ipv_f*66.667*pow(2,-15)
		print "Charging current, filtered= %.2f" %adc_ipv_f
	
		# Point Addr = 4013
		adc_iload_f=int(out[11:13].encode('hex'),16)
		adc_iload_f = adc_iload_f*316.67*pow(2,-15)
		print "Load current, filtered= %.2f" %adc_iload_f
	
		# Point Addr = 4014
		Vb_f=int(out[13:15].encode('hex'),16)
		Vb_f = Vb_f*96.667*pow(2,-15)
		print "Battery voltage, slow filter= %.2f V" %Vb_f
	
		# Point Addr = 4015
		T_hs=int(out[15:17].encode('hex'),16)
		print "Heatsink temperature= ", T_hs
	
		# Point Addr = 4016
		T_batt=int(out[17:19].encode('hex'),16)
		print "Battery temperature= ",T_batt
	
		# Point Addr = 4017
		V_ref=int(out[19:21].encode('hex'),16)
		V_ref =V_ref*96.667*pow(2,-15)
		print "Charge regulator reference voltage= %.2f" %V_ref
		
		sp.close()
		
		# Actualizo los valores de cada sensor en el diccionario
		self.valorSensor['TS60-V_bat']=round(adc_vb_f,2)
		self.valorSensor['TS60-V_pan']=round(adc_vx_f,2)
		self.valorSensor['TS60-I_carga']=round(adc_ipv_f,2)
		self.valorSensor['TS60-I_load']=round(adc_iload_f,2)
		self.valorSensor['TS60-T_equipo']=T_hs
		self.valorSensor['TS60-T_bat']=T_batt
		
class TS60V_Bat(TristarTS60):
	"Clase que representa a un Sensor."
	def __init__(self,name="TS60-V_bat"):
		# llamamos al constructor Sensor
		TristarTS60.__init__(self,name)
	
	def getValor(self):
		return TristarTS60.getValor("TS60-V_bat")
		
class TS60V_pan(TristarTS60):
	def __init__(self,name="TS60-V_pan"):
		# llamamos al constructor Sensor
		TristarTS60.__init__(self,name)
		
class TS60I_carga(TristarTS60):
	def __init__(self,name="TS60-I_car"):
		# llamamos al constructor de Sensor
		TristarTS60.__init__(self,name)
	
class TS60I_load(TristarTS60):
	def __init__(self,name="TS60-I_load"):
		# llamamos al constructor Sensor
		TristarTS60.__init__(self,name)
		
class TS60T_equipo(TristarTS60):
	def __init__(self,name="TS60-T_equipo"):
		# llamamos al constructor Sensor
		TristarTS60.__init__(self,name)
	
class TS60T_bat(TristarTS60):
	def __init__(self,name="TS60-T_bat"):
		# llamamos al constructor Sensor
		TristarTS60.__init__(self,name)
	
	
		
'''		
if __name__ == '__main__':
	
	print TS60I_carga().getName()
	print TS60I_load().getName()
	print TS60V_pan().getName()
	print TS60V_pan().getValor(TS60V_pan().getName())
'''	

# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import serial
import os
import json
from tristar2 import *
from class_baseDatos import BaseDatos

import cPickle as pickle

def main():

	# Tiene que tener un método ListarSensores que me muestre todos los 
	# sensores que esta manejando.
	'''
	Sensor = { 'TS60-V_bat' : [TS60V_Bat(),10],
				'TS60-V_pan' : [TS60V_pan(),15],
				'TS60-I_carga' : [TS60I_carga(),10],
				'TS60-I_load' : [TS60I_load(),10],
				'TS60-T_equipo' : [TS60T_equipo(),25],
				'TS60-T_bat' : [TS60T_bat(),25]
				}
	
	f1 = file('/home/leo/Documentos/Datalogger-TESIS/temp.pkl', 'wb')
	pickle.dump(Sensor,f1,True)
	#pickle.dump(TS60V_pan(), f1, True)
	f1.close()
	
	f2 = file('/home/leo/Documentos/Datalogger-TESIS/temp.pkl', 'rb') 
	sensores = pickle.load(f2)
	
	print sensores
	'''
	with open("/home/leo/Documentos/Datalogger-TESIS/sensoresEstado.json", 'r') as fp:
		sensores = json.load(fp)
	fp.close()
	
	print sensores
	
	# De esta manera estoy guardando en v el objeto que corresponde
	exec("v=%s()" % sensores['TS60V_bat'][0])
	print v
	exec("x=v.getName()")
	print x
	
	
	tiempo = 1
	
	while 1:
		
		for key,value in sorted(sensores.items()):
			if tiempo%value[1]==0 and value[2]=='Activado':
				print tiempo%value[1]
				print key
				print "Tiempo: ",tiempo
				print "Tsensor: ",value[1]
				# Esto me permite guardar el nombre de la instancia que 
				# voy a usar
				exec("v=%s()" % sensores[key][0])
				# En esta voy a usar el objeto para pedirle su valor
				exec("x=v.getValor(key)")
				print x
				#print sensores[key][0].getValor(key)
				#valor = sensores[key][0].getValor(key)
				#BaseDatos(5).storeData("%.2f" %valor, sensores[key][0].getName(), sensores[key][0].getUnit())
				#time.sleep(2)
			else:
				print "------------------------------", tiempo
				pass
		tiempo += 1
		time.sleep(1)		
		
		'''
		for key,value in sorted(sensores.items()):
			if tiempo%value[1]==0 and value[3]=='Activado':
				print tiempo%value[1]
				print key
				print "Tiempo: ",tiempo
				print "Tsensor: ",value[1]
				#print sensores[key][0].getValor(key)
				valor = sensores[key][0].getValor(key)
				BaseDatos(5).storeData("%.2f" %valor, sensores[key][0].getName(), sensores[key][0].getUnit())
				#time.sleep(2)
			else:
				#tiempo = tiempo +1
				print "------------------------------", tiempo
				#time.sleep(5)
				pass
			#time.sleep(2)
		tiempo += 1
		time.sleep(1)
		'''
	
	return 0

if __name__ == '__main__':
	main()

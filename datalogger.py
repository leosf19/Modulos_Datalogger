# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import serial
import os
import Queue
from tristar2 import *
from class_baseDatos import BaseDatos

import cPickle as pickle

def main():

	# Tiene que tener un método ListarSensores que me muestre todos los 
	# sensores que esta manejando.
	'''
	print TS60I_carga().getName()
	print TS60I_load().getName()
	print TS60V_pan().getName()
	'''
	Sensor = { 'TS60-V_bat' : [TS60V_Bat(),10],
				'TS60-V_pan' : [TS60V_pan(),15],
				'TS60-I_carga' : [TS60I_carga(),10],
				'TS60-I_load' : [TS60I_load(),10],
				'TS60-T_equipo' : [TS60T_equipo(),25],
				'TS60-T_bat' : [TS60T_bat(),25]}
	
	f1 = file('/home/leo/Documentos/Datalogger-TESIS/temp.pkl', 'wb')
	pickle.dump(Sensor,f1,True)
	#pickle.dump(TS60V_pan(), f1, True)
	f1.close()
	
	f2 = file('/home/leo/Documentos/Datalogger-TESIS/temp.pkl', 'rb') 
	sensores = pickle.load(f2)

	tiempo = 1
	
	while 1:
		
		for key,value in sorted(sensores.items()):
			if tiempo%value[1]==0:
				print key
				print "Tiempo: ",tiempo
				print "Tsensor: ",value[1]
				valor = sensores[key][0].getValor(key)
				print valor
				BaseDatos(5).storeData("%.2f" %valor,sensores[key][0].getName(),"P01")
				#print sensores[key][0].getName()
				#time.sleep(2)
			else:
				#tiempo = tiempo +1
				print "------------------------------", tiempo
				#time.sleep(5)
				pass
			#time.sleep(2)
		tiempo += 1
		time.sleep(5)
		'''
		time.sleep(5)
		print "T_bat: ",sensores['TS60-T_bat'][0].getValor('TS60-T_bat')
		#print "T_bat: ",y.getValor(TS60T_bat().getName())
		time.sleep(15)
		print "V_bat: ",sensores['TS60-V_bat'][0].getValor('TS60-V_bat')
		'''
		
	return 0

if __name__ == '__main__':
	main()

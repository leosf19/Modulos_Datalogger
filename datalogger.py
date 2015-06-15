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

	f1 = file('/home/leo/Documentos/Datalogger-TESIS/temp.pkl', 'wb')
	pickle.dump(TS60V_pan(), f1, True)
	f1.close()
	
	f2 = file('/home/leo/Documentos/Datalogger-TESIS/temp.pkl', 'rb') 
	a2 = pickle.load(f2)
	# Tiene que tener un método ListarSensores que me muestre todos los 
	# sensores que esta manejando.
	'''
	print TS60I_carga().getName()
	print TS60I_load().getName()
	print TS60V_pan().getName()
	'''
	Sensor = { 'TS60-V_bat' :TS60V_pan,
				'TS60-V_pan' : TS60T_bat}
	
	x = TS60V_pan()
	y = TS60T_bat()
	while 1:
		print "V_pan: ",a2.getValor('TS60-V_bat')
		#print "T_bat: ",y.getValor(TS60T_bat().getName())
		time.sleep(20)
		
	return 0

if __name__ == '__main__':
	main()

# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import serial
import os
import json
from tristar2 import *
import cPickle as pickle

'''Este modulo se encarga de generar un diccionario persistente en memoria
el cual va a tener el nombre de la instancia de cada sensor, el tiempo de 
cada sensor, el timestamp y su estado. La idea es que sirva de nexo entre
el archivo generado por el servidor 
'''

def generaPersistente(sensoresEstado):
	
	Sensor = { 'TS60-V_bat' : [TS60V_Bat(),10,int(time.time())],
				'TS60-V_pan' : [TS60V_pan(),15,int(time.time())],
				'TS60-I_carga' : [TS60I_carga(),10,int(time.time())],
				'TS60-I_load' : [TS60I_load(),10,int(time.time())],
				'TS60-T_equipo' : [TS60T_equipo(),60,int(time.time())],
				'TS60-T_bat' : [TS60T_bat(),60,int(time.time())]
				}
				
	for key, value in Sensor.items():
		Sensor[key] = value[0],value[1],value[2],sensoresEstado[key]
		print Sensor[key]
		
	f1 = file('/home/leo/Documentos/Datalogger-TESIS/temp.pkl', 'wb')
	pickle.dump(Sensor,f1,True)
	f1.close()


# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import serial
import os
import Queue
from tristar2 import SensorTristarTS60
from class_baseDatos import BaseDatos


def main():

	nombreSensores=[] # la uso para saber que sensores hay o tiene SensorTristarTS60
	#global tnow
	
	st=SensorTristarTS60() # Creacion de un objeto tristar
	
	nombreSensores = st.ListarSensores() # le pido que me de el nombre de los sensores que contiene
	
	print "Listado de sensores:\n",nombreSensores # imprimo los nombres de sensores
	
	tiemposSensores = {}
	
	# Genero un diccionario de nombre de sensores y los tiempos maximos de c/u
	for i in range(len(nombreSensores)):
		#tiemposSensores[nombreSensores[i]]=1			# Solo con tmax
		tiemposSensores[nombreSensores[i]]=[1,0]	# Con tmax y tactual
		
	
	print tiemposSensores
	#print tiempoSensores['V_bat'][0]
	 
	#st.Sensar('V_bat')
	while 1:
		# Con el sorted lo que logro es leer la lista ordenada
		for key, value in sorted(tiemposSensores.items(),key=lambda x: x[1]):
			print key
			tmax = value[0]
			tnow = value[1]
			if 	tnow == tmax:
				print "Entre al if"
				tiemposSensores[key][1]=0
				dato=st.Sensar(key)
				print "Dato: ",dato
				BaseDatos(5).storeData("%.2f" %dato, key, "P01")
			else:
				print "Sumo uno"	
				tiemposSensores[key][1]=tnow+1
				print tiemposSensores[key]
			time.sleep(1)
	
	return 0

if __name__ == '__main__':
	main()

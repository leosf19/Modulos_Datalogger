#  sensor.py
#  Copyright 2015 Leandro Saavedra
#  

class Sensor(object):
	'''
		Permite crear un sensor. Parametros:
		Nombre / Valor / Parametros (pensado para despues)
	'''
	def __init__(self,name):
		self.name = name
		self.value = 0
	
	# Devuelve el nombre del sensor	
	def getName(self):
		return self.name
	
	# Modifica el nombre del sensor	
	def setName(self,newname):
		self.name=newname
	
	# Guarda un valor en la cola
	def setValue(self,value):
		self.value=value
	
	# Devuelve el valor medido
	def getValue(self):
		if self.value ==0:
			return "No-value"
		else:
			return self.value
		#if self.ColaSensor.empty() == True:
		#	return "Vacia"
		#else:
		#	return self.colaSensor.get()
		
		# Aca deberia hacer una llamada al metodo mas abstracto "sensar(name)"
		# donde acorde al nombre del sensor que lo llama pide de la cola de ese sensor
		# el valor 
'''
class TS60V_Bat(Sensor):
	"Clase que representa a un Sensor."
	def __init__(self,name):
		# llamamos al constructor Sensor
		Sensor.__init__(self,"TS60-Vbat")
			
	def getValue(self):
		return self.valorSensores["TS60-Vbat"]
		
class TS60V_pan(Sensor):
	def __init__(self,name="TS60-Vpan"):
		# llamamos al constructor Sensor
		Sensor.__init__(self,name)
		
class TS60I_carga(Sensor):
	def __init__(self,name="TS60-Icar"):
		# llamamos al constructor de Sensor
		Sensor.__init__(self,name)
	
class TS60I_load(Sensor):
	def __init__(self,name="TS60-Iload"):
		# llamamos al constructor Sensor
		Sensor.__init__(self,name)
		
class TS60T_equipo(Sensor):
	def __init__(self,name="TS60-Teq"):
		# llamamos al constructor Sensor
		Sensor.__init__(self,name)
	
class TS60T_bat(Sensor):
	def __init__(self,name="TS60-Tbat"):
		# llamamos al constructor Sensor
		Sensor.__init__(self,name)
'''		
'''
sens1=sensV_Bat('V_bat')
print sens1.getName()
sens1.setValue(2)
print sens1.getValue()

#sens1.setName('I_carga')
#print sens1.getName()
#sens2=sensT_bat('T_bat')
#print sens2.getName()		
'''
#print TS60I_carga().getName()

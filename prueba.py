# -*- coding: utf-8 -*-
#!/usr/bin/python
import time
import serial
import os
import Queue
from tristar2 import *
from class_baseDatos import BaseDatos


x=TS60V_Bat()
y=TS60V_pan()
z=TS60I_carga()

print x.valorSensor

x.valorSensor['TS60-V_bat'][1]=1

print x.valorSensor

print y.valorSensor

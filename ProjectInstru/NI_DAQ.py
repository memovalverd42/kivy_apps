import nidaqmx
from nidaqmx import Task

def get_temp():
    ''' Funcion para lectura de temperatura desde modulo NI9211 '''
    with Task() as task:
        task.ai_channels.add_ai_thrmcpl_chan("cDAQ1Mod2/ai0", thermocouple_type=nidaqmx.constants.ThermocoupleType(10073))
        return task.read()

def get_hum():
    ''' Funcion para lectura de humedad a traves del DAC ESP32 desde modulo NI9215 '''
    with Task() as task:
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
        volt = task.read()
        h = int((volt*90)/3.3)
        return h

def light(state: bool):
    ''' Funcion para encencer/apagar foco a traves del modulo NI9401 '''
    with Task() as task:
        task.do_channels.add_do_chan("cDAQ1Mod4/port0/line1")
        task.write(not state)

def fan(state: bool):
    ''' Funcion para encencer/apagar ventilador a traves del modulo NI9401 '''
    with Task() as task:
        task.do_channels.add_do_chan("cDAQ1Mod4/port0/line0")
        task.write(not state)
        
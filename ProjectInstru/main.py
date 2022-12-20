from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.vkeyboard import VKeyboard 
from kivy.core.window import Window

import NI_DAQ

VKeyboard.docked = True

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '700')
Config.write()

temperatura_min = 27.0
temperatura_max = 30.0

light_state = True
fan_state = True


class App(MDApp):
    title="Control de Incubadora"
    def build(self):
        Clock.schedule_interval(self.callback, 5)    # Lectura de parametros cada 5s
        return Builder.load_file('UI.kv')            # Construccion de la interfaz

    def callback(self, dt):
        ''' Funcion para la lectura continua de los datos de los modulos '''
        global temperatura_max, temperatura_min, light_state, fan_state
        try:
            temp = NI_DAQ.get_temp()        # Lectura de temperatura
            hum = NI_DAQ.get_hum()          # Lectura de humedad

            if temp <= temperatura_min:     # Si temperatura leida es menor que la temperatura minima...
                # if lightState:
                self.root.ids.foco01.source = './images/focoON.png'
                self.root.ids.venti01.source = './ventiladorOFF.png'
                NI_DAQ.light(True)
                NI_DAQ.fan(False)
                # lightState = False

            elif temp >= temperatura_max:     # Si temperatura leida es mayor que la temperatura maxima...
                self.root.ids.foco01.source = './images/focoOFF.png'
                self.root.ids.venti01.source = './ventiladorON.gif'
                NI_DAQ.light(False)
                NI_DAQ.fan(True)

            else:
                if light_state:
                    self.root.ids.foco01.source = './images/focoOFF.png'
                    NI_DAQ.light(False)
                if fan_state:
                    self.root.ids.venti01.source = './ventiladorOFF.png'
                    NI_DAQ.fan(False)
                # lightState = True
            
            self.root.ids.temp02.text = str(round(temp, 2)) + '°C'
            self.root.ids.hum02.text = str(hum) + '%'
            
        # print(temperatura)
        except:
            self.root.ids.temp02.text = 'Error en el modulo'
            self.root.ids.hum02.text = 'Error en el modulo'
        # print(self.root.ids.temp02.text)

    def set_points(self):
        ''' Funcion para establecer los set-points de temperatura '''
        global temperatura_max, temperatura_min
        try:
            content_temp_min = self.root.ids.temp_min01.text
            content_temp_max = self.root.ids.temp_max01.text
            if content_temp_min != '': 
                temperatura_min = float(content_temp_min)
            if content_temp_max != '':
                temperatura_max = float(content_temp_max)

            print(f'{temperatura_min = } | {temperatura_max = }')
        except:
            pass

    def toggle_light(self):
        ''' Funcion para encender/apagar el foco '''
        global light_state
        state = self.root.ids.foco01.source
        if state == './images/focoON.png':
            self.root.ids.foco01.source = './images/focoOFF.png'
            light_state = True
            try:
                NI_DAQ.light(False)
            except:
                print('Error en el modulo')

        else:
            self.root.ids.foco01.source = './images/focoON.png'
            light_state = False
            try:
                NI_DAQ.light(True)
            except:
                print('Error en el modulo')

        # print('Luz encendida')

    def toggle_fan(self):
        ''' Funcion para encender/apagar el ventilador '''
        global fan_state
        state = self.root.ids.venti01.source 
        if state == './ventiladorON.gif':
            fan_state = True
            self.root.ids.venti01.source = './ventiladorOFF.png'
            try:
                NI_DAQ.fan(False)
            except:
                print("Error en el modulo")
        else:
            fan_state = False
            self.root.ids.venti01.source = './ventiladorON.gif'
            try:
                NI_DAQ.fan(True)
            except:
                print("Error en el modulo")

        # print(self.root.ids.venti01.source)
        # print('Fan encendido')
        
App().run()
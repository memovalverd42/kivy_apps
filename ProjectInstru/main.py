from kivy.lang import Builder

from kivymd.app import MDApp
from kivy.clock import Clock

from kivy.config import Config
from kivy.uix.vkeyboard import VKeyboard 
from kivy.core.window import Window

VKeyboard.docked = True

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '800')
Config.write()

class App(MDApp):
    title="Control de Incubadora"
    def build(self):
        return Builder.load_file('UI.kv')

    def start(self):
        Clock.schedule_interval(self.callback, 0.5)

    def callback(self, dt):
        print('In callback')
    
    # def calculo(self):
    #     ts = float(self.root.ids.ts01.text)
    #     po = float(self.root.ids.po01.text)
    #     label_result = self.root.ids['resultado']
    #     r = get_P_y_K(po, ts)
    #     label_result.text = r
    #     print(r)

    def set_points(self):
        temperatura = float(self.root.ids.temp01.text)
        humedad = float(self.root.ids.hum01.text)
        print(f'{temperatura = } | {humedad =}')

    def toggle_light(self):
        state = self.root.ids.foco01.source
        if state == './images/focoON.png':
            self.root.ids.foco01.source = './images/focoOFF.png'
        else:
            self.root.ids.foco01.source = './images/focoON.png'
        print('Luz encendida')

    def toggle_fan(self):
        state = self.root.ids.venti01.source 
        if state == './ventiladorON.gif':
            self.root.ids.venti01.source = './ventiladorOFF.png'
        else:
            self.root.ids.venti01.source = './ventiladorON.gif'

        # print(self.root.ids.venti01.source)
        # print('Fan encendido')
        
    # def on_start(self):
    #     App().start()

# class Cliente(MDApp):
#     def build(self):
#         objeto = App()

#         Clock.schedule_interval(objeto.HOLA, 30)

# App().start()
App().run()
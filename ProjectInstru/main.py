from kivy.lang import Builder
from kivy.metrics import dp


from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock

from kivy.config import Config
from kivy.uix.vkeyboard import VKeyboard 
from kivy.core.window import Window
import math

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
        
    # def on_start(self):
    #     App().start()
# class Cliente(MDApp):
#     def build(self):
#         objeto = App()

#         Clock.schedule_interval(objeto.HOLA, 30)

App().start()
App().run()
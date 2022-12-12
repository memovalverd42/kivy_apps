from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

from kivy.config import Config
from kivy.uix.vkeyboard import VKeyboard 
from kivy.core.window import Window
import math

VKeyboard.docked = True

Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '300')
Config.write()

zetas = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
pos = [0.2, 1.5, 4.6, 9.5, 16.3, 25.4, 37.2]

x0 = 0
x1 = 0
y0 = 0
y1 = 0

def get_P_y_K(p_o, t_s):
    cont = 0

    if p_o > 37.2:
        return "El PO que colocaste es muy grande"
    for i in pos:
        cont += 1
        if i == p_o:
            break

        if p_o > i:
            x0 = i
            x1 = pos[cont]
            y0 = zetas[cont-1]
            y1 = zetas[cont]
    
    zeta = (((p_o-x0)*(y1-y0))/(x1-x0))+y0
    zetaOmega = 4/t_s
    theta = math.degrees(math.acos(zeta))
    tan = math.tan(60)
    y = zetaOmega*math.tan(math.radians(theta))
    omega = math.sqrt((zetaOmega**2)+(y**2))
    K=omega**2
    P=2*zetaOmega

    return f"P = {round(P, 4)} & K = {round(K, 4)}"

class Test(MDApp):
    title="Practica Inventada 2 - Control"
    def build(self):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"PO %{i}",
                "height": dp(56),
                "on_release": lambda x=f"PO %{i}": self.menu_callback(x, i),
             } for i in range(5, 40, 5)

        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        return Builder.load_file('UI.kv')

    def calculo(self):
        ts = float(self.root.ids.ts01.text)
        po = float(self.root.ids.po01.text)
        label_result = self.root.ids['resultado']
        r = get_P_y_K(po, ts)
        label_result.text = r
        print(r)
    
    def slider(self, *args):
        print(args[1])
        self.root.ids.ts01.text = str(args[1])

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item, p_o2):
        self.menu.dismiss()
        Snackbar(text=text_item, duration=0.5).open()
        porce = text_item.split('%')
        print(text_item, porce)
        self.root.ids.po01.text = str(porce[1])


Test().run()
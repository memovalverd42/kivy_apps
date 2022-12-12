import cmath
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('IU.kv')

def degree2rad(fase):
    result = fase*cmath.pi/180
    return result

def rad2degree(fase):
    fase = (fase*180)/cmath.pi
    if fase < 0:
        fase = fase + 360
    return fase

def coeficiente_A(complex1, complex2, complex3):
    coef = (complex2-complex1)/complex3
    coef_polar = cmath.polar(coef)
    coef_degree = rad2degree(coef_polar[1])
    result = [coef_polar[0], coef_degree, coef]
    return result

def peso(num1, den1):
    peso = -num1/den1
    peso_polar = cmath.polar(peso)
    peso_degree = rad2degree(peso_polar[1])
    result = [peso_polar[0], peso_degree]
    return result


class BoxAplication(BoxLayout):
    def calculo(self):
        N = cmath.rect(float(self.nm.text), degree2rad(float(self.nf.text)))
        N2 = cmath.rect(float(self.n2m.text), degree2rad(float(self.n2f.text)))
        W = cmath.rect(float(self.wm.text), degree2rad(float(self.wf.text)))

        A = coeficiente_A(N, N2, W)
        Wp = peso(N, A[2])

        R = f"{round(Wp[0], 4)} > {round(Wp[1], 4)}°"
        print(R)
        self.result.text = str(R)

class Main(App):
    title='Practica Inventada 1 - Vibraciones Mecanicas'
    def build(self):
        return BoxAplication()


Main().run()

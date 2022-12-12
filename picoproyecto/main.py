"""
-->  PICOPROYECTO - PROGRAMADOR DE LLENADO DE TANQUE

-->  PROGRAMACIÓN AVANZADA

-->  VALVERDE BAEZ GUILLERMO
"""

# Base de datos sqlite3
import sqlite3
# Obtener fecha y hora                     
from datetime import  datetime
# Conexion con ESP32 con sockets
import socket

# KIVYMD MODULOS
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem
from kivymd.uix.textfield import MDTextField
from kivy.config import Config

# Config.set('graphics', 'width', '380')
# Config.set('graphics', 'height', '720')
# Config.write()


conexion = sqlite3.connect('picoproyecto/sensor.db')    # Conexion a base de datos sqlite3 --> sensor.db
cursor   = conexion.cursor()                            # Creación de un cursor para ejecutar sentencias SQL

unidades="Litros" # Unidades del volumen por defecto
# volumen_total=0   # Variable global para guardar el volumen total del tanque

class main(MDApp):
    tipo_de_tanque = 'Cuadrado'
    title="REGISTRO DE LLENADO" # Titulo de la ventana

    def build(self):          # Clase constructora
        menu_items = [        # Añadimos las opciones que tiene el menú en el header
            {
                "viewclass": "OneLineListItem",
                "text": "Listros",
                "height": dp(56),
                "on_release": lambda x="Litros": self.menu_callback(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Galones",
                "height": dp(56),
                "on_release": lambda x="Galones": self.menu_callback(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "%",
                "height": dp(56),
                "on_release": lambda x="%": self.menu_callback(x),
            },
        ]

        menu_items_2 = [        # Añadimos las opciones que tiene el menú en el header
            {
                "viewclass": "OneLineListItem",
                "text": "Cuadrado/Rectangular",
                "height": dp(56),
                "on_release": lambda x="Cuadrado/Rectangular": self.menu_callback_2(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Circular",
                "height": dp(56),
                "on_release": lambda x="Circular": self.menu_callback_2(x),
            },
        ]


        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

        self.menu2 = MDDropdownMenu(
            items=menu_items_2,
            width_mult=4,
        ) 

        return Builder.load_file('UI.kv')
    

    def callback(self, button):                             # Función para configurar boton que desplegará menú en el header (se manda a llamar en UI.kv)
        self.menu.caller = button
        self.menu.open()

    def callback_2(self, button):                             # Función para configurar boton que desplegará menú en el header (se manda a llamar en UI.kv)
        self.menu2.caller = button
        self.menu2.open()

    def menu_callback(self, text_item):                     # Función para obtener el valor seleccionado del menú en el header (Configuración de unidades: Litros o Galones)
        self.menu.dismiss()
        unidades = text_item                                  # La variable 'unidades' toma el valor seleccionado en el menú
        self.root.ids.unidades01.text = unidades            # Asignamos el nombre de la unidad de volumen a al Label (id: unidades01)
        Snackbar(text=text_item, duration=0.5).open()       # Se lanza una snackbar con la opción se leccionada
        print(unidades, type(unidades))

    def menu_callback_2(self, text_item):                     # Función para obtener el valor seleccionado del menú en el header (Configuración de unidades: Litros o Galones)
        self.menu2.dismiss()
        if text_item == 'Cuadrado/Rectangular':
            self.root.ids.titulo01.title = 'TANQUE CUADRADO'
            self.root.ids.ancho01.hint_text = 'Ancho (cm)'
            self.root.ids.largo01.hint_text = 'Largo (cm)'
        elif text_item == 'Circular':
            self.root.ids.titulo01.title = 'TANQUE CIRCULAR'
            self.root.ids.ancho01.hint_text = 'Diametro (cm)'
            self.root.ids.largo01.hint_text = '*vacio*'
        Snackbar(text=text_item, duration=0.5).open()       # Se lanza una snackbar con la opción se leccionada
    

    def on_start(self):                                     # Función que se encarga de mostrar los items de la base de datos en scrollview
        self.root.ids.container.clear_widgets()             # Eliminamos todos los widgets "viejos" para poder meter el listado actualizado
        cursor.execute("SELECT * FROM historial;")          # Sentencia SQL para seleccionar todos los datos de la base de datos
        conexion.commit()                                   # Ejecutamos sentencia
        data = cursor.fetchall()                            # Guardamos la tupla de datos en variable 'data'
        # print(data)
        for i in data[::-1]:                                # Ciclo para enlistar los datos de mas reciente a mas viejo
            muestra = f"{i[1]} | {i[2]} | {i[3]}"           # muestra = Llenado | Fecha | Hora
            self.root.ids.container.add_widget(
                OneLineListItem(text=f"{muestra}")
            )

    def getvolumen(self):                                                   # Funcion para obtener el volumen del tanque
        alto=self.root.ids.altura01.text                                    # Obtenemos el valor de la altura (TextField: id: altura01)
        ancho=self.root.ids.ancho01.text                                    # Obtenemos el valor del ancho (TextField: id: ancho01)
        largo=self.root.ids.largo01.text                                    # Obtenemos el valor del largo (TextField: id: largo01)
        maxi = 0
        if self.root.ids.titulo01.title.split()[1] == 'CUADRADO':
            if self.root.ids.unidades01.text == 'Litros':                       # Si las unidades seleccionadas son Litros se ejecuta
                maxi = float(alto)*float(ancho)*float(largo)*0.001
            elif self.root.ids.unidades01.text == 'Galones':                    # Si las unidades seleccionadas son Galones se ejecuta    
                maxi = float(alto)*float(ancho)*float(largo)*0.000264           
            elif self.root.ids.unidades01.text == '%':                          # Si las unidades seleccionadas son % se ejecuta
                maxi = 100

        elif self.root.ids.titulo01.title.split()[1] == 'CIRCULAR':
            if self.root.ids.unidades01.text == 'Litros':                       # Si las unidades seleccionadas son Litros se ejecuta
                maxi = (3.14159265*(float(ancho)/2)**2)*float(alto)*0.001
            elif self.root.ids.unidades01.text == 'Galones':                    # Si las unidades seleccionadas son Galones se ejecuta    
                maxi = (3.14159265*(float(ancho)/2)**2)*float(alto)*0.000264           
            elif self.root.ids.unidades01.text == '%':                          # Si las unidades seleccionadas son % se ejecuta
                maxi = 100                                            
            # self.root.ids.slider01.max=int(100)
        self.root.ids.slider01.max=maxi                              # Añadimos como valor maximo el volumen total del estanque
        self.root.ids.resultado.text=''
        print(maxi, largo)
    
    def slider(self, *args):                                # Función para el obetener datos del slider y asignar valores a un Label (id: cantidad01)
        # print(args[1])
        self.root.ids.cantidad01.text = str(args[1])
        Snackbar(text=self.root.ids.cantidad01.text + ' ' + self.root.ids.unidades01.text + ' ' + 'de' + ' ' + str(self.root.ids.slider01.max), duration=0.5).open()       # Se lanza una snackbar con la opción se leccionada

    def calculo(self):                                                               # Función para realizar el envio de datos y su recepción
        alto=self.root.ids.altura01.text                                             # Obtenemos el valor de la altura (TextField: id: altura01)
        ancho=self.root.ids.ancho01.text                                             # Obtenemos el valor del ancho (TextField: id: ancho01)
        largo=self.root.ids.largo01.text                                             # Obtenemos el valor del largo (TextField: id: largo01)
        requisito=self.root.ids.cantidad01.text                                      # Obtenemos porcentaje o volumen deseado deseado de Label (id: cantidad01)
        unit = self.root.ids.unidades01.text                                         # Obtenemos las unidades en las que va a trabajar la ESP32                                                   
        if largo == '':
            largo = 'vacio'
        send_dato = largo + ' ' + ancho + ' ' + alto + ' ' + requisito + ' ' + unit  # String enviada a la ESP32
      
        print(send_dato)
        try:                                                                         # Intento de creación de socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print ("Socket Credado exitosamente")
        except socket.error as err:                                                  # Si hay fallo creando socket
            print ("error en la creacion del socket %s" %(err))

        direccionServidor = "192.168.100.116"                                       # Dirección IP del servidor (ESP32)
        puerto=8000                                                                 # PUERTO DEL SERVIDOR
        s.connect((direccionServidor, puerto))                                           
        s.sendall(send_dato.encode())                                               # Envio del string 'send_dato' codificado
        recivido = s.recv(1024).decode()                                            # Respuesta recibida -> "ALERT 'VOLUMEN/PORCENTAJE'"
        alerta, distancia = recivido.split()                                        # Dividimos el string
        fecha, hora = datetime.today().strftime('%Y-%m-%d %H:%M').split()           # Obtenemos el la fecha y la hora
        datos = (distancia, fecha, hora)                                            # Tupla con datos para la DB
        cursor.execute("INSERT INTO historial VALUES(null, ?, ?, ?);", datos)       # Sentencia para añadir los datos a la DB
        conexion.commit()
        print(recivido)
        self.root.ids.resultado.text = alerta                                       # Se pone la alerta en el Label: resultado
        # Se vacian los TextField
        self.root.ids.altura01.text = ''
        self.root.ids.ancho01.text = ''
        self.root.ids.largo01.text = ''
        self.on_start()                                 # Actualizamos la lista de los registross

main().run()


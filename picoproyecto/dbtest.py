import sqlite3 
from datetime import datetime



conexion = sqlite3.connect('sensor.db')
# #cursor

cursor = conexion.cursor()
# #creación de tablas

cursor.execute("INSERT INTO historial VALUES(null, 'nuevo', '20-07-2020', '8');")

conexion.commit()


# cursor.execute("SELECT * FROM historial;")
# data = cursor.fetchall()
# print(data)
# for i in data[::-1]:
#     muestra = f"{i[1]}cm | {i[2]} | {i[3]}"

#     print(muestra)
    
# fecha, hora = datetime.today().strftime('%Y-%m-%d %H:%M').split()

# print(f"Es el dia {fecha} y son las {hora}")
conexion.close()
import math

ts = float(input('Ts deseado: '))
po = input('PO deseado: ')
x = float(po)
po = float(po)

zetas = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
pos = [0.2, 1.5, 4.6, 9.5, 16.3, 25.4, 37.2]
cont = 0
x0 = 0
x1 = 0
y0 = 0
y1 = 0


for i in pos:
    cont += 1
    if i == po:
        break

    if po > i:
        x0 = i
        x1 = pos[cont]
        y0 = zetas[cont-1]
        y1 = zetas[cont]

zeta = (((x-x0)*(y1-y0))/(x1-x0))+y0
zetaOmega = 4/ts
theta = math.degrees(math.acos(zeta))
tan = math.tan(60)
y = zetaOmega*math.tan(math.radians(theta))
omega = math.sqrt((zetaOmega**2)+(y**2))
K=omega**2
P=2*zetaOmega
print(zeta, zetaOmega, theta, y, omega, K, P)
# # omega = math.sqrt((zetaOmega**2)+())

# # print(type(po), type(x0), type(x1), type(y0), type(y1))

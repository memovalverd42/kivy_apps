import cmath

def degree2rad(fase):
    result = fase*cmath.pi/180
    return result

def rad2degree(fase):
    fase = (fase*180)/cmath.pi
    if fase < 0:
        fase = fase + 360
    return fase

def coeficientes(complex1, complex2, complex3):
    coef = (complex2-complex1)/complex3
    coef_polar = cmath.polar(coef)
    coef_degree = rad2degree(coef_polar[1])
    result = [coef_polar[0], coef_degree, coef]
    return result

def operadores(num, den):
    oper = num/den
    oper_polar = cmath.polar(oper)
    oper_degree = rad2degree(oper_polar[1])
    result = [oper_polar[0], oper_degree, oper]
    return result

def pesos(num1, num2, num3, den1, den2):
    peso = (num1*num2-num3)/(den1*den2)
    peso_polar = cmath.polar(peso)
    peso_degree = rad2degree(peso_polar[1])
    result = [peso_polar[0], peso_degree, peso]
    return result

def coef_p(num1, num2, num3, num4, num5, den1):
    coef = ((num1-num2)-num3*(num4*num5))/den1
    coef_polar = cmath.polar(coef)
    coef_degree = rad2degree(coef_polar[1])
    result = [coef_polar[0], coef_degree, coef]
    return result

def deltaW(num1, num2, num3, den1):
    delta = num1-(num2*num3)/den1
    delta_polar = cmath.polar(delta)
    delta_degree = rad2degree(delta_polar[1])
    result =[delta_polar[0], delta_degree]
    return result

# r = float(input("N_r = ")) 
# phi = float(input(f"N_phi = "))
# N = cmath.rect(r, degree2rad(phi))              # N Tal cual
N = cmath.rect(20, degree2rad(30))

# r2 = float(input("N2_r = ")) 
# phi2 = float(input(f"N2_phi = "))
# N2 = cmath.rect(r2, degree2rad(phi2))           # N2 con Peso de Prueba 1
N2 = cmath.rect(3.9, degree2rad(60))

# r_p = float(input("Wp1_r = "))
# phi_p = float(input("Wp1_phi = "))
# Wp1 = cmath.rect(r_p, degree2rad(phi_p))        # Peso de prueba 1
Wp1 = cmath.rect(30, degree2rad(50))

# r_F = float(input("F_r = ")) 
# phi_F = float(input(f"F_phi = "))
# F = cmath.rect(r_F, degree2rad(phi_F))          # F Tal cual
F = cmath.rect(24, degree2rad(270))

# r_F2 = float(input("F2_r = ")) 
# phi_F2 = float(input(f"F2_phi = "))
# F2 = cmath.rect(r_F2, degree2rad(phi_F2))       # F2 con peso de prueba 1
F2 = cmath.rect(16, degree2rad(300))

# r_p2 = float(input("Wp2_r = "))
# phi_p2 = float(input("Wp2_phi = "))
# Wp2 = cmath.rect(r_p2, degree2rad(phi_p2))      # Peso de prueba 2
Wp2 = cmath.rect(30, degree2rad(270))

# r_N3 = float(input("N3_r = "))
# phi_N3 = float(input("N3_phi = "))
# N3 = cmath.rect(r_N3, degree2rad(phi_N3))       # N3 redidual
N3 = cmath.rect(23, degree2rad(40))

# r_F3 = float(input("F3_r = "))
# phi_F3 = float(input("F3_phi = "))
# F3 = cmath.rect(r_F3, degree2rad(phi_F3))       # F3 residual
F3 = cmath.rect(4.4, degree2rad(60))

# ************Coeficientes de Influencia*****************

A = coeficientes(N, N2, Wp1)
print(f"---> \n A = {A[0]} < {A[1]}°")
alphaA = coeficientes(F, F2, Wp1)
print(f"---> \n alphaA = {alphaA[0]} < {alphaA[1]}°")
B = coeficientes(F, F3, Wp2)
print(f"---> \n B = {B[0]} < {B[1]}°")
betaB = coeficientes(N, N3, Wp2)
print(f"---> \n betaB = {betaB[0]} < {betaB[1]}°")

# ************Operadores de Efecto Cruzado*****************

alpha = operadores(alphaA[2], A[2])
print(f"---> \n alpha = {alpha[0]} < {alpha[1]}°")
beta = operadores(betaB[2], B[2])
print(f"---> \n beta = {beta[0]} < {beta[1]}°")

uno_alpha_beta = 1-alpha[2]*beta[2]
uno_alpha_beta_polar = cmath.polar(uno_alpha_beta)
uno_alpha_beta_degree = rad2degree(uno_alpha_beta_polar[1])
print(f"---> \n (1 - alpha*beta) = {uno_alpha_beta_polar[0]} < {uno_alpha_beta_degree}°")

# # ************Pesos de Balanceo*****************

Wc1 = pesos(beta[2], F, N, A[2], uno_alpha_beta)
print(f"---> \n Wc1 = {Wc1[0]} < {Wc1[1]}°")
Wc2 = pesos(alpha[2], N, F, B[2], uno_alpha_beta)
print(f"---> \n Wc2 = {Wc2[0]} < {Wc2[1]}°")


#***************Vibraciones residuales*******************

# r_Nr = float(input("Nr_r = "))
# phi_Nr = float(input("Nr_phi = "))
# Nr = cmath.rect(r_Nr, degree2rad(phi_Nr))       # Nr redidual
Nr = cmath.rect(6, degree2rad(330))

# r_Fr = float(input("Fr_r = "))
# phi_Fr = float(input("Fr_phi = "))
# Fr = cmath.rect(r_Fr, degree2rad(phi_Fr))       # Fr redidual
Fr = cmath.rect(4, degree2rad(270))

Ap = coef_p(Nr, N, beta[2], Fr, F, Wc1[2])
print(f"---> \n Ap = {Ap[0]} < {Ap[1]}°")

Bp = coef_p(Fr, F, alpha[2], Nr, N, Wc2[2])
print(f"---> \n Bp = {Bp[0]} < {Bp[1]}°")

dWc1 = deltaW(Nr, beta[2], Fr, Ap[2])
print(f"---> \n DWc1 = {dWc1[0]} < {dWc1[1]}°")

dWc2 = deltaW(Fr, alpha[2], Nr, Bp[2])
print(f"---> \n DWc2 = {dWc2[0]} < {dWc2[1]}°")
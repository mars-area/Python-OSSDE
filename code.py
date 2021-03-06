#import matrix lib
import numpy.matlib 
import numpy as np

#k is my attendance number
k = 17

#number 1
#Impedansi Jaringan
Z = np.zeros((7,7), dtype=complex)
Z[0][1] = 3.4914+18.6208j
Z[0][5] = 3.5+20j
Z[0][6] = 3.4914+18.6208j
Z[1][3] = 5.2371+22.6412j
Z[1][5] = 5.3429+26.45j
Z[2][4] = 4.3907+24.0695j
Z[2][5] = 9.3633+27.4022j
Z[3][4] = 3.4914+18.6208j
Z[5][6] = 6.35329+25.0217j

# Line Charging / Y'
Lc = np.zeros((7,7), dtype=complex)
Lc[0][1] = 0.00014j
Lc[0][5] = 0.00014j
Lc[0][6] = 0.00014j
Lc[1][3] = 0.00021j
Lc[1][5] = 0.00035j
Lc[2][4] = 0.00002j
Lc[2][5] = 0.00005j
Lc[3][4] = 0.00014j
Lc[5][6] = 0.00001j
Lc[1][0] = Lc[0][1]
Lc[5][0] = Lc[0][5]
Lc[6][0] = Lc[0][6]
Lc[3][1] = Lc[1][3]
Lc[5][1] = Lc[1][5]
Lc[4][2] = Lc[2][4]
Lc[5][2] = Lc[2][5]
Lc[4][3] = Lc[3][4]
Lc[6][5] = Lc[5][6]

# Matriks Ybus
# off diagonal
Y = np.zeros((7,7), dtype=complex)
Y[0][1] = -1/Z[0][1]
Y[1][0] = Y[0][1]
Y[0][5] = -1/Z[0][5]
Y[5][0] = Y[0][5]
Y[0][6] = -1/Z[0][6]
Y[6][0] = Y[0][6]
Y[1][3] = -1/Z[1][3]
Y[3][1] = Y[1][3]
Y[1][5] = -1/Z[1][5]
Y[5][1] = Y[1][5]
Y[2][4] = -1/Z[2][4]
Y[4][2] = Y[2][4]
Y[2][5] = -1/Z[2][5]
Y[5][2] = Y[2][5]
Y[3][4] = -1/Z[3][4]
Y[4][3] = Y[3][4]
Y[5][6] = -1/Z[5][6]
Y[6][5] = Y[5][6]

# diagonal
for i in range(0,7):
    Y[i][i] = sum(-Y[i,:]) + sum(Lc[i,:])
print('Matrix Ybus :', Y)

# Daya
S = np.array([[0], [100+40j], [75+25j], [-(100+30j)], [-((30+2*k)+(10+2*k)*1j)], [-(45+15j)], [-(50+15j)]], dtype=complex)
print('Daya', S)

# Tegangan
V = np.array([[220], [220], [220], [220], [220], [220], [220]], dtype=complex)

# Gauss Seidel
# V = Vold[1:,:] #return baris 2 sampai 7, kolom 1
for iterasi in range(0,100):
    print('__________________________________________\niterasi ke', iterasi + 1)
    for i in range(1,7):
        arus1 = np.conjugate(np.divide(S[i], V[i]))
        V[i] = 0
        arus2 = np.matmul(Y[i], V)
        V[i] = np.divide(np.subtract(arus1, arus2), Y[i][i])
print('Vbus: \n', V)

# Magnitude
Magnitude = np.real(V)
print('\nV (Magnitude, kV)\n', Magnitude)

# Sudut
Radian = np.angle(V)
print('\nV (Angle, rad)\n', Radian)

#Ibus
I = np.matmul(Y, V)

#Sbus
Sbus = np.matmul(np.diagflat(V), np.conjugate(I))
print('\nSbus :\n', Sbus)

#Sloss
Sloss = np.matmul(np.transpose(V), np.conjugate(I))
print('\nSloss :', Sloss)

#Ploss
Ploss = np.real(Sloss)
print('\nPloss :', Ploss)

#number 2
#create matrix Zbus
Z = np.linalg.inv(Y)
print('\nMatrix Zbus :', Z)
Igen = I[:3]
Iload = I[3:]
ID = sum(Iload)
d = np.divide(Iload, ID)

#create A1 and A2 matrix from Zbus matrix
matrixA1 = Z[3][0:4]
print('\nMatrix A1 =', matrixA1)
matrixA2 = Z[3][3:7]
print('\nMatrix A2 =', matrixA2)

#create t
tranA1 = matrixA1.reshape(4,1)
t1 = np.divide(1, np.matmul(matrixA2, d))
t = t1 * tranA1
print('\nt =', t)

# create matrix A3
# transpose matrix t
trant = t.reshape(1,4)
A3 = -d * trant
print('\nA3 =', A3)

# create trasformation matrix C
# create identity matrix C 
Ci = np.identity(4)
# delete last row matrix C
C = np.delete(Ci, 3, 0)
# append matrix A3 to matix C
C = np.append(C, A3, axis = 0)
print('\nC =', C)

# create matrix T1
# transpose C
ctran = np.transpose(C)
# Rbus
Rbus = np.real(Z)
# C conjugate
Ccon = np.conjugate(C)
# T1
T1 = np.matmul(np.matmul(ctran, Rbus), Ccon)
print('\nT1 =', T1)

# create diagonal matrix Ta that have element aii
Ta = np.zeros((4,4), dtype=complex)
for i in range(0,3):
    Ta[i][i] = I[i] / np.real(Sbus[i])
In0 = -(V[3] / Z[3][3])
Ta[3][3] = In0
print('\nTa =', Ta)

# create matrix T2
# conjugate matrix Ta
Taconj = np.conjugate(Ta)
T2 = np.matmul(np.matmul(Ta, T1), Taconj)
print('\nT2 =', T2)

# matrix B
T2real = np.real(T2)
B = T2real[:3,:3]
print('\nB =', B)

# matrix Bo
Boi = T2real[3,:3] * 2
Bo = Boi.reshape(3,1)
print('\nBo =', Bo)

# matrix Boo
Boo = T2real[3,3]
print('\nBoo =', Boo)

# calculate transmision losses
Pg = np.real(Sbus[:3])
Pl = (np.matmul(np.matmul(np.transpose(Pg), B), Pg)) + (np.matmul(np.transpose(Pg), Bo)) + Boo
print('\nPl =', Pl)
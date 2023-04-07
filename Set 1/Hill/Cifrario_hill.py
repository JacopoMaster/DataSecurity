import numpy as np
import math
from sympy import Matrix


#trasforma il testo in numeri mod 26 per il calcolo della matrice
def convert_to_numbers(stringa):
    nums = []
    for i in range(0, len(stringa)):
        nums.append((ord(stringa[i])-19) %26)
    return nums

#funzione per cifrare il testo
def encryption(plaintext, chiave, m):
    plaintext = convert_to_numbers(plaintext)
    lettere = []
    for i in range(0, len(plaintext), m):
        blocco = plaintext[i:i+m]
        num = (np.dot(chiave, blocco)%26)
        for i in range(0, len(num)):
            lettere.append(chr(num[i]+97))
        
    return ''.join(lettere)    

# controlla se la matrice passata è invertibile mod 26 e nel caso restituisce l'inversa mod26
def get_inverse(matrix):
    if math.gcd(int(round(np.linalg.det(matrix))), 26) == 1:
        matrix = Matrix(matrix)
        return matrix.inv_mod(26)
    else:
        return None
    

#funzione per decifrare il testo
def decryption(cypehrtext, chiave, m):
    cypehrtext = convert_to_numbers(cypehrtext)
    lettere = []
    for i in range(0, len(cypehrtext), m):
        blocco = cypehrtext[i:i+m]
        inv=get_inverse(chiave)
        num = (np.dot(inv, blocco)%26)
        for i in range(0, len(num)):
           lettere.append(chr(num[i]+97))
    
    return ''.join(lettere)




#prende l'array di numeri ottenuti dalla parola e crea la matrice corrispondente (m x len(arr)/m)
def group_array(arr, m):
    a = [arr[i:i+m] for i in range(0, len(arr), m)]
    matrix =  np.array(a)
    return matrix.transpose()

def calculate_key(matrix_cp, inv_matrix_pt):
    key = (np.dot(matrix_cp, inv_matrix_pt)% 26)
    return key



def attack_hill(ciphertext, plaintext, m):
    ct = group_array(convert_to_numbers(ciphertext), m)
    pt = group_array(convert_to_numbers(plaintext), m)
    matrices_pt = extract_square_matrices(pt, m)
    matrices_ct = extract_square_matrices(ct, m)

    for i in range (0, len(matrices_pt)):
        matrix = matrices_pt[i]
        if math.gcd(int(round(np.linalg.det(matrix))), 26) == 1:
                 pt = Matrix(matrix)
                 pt = pt.inv_mod(26)
                 ct = matrices_ct[i]
                 
                 return calculate_key(ct, pt)
     
    return print("No invertible matrices found in plaintext, attack failed ")   




def extract_square_matrices(matrix, m):
    square_matrices = []
    rows, cols = matrix.shape
    
    for i in range(rows-m+1):
        for j in range(cols-m+1):
            square_matrices.append(matrix[i:i+m, j:j+m])
    
    return square_matrices

            











print("-----esempio wikipedia-----")
#esempio wikipedia cifrario di hill (tuo->cny cny->tuo)

p="tuo" 

#la matrice fornita come chiave deve essere invertibile mod 26
k=np.array([[24,24,15],[17,25,22],[8,25,9]])

c=encryption(p,k,3)
print(c)
print(decryption(c,k,3))

print("-----esempio libro (2x2)-----")
#esempio libro
pt = "friday"
ct = "pqcfku"

print(group_array(convert_to_numbers(pt),2))
print(group_array(convert_to_numbers(ct),2))

print("La chiave è:")
print(attack_hill(ct,pt,2))







print("-----attacco known plaintext (3x3)-----")
#esempio attacco known plaintext

pt="quandomisentodebolequandolamiadeterminazionesiinfiacchiscerivedoconlamentelespalledisimonintentoascavaresenzasostaemidicoiononrideromaiallespallediunapersonacosiascoltamisimonnondimenticarlomaidevicredereintestessoenonperlafiduciacheioripongointenetantomenoperquellachetureponiinmedevifidartidellaparteditechecredeinsestessa"
k=np.array([[24,24,15],[17,25,22],[8,25,9]])
ct=encryption(pt,k,3)

print("Plantext= ")
print(pt)
print("")

print("Cyphertext= ")
print(ct)
print("")

print("chiave ottenuta dall'attacco= ")
print(attack_hill(ct,pt,3)) 






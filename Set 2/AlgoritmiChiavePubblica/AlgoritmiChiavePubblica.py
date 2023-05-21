import random
import math
import timeit


def algoritmo_euclide_esteso(a, b):
    
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        # Calcola il quoziente (q) e il resto (b) della divisione tra a e b
        q = a // b
        a, b = b, a % b
        # Aggiorna i coefficienti di Bézout
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0



# codice come negli appunti
# def esponenziazione_modulare_veloce(base, exp, mod):
#     if mod == 1:
#         return 0

#     # Convertiamo l'esponente in binario e rimuoviamo i primi due caratteri ('0b').
#     exp = bin(exp)[2:]

#     bexp = []
#     for i in str(exp):
#         bexp.append(int(i))

#     # Inizializziamo il risultato (d) e un contatore (c) a 0.
#     d = 1
#     c = 0

#     # Iteriamo su ogni cifra binaria nell'array bexp.
#     for i in bexp:
#         # Raddoppiamo il contatore c equivale a shiftare a sinistra e aggiungere uno 0.
#         c = 2 * c
#         d = (d * d) % mod
#         if i == 1:
#             c = c + 1
#             d = (d * base) % mod
#     return d


def esponenziazione_modulare_veloce(base, exp, mod):
    if mod == 1:
        return 0

    d = 1
    base = base % mod

    while exp > 0:
        # Se l'ultimo bit di exp è 1, moltiplichiamo il risultato per base modulo mod.
        if exp % 2 == 1:
            d = (d * base) % mod

        # Shiftiamo exp di un bit a destra (dividiamo exp per 2).
        exp = exp >> 1

        # Calcoliamo il quadrato di base modulo mod.
        base = (base * base) % mod

    return d



def miller_rabin(n, k):
    if n <= 1 or n % 2 == 0:
        return False

    # Scriviamo n - 1 come 2^r * m.
    r, m = 0, n - 1
    while m % 2 == 0:
        r += 1
        m //= 2

    # Eseguiamo il test k volte.
    for _ in range(k):
        # Scegliamo un numero casuale a tra 2 e n - 2.
        a = random.randint(1, n - 1)

        # Calcoliamo a^d % n.
        x = esponenziazione_modulare_veloce(a, m, n)

        # Se x è uguale a 1 o n - 1, passiamo al prossimo test.
        if x == 1 or x == n - 1:
            continue

        # Controlliamo se uno degli elementi nella sequenza x, x^2, x^4, ..., x^(2^(r-1)) è uguale a n - 1.
        for _ in range(r - 1):
            x = esponenziazione_modulare_veloce(x, 2, n)

            if x == n - 1:
                break
        else:
            # Se non abbiamo trovato nessun elemento nella sequenza uguale a n - 1, concludiamo che n è composto.
            return False

    # Se tutti i test hanno avuto successo, assumiamo che n sia probabilmente primo.
    return True



def genera_primo(k):
    if k < 2:
        raise ValueError("k deve essere maggiore o uguale a 2")
    
    candidato = 1 + 2 ** (k - 1)  # Creo numero con bit più e meno significativo a 1 e gli altri a 0

    while True:

        for i in range(1, k - 1): # Modifico in maniera casuale i valori intermedi
            bit_casuale = random.choice([0, 1])
            candidato += bit_casuale * (2 ** i)


        if miller_rabin(candidato, 10):
            return candidato
    

#RSA

def rsa_keygen(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Trova un e coprimo con phi_n
    for e in range(2, phi_n-1):
        if math.gcd(e, phi_n) == 1:
            break
    
    # Calcola d
    _, _, d = algoritmo_euclide_esteso(e, phi_n)
    d = d % phi_n

    return (e, n), (d, n)


def rsa_encrypt(plain_text, public_key):
    e, n = public_key
    cipher_text = esponenziazione_modulare_veloce(plain_text, e, n)
    return cipher_text


def rsa_decrypt(cipher_text, private_key):
    d, n = private_key
    plain_text = esponenziazione_modulare_veloce(cipher_text, d, n)
    return plain_text





#versione con ottimizzazione CRT

def rsa_keygen_crt(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Trova un e coprimo con phi_n
    for e in range(2, phi_n-1):
        if math.gcd(e, phi_n) == 1:
            break

    # Calcola d
    _, _, d = algoritmo_euclide_esteso(e, phi_n)
    d = d % phi_n

    # Calcola d_p, d_q, q_inv
    d_p = d % (p - 1)
    d_q = d % (q - 1)
    _, q_inv, _ = algoritmo_euclide_esteso(q, p)

    return (e, n), (d_p, d_q, p, q, q_inv)


def rsa_encrypt_crt(plain_text, public_key):
    e, n = public_key
    cipher_text = esponenziazione_modulare_veloce(plain_text, e, n)
    return cipher_text


def rsa_decrypt_crt(cipher_text, private_key):
    d_p, d_q, p, q, q_inv = private_key

    # Decripta il messaggio usando CRT
    m1 = esponenziazione_modulare_veloce(cipher_text, d_p, p)
    m2 = esponenziazione_modulare_veloce(cipher_text, d_q, q)
    h = (q_inv * (m1 - m2)) % p
    plain_text = m2 + h * q

    return plain_text





# Esempio d'uso

print("""Digita il numero corrispondente all'algoritmo da utilizzare:
1. Algoritmo di Euclide esteso.
2. Algoritmo di esponenziazione modulare veloce.
3. Test di Miller-Rabin.
4. Algoritmo per la generazione di numeri primi.
5. Schema RSA, senza ottimizzazione CRT
6. Schema RSA, con ottimizzazione CRT
7. Test RSA, CRT vs NoCRT, su 100 cyphertext""")

scelta = int(input())

if scelta == 1:
    print("Algoritmo di Euclide esteso")
    print("Inserisci il primo numero: ")
    a = int(input())
    print("Inserisci il secondo numero: ")
    b = int(input())

    mcd, x, y = algoritmo_euclide_esteso(a, b)

    print("MCD({}, {}) = {}".format(a, b, mcd))
    print("Coefficienti di Bézout: x = {}, y = {}".format(x, y))
    print("Verifica: {} * {} + {} * {} = {}".format(a, x, b, y, a * x + b * y))

elif scelta == 2:
    print("Algoritmo di esponenziazione modulare veloce")
    print("Inserisci la base: ")
    base = int(input())
    print("Inserisci l'esponente: ")
    exp = int(input())
    print("Inserisci il modulo: ")
    mod = int(input())
    print("Risultato: {}".format(esponenziazione_modulare_veloce(base, exp, mod)))

elif scelta == 3:
    print("Test di Miller-Rabin")    
    print("Inserisci il numero da testare: ")
    n = int(input())
    print("Inserisci il numero di test da eseguire: (solitamente un numero tra 5-10 è sufficiente) ")
    k = int(input())
    print("Il numero {} è {}.".format(n, "probabilmente primo" if miller_rabin(n, k) else "composto"))

elif scelta == 4:
    print("Algoritmo per la generazione di numeri primi")
    print("Inserisci l'ordine di grandezza del numero primo da generare: ")
    k = int(input())
    print("Il numero primo generato compreso tra 2**{} e (2**{})-1 è: {}".format(k-1, k, genera_primo(k)))
    x = math.ceil(math.log(2**k)/2)
    print("Per individuare un numero primo di queste dimensioni sono necessarie in media {} iterazioni".format(x))

elif scelta == 5:
    print("Schema RSA, senza ottimizzazione CRT")
    print("Inserisci l'ordine di grandezza del primo numero primo da generare: ")
    p = genera_primo(int(input()))
    print("Inserisci l'ordine di grandezza del secondo numero primo da generare: ")
    q = genera_primo(int(input()))
    public , private = rsa_keygen(p,q)
    print("Chiavi generate, pubblica: {} privata: {}".format(public , private))

    print("Inserisci il messaggio da criptare: ")
    m = int(input())
    c= rsa_encrypt(m,public)
    print("Messaggio cifrato: {}".format(c))
    print("Messaggio decifrato: {}".format(rsa_decrypt(c,private)))

elif scelta == 6:
    print("Schema RSA, con ottimizzazione CRT")
    print("Inserisci l'ordine di grandezza del primo numero primo da generare: ")
    p = genera_primo(int(input()))
    print("Inserisci l'ordine di grandezza del secondo numero primo da generare: ")
    q = genera_primo(int(input()))
    public , private = rsa_keygen_crt(p,q)
    print("Chiavi generate, pubblica: {} privata: {}".format(public , private))

    print("Inserisci il messaggio da criptare: ")
    m = int(input())
    c= rsa_encrypt_crt(m,public)
    print("Messaggio cifrato: {}".format(c))
    print("Messaggio decifrato: {}".format(rsa_decrypt_crt(c,private)))    
      
elif scelta == 7:
    # Genera chiavi RSA
    p = genera_primo(512)
    q = genera_primo(512)
    public_key, private_key = rsa_keygen(p, q)
    public_key_crt, private_key_crt = rsa_keygen_crt(p, q)

    # Genera 100 ciphertext casuali
    ciphertexts = [rsa_encrypt(random.randint(2, p * q - 1), public_key) for _ in range(100)]

    # Precomputa i valori m1 e m2 per la versione CRT
    precomputed_crt_values = [(esponenziazione_modulare_veloce(ct, private_key_crt[0], private_key_crt[2]),
                               esponenziazione_modulare_veloce(ct, private_key_crt[1], private_key_crt[3]))
                               for ct in ciphertexts]

    # Misura il tempo di esecuzione della versione senza CRT
    def decrypt_no_crt():
        for ct in ciphertexts:
           rsa_decrypt(ct, private_key)

    time_no_crt = timeit.timeit(decrypt_no_crt, number=1)

    # Misura il tempo di esecuzione della versione con CRT
    def decrypt_crt():
        for i, ct in enumerate(ciphertexts):
           m1, m2 = precomputed_crt_values[i]
           h = (private_key_crt[4] * (m1 - m2)) % private_key_crt[2]
           plain_text = m2 + h * private_key_crt[3]

    time_crt = timeit.timeit(decrypt_crt, number=1)

    print(f"Tempo di esecuzione senza CRT: {time_no_crt:.6f} secondi")
    print(f"Tempo di esecuzione con CRT: {time_crt:.6f} secondi")





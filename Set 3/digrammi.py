import numpy as np
from Huffman import huffman_coding

# Distribuzione dei digrammi presa da Wikipedia
digrams = {
    'th': 3.56, 'of': 1.17, 'io': 0.83,
    'he': 3.07, 'ed': 1.17, 'le': 0.83,
    'in': 2.43, 'is': 1.13, 've': 0.83,
    'er': 2.05, 'it': 1.12, 'co': 0.79,
    'an': 1.99, 'al': 1.09, 'me': 0.79,
    're': 1.85, 'ar': 1.07, 'de': 0.76,
    'on': 1.76, 'st': 1.05, 'hi': 0.76,
    'at': 1.49, 'to': 1.05, 'ri': 0.73,
    'en': 1.45, 'nt': 1.04, 'ro': 0.73,
    'nd': 1.35, 'ng': 0.95, 'ic': 0.70,
    'ti': 1.34, 'se': 0.93, 'ne': 0.69,
    'es': 1.34, 'ha': 0.93, 'ea': 0.69,
    'or': 1.28, 'as': 0.87, 'ra': 0.69,
    'te': 1.20, 'ou': 0.87, 'ce': 0.65,
}

# Calcolo la distribuzione di probabilità dei digrammi
total = sum(digrams.values())
prob_digrams = {k: v / total for k, v in digrams.items()}

# Calcolo le distribuzioni di probabilità p_X1 e p_X2
p_X1 = {k[0]: 0 for k in digrams.keys()}
p_X2 = {k[1]: 0 for k in digrams.keys()}

for k, v in prob_digrams.items():
    p_X1[k[0]] += v
    p_X2[k[1]] += v

# Calcolo la distribuzione prodotto p_X1 * p_X2
prod_prob_digrams = {k: p_X1[k[0]] * p_X2[k[1]] for k in digrams.keys()}


# Costruisco i codici Huffman per la vera distribuzione e la distribuzione prodotto
huffman_c1 = huffman_coding(list(prob_digrams.keys()), list(prob_digrams.values()))
huffman_c2 = huffman_coding(list(prod_prob_digrams.keys()), list(prod_prob_digrams.values()))

# Calcola la lunghezza media dei codici
Lp_C1 = sum(prob_digrams[k] * len(huffman_c1[k]) for k in digrams.keys())
Lp_C2 = sum(prob_digrams[k] * len(huffman_c2[k]) for k in digrams.keys())

# Calcola la differenza tra le lunghezze medie
Delta = Lp_C2 - Lp_C1

# Calcola la divergenza Kullback-Leibler e l'informazione mutua
KL_divergence = sum(prob_digrams[k] * np.log(prob_digrams[k] / prod_prob_digrams[k]) for k in digrams.keys())
mutual_information = sum(prob_digrams[k] * np.log(prob_digrams[k] / (p_X1[k[0]] * p_X2[k[1]])) for k in digrams.keys())

print(f'Delta: {Delta}')
print(f'Divergenza di Kullback-Leibler: {KL_divergence}')
print(f'Informazione mutua: {mutual_information}')


# Funzione per convertire un testo in digrammi
def text_to_digrams(text):
    return [text[i:i+2] for i in range(0, len(text) - 1)]

# Apri il file di testo e leggi il contenuto
with open('Akira.txt', 'r') as file:
    text = file.read()

# Converti il testo in digrammi
text_digrams = text_to_digrams(text)

# Comprimi il testo usando i codici Huffman
compressed_text_c1 = ''.join(huffman_c1[d] for d in text_digrams if d in huffman_c1)
compressed_text_c2 = ''.join(huffman_c2[d] for d in text_digrams if d in huffman_c2)

# Calcola la lunghezza del testo compresso
length_c1 = len(compressed_text_c1)
length_c2 = len(compressed_text_c2)

print(f'Lunghezza del testo compresso con C1: {length_c1}')
print(f'Lunghezza del testo compresso con C2: {length_c2}')


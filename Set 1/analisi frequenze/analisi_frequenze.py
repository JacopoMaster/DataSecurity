import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#metodo che conta le occorrenze del testo passato e ne stampa l'istogramma
def count_letter(text):
    #prepara il testo
    text = set_text(text)
    #conta le occorrenze
    occurency = pd.Series(list(text)).value_counts()
    occurency = occurency.sort_index() #opzionale, istogramma in ordine alfabetico
    #stampa l'istogramma
    occurency.plot.bar()
    plt.xticks(rotation=0)
    print(occurency)
    plt.show()

#metodo che prepara il testo per il calcolo
def set_text(text):
    text = text.lower()
    text = text.replace(" ", "")
    text = text.replace(",", "")
    text = text.replace(".", "")
    text = text.replace("\n", "")
    text = text.replace("—", "")
    text = text.replace(";", "")
    text = text.replace("-", "")
    text = text.replace("?", "")
    text = text.replace("’", "")
    text = text.replace("!", "")
    text = text.replace("“", "")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace(":", "")
    text = text.replace("”", "")

    return text


def count_mgrams(text, m):
    # Prepara il testo
    text = set_text(text)
    # Calcola gli m-grammi e conta le occorrenze
    mgrams = {}
    for i in range(len(text)-m+1):
        mgram = text[i:i+m]
        if mgram in mgrams:
            mgrams[mgram] += 1
        else:
            mgrams[mgram] = 1
    # Normalizza le frequenze
    total = sum(mgrams.values())
    freqs = {mgram: count/total for mgram, count in mgrams.items()}
    # Stampa il risultato
    print("Empirical distribution of {}-grams:".format(m))
    for mgram in sorted(freqs):
        print("{}: {:.4f}".format(mgram, freqs[mgram]))


def calc_ic_entropy(text, m):
    # Prepara il testo
    text = set_text(text)
    # Calcola gli m-grammi e conta le occorrenze
    mgrams = {}
    for i in range(len(text)-m+1):
        mgram = text[i:i+m]
        if mgram in mgrams:
            mgrams[mgram] += 1
        else:
            mgrams[mgram] = 1
    # Calcola l'indice di coincidenza
    total = sum(mgrams.values())
    ic = 0
    for count in mgrams.values():
        ic += count*(count-1)
    ic /= total*(total-1)
    # Calcola l'entropia
    freqs = [count/total for count in mgrams.values()]
    entropy = sum([-p*np.log2(p) for p in freqs])
    # Stampa il risultato
    print("Index of coincidence: {:.4f}".format(ic))
    print("Entropy: {:.4f}".format(entropy))















#apro file da testare
file = open("Moby Dick first chapter.txt", encoding='utf-8')
text = file.read()
#es 1
print(count_letter(text))

#es 2
#print(count_mgrams(text, 1))   
print(count_mgrams(text, 2))
#print(count_mgrams(text, 3))
#print(count_mgrams(text, 4))


#es 3
#print(calc_ic_entropy(text, 1))
print(calc_ic_entropy(text, 2))
#print(calc_ic_entropy(text, 3))
#print(calc_ic_entropy(text, 4))

file.close() 








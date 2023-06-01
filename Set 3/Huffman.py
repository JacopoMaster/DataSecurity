class Node:

    def __init__(self, frequency, symbol, left=None, right=None):
        self.frequency = frequency  
        self.symbol = symbol  
        self.left = left  
        self.right = right  
        self.huff = ''  # codice binario Huffman assegnato al nodo

       

# Ottengo dizionario lettera-frequenza
def calc_freq(letters, prob):
    freq = {}
    for l, p in zip(letters, prob):
        freq[l] = p      
    return freq

# Assegno un codice Huffman a ogni nodo
def huffman_code_node(node, val=''):
    newVal = val + str(node.huff)
    if(node.left):
        huffman_code_node(node.left, newVal)
    if(node.right):
        huffman_code_node(node.right, newVal)
    if(not node.left and not node.right):  # Se il nodo è una foglia
        huffman_code[node.symbol]=newVal

# Algoritmo di Huffman per codificare le lettere
def huffman_coding(letters, prob):
    freq = calc_freq(letters, prob)
    nodes = []
    for key in freq:  # Creo nodi per ogni lettera
        nodes.append(Node(freq[key], key))
    
    # Creo l'albero di Huffman
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.frequency)  # Ordina i nodi in base alla frequenza
        left = nodes[0]
        right = nodes[1]
        left.huff = 0  # Assegna 0 al nodo a sinistra
        right.huff = 1  # Assegna 1 al nodo a destra
        # Crea un nuovo nodo che ha come figli i due nodi con le minori frequenze
        newNode = Node(left.frequency+right.frequency, left.symbol+right.symbol, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    global huffman_code #per esercizio sui digrammi
    huffman_code = {}
    huffman_code_node(nodes[0])  # Assegna il codice Huffman a ogni nodo
    return huffman_code

# Decodifica una stringa binaria usando un dato codice prefix free
def decode(codex, binary_string):
    decoded_text = ""
    current_code = ""
    for bit in binary_string:  # Scansiona la stringa binaria bit per bit
        current_code += bit
        for symbol in codex:  # Scansiona il codice prefix free
            if codex[symbol] == current_code:  # Se il codice corrente corrisponde a un simbolo
                decoded_text += symbol  # Aggiunge il simbolo al testo decodificato
                current_code = ""  # Resetta il codice corrente
                break
    return decoded_text





# Esempio d'uso

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
prob = [0.4, 0.25, 0.125, 0.0625, 0.03125, 0.03125, 0.1]
huffman_code = {}

huffman_coding(letters, prob)

print("Codice Huffman per ogni lettera:")
print(huffman_code)


binary_string = '10110100100101111011110'
decoded_text = decode(huffman_code, binary_string)

print("Testo decodificato:")
print(decoded_text)

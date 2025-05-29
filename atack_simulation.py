import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, data, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.data = data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Node:
    def __init__(self, node_id):
        self.blockchain = []
        self.node_id = node_id

    def add_block(self, data):
        last_block = self.blockchain[-1] if self.blockchain else None
        index = len(self.blockchain)
        previous_hash = last_block.hash if last_block else "0"
        block = Block(index, previous_hash, data)
        self.blockchain.append(block)

# Creamos varios nodos
nodes = [Node(i) for i in range(5)]

# Nodo atacante controla 3 de 5 nodos
attacker_nodes = nodes[:3]
honest_nodes = nodes[3:]

##########################################
# La Cadena mas larga será la que persista
##########################################

# Los honestos minan bloques normalmente
for node in honest_nodes:
    for i in range(6):
        node.add_block(f"Tx H{i}")

# Los atacantes crean una cadena más larga (simulan PoW)
for node in attacker_nodes:
    for i in range(3):
        node.add_block(f"Tx A{i}")

# Ahora se propaga la cadena atacante como la "válida"
# (asumimos regla de cadena más larga)
longest_chain = max(nodes, key=lambda n: len(n.blockchain)).blockchain

# Todos los nodos aceptan la cadena más larga
for node in nodes:
    node.blockchain = longest_chain

print(f"Cadena final (longitud {len(nodes[0].blockchain)}):")
for block in nodes[0].blockchain:
    print(f"Block {block.index}: {block.data}")


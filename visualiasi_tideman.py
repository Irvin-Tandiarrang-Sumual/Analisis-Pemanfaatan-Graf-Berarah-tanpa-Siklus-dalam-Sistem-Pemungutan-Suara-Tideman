import json
import networkx as nx
import matplotlib.pyplot as plt

# Load hasil dari file JSON
with open("hasil_tideman.json", "r") as f:
    data = json.load(f)

candidates = data["candidates"]
locked = data["locked"]

# Buat graf
G = nx.DiGraph()
G.add_nodes_from(candidates)

for i in range(len(candidates)):
    for j in range(len(candidates)):
        if locked[i][j]:
            G.add_edge(candidates[i], candidates[j])

# Gambar graf
plt.figure(figsize=(6, 3))  # Ukuran gambar lebih kecil dan proporsional
pos = nx.spring_layout(G, k=10)  # Bikin node lebih dekat dan panah lebih pendek
nx.draw(
    G, pos,
    with_labels=True,
    node_color='lightblue',
    node_size=1200,       # Ukuran node sedang
    font_size=7,         # Ukuran font label
    arrows=True,
    arrowsize=5          # Ukuran panah
)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels={(u, v): "wins" for u, v in G.edges()},
    font_size=7
)
plt.title("Graf Hasil Locking Pairs (Metode Tideman)", fontsize=12)
plt.tight_layout()
plt.show()
from PIL import Image
import networkx as nx
from collections import deque

def process_image(file_path):
    try:
        img = Image.open(file_path)
        
        print("Image size: ", img.size)
        print("Image format: ", img.format)
        print("Image mode: ", img.mode)


    except FileNotFoundError:
        print("File not found")

caminho_imagem = 'c:/Users/Samuell/Desktop/AEDS III/Trabalho/src/toy.bmp'
process_image(caminho_imagem)
print(" ")

def criar_grafo(imagem):

    img = Image.open(imagem).convert('1')

    grafo = nx.Graph()

    largura, altura = img.size

    for x in range(largura):
        for y in range(altura):
            pixel = img.getpixel((x, y))

            if pixel != 0:
                grafo.add_node((x, y))

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue

                    nx_val = x + dx
                    ny_val = y + dy

                    if 0 <= nx_val < largura and 0 <= ny_val < altura:
                        neighbor_pixel = img.getpixel((nx_val, ny_val))

                        if neighbor_pixel != 0:
                            grafo.add_edge((x, y), (nx_val, ny_val))
    return grafo

caminho_imagem = 'c:/Users/Samuell/Desktop/AEDS III/Trabalho/src/toy.bmp'

grafo = criar_grafo(caminho_imagem)

num_nos = grafo.number_of_nodes()
num_arestas = grafo.number_of_edges()

print("Número de nós: ", num_nos)
print("Número de arestas: ", num_arestas)
print(" ")

def encontrar_caminho(grafo, inicio, fim):
    fila = deque([(inicio, [inicio])])
    visitados = set()

    while fila:
        atual, caminho = fila.popleft()

        if atual == fim:
            return caminho
        
        visitados.add(atual)
        vizinhos = list(grafo.neighbors(atual))
        for vizinho in vizinhos:
            if vizinho not in visitados:
                novo_caminho = caminho + [vizinho]
                fila.append((vizinho, novo_caminho))
    
    return None


caminho_imagem = 'c:/Users/Samuell/Desktop/AEDS III/Trabalho/src/toy.bmp'
img = Image.open(caminho_imagem)

equipamento = None
area_manuntecao = None
for node in grafo.nodes():
    pixel = img.getpixel(node)
    if pixel == (255, 0, 0):
        equipamento = node
    if pixel == (0, 255, 0):
        area_manuntecao = node

if equipamento and area_manuntecao:
    try:
        sequencia_passos = nx.shortest_path(grafo, equipamento, area_manuntecao)
        print("Sequência de passos: ")
        for passo in sequencia_passos:
            print(passo)
    except nx.NetworkXNoPath:
        print("Não foi possível encontrar um caminho")
else:
    print("Não foi possível encontrar um caminho")

    
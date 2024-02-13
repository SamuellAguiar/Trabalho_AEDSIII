#   Grupo:
# Samuell Carlos de Oliveira Aguiar - 21.2.8025
# Gustavo Gomes Rolim - 21.2.8031

from collections import deque
import heapq
from tkinter import filedialog
from PIL import Image
from matplotlib import pyplot as plt

class GrafoImagem:

    def __init__(self, caminho_imagems):

        # Abre as imagens e obtém a largura e altura
        self.imagens = [Image.open(caminho_imagem)
                        for caminho_imagem in caminho_imagems]
        self.largura, self.altura = self.imagens[0].size

        # Inicializa listas para armazenar pixels verdes e vermelhos
        self.pixels_verdes = self.obter_pixels_por_cor((0, 255, 0))
        
        self.pixels_vermelhos = self.obter_pixels_por_cor((255, 0, 0))
        
        self.pixels_vermelho = self.pixels_vermelhos[0]

        # Inicializa o dicionário do grafo e o conjunto de visitados
        self.grafo = {}
        self.visitado = set()

    def visualizar_grafo(self, caminho=None, index=0):

        # Verifica se o índice fornecido está dentro dos limites das imagens
        if index < len(self.imagens):
        
            # Cria um gráfico para exibir a imagem
            plt.figure(figsize=(8, 8))
            plt.imshow(self.imagens[index])
            plt.axis('off')

            # Se um caminho foi encontrado, marca os nós do caminho no gráfico com quadrados azuis
            if caminho:

                for no in caminho:
                    x, y, z = no
                    if z == index:
                        plt.scatter(x, y, s=150, c='blue', marker='s')
            
            plt.show()

        else:

            print(f"Índice de imagem inválido: {index}")

    def obter_pixels_por_cor(self, cor):

        # Percorre todos os pixels da imagem para econtrar os pixels com a cor especificada
        pixels = []

        for z, image in enumerate(self.imagens):
            for x in range(self.largura):
                for y in range(self.altura):
                    if image.getpixel((x, y)) == cor:
                        pixels.append((x, y))
        
        return pixels

    def construir_grafo(self):

        # Precorre todos os pixels para construir o grafo, considerando vizinhança de 4 vizinhos
        for z, image in enumerate(self.imagens):
            for x in range(self.largura):
                for y in range(self.altura):
                    cor = image.getpixel((x, y))

                     # Verifica se o pixel é verde ou vermelho e os armazena nas listas apropriadas
                    if cor == (0, 255, 0):
                        self.pixels_verdes.append((x, y, z))
                    elif cor == (255, 0, 0):
                        self.pixel_vermelho = (x, y, z)
                        self.pixels_vermelhos.append((x, y, z))

                    # Se o pixel não for preto, adiciona-o ao grafo
                    if cor != (0, 0, 0):
                        self.grafo[(x, y, z)] = {}

         # Percorre novamente para adicionar as arestas entre os pixels
        for z, image in enumerate(self.imagens):
            for x in range(self.largura):
                for y in range(self.altura):
                    cor = image.getpixel((x, y))

                    # Se o pixel não for preto, cria as arestas com seus vizinhos
                    if cor != (0, 0, 0):
                        vizinhos = [(x-1, y, z), (x+1, y, z), (x, y-1, z),
                                    (x, y+1, z), (x, y, z-1), (x, y, z+1)]
                        
                        for vizinho in vizinhos:
                            if vizinho in self.grafo and image.getpixel((vizinho[0], vizinho[1])) != (0, 0, 0):
                                peso = self.define_pesos(cor, image.getpixel(
                                    (vizinho[0], vizinho[1])), z != vizinho[2])
                                self.grafo[(x, y, z)][vizinho] = peso

    def define_pesos(self, cor1, cor2, andar_diferente):

        # Define os pesos das arestas com base nas cores dos pixels
        if andar_diferente:
            return 5

        if cor2 == (128, 128, 128):
            return 4

        if cor2 == (196, 196, 196):
            return 2

        else:
            return 1

    def busca(self, inicio, fim):

        # Algoritmo de Busca em Largura (BFS) para encontrar um caminho entre dois pontos
        fila = deque([[inicio]])
        
        while fila:
            caminho = fila.popleft()
            no = caminho[-1]

            # Marca um nó como visitado
            if no not in self.visitado:
                self.visitado.add(no)

                # Retorna o caminho se o nó de destino for alcançado
                if no == fim:
                    return caminho

                # Adiciona os nós adjacentes à fila
                for adjacente in self.grafo.get(no, []):
                    novo_caminho = list(caminho)
                    novo_caminho.append(adjacente)
                    fila.append(novo_caminho)

        # Imprime uma mensagem se não houver caminho entre os nós de origem e destino
        return print("Não há caminho entre os nós de origem e destino")

    def encontrar_caminho(self):

        # Encontre o caminho usando o dijkstra
        dist, pred, primeiro_verde = self.dijkstra(self.pixel_vermelho)
        caminho = []

        # reconstrói o caminho
        atual = primeiro_verde
        while atual is not None:
            caminho.append(atual)
            atual = pred[atual]

        caminho.reverse()

        return caminho

    def dijkstra(self, s):

        dist = {node: float("inf") for node in self.grafo}
        pred = {node: None for node in self.grafo}
        
        dist[s] = 0
        Q = [(dist[s], s)]
        u = None
        
        while Q:
            dist_u, u = heapq.heappop(Q)

            if u in self.pixels_verdes:
                return dist, pred, u
            
            for v in self.grafo[u]:
                if dist[v] > dist[u] + self.grafo[u][v]:
                    dist[v] = dist[u] + self.grafo[u][v]
                    heapq.heappush(Q, (dist[v], v))
                    pred[v] = u
        
        return dist, pred, None


# Cria uma instância da classe GrafoImagem e encontra o caminho da imagem 'toy.bmp'
files = filedialog.askopenfilenames(filetypes=[("Bitmap files", "*.bmp")])
file = list(files)
grafo_imagem = GrafoImagem(file)

# Constrói o grafo baseado na imagem fornecida
grafo_imagem.construir_grafo()

# Encontra o caminho entre os pixels vermelho e verde na imagem
caminho_encontrado = grafo_imagem.encontrar_caminho()

# Imprime o caminho encontrado e visualiza o grafo representando o caminho na imagem
print(caminho_encontrado)
for i in range(len(grafo_imagem.imagens)):
    grafo_imagem.visualizar_grafo(caminho_encontrado, index=i)

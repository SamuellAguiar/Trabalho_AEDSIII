#   Grupo:
# Samuell Carlos de Oliveira Aguiar - 21.2.8025
# Gustavo Gomes Rolim - 21.2.8031

from collections import deque
from PIL import Image
from matplotlib import pyplot as plt


class GrafoImagem:

    def __init__(self, caminho_imagem):

        # Abre a imagem e obtem a largura e altura
        self.imagem = Image.open(caminho_imagem)
        self.largura, self.altura = self.imagem.size

        # Inicializa o dicionário do grafo e o conjunto de visitados
        self.grafo = {}
        self.visitado = set()

    def visualizar_grafo(self, caminho=None):

        # Cria um gráfico para exibir a imagem
        plt.figure(figsize=(8, 8))
        plt.imshow(self.imagem)
        plt.axis('off')

        # Se um caminho foi encontrado, marca os nós do caminho no gráfico com quadrados azuis
        if caminho:
            for no in caminho:
                x, y = no
                plt.scatter(x, y, s=750, c='blue', marker='s')
        plt.show()

    def obter_pixels_por_cor(self, cor):

        # Percorre todos os pixels da imagem para econtrar os pixels com a cor especificada
        pixels = []
        for x in range(self.largura):
            for y in range(self.altura):
                if self.imagem.getpixel((x, y)) == cor:
                    pixels.append((x, y))
        return pixels

    def construir_grafo(self):

        # Precorre todos os pixels para construir o grafo, considerando vizinhança de 4 vizinhos
        for x in range(self.largura):
            for y in range(self.altura):
                cor = self.imagem.getpixel((x, y))

                # Adiciona os pixels não pretos ao grafo com seus vizinhos não pretos
                if cor != (0, 0, 0):
                    self.grafo[(x, y)] = [(nx, ny) for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                                          if 0 <= nx < self.largura and 0 <= ny < self.altura and self.imagem.getpixel((nx, ny)) != (0, 0, 0)]

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

        # Encontra os pixels vermelhos e verdes na imgem
        pixels_vermelhos = self.obter_pixels_por_cor((255, 0, 0))
        pixels_verdes = self.obter_pixels_por_cor((0, 255, 0))

        # Tenta encontrar um caminho entre pixels vermelhos e verdes
        for pixel_vermelho in pixels_vermelhos:
            for pixel_verde in pixels_verdes:
                caminho = self.busca(pixel_vermelho, pixel_verde)
                if caminho:
                    return caminho
        return None


# Cria uma instância da classe GrafoImagem e encontra o caminho da imagem 'toy.bmp'
grafo_imagem = GrafoImagem('toy.bmp')

# Constrói o grafo baseado na imagem fornecida
grafo_imagem.construir_grafo()

# Encontra o caminho entre os pixels vermelho e verde na imagem
caminho_encontrado = grafo_imagem.encontrar_caminho()

# Imprime o caminho encontrado e visualiza o grafo representando o caminho na imagem
print(caminho_encontrado)
grafo_imagem.visualizar_grafo(caminho_encontrado)

from PIL import Image
import networkx as nx
from collections import deque

class ImageGraph:
    def __init__(self):
        self.image = None
        self.width = 0
        self.height = 0
        self.graph = nx.Graph()
        self.equipment = None
        self.maintenance_area = None

    def process_image(self, file_path):
        try:
            self.image = Image.open(file_path).convert('RGB')
            self.width, self.height = self.image.size
        except FileNotFoundError:
            print("File not found")

    def build_graph(self):
        if self.image is not None:
            for x in range(self.width):
                for y in range(self.height):
                    pixel = self.image.getpixel((x, y))

                    if pixel == (255, 0, 0):  # Pixel vermelho (equipamento)
                        self.equipment = (x, y)
                    elif pixel == (0, 255, 0):  # Pixel verde (área de manutenção)
                        self.maintenance_area = (x, y)

                    if pixel != (0, 0, 0):  # Ignorar pixels pretos
                        self.graph.add_node((x, y))

                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                nx_val = x + dx
                                ny_val = y + dy

                                if 0 <= nx_val < self.width and 0 <= ny_val < self.height:
                                    neighbor_pixel = self.image.getpixel((nx_val, ny_val))

                                    if neighbor_pixel != (0, 0, 0):
                                        self.graph.add_edge((x, y), (nx_val, ny_val))

    def find_path(self):
        queue = deque([(self.equipment, [])])  # Inicializa fila com tupla contendo ponto atual e caminho percorrido
        visited = set()
        directions = {
            (-1, 0): '↑', (1, 0): '↓', (0, -1): '←', (0, 1): '→'
        }

        while queue:
            (current_point, path) = queue.popleft()
            if current_point == self.maintenance_area:
                return ' '.join(path)  # Retorna o caminho encontrado

            if current_point not in visited:
                visited.add(current_point)

                for dx, dy in directions:
                    nx_val = current_point[0] + dx
                    ny_val = current_point[1] + dy

                    if (nx_val, ny_val) in self.graph[current_point]:
                        new_point = (nx_val, ny_val)
                        new_path = path + [directions[(dx, dy)]]
                        queue.append((new_point, new_path))

        return None

def main():
    caminho_imagem = 'toy.bmp'

    image_graph = ImageGraph()
    image_graph.process_image(caminho_imagem)
    image_graph.build_graph()

    path = image_graph.find_path()
    if path:
        print("Caminho encontrado:", path)
    else:
        print("Não foi possível encontrar um caminho")

if __name__ == "__main__":
    main()

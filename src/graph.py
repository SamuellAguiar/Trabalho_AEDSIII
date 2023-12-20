from collections import deque
from PIL import Image
from matplotlib import pyplot as plt
import networkx as nx

class ImageGraph:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.graph = {}
        self.visited = {}
        

    def visualize_graph(self):
        G = nx.Graph()
        for node, edges in self.graph.items():
            for edge in edges:
                G.add_edge(node, edge)

        pos = {node: (node[0], -node[1]) for node in G.nodes()}  # Flip the y-axis to match image coordinates
        nx.draw(G, pos, with_labels=False, node_size=10)
        plt.show()
    

    def get_red_pixels(self):
        red_pixels = []
        for x in range(self.width):
            for y in range(self.height):
                color = self.image.getpixel((x, y))
                if color == (255, 0, 0):
                    red_pixels.append((x, y))
        return red_pixels

    def get_green_pixels(self):
        green_pixels = []
        for x in range(self.width):
            for y in range(self.height):
                color = self.image.getpixel((x, y))
                if color == (0, 255, 0):
                    green_pixels.append((x, y))
        return green_pixels
    
    def build_graph(self):
        for x in range(self.width):
            for y in range(self.height):
                color = self.image.getpixel((x, y))
                if color != (0, 0, 0):
                    self.graph[(x, y)] = [(nx, ny) for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] 
                                          if 0 <= nx < self.width and 0 <= ny < self.height and self.image.getpixel((nx, ny)) != (0, 0, 0)]


    def bfs(self, start, end):
        queue = deque([[start]])
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node not in self.visited:
                self.visited[node] = True
                if node == end:
                    return path
                for adjacent in self.graph.get(node, []):
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)
        return None
    
    
    def find_path(self):
        red_pixels = self.get_red_pixels()
        green_pixels = self.get_green_pixels()
        for red_pixel in red_pixels:
            for green_pixel in green_pixels:
                path = self.bfs(red_pixel, green_pixel)
                if path:
                    return path
        return None
    
image_graph = ImageGraph('toy.bmp')
red_pixels = image_graph.get_red_pixels()
green_pixels = image_graph.get_green_pixels()
image_graph.build_graph()
path = image_graph.find_path()
print(path)
image_graph.visualize_graph()
import heapq

from typing import Any, List, Tuple
from PIL import Image
from load_image import load_image
from colors import Color
import os

class Graph:
  def __init__(self):
    self.num_nodes = 0
    self.num_edges = 0
    self.adj = {}
    self.map_z_to_dungeon_image = {}

  def add_node(self, node: Any) -> None:
    """
    Adds a node to the graph.

    Parameters:
        node (Any): The node to be added (as a key to a dict)
    """
    try: 
      if self.adj[node] != {}:
        return
    except KeyError:
      self.adj[node] = {}
      self.num_nodes += 1

  def add_nodes(self, nodes: List[Any]) -> None:
    """
    Adds a list of nodes to the graph

    Parameters:
    - nodes (List[Any]): The list of nodes to be added (as keys to a dict)
    """
    for node in nodes:
      self.add_node(node)
      
  def add_directed_edge(self, u, v, weight):
    """
    Add a directed edge from node 'u' to node 'v' with the specified weight.

    Parameters:
    - u: The source node.
    - v: The target node.
    - weight: The weight of the directed edge.

    If the nodes 'u' and 'v' do not exist in the graph, they are added using the 'add_node' function.
    """
    self.add_node(u)
    self.add_node(v)
    self.adj[u][v] = weight
    self.num_edges += 1

  def add_undirected_edge(self, u, v, weight):
    """
    Add a two-way (undirected) edge between nodes 'u' and 'v' with the specified weight.

    Parameters:
    - u: One of the nodes.
    - v: The other node.
    - weight: The weight of the undirected edge.

    This function calls the 'add_edge' function for both (u, v) and (v, u) to represent the undirected edge.
    """
    self.add_directed_edge(u, v, weight)
    self.add_directed_edge(v, u, weight)
    
  def get_file_paths(self,folder:str) -> List[str]:
      return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".bmp")]

  def __repr__(self) -> str:
    str = ""
    for u in self.adj:
      str += f"{u} -> {self.adj[u]}\n"
    return str
  
  def build_graph(self, image_paths: List[str], max_floors: int) -> Tuple[Tuple[int, int, int], List[Tuple[int, int, int]]]:
    """
    Build a graph from bitmap images.

    Parameters:
    - image_paths (List[str]): The list of file paths of the bitmap images.
    - max_floors (int): The maximum number of floors in the building.

    Returns:
    - A tuple containing the source pixel and destination pixels representing the edges of the graph.
    """
    # Load the images using the load_image function.
    images = [load_image(image_path) for image_path in image_paths]

    source_pixel = None
    destination_pixels = []
    
    for z in range(max_floors):
      width, height = images[z].size

 
      for x in range(width):
        for y in range(height):
          current_pixel = (x, y, z)
          pixel_color = images[z].getpixel((x, y))


          if pixel_color != Color.BLACK:
            if pixel_color == Color.RED:
              source_pixel = current_pixel
      
            if pixel_color == Color.GREEN:
              destination_pixels.append(current_pixel)

            self.add_edges_for_pixel(current_pixel, width, height, max_floors, images)
    return (source_pixel, destination_pixels)
    
  def build_graph2(self, image_path) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
      """
      Build a graph from a single bitmap image (mapa principal).

      Parameters:
      - image_path (str): File path of the bitmap image.

      Returns:
      - A tuple containing:
        - source_pixel: starting point (Link)
        - destination_pixels: list of target points (entradas das dungeons e Master Sword)
      """
      image = load_image(image_path)

      source_pixel = None
      destination_pixels = []

      width, height = image.size

      for x in range(width):
          for y in range(height):
              current_pixel = (x, y)
              pixel_color = image.getpixel((x, y))
              if pixel_color != Color.DUNGEON_WALL:
                if pixel_color == Color.LINK or pixel_color == Color.DUNGEON_ENTRANCE:
                    source_pixel = current_pixel

                if pixel_color in [Color.MASTER_SWORD, Color.DUNGEON1, Color.DUNGEON2, Color.DUNGEON3, Color.PENDANT]:
                    destination_pixels.append(current_pixel)
              if pixel_color != Color.DUNGEON_WALL:
                self.add_edges_for_pixel(current_pixel, width, height, image)

      return source_pixel, destination_pixels

  
  def add_edges_for_pixel(
      self, 
      coordinates: Tuple[int, int], 
      width: int, 
      height: int, 
      image: Image.Image
  ) -> None:

      neighbor_coordinates_list = self.get_neighbors(coordinates, width, height, image)

      color_weights = {
          Color.GRASS: 10,
          Color.SAND: 20,
          Color.FOREST: 100,
          Color.MOUNTAIN: 150,
          Color.WATER: 180,
          Color.DUNGEON_PATH: 10,
          Color.LINK: 0,
          Color.MASTER_SWORD: 0,
          Color.DUNGEON1: 0,
          Color.DUNGEON2: 0,
          Color.DUNGEON3: 0,
          Color.PENDANT: 0,
          Color.DUNGEON_ENTRANCE: 0
      }

      for neighbor_x, neighbor_y in neighbor_coordinates_list:
          pixel_color = image.getpixel((neighbor_x, neighbor_y))
          weight = color_weights.get(pixel_color)
          if weight is None:
              raise ValueError(f"Unknown color found: {pixel_color}")

          self.add_undirected_edge(coordinates, (neighbor_x, neighbor_y), weight)



  def get_neighbors(self, coordinates, width, height, image):
      neighbors = []
      x, y = coordinates
      directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

      for nx, ny in directions:
          if 0 <= nx < width and 0 <= ny < height:
              # usar a imagem correta para o plano atual
              img = image
              if img.getpixel((nx, ny)) != Color.DUNGEON_WALL:
                  neighbors.append((nx, ny))
      return neighbors

  
  def path_bfs(self, source_pixel: Tuple[int, int, int], destination_pixels: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Perform Breadth-First Search (BFS) starting from the specified source node.

    Parameters:
    - source_pixel: The source pixel (origin) for the BFS traversal.
    - destination_pixels: The destination pixels to stop the BFS.

    This function explores the graph in breadth-first order
    starting from the given source node 'source_pixel' to the 'destination_pixel' and returns the path.
    """
    dist = {node: float("inf") for node in self.adj}
    pred = {node: None for node in self.adj}
    Q = [source_pixel]
    dist[source_pixel] = 0
    while Q:
      u = Q.pop(0)
      for v in self.adj[u]:
        if dist[v] == float("inf"):
          Q.append(v)
          dist[v] = dist[u] + 1
          pred[v] = u
          if v in destination_pixels:
            return self.reconstruct_path(source_pixel, v, pred)
    return []
  
  def reconstruct_path(self, source_pixel: Tuple[int, int, int], destination_pixel: Tuple[int, int, int], pred: dict) -> List[Any]:
    """
    Reconstruct the path from the source pixel to the destination pixel using the predecessor dictionary.

    Parameters:
    - source_pixel: The source pixel of the path.
    - destination_pixel: The destination pixel of the path.
    - pred: The predecessor dictionary obtained from the BFS traversal.

    Returns:
    - The reconstructed path from the source to the destination.
    """
    path = [destination_pixel]
    current_pixel = destination_pixel

    # Traverse the predecessor dictionary to reconstruct the path.
    while current_pixel != source_pixel:
      current_pixel = pred[current_pixel]
      path.insert(0, current_pixel)
    return path

  def dijkstra(self, source_pixel: Tuple[int, int, int], destination_pixels: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Apply Dijkstra's algorithm to find the shortest path from a source pixel to any of the destination pixels in the graph.

    Parameters:
    - source_pixel: The source pixel (origin) for the Dijkstra's algorithm.
    - destination_pixels: List of destination pixels to find the shortest path to.

    Returns:
    - List of coordinates representing the shortest path from the source pixel to any of the destination pixels.
    """
    dist = {node:float("inf") for node in self.adj}
    pred = {node:None for node in self.adj}
    dist[source_pixel] = 0
    Q = [(dist[source_pixel], source_pixel)]
    while Q:
      dist_u, u = heapq.heappop(Q)
      for v in self.adj[u]:
        if dist[v] > dist[u] + self.adj[u][v]:
          dist[v] = dist[u] + self.adj[u][v]
          heapq.heappush(Q, (dist[v], v))
          pred[v] = u
      if u in destination_pixels:
        return self.reconstruct_path(source_pixel, u, pred)
    return []


  def a_star(self, source_pixel: Tuple[int, int], destination_pixels: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
      """
      Apply A* algorithm to find the shortest path from a source pixel to any of the destination pixels in the graph.

      Parameters:
      - source_pixel: The source pixel (x, y) for the search.
      - destination_pixels: List of destination pixels (x, y) to find the shortest path to.

      Returns:
      - List of coordinates representing the shortest path from the source pixel to any of the destination pixels.
      """
      import heapq

      open_set = [(0, source_pixel)]  
      came_from = {source_pixel: None}
      g_score = {node: float('inf') for node in self.adj}
      g_score[source_pixel] = 0

      def heuristic(u):
          ux, uy = u
          return min(abs(ux - dx) + abs(uy - dy) for dx, dy in destination_pixels)

      while open_set:
          _, current = heapq.heappop(open_set)

          if current in destination_pixels:
              
              path = []
              while current:
                  path.append(current)
                  current = came_from[current]
              path.reverse()
              return path

          for neighbor in self.adj[current]:
              tentative_g_score = g_score[current] + self.adj[current][neighbor]
              if tentative_g_score < g_score[neighbor]:
                  g_score[neighbor] = tentative_g_score
                  priority = tentative_g_score + heuristic(neighbor)
                  heapq.heappush(open_set, (priority, neighbor))
                  came_from[neighbor] = current

      return []


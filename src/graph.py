import heapq

from typing import Any, List, Tuple
from PIL import Image
from load_image import load_image
from colors import Color

class Graph:
  def __init__(self):
    self.num_nodes = 0
    self.num_edges = 0
    self.adj = {}

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

      # Iterate over all pixels in the image.
      for x in range(width):
        for y in range(height):
          current_pixel = (x, y, z)
          pixel_color = images[z].getpixel((x, y))

          # Check if the pixel is not black.
          if pixel_color != Color.BLACK:
            if pixel_color == Color.RED:
              source_pixel = current_pixel
      
            if pixel_color == Color.GREEN:
              destination_pixels.append(current_pixel)
              
            # Add edges for the non-black pixel.
            self.add_edges_for_pixel(current_pixel, width, height, max_floors, images)
    return (source_pixel, destination_pixels)
  
  def add_edges_for_pixel(self, coordinates: Tuple[int, int, int], width: int, height: int, max_floors: int, images: List[Image.Image]) -> None:
    """
    Add edges for a non-black pixel in the graph.

    Parameters:
    - coordinates (tuple): The (x, y, z) coordinates of the current pixel.
    - width (int): The width of the image.
    - height (int): The height of the image.
    - max_floors (int): The maximum number of floors in the building.
    - images (List[Image.Image]): The list of images containing the floor plans.

    Returns:
    - None
    """
    # Get neighbors of the current pixel.
    neighbor_coordinates_list = self.get_neighbors(coordinates, width, height, max_floors, images)

    # Define weights for different colors.
    color_weights = {
      Color.WHITE: 1,
      Color.RED: 1,
      Color.GREEN: 1,
      Color.GRAY_LIGHT: 2,
      Color.GRAY_DARK: 4,
    }

    # Add edges between the current pixel and its neighbors.
    for neighbor_x, neighbor_y, neighbor_z in neighbor_coordinates_list:
        # Get the pixel color of the neighbor and calculate your weight.
        pixel_color = images[neighbor_z].getpixel((neighbor_x, neighbor_y))
        weight = color_weights.get(pixel_color, None)

        if weight is None:
          raise ValueError(f"Unknown color found: {pixel_color}")
        
        # Check if the neighbor is on the same floor.
        same_floor = (neighbor_z == coordinates[2])

        if not same_floor:
          weight = 5  # Higher cost for transitioning between floors.
        
        # Add an undirected edge between the current pixel and its neighbor with the calculated weight.
        self.add_undirected_edge(coordinates, (neighbor_x, neighbor_y, neighbor_z), weight)

  def get_neighbors(self, coordinates: Tuple[int, int, int], width: int, height: int, max_floors: int, images: List[Image.Image]) -> List[Tuple[int, int, int]]:
    """
    Get non-black neighbors of a pixel in a bitmap image.

    Parameters:
    - coordinates (tuple): (x, y, z) coordinates of the pixel.
    - width (int): Width of the image.
    - height (int): Height of the image.
    - max_floors (int): The maximum number of floors in the building.
    - images (List[Image.Image]): The list of bitmap images for each floor.

    Returns:
    - A list of coordinates representing non-black neighbors.
    """
    neighbors = []
    x, y, z = coordinates
    
    # Define directions to check for neighbors: left, right, up, down, front, back.
    directions = [(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z + 1), (x, y, z - 1)]

    # Iterate over each direction.
    for neighbor_x, neighbor_y, neighbor_z in directions:
       # Check if the neighbor is within the image boundaries.
      is_within_bounds = 0 <= neighbor_x < width and 0 <= neighbor_y < height and 0 <= neighbor_z < max_floors

      if is_within_bounds:
        # Get the pixel color of the corresponding floor.
        pixel_color = images[neighbor_z].getpixel((neighbor_x, neighbor_y))
        
        # Check if the pixel is not black.
        if pixel_color != Color.BLACK:
          neighbors.append((neighbor_x, neighbor_y, neighbor_z))
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

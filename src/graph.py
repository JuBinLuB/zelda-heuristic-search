from typing import Any, Dict, List, Optional, Tuple
import heapq
import os

from PIL import Image

from load_image import load_image
from colors import Colors


class Graph:

    def __init__(self) -> None:
        self.num_nodes = 0
        self.num_edges = 0
        self.adj = {}
        self.image = None

    def add_node(self, node: Any) -> None:
        """Adds a node to the graph.

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
        """Adds a list of nodes to the graph

        Parameters:
        - nodes (List[Any]): The list of nodes to be added (as keys to a dict)
        """
        for node in nodes:
            self.add_node(node)

    def add_directed_edge(self, u, v, weight):
        """Add a directed edge from node 'u' to node 'v' with the specified weight.

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
        """Add a two-way (undirected) edge between nodes 'u' and 'v' with the specified weight.

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

    def build_graph(self, image_path: str) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        """Build a graph from a single bitmap image (mapa principal).

        Parameters:
        - image_path (str): File path of the bitmap image.

        Returns:
        - A tuple containing:
        - source_pixel: starting point
        - destination_pixels: list of target points (dungeons and Master Sword)
        """
        self.image = load_image(image_path)

        source_pixel = None
        destination_pixels = []
        width, height = self.image.size

        for x in range(width):
            for y in range(height):
                current_pixel = (x, y)
                pixel_color = self.image.getpixel((x, y))
                if pixel_color != Colors.DUNGEON_WALL:
                    if pixel_color == Colors.LINK or pixel_color == Colors.DUNGEON_ENTRANCE:
                        source_pixel = current_pixel
                    if pixel_color in [
                        Colors.MASTER_SWORD,
                        Colors.DUNGEON1,
                        Colors.DUNGEON2,
                        Colors.DUNGEON3,
                        Colors.PENDANT
                    ]:
                        destination_pixels.append(current_pixel)
                if pixel_color != Colors.DUNGEON_WALL:
                    self.add_edges_for_pixel(current_pixel, width, height, self.image)
        if source_pixel is None:
            raise ValueError("No source pixel found in the image")
        return source_pixel, destination_pixels

    def add_edges_for_pixel(
        self,
        coordinates: Tuple[int, int],
        width: int,
        height: int,
        image: Image.Image
    ) -> None:
        """Adds edges for a pixel to all traversable neighboring pixels.

        Parameters:
            coordinates: (x,y) position of the current pixel
            width: Width of the image/map
            height: Height of the image/map
            image: PIL Image object representing the map

        Raises:
            ValueError: If encountering an undefined color in the image
        """
        neighbor_coordinates_list = self.get_neighbors(coordinates, width, height, image)

        color_weights = {
            # Terrain Colors.
            Colors.GRASS: 10,
            Colors.SAND: 20,
            Colors.FOREST: 100,
            Colors.MOUNTAIN: 150,
            Colors.WATER: 180,
            # Special Points.
            Colors.LINK: 10,
            Colors.MASTER_SWORD: 10,
            Colors.DUNGEON1: 20,
            Colors.DUNGEON2: 20,
            Colors.DUNGEON3: 20,
            # Dungeon Features.
            Colors.PENDANT: 10,
            Colors.DUNGEON_PATH: 10,
            Colors.DUNGEON_ENTRANCE: 10
        }

        for neighbor_x, neighbor_y in neighbor_coordinates_list:
            pixel_color = image.getpixel((neighbor_x, neighbor_y))
            weight = color_weights.get(pixel_color)
            if weight is None:
                raise ValueError(f"Unknown color found: {pixel_color}")
            self.add_undirected_edge(coordinates, (neighbor_x, neighbor_y), weight)

    def get_neighbors(self,
        coordinates: Tuple[int, int],
        width: int,
        height: int,
        image: Image.Image
    ) -> List[Tuple[int, int]]:
        """Finds all traversable neighboring pixels of a given coordinate.

        Parameters:
            coordinates: (x,y) position to check neighbors for
            width: Map width boundary
            height: Map height boundary
            image: PIL Image object for color checking

        Returns:
            List of valid (x,y) neighbor coordinates
        """
        x, y = coordinates
        directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        neighbors = []

        for nx, ny in directions:
            if 0 <= nx < width and 0 <= ny < height:
                img = image
                if img.getpixel((nx, ny)) != Colors.DUNGEON_WALL:
                    neighbors.append((nx, ny))
        return neighbors

    def a_star(self,
        source_pixel: Tuple[int, int],
        destination_pixels: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Apply A* algorithm to find the shortest path from a source pixel to any of the destination pixels in the graph.

        Parameters:
        - source_pixel: The source pixel (x, y) for the search.
        - destination_pixels: List of destination pixels (x, y) to find the shortest path to.

        Returns:
        - List of coordinates representing the shortest path from the source pixel to any of the destination pixels.
        """
        open_set = [(0, source_pixel)]
        came_from = {}
        g_score = {node: float('inf') for node in self.adj}
        g_score[source_pixel] = 0

        def heuristic(u):
            ux, uy = u
            return min(abs(ux - dx) + abs(uy - dy) for dx, dy in destination_pixels)

        while open_set:
            _, current = heapq.heappop(open_set)
            if current in destination_pixels:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
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

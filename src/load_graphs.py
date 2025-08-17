from typing import Dict
from graph import Graph


def load_all_graphs(map_files: Dict[str, str]) -> Dict[str, Dict]:
    """Builds all graph structures from map files and stores their metadata.

    Processes each map file to create a graph representation of the game world,
    identifying key locations (source and destinations) for pathfinding purposes.

    Parameters:
        map_files: Dictionary mapping graph names to their corresponding file paths.
            Example: {"main": "overworld.bmp", "dungeon1": "dungeon1.bmp"}

    Returns:
        A dictionary where each key is a graph name and each value contains:
            - "graph": Graph object representing the map
            - "source": Starting pixel coordinates (Link's position or dungeon entrance)
            - "destinations": List of target pixels (dungeon entrances, pendants, Master Sword)
    """
    graphs_info = {}
    for name, path in map_files.items():
        g = Graph()
        source, destinations = g.build_graph(path)
        graphs_info[name] = {
            "graph": g,
            "source": source,
            "destinations": destinations
        }
    return graphs_info

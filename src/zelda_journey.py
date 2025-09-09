from typing import Dict, Tuple, List

from colors import Colors
from graph import Graph


class ZeldaJourney:

    def __init__(self, graphs_info: Dict[str, Dict], dungeons: Dict[Tuple, str]):
        self.graphs_info = graphs_info
        self.dungeons = dungeons
        self.total_cost = 0
        self.full_path = []
        self.steps = []

    def run(self) -> List[Tuple[int, int]]:
        """Execute the complete journey: collect all pendants across the dungeons
        and finally reach the Master Sword.

        The journey proceeds in the following order:
            1. From Link's starting position on the overworld, travel to the
               nearest dungeon entrance.
            2. Inside the dungeon, travel from entrance to the pendant.
            3. Travel back from the pendant to the entrance (to exit the dungeon).
            4. Repeat until all dungeons are completed.
            5. Finally, from the last dungeon exit, travel to the Master Sword.

        The nearest dungeon at each step is chosen dynamically based on the
        A* pathfinding cost from the current position.

        Returns:
            List[Tuple[int, int]]: The complete path (sequence of pixel coordinates)
            that Link follows during the entire journey.
        """
        # Initialize from main map data.
        main_info = self.graphs_info["main"]
        main_graph = main_info["graph"]
        current_pixel = main_info["source"]

        # Filter which pixels on the main map are dungeon entrances.
        remaining_dungeons = {
            dest: self.dungeons[main_graph.image.getpixel(dest)]
            for dest in self.graphs_info["main"]["destinations"]
            if main_graph.image.getpixel(dest) in self.dungeons
        }

        # While there are still dungeons to visit.
        while remaining_dungeons:
            best_entry = None
            best_path = None
            best_cost = float("inf")

            # Find nearest reachable dungeon.
            for entry_pixel, dungeon_name in remaining_dungeons.items():
                path = main_graph.a_star(current_pixel, [entry_pixel])
                if path:
                    cost = self._path_cost(main_graph, path)
                    if cost < best_cost:
                        best_cost = cost
                        best_entry = entry_pixel
                        best_path = path

            if best_entry is None or best_path is None:
                raise ValueError("Nenhuma dungeon alcançável encontrada.")

            # 1. Overworld: Current position → dungeon entrance.
            self._add_path_and_cost(
                main_graph, best_path, action=f"Overworld → {remaining_dungeons[best_entry]}")

            # 2. Dungeon: entrance → pendant.
            dungeon_info = self.graphs_info[remaining_dungeons[best_entry]]
            dungeon_graph = dungeon_info["graph"]
            pendant_pixel = dungeon_info["destinations"][0]
            path_to_pendant = dungeon_graph.a_star(
                dungeon_info["source"], [pendant_pixel])
            self._add_path_and_cost(
                dungeon_graph, path_to_pendant, action=f"{remaining_dungeons[best_entry]} → Pendant")

            # 3. Dungeon: pendant → entrance.
            path_back = dungeon_graph.a_star(
                pendant_pixel, [dungeon_info["source"]])
            self._add_path_and_cost(
                dungeon_graph, path_back, action=f"Pendant → Exit {remaining_dungeons[best_entry]}")

            current_pixel = best_entry
            del remaining_dungeons[best_entry]

        # 4. Overworld: dungeon exit/entrance → Master Sword.
        master_sword_pixel = [
            dest for dest in main_info["destinations"]
            if main_info["graph"].image.getpixel(dest) == Colors.MASTER_SWORD
        ][0]

        path_to_master_sword = main_graph.a_star(
            current_pixel, [master_sword_pixel])
        self._add_path_and_cost(
            main_graph, path_to_master_sword, action="Exit Dungeons → Master Sword")

        return self.full_path

    def _add_path_and_cost(self, graph: Graph, path: List[Tuple[int, int]], action: str) -> None:
        """Add a path segment to the journey, update total cost, and record the step."""
        if not path:
            return
        incremental_cost = self._path_cost(graph, path)
        self.full_path.extend(path)
        self.total_cost += incremental_cost

        self.steps.append({
            "Action": action,
            "PathLength": len(path),
            "IncrementalCost": incremental_cost,
            "TotalCost": self.total_cost,
            "Path": path
        })

    def _path_cost(self, graph: Graph, path: List[Tuple[int, int]]) -> int:
        """Calculate cost of a path segment."""
        return sum(graph.adj[u][v] for u, v in zip(path[:-1], path[1:]))

    def get_report(self) -> None:
        """Print a human-readable journey report."""
        print("\n--- Journey Report ---")
        for step in self.steps:
            print(f"{step['Action']}:")
            print(f"   Segment length : {step['PathLength']} steps")
            print(f"   Incremental cost: {step['IncrementalCost']}")
            print(f"   Total cost so far: {step['TotalCost']}")
        print("----------------------")

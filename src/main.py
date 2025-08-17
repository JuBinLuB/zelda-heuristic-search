from build_map import build_map_from_txt
from colors import Colors
from draw_path import draw_path
from load_graphs import load_all_graphs
from zelda_journey import ZeldaJourney


def main():
    # 1. Build maps from TXT to BMP.
    print("Generating maps from TXT files...")
    build_map_from_txt("../Datasets/txt/main_map.txt", "../Datasets/bmp/main_map.bmp")

    for i in range(3):
        build_map_from_txt(
            f"../Datasets/txt/dungeon_{i}.txt",
            f"../Datasets/bmp/dungeon_{i}.bmp"
        )

    # 2. Define map files.
    map_files = {
        "main": "../Datasets/bmp/main_map.bmp",
        **{f"dungeon_{i}": f"../Datasets/bmp/dungeon_{i}.bmp" for i in range(3)}
    }

    # 3. Load graphs.
    print("\nLoading graphs...")
    graphs_info = load_all_graphs(map_files)

    # 4. Run the journey.
    print("Starting Zelda's journey...")
    journey = ZeldaJourney(graphs_info, {
        Colors.DUNGEON1: "dungeon_0",
        Colors.DUNGEON2: "dungeon_1",
        Colors.DUNGEON3: "dungeon_2",
    })
    final_path = journey.run()

    # 5. Show results.
    print("\n--- Journey Finished ---")
    print(f"Total Path Length: {len(final_path)} steps")
    print(f"Total Cost: {journey.total_cost}")
    print("------------------------")
    
    # Detailed report.
    journey.get_report()

    # Save and draw the path on the main map and the dungeons.
    print("\nDrawing the path...")
    draw_path(journey.steps, output_folder="../Images/")


if __name__ == "__main__":
    main()

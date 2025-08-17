import os
from typing import Dict, List

from PIL import Image, ImageDraw

from colors import Colors


def draw_path(journey_steps: List[Dict], output_folder: str) -> None:
    # Create output directory if it doesn't exist.
    os.makedirs(output_folder, exist_ok=True)

    # Define map paths.
    map_paths = {
        "main": "../Datasets/bmp/main_map.bmp",
        "dungeon_0": "../Datasets/bmp/dungeon_0.bmp",
        "dungeon_1": "../Datasets/bmp/dungeon_1.bmp",
        "dungeon_2": "../Datasets/bmp/dungeon_2.bmp"
    }

    # Carregar imagens.
    images = {
        name: Image.open(path).convert("RGB")
        for name, path in map_paths.items()
    }

    # Create drawing objects for each image.
    draws = {
        name: ImageDraw.Draw(img)
        for name, img in images.items()
    }

    # Draw each path segment on the appropriate map.
    for step in journey_steps:
        path = step["Path"]
        action = step["Action"]

        # Determine which map to draw on based on the action description.
        if "Overworld" in action or "Master Sword" in action:
            map_key = "main"
        elif "dungeon_0" in action.lower():
            map_key = "dungeon_0"
        elif "dungeon_1" in action.lower():
            map_key = "dungeon_1"
        elif "dungeon_2" in action.lower():
            map_key = "dungeon_2"
        else:
            continue

        # Draw each point in the path.
        for x, y in path:
            try:
                if images[map_key].getpixel((x ,y)) not in [
                    Colors.LINK, 
                    Colors.DUNGEON1, 
                    Colors.DUNGEON2, 
                    Colors.DUNGEON3, 
                    Colors.MASTER_SWORD, 
                    Colors.PENDANT
                ]:
                    # Draw the path point only if it's not already a special color.
                    draws[map_key].point((x, y), fill=Colors.PATH)
            except ValueError as e:
                print(f"Warning: Invalid coordinates ({x}, {y}) in {action}: {e}")

    # Save all modified images.
    for name, img in images.items():
        output_path = os.path.join(output_folder, f"{name}_path.bmp")
        img.save(output_path)
        print(f"Saved path visualization: {output_path}")

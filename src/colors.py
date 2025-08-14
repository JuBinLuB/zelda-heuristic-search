class Colors:
    # Mapping of terrain characters to their RGB color values
    char_to_color = {
        # Terrain Types
        'F': (0, 100, 0),     # Forest (Dark Green)
        'G': (144, 238, 144), # Grass (Light Green)
        'M': (139, 69, 19),   # Mountain (Brown)
        'A': (238, 214, 175), # Sand (Light Beige)
        'W': (0, 191, 255),   # Water (Blue)

        # Special Points
        'L': (255, 215, 0),   # Link - Start Point (Gold)
        'S': (255, 0, 255),   # Master Sword - Lost Woods (Bright Magenta)
        '1': (255, 69, 0),    # Dungeon Entrance 1 (Red Orange)
        '2': (255, 140, 0),   # Dungeon Entrance 2 (Dark Orange)
        '3': (255, 20, 147),  # Dungeon Entrance 3 (Pink)

        # Dungeon Features
        'X': (64, 64, 64),    # Dungeon Wall (Dark Gray)
        'C': (192, 192, 192), # Dungeon Path (Light Gray)
        'E': (255, 69, 0),    # Dungeon Entrance/Exit (Orange)
        'P': (255, 215, 0),   # Pendant (Bright Gold)
    }

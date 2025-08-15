class Color:
    # Terrain Colors
    FOREST = (0, 100, 0)             # F
    GRASS = (144, 238, 144)          # G
    MOUNTAIN = (139, 69, 19)         # M
    SAND = (238, 214, 175)           # A
    WATER = (0, 191, 255)            # W

    # Special Points
    LINK = (255, 215, 0)             # L
    MASTER_SWORD = (255, 0, 255)     # S
    DUNGEON1 = (255, 69, 0)          # 1
    DUNGEON2 = (255, 140, 0)         # 2
    DUNGEON3 = (255, 20, 147)        # 3

    # Dungeon Features
    DUNGEON_WALL = (64, 64, 64)      # X
    DUNGEON_PATH = (192, 192, 192)   # C
    DUNGEON_ENTRANCE = (255, 69, 0)  # E
    PENDANT = (255, 215, 0)          # P

    # Path Color
    PATH = (255, 0, 0)

    # Mapping from chars to colors
    char_to_color = {
        'F': FOREST,
        'G': GRASS,
        'M': MOUNTAIN,
        'A': SAND,
        'W': WATER,
        'L': LINK,
        'S': MASTER_SWORD,
        '1': DUNGEON1,
        '2': DUNGEON2,
        '3': DUNGEON3,
        'X': DUNGEON_WALL,
        'C': DUNGEON_PATH,
        'E': DUNGEON_ENTRANCE,
        'P': PENDANT
    }

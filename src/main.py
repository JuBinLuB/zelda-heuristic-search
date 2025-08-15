from build_map import build_map_from_txt
from graph import Graph
from colors import Color
from load_image import load_image

def main():
    build_map_from_txt(f"../Datasets/txt/dungeon_0.txt", f"../Datasets/bmp/dungeon_0.bmp")
    build_map_from_txt(f"../Datasets/txt/dungeon_1.txt", f"../Datasets/bmp/dungeon_1.bmp")
    build_map_from_txt(f"../Datasets/txt/dungeon_2.txt", f"../Datasets/bmp/dungeon_2.bmp")
    build_map_from_txt(f"../Datasets/txt/main_map.txt", f"../Datasets/bmp/main_map.bmp")
    
    main_map_path = "../Datasets/bmp/main_map.bmp"
    dungeon_paths = [
        "../Datasets/bmp/dungeon_0.bmp",
        "../Datasets/bmp/dungeon_1.bmp",
        "../Datasets/bmp/dungeon_2.bmp"
    ]

  
    graph = Graph()
    start_pixel, _ = graph.build_graph2(main_map_path)

    main_image = load_image(main_map_path)
    graph.map_to_dungeon_image = {}
    master_sword_pixel = None

    width, height = main_image.size
    for x in range(width):
        for y in range(height):
            pixel_color = main_image.getpixel((x, y))
            current_pixel = (x, y)

            if pixel_color == Color.MASTER_SWORD:
                master_sword_pixel = current_pixel
            elif pixel_color in (Color.DUNGEON1, Color.DUNGEON2, Color.DUNGEON3):
                dungeon_index = {Color.DUNGEON1:0, Color.DUNGEON2:1, Color.DUNGEON3:2}[pixel_color]
                graph.map_to_dungeon_image[current_pixel] = dungeon_paths[dungeon_index]

    current_pixel = start_pixel
    collected_dungeons = []

    etapas = []

    while len(collected_dungeons) < 3:
       
        best_entry = None
        best_path = None
        best_cost = float('inf')
        for entry in graph.map_to_dungeon_image:
            if entry in collected_dungeons:
                continue
            path = graph.a_star(current_pixel, [entry])
            cost = sum(graph.adj[path[i]][path[i+1]] for i in range(len(path)-1))
            if cost < best_cost:
                best_cost = cost
                best_entry = entry
                best_path = path

   
        etapas.append({
            "etapa": f"Indo para dungeon {len(collected_dungeons)+1}",
            "caminho": best_path[1:],
            "custo": best_cost
        })
        current_pixel = best_entry

  
        dungeon_img_path = graph.map_to_dungeon_image[best_entry]
        dungeon_graph = Graph()
        dungeon_source, dungeon_destination = dungeon_graph.build_graph2(dungeon_img_path)
        pendant_pixel = dungeon_destination[0]

       
        path_to_pendant = dungeon_graph.a_star(dungeon_source, [pendant_pixel])
        cost_to_pendant = sum(dungeon_graph.adj[path_to_pendant[i]][path_to_pendant[i+1]] for i in range(len(path_to_pendant)-1))
        etapas.append({
            "etapa": f"Dentro da dungeon {len(collected_dungeons)+1}",
            "caminho": path_to_pendant[1:],
            "custo": cost_to_pendant
        })
        current_pixel = pendant_pixel

    
        path_back = dungeon_graph.a_star(current_pixel, [dungeon_source])
        cost_back = sum(dungeon_graph.adj[path_back[i]][path_back[i+1]] for i in range(len(path_back)-1))
        etapas.append({
            "etapa": f"Voltando da dungeon {len(collected_dungeons)+1}",
            "caminho": path_back[1:],
            "custo": cost_back
        })
        current_pixel = best_entry
        collected_dungeons.append(best_entry)

   
    path_to_sword = graph.a_star(current_pixel, [master_sword_pixel])
    cost_to_sword = sum(graph.adj[path_to_sword[i]][path_to_sword[i+1]] for i in range(len(path_to_sword)-1))
    etapas.append({
        "etapa": "Indo para Master Sword",
        "caminho": path_to_sword[1:],
        "custo": cost_to_sword
    })

   
    total_cost = sum(etapa["custo"] for etapa in etapas)
    return etapas, total_cost

if __name__ == "__main__":
    etapas, total = main()
    print(f"Etapas:{etapas}")
    print(f"Custo total:{total}")
    graph = Graph()
    sp, dp = graph.build_graph2("../Datasets/bmp/dungeon_0.bmp")
    print(sp, dp)

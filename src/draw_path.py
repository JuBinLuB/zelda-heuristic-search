from PIL import Image, ImageDraw
import os

def draw_path(etapas, output_folder="caminho_final"):
    os.makedirs(output_folder, exist_ok=True)

    # Caminho para cada imagem
    main_map_path = "../Datasets/bmp/main_map.bmp"
    dungeon_paths = [
        "../Datasets/bmp/dungeon_0.bmp",
        "../Datasets/bmp/dungeon_1.bmp",
        "../Datasets/bmp/dungeon_2.bmp"
    ]

    # Carregar imagens
    images = {
        "main_map": Image.open(main_map_path).convert("RGB"),
        "dungeon_0": Image.open(dungeon_paths[0]).convert("RGB"),
        "dungeon_1": Image.open(dungeon_paths[1]).convert("RGB"),
        "dungeon_2": Image.open(dungeon_paths[2]).convert("RGB")
    }
    draws = {k: ImageDraw.Draw(v) for k, v in images.items()}

    path_color = (255, 0, 0)  # vermelho

    # Preencher caminhos
    for etapa in etapas:
        coords = etapa["caminho"]
        if "Indo para dungeon" in etapa["etapa"] or "Indo para Master Sword" in etapa["etapa"]:
            for x, y in coords:
                draws["main_map"].point((x, y), fill=path_color)
        elif "Dentro da dungeon" in etapa["etapa"] or "Voltando da dungeon" in etapa["etapa"]:
            dungeon_index = int(etapa["etapa"].split(" ")[-1]) - 1
            dungeon_key = f"dungeon_{dungeon_index}"
            for x, y in coords:
                draws[dungeon_key].point((x, y), fill=path_color)

    # Salvar imagens
    images["main_map"].save(os.path.join(output_folder, "main_map_path.bmp"))
    for i, dungeon_key in enumerate(["dungeon_0", "dungeon_1", "dungeon_2"]):
        images[dungeon_key].save(os.path.join(output_folder, f"{dungeon_key}_path.bmp"))

from colors import Colors
from PIL import Image


def build_map(file_path: str, output_path: str):
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        height, width = len(lines), len(lines[0])

        image = Image.new('RGB', (width, height))
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                image.putpixel((x, y), Colors.char_to_color.get(char, (0, 0, 0)))  # Black for unknown.

        image.save(output_path, 'BMP')
        print(f"Map created successfully: {output_path}")
        print(f"Dimensions: {width}x{height} pixels")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

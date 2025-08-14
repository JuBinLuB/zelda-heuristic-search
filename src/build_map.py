from colors import Colors
from PIL import Image


def build_map_from_txt(file_path: str, output_path: str) -> None:
    """
    Reads a text file representing a map and generates a BMP image based on defined colors.

    Parameters:
    - file_path: Path to the input text file containing the map characters.
    - output_path: Path to save the generated BMP image.

    Returns:
    - None
    """
    try:
        # Open the text file and read all lines, stripping whitespace.
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        # Determine the image dimensions based on the number of lines and line length.
        height, width = len(lines), len(lines[0])

        # Create a new RGB image with the calculated dimensions.
        image = Image.new('RGB', (width, height))

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                image.putpixel((x, y), Colors.char_to_color.get(char, (0, 0, 0)))

        # Save the generated image as BMP.
        image.save(output_path, 'BMP')

        print(f"Map created successfully: {output_path}")
        print(f"Dimensions: {width}x{height} pixels")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

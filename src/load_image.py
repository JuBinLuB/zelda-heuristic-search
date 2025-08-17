from PIL import Image


def load_image(file_path: str) -> Image.Image:
    """Load an image from a file.

    Parameters:
    - file (str): The image file path.

    Returns:
    - Image.image: An image object representing the loaded image.

    Raises:
    - Exception: If an error occurs when opening the image.
    """
    try:
        # Try to open the image using the Pillow library (PIL).
        image = Image.open(file_path)
        return image
    except Exception as e:
        raise ValueError(f"Error loading image from {file_path}: {str(e)}")

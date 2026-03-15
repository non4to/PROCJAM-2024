import numpy as np
from pathlib import Path
from PIL import Image


def load_image(file_path: Path, output_resolution: tuple[int, int] = (64, 64)) -> np.ndarray:
    with Image.open(file_path) as img:
        img = img.resize(output_resolution)
        img = img.convert("RGB")
        img_array = np.array(img)
        return img_array

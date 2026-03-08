from pathlib import Path

import numpy as np
from PIL import Image


def load_rgb_image(path):
    return np.array(Image.open(path).convert('RGB'), dtype=np.uint8)


def save_rgb_image(path, array):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array.astype(np.uint8), mode='RGB').save(path)


def save_gray_image(path, array):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(array.astype(np.uint8), mode='L').save(path)


def ensure_output_dir(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalize_input_path(text):
    text = text.strip()
    if len(text) >= 2 and ((text[0] == '"' and text[-1] == '"') or (text[0] == "'" and text[-1] == "'")):
        text = text[1:-1]
    return text

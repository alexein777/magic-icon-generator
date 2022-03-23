from mpl_toolkits.axes_grid1 import ImageGrid
from typing import Iterable, Union, Any
import datetime
import io
import logging
import matplotlib.pyplot as plt
import os
import re
import requests

from PIL import Image
import bs4
import numpy as np


IMG_EXTS = ['.png', '.jpg', '.tiff', '.bmp']


def get_img_name_from_url(url: str) -> str:
    """
    Gets image name from an url.

    Example:

    https://www.something.com/something1/something2/fire.png -> fire.png

    :param url: Image url.
    :return: Image name.
    """
    match = re.search(r'/([-_A-Za-z0-9]+[.](png|jpg|tiff|bmp))\??', url)
    return match.group(1) if match is not None else url[url.rfind('/') + 1:]


def save_image_from_url(url: str, dest: os.PathLike, overwrite=False):
    """
    Downloads an image from a given url and saves is to dest.
    :param url: Image url.
    :param dest: Destination where to store the image.
    :param overwrite: If image already exists at dest, overwrite it if True.
    :return: None
    """
    try:
        img = requests.get(url).content
    except:
        return

    img_name = get_img_name_from_url(url)
    if not overwrite and img_name in os.listdir(dest):
        return

    with open(os.path.join(dest, img_name), 'wb') as f:
        f.write(img)


def get_img_ext(src: str) -> Union[str, None]:
    """
    Extract image extension for a given image name or url. Returns None for invalid image extensions.

    :param src: Image name or url.
    :return: Image extension or None for invalid image extensions.
    """

    dot_idx = src.rfind('.')
    if dot_idx == -1:
        return None

    ext = src[dot_idx + 1:].lower()
    return ext if ext in IMG_EXTS else None


def trim_img_ext(fname: str) -> str:
    """
    Return file name without image extension, if any.

    :param fname: Filename
    :return: File name without extension.
    """
    dot_idx = fname.rfind('.')
    if dot_idx == -1:
        return fname

    return fname[:dot_idx] if fname[dot_idx + 1:] in IMG_EXTS else fname


def is_valid_img_ext(ext: str):
    """
    Checks if given extension is an image extension
    :param ext: File extension.
    :return: True if extension is in IMG_EXTS (see utils.image_process)
    """
    if ext is None:
        return False

    return ext.lower() in IMG_EXTS

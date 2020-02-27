import math

import numpy as np


def generate_patches(im: np.ndarray, *, patch_size: int = 8) -> np.ndarray:
    """
    Generates patches from a given image.

    Parameters
    ----------
    im : np.ndarray
        Image
    patch_size, optional (default : 8)
        Patch size.

    Returns
    -------
    np.ndarray : A patch.
    """
    if len(im.shape) != 2:
        raise ValueError(f'Expecting 2D image: {im.shape}')
    for y in range(0, im.shape[0], patch_size):
        for x in range(0, im.shape[1], patch_size):
            yield im[y: y + patch_size, x: x + patch_size]


def bits_to_int(bits: str) -> int:
    """
    Convert a bit string to an integer.

    Parameters
    ----------
    bits : str
        The bit string to be converted.

    Returns
    -------
    int : The final integer.
    """
    return sum([
        2 ** p if b == '1' else 0
        for p, b in enumerate(bits[::-1])
    ])


def int_to_bits(int_: int) -> str:
    """
    Convert a postive integer to a bit string.

    Parameters
    ----------
    int_ : int
        The integer to be converted.

    Returns
    -------
    str : The bit string represetnation of the integer.
    """
    if int_ < 0:
        raise ValueError(f'Integer should be positive: {int_}')
    if int_ == 0:
        return '0'
    bits = ''
    # The maximum power of two is needed to determine the number of bits
    # needed to represent the integer.
    for p in range(int(math.log(int_, 2)), -1, -1):
        to_subtract = 2 ** p
        bits += '1' if to_subtract <= int_ else '0'
        int_ = int_ % to_subtract
    return bits


def zigzag_patch(patch: np.ndarray) -> np.array:
    """
    Reorders the elements in a patch in a zigzag order.

    Parameters
    ----------
    patch : np.ndarray
        The patch.

    Returns
    -------
    np.array : The elements of the patch (in zigzag order).

    Source
    ------
    https://en.wikipedia.org/wiki/File:JPEG_ZigZag.svg
    """
    if not patch.shape == (8, 8):
        raise ValueError(f'Patch should have shape (8, 8): {patch.shape}')
    patch_90 = np.rot90(patch)
    return np.concatenate([
        # The direction of the diagonal is alternated for the zigzag order
        patch_90.diagonal(index)[::-1 if index % 2 else 1]
        for index in range(-7, 8)
    ])


def izigzag_patch(vector: np.array) -> np.ndarray:
    """
    Inverse of :func:zigzag_patch.

    Parameters
    ----------
    vector : np.array
        The vector to be converted in a 8 by 8 patch

    Returns
    -------
    np.ndarray : The 8 by 8 patch.
    """
    if not len(vector) == 64:
        raise ValueError('Only implemented for a vector of length 64')

    indices = [
        0, 1, 5, 6, 14, 15, 27, 28, 2, 4, 7, 13, 16, 26, 29, 42, 3, 8,
        12, 17, 25, 30, 41, 43, 9, 11, 18, 24, 31, 40, 44, 53, 10, 19, 23, 32,
        39, 45, 52, 54, 20, 22, 33, 38, 46, 51, 55, 60, 21, 34, 37, 47, 50, 56,
        59, 61, 35, 36, 48, 49, 57, 58, 62, 63
    ]
    return vector[indices].reshape(8, 8)

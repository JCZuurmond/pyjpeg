import math

import numpy as np


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
    Convert an integer to a bit string.

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

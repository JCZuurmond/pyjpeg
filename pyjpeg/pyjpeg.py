import math

import numpy as np


ONE_OVER_SQRT_TWO = 2 ** (-0.5)


def _dct_cos(pixel: int, spatial_frequency: int) -> float:
    """
    Get the cosine value used in the (inverse) DCT.

    Parameters
    ----------
    pixel : int
        Pixel location.
    spatial_frequency : int
        Spatial frequency.

    Returns
    -------
    float : The cosine value for the (inverse) DCT.
    """
    return np.cos(((2 * pixel + 1) * spatial_frequency * np.pi) / 16)


def _normalization_constant(value: int) -> float:
    """
    Normalization constant.

    Parameters
    ----------
    value : int
        Given the value get the normalization constant.

    Returns
    -------
    float : The normalization constant.
    """
    return ONE_OVER_SQRT_TWO if value == 0 else 1.


def _dct_spatial_frequency(
        patch: np.ndarray,
        v: int,
        u: int) -> float:
    """
    Get the DCT value for a certain spatial frequency.

    Parameters
    ----------
    patch : np.ndarray
        The 8 by 8 patch of which the discrete cosine transform is taken.
    v : int
        The vertical spatial frequency.
    u : int
        The horizontal spatial frequency.

    Returns
    -------
    float : The DCT value for a certain spatial frequency.
    """
    out = 0
    for y in range(8):
        for x in range(8):
            out += patch[y, x] * _dct_cos(y, v) * _dct_cos(x, u)
    return out * _normalization_constant(v) * _normalization_constant(u) * 0.25


def _idct_pixel(
        patch: np.ndarray,
        y: int,
        x: int) -> float:
    """
    Get the inverse DCT value for a certain pixel.

    Parameters
    ----------
    patch : np.ndarray
        The 8 by 8 patch spatial frequency patch.
    y : int
        The vertical pixel location.
    x : int
        The horizontal pixel location

    Returns
    -------
    float : The inverse DCT value for a certain pixel.
    """
    out = 0
    for v in range(8):
        for u in range(8):
            c = (
                _normalization_constant(v) * _normalization_constant(u)
            )
            out += c * patch[v, u] * _dct_cos(y, v) * _dct_cos(x, u)
    return out * 0.25


def dct(patch: np.ndarray) -> np.ndarray:
    """
    Get the discrete cosine transform of the patch.

    Parameters
    ----------
    patch : np.ndarray
        The 8 by 8 patch of which the discrete cosine transform is taken.

    Returns
    -------
    np.ndarray : The discrete cosine transform of the patch.

    Raises
    ------
    ValueError : If the patch is not 8 by 8
    """
    if not patch.shape == (8, 8):
        raise ValueError(f'Patch should have shape (8, 8): {patch.shape}')

    return (
        np.array([_dct_spatial_frequency(patch, v, u)
                  for v in range(8) for u in range(8)])
        .reshape(8, 8)
    )


def idct(patch: np.ndarray) -> np.ndarray:
    """
    Get the inverse discrete cosine transform of the patch.

    Parameters
    ----------
    patch : np.ndarray
        The patch of which the inverse discrete cosine transform is taken.

    Returns
    -------
    np.array : The inverse discrete cosine transform of the patch.

    Raises
    ------
    ValueError : If the patch is not 8 by 8
    """
    if not patch.shape == (8, 8):
        raise ValueError(f'Patch should have shape (8, 8): {patch.shape}')
    return (
        np.array([_idct_pixel(patch, y, x)
                  for y in range(8) for x in range(8)])
        .reshape(8, 8)
    )


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

from typing import Union

import numpy as np

from .huffman import (
    int_to_bits,
    ENCODER,
    zigzag_patch,
)


ONE_OVER_SQRT_TWO = 1 / np.sqrt(2)


def _norm_constant(freq: int) -> float:
    """
    Get the normalization constant belonging to a certain frequency.

    Parameters
    ----------
    freq : int
        The frequency.

    Returns
    -------
    float : The normalization constant.
    """
    return ONE_OVER_SQRT_TWO if freq == 0 else 1


def discrete_cosine(pixel: int, freq: int) -> float:
    """
    The discrete cosine.

    Parameters
    ----------
    pixel : int
        Pixel index.
    freq : int
        Frequency index.

    Returns
    -------
    float : Discrete cosine value.
    """
    return np.cos((np.pi / 8) * (pixel + .5) * freq)


def dcos(*args, **kwargs) -> float:
    """Shorthand for :func:discrete_cosine."""
    return discrete_cosine(*args, **kwargs)


def dct_frequency(
    patch: np.ndarray,
    v: int,
    u: int,
) -> np.ndarray:
    """
    Get the DCT value for a certain frequency.

    Parameters
    ----------
    patch : np.ndarray
        The patch.
    v : int
        The vertical frequency
    u : int
        The horizontal frequncy.

    Returns
    -------
    np.ndarray : The discrete cosine transformation of the patch.
    """
    if patch.shape != (8, 8):
        raise ValueError('Patch shape should be (8, 8).')

    out = 0
    for y in range(patch.shape[0]):
        for x in range(patch.shape[1]):
            out += patch[y, x] * dcos(y, v) * dcos(u, x)
    return out * 0.25 * _norm_constant(v) * _norm_constant(u)


def dct_patch(patch: np.ndarray) -> np.ndarray:
    """
    Get the DCT cosine transform for a patch.

    Parameters
    ----------
    patch : np.ndarray
        The patch from which the frequency is taken.

    Returns
    -------
    np.ndarray : The discrete cosine transform value of a patch.
    """
    if patch.shape != (8, 8):
        raise ValueError('Patch shape should be (8, 8).')

    return np.array([
        dct_frequency(patch, v, u)
        for v in range(8)
        for u in range(8)
    ]).reshape(8, 8)


def dct(image: np.ndarray) -> np.ndarray:
    """
    Apply the dct to an image.

    Parameters
    ----------
    image : np.ndarray
        The 2D image. The dimensions should be a multiple of 8.

    Returns
    -------
    np.ndarray : The discrete cosine transformed image.
    """
    if len(image.shape) != 2:
        raise ValueError('Only implemented for 2D image.')
    if (image.shape[0] % 8 != 0) or (image.shape[1] % 8 != 0):
        raise ValueError('Only implemented for images where the dimensions '
                         'are multiple of 8')

    # A zero centered images matches the discrete cosine filters better
    image = image - 128

    out = np.zeros(image.shape)
    for y in range(0, image.shape[0], 8):
        for x in range(0, image.shape[1], 8):
            patch = image[y: y + 8, x: x + 8]
            patch_dct = dct_patch(patch)
            out[y: y + 8, x: x + 8] = patch_dct
    return out


def encode(sequence: np.array) -> str:
    """
    Encode a sequence of numbers using Huffman compression.

    Parameters
    ----------
    sequence : np.array
        The sequence of numbers to be encoded.

    Returns
    -------
    str : The encoded numbers.
    """
    runlength = 0
    code = ''
    for val in sequence:
        if val == 0:
            runlength += 1
            continue

        while runlength >= 15:
            code += '11110000'
            runlength -= 15

        val_code = ENCODER[abs(val)]
        code += int_to_bits(runlength).zfill(4)
        code += int_to_bits(len(val_code)).zfill(4)
        code += '1' if val < 0 else '0'
        code += val_code
        runlength = 0

    code += '0' * 8
    return code


def compress(image: np.ndarray, Q: Union[float, np.ndarray] = 1) -> str:
    """
    Compress an image.

    Parameters
    ----------
    image : np.ndarray
        The 2D image. The dimensions should be a multiple of 8.
    Q : Union[float, np.ndarray] (default : 1)
        Quantization table used for compression.

    Returns
    -------
    str : The byte sequence of the compressed image.
    """
    if len(image.shape) != 2:
        raise ValueError('Only implemented for 2D image.')
    if (image.shape[0] % 8 != 0) or (image.shape[1] % 8 != 0):
        raise ValueError('Only implemented for images where the dimensions '
                         'are multiple of 8')

    # A zero centered images matches the discrete cosine filters better
    image = image - 128

    code = ''
    for y in range(0, image.shape[0], 8):
        for x in range(0, image.shape[1], 8):
            patch = image[y: y + 8, x: x + 8]
            dct = dct_patch(patch)
            low_pass = dct / Q
            dct_flatten = zigzag_patch(low_pass)
            code += encode(dct_flatten.astype(int))
    return code

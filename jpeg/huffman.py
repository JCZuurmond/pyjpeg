import math
from typing import Iterable

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


ENCODER = {int_: int_to_bits(int_) for int_ in range(1000)}
DECODER = {v: k for k, v in ENCODER.items()}


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


def encode(sequence: Iterable) -> str:
    """
    Encode a sequence with Huffman (entropy) encoding.

    The encoding is done with entropy encoding, i.e. using a smaller bit
    representation for more frequent occurring values. The mapping above is
    used. Also there are markers for many sequential zeros.

    Parameters
    ----------
    sequence : Iterable
        The sequence to encoded.

    Returns
    -------
    str : The bit string.
    """
    code = ''
    runlength = 0      # number of sequential zeros
    for s in sequence:
        if s == 0:
            runlength += 1
            continue

        while runlength >= 15:
            code += '11110000'   # marker for 15 sequential zeros
            runlength -= 15

        # Half a byte describes the number of zeros before this non-zero
        # value.
        code += int_to_bits(runlength).zfill(4)

        # Half a byte describes the number of bits needed to describe the
        # non-zero value.
        code += int_to_bits(len(ENCODER[abs(s)])).zfill(4)

        # One bit describes the sign (positive or negative)
        code += '1' if s < 0 else '0'

        # The bits to describe the value
        code += ENCODER[abs(s)]

        runlength = 0

    code += '0' * 8   # end of block (patch) marker
    return code


def decode(code: str) -> np.array:
    """
    The Huffman encoded code, to be decoded.

    Parameters
    ----------
    code : str
        The code to be decoded.

    Returns
    -------
    np.array : The decoded sequence.
    """
    # We expect an 8 by 8 sequence!!!
    sequence = np.zeros(64)

    sequence_idx = 0
    code_idx = 0
    while True:
        runlength = bits_to_int(code[code_idx: code_idx + 4])
        n_bits = bits_to_int(code[code_idx + 4: code_idx + 8])

        if runlength == 0 and n_bits == 0:    # End of block
            break

        sign = -1 if code[code_idx + 8] == '1' else 1
        bit_rep = code[code_idx + 9: code_idx + 9 + n_bits]

        sequence_idx += runlength
        sequence[sequence_idx] = sign * DECODER[bit_rep]

        code_idx += 9 + n_bits
        sequence_idx += 1

    return sequence.reshape(8, 8)

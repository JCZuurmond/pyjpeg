from typing import (
    Iterable,
    Union,
)

import numpy as np

from .freq import dct
from .utils import (
    bits_to_int,
    int_to_bits,
    zigzag_patch,
)


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
        code += int_to_bits(len(int_to_bits[abs(s)])).zfill(4)

        # One bit describes the sign (positive or negative)
        code += '1' if s < 0 else '0'

        # The bits to describe the value
        code += int_to_bits[abs(s)]

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
        sequence[sequence_idx] = sign * bits_to_int[bit_rep]

        code_idx += 9 + n_bits
        sequence_idx += 1

    return sequence.reshape(8, 8)


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

    code = int_to_bits(image.shape[0]).zfill(8)
    code += int_to_bits(image.shape[1]).zfill(8)
    for y in range(0, image.shape[0], 8):
        for x in range(0, image.shape[1], 8):
            patch = image[y: y + 8, x: x + 8]
            dct_patch = dct(patch)
            low_pass = dct_patch / Q
            dct_flatten = zigzag_patch(low_pass)
            code += encode(dct_flatten.astype(int))
    return code


def decompress(sequence: str) -> np.ndarray:
    """
    Decompress a compressed image.

    Parameters
    ----------
    sequence : str
        TODO

    Returns
    -------
    np.ndarray : TODO
    """
    height = bits_to_int(sequence[:8])
    width = bits_to_int(sequence[8: 16])
    im = np.zeros((height, width))

    i = 0
    byte_blocks = sequence[16:].split('0' * 8)
    for y in range(0, im.shape[0], 8):
        for x in range(0, im.shape[1], 8):
            im[y: y + 8, x: x + 8] = decode(byte_blocks[i] + '0' * 8)
            i += 1

    return im + 128

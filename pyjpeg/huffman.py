import math
from typing import Iterable

import numpy as np


ENCODER = {
    1: '10',
    2: '11',
    3: '011',
    17: '000',
    4: '0101',
    65: '00100',
    5: '001101',
    18: '001110',
    33: '001111',
    49: '010011',
    97: '001010',
    6: '0100001',
    19: '0100011',
    81: '0100101',
    113: '0010110',
    7: '01000100',
    34: '01001000',
    129: '00101111',
    145: '00110000',
    161: '00110001',
    20: '010000011',
    50: '010001011',
    177: '001100101',
    193: '001100110',
    8: '0100000101',
    35: '0100010101',
    66: '0100100101',
    209: '0011001111',
    240: '0100000010',
    21: '01000001001',
    82: '01001001100',
    36: '010001010001',
    51: '010001010011',
    98: '010010011100',
    114: '010010011111',
    130: '001011100011',
    117: '0010111000000',
    118: '0010111000001',
    119: '0010111000010',
    120: '0010111000011',
    121: '0010111000100',
    122: '0010111000101',
    131: '0010111001000',
    132: '0010111001001',
    133: '0010111001010',
    134: '0010111001011',
    135: '0010111001100',
    136: '0010111001101',
    137: '0010111001110',
    138: '0010111001111',
    146: '0010111010000',
    147: '0010111010001',
    148: '0010111010010',
    149: '0010111010011',
    150: '0010111010100',
    151: '0010111010101',
    152: '0010111010110',
    153: '0010111010111',
    154: '0010111011000',
    162: '0010111011001',
    163: '0010111011010',
    164: '0010111011011',
    165: '0010111011100',
    166: '0010111011101',
    167: '0010111011110',
    168: '0010111011111',
    169: '0011001000000',
    170: '0011001000001',
    178: '0011001000010',
    179: '0011001000011',
    180: '0011001000100',
    181: '0011001000101',
    182: '0011001000110',
    183: '0011001000111',
    184: '0011001001000',
    185: '0011001001001',
    186: '0011001001010',
    194: '0011001001011',
    195: '0011001001100',
    196: '0011001001101',
    197: '0011001001110',
    198: '0011001001111',
    199: '0011001110000',
    200: '0011001110001',
    201: '0011001110010',
    202: '0011001110011',
    210: '0011001110100',
    211: '0011001110101',
    212: '0011001110110',
    213: '0011001110111',
    214: '0100000000000',
    215: '0100000000001',
    216: '0100000000010',
    217: '0100000000011',
    218: '0100000000100',
    225: '0100000000101',
    226: '0100000000110',
    227: '0100000000111',
    228: '0100000001000',
    229: '0100000001001',
    230: '0100000001010',
    231: '0100000001011',
    232: '0100000001100',
    233: '0100000001101',
    234: '0100000001110',
    241: '0100000001111',
    242: '0100000011000',
    243: '0100000011001',
    244: '0100000011010',
    245: '0100000011011',
    246: '0100000011100',
    247: '0100000011101',
    248: '0100000011110',
    249: '0100000011111',
    250: '0100000100000',
    9: '01000001000010',
    10: '01000001000011',
    22: '01000001000100',
    23: '01000001000101',
    24: '01000001000110',
    25: '01000001000111',
    26: '01000101000000',
    37: '01000101000001',
    38: '01000101000010',
    39: '01000101000011',
    40: '01000101001000',
    41: '01000101001001',
    42: '01000101001010',
    52: '01000101001011',
    53: '01001001000000',
    54: '01001001000001',
    55: '01001001000010',
    56: '01001001000011',
    57: '01001001000100',
    58: '01001001000101',
    67: '01001001000110',
    68: '01001001000111',
    69: '01001001001000',
    70: '01001001001001',
    71: '01001001001010',
    72: '01001001001011',
    73: '01001001001100',
    74: '01001001001101',
    83: '01001001001110',
    84: '01001001001111',
    85: '01001001101000',
    86: '01001001101001',
    87: '01001001101010',
    88: '01001001101011',
    89: '01001001101100',
    90: '01001001101101',
    99: '01001001101110',
    100: '01001001101111',
    101: '01001001110100',
    102: '01001001110101',
    103: '01001001110110',
    104: '01001001110111',
    105: '01001001111000',
    106: '01001001111001',
    115: '01001001111010',
    116: '01001001111011'
}


DECODER = {v: k for k, v in ENCODER.items()}


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
    while code_idx < len(code):
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

    return sequence

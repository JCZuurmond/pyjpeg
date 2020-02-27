from typing import Iterable

import numpy as np

from .utils import (
    bits_to_int,
    int_to_bits,
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

        number_in_bits = int_to_bits(abs(s))
        # Half a byte describes the number of bits needed to describe the
        # non-zero value.
        code += int_to_bits(len(number_in_bits)).zfill(4)

        # One bit describes the sign (positive or negative)
        code += '1' if s < 0 else '0'

        # The bits to describe the value
        code += number_in_bits

        runlength = 0

    code += '0' * 8   # end of block (patch) marker
    return code


def decode(code: str, *, remainder: bool = False) -> np.array:
    """
    The Huffman encoded code, to be decoded.

    Parameters
    ----------
    code : str
        The code to be decoded.
    remainder : bool
        If true, also return the remainder of the code.

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
            code_idx += 8
            break

        if runlength == 15 and n_bits == 0:
            sequence_idx += 15
            code_idx += 8
            continue

        sign = -1 if code[code_idx + 8] == '1' else 1
        bit_rep = code[code_idx + 9: code_idx + 9 + n_bits]

        sequence_idx += runlength
        sequence[sequence_idx] = sign * bits_to_int(bit_rep)

        code_idx += 9 + n_bits
        sequence_idx += 1

    if remainder:
        return sequence, code[code_idx:]
    else:
        return sequence

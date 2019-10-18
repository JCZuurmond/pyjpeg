import numpy as np
from numpy.testing import assert_array_equal

from pyjpeg import huffman


BITS_INT = {
    '1111101': 125,
    '1111110': 126,
    '1111111': 127,
    '1111': 15,
    '1110': 14,
    '1101': 13,
    '1100': 12,
    '1011': 11,
    '1010': 10,
    '1001': 9,
    '0111': 7,
    '1000': 8,
    '0110': 6,
    '0101': 5,
    '0100': 4,
    '0011': 3,
    '0010': 2,
    '0001': 1,
    '0000': 0,
}


def test_bits_to_int():
    for bits, int_ in BITS_INT.items():
        assert huffman.bits_to_int(bits) == int_


def test_int_to_bits():
    for bits, int_ in BITS_INT.items():
        assert huffman.int_to_bits(int_).zfill(len(bits)) == bits


def test_encode_all_zeros():
    zeros = np.zeros(20)
    out = huffman.encode(zeros)
    assert_array_equal(out, '0' * 8)


def test_decode_all_zeros():
    code = '0' * 8
    out = huffman.decode(code)
    assert_array_equal(out, np.zeros(64))

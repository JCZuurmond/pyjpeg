import numpy as np
import pytest
from numpy.testing import assert_array_equal

from jpeg import huffman


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


@pytest.fixture
def B():
    return np.array([
        [-26, -3, -6, 2, 2, -1, 0, 0],
        [0, -2, -4, 1, 1, 0, 0, 0],
        [-3, 1, 5, -1, -1, 0, 0, 0],
        [-3, 1, 2, -1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ])


@pytest.fixture
def B_zigzag():
    return np.array([
        -26, -3, 0, -3, -2, -6, 2, -4,
        1, -3, 1, 1, 5, 1, 2, -1,
        1, -1, 2, 0, 0, 0, 0, 0,
        -1, -1, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
    ])


def test_bits_to_int():
    for bits, int_ in BITS_INT.items():
        assert huffman.bits_to_int(bits) == int_


def test_int_to_bits():
    for bits, int_ in BITS_INT.items():
        assert huffman.int_to_bits(int_).zfill(len(bits)) == bits


def test_bits_to_int_and_back():
    for bits in BITS_INT.keys():
        int_ = huffman.bits_to_int(bits)
        assert huffman.int_to_bits(int_).zfill(len(bits)) == bits


def test_int_to_bits_and_back():
    for int_ in BITS_INT.values():
        bits = huffman.int_to_bits(int_)
        assert huffman.bits_to_int(bits) == int_


@pytest.mark.parametrize(
    "bits,expected",
    [('11101001', 233),
     ('1010110101', 693),
     ('1111000100', 964),
     ('1001111001', 633),
     ('1101101101', 877)]
)
def test_bits_to_int_large_numbers(bits, expected):
    assert huffman.bits_to_int(bits) == expected


def test_zfill_bits_to_int():
    bits = '1010'
    assert huffman.bits_to_int(bits) == huffman.bits_to_int(bits.zfill(10))


@pytest.mark.parametrize(
    "number,expected",
    [(233, '11101001'),
     (693, '1010110101'),
     (964, '1111000100'),
     (633, '1001111001'),
     (877, '1101101101')]
)
def test_int_to_bits_large_numbers(number, expected):
    assert huffman.int_to_bits(number) == expected


def test_encode_all_zeros():
    zeros = np.zeros(20)
    out = huffman.encode(zeros)
    assert_array_equal(out, '0' * 8)


def test_decode_all_zeros():
    code = '0' * 8
    out = huffman.decode(code)
    assert_array_equal(out, np.zeros(64))


def test_zigzag_patch(B, B_zigzag):
    out = huffman.zigzag_patch(B)
    np.testing.assert_array_equal(out, B_zigzag)


def test_izigzag_patch(B, B_zigzag):
    out = huffman.izigzag_patch(B_zigzag)
    np.testing.assert_array_equal(out, B)


def test_huffman_encode_decode_b(B):
    out = huffman.decode(huffman.encode(B.flatten()))
    np.testing.assert_array_equal(out, B.flatten())


def test_huffman_encode_decode_b_zigzag(B_zigzag):
    out = huffman.decode(huffman.encode(B_zigzag))
    np.testing.assert_array_equal(out, B_zigzag)

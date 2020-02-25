import numpy as np
import pytest
from numpy.testing import assert_array_equal

from jpeg import huffman


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

import numpy as np
from numpy.testing import assert_array_equal

from pyjpeg import huffman


def test_encode_all_zeros():
    zeros = np.zeros(20)
    out = huffman.encode(zeros)
    assert_array_equal(out, '0' * 8)


def test_decode_all_zeros():
    code = '0' * 8
    out = huffman.decode(code)
    assert_array_equal(out, np.zeros(64))

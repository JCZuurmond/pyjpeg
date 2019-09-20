import numpy as np
import pytest
from scipy import fftpack

from pyjpeg import pyjpeg


@pytest.fixture
def g():
    # Example from: https://en.wikipedia.org/wiki/JPEG
    return np.array([
        [-76, -73, -67, -62, -58, -67, -64, -55],
        [-65, -69, -73, -38, -19, -43, -59, -56],
        [-66, -69, -60, -15, 16, -24, -62, -55],
        [-65, -70, -57, -6, 26, -22, -58, -59],
        [-61, -67, -60, -24, -2, -40, -60, -58],
        [-49, -63, -68, -58, -51, -60, -70, -53],
        [-43, -57, -64, -69, -73, -67, -63, -45],
        [-41, -49, -59, -60, -63, -52, -50, -34],
    ])


@pytest.fixture
def G():
    # Example from: https://en.wikipedia.org/wiki/JPEG
    return np.array([
        [-415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46],
        [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88],
        [-46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65],
        [-48.53, 12.07, 34.10, 14.76, -10.24, 6.30, 1.83, 1.95],
        [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79, 3.14],
        [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
        [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
        [-0.17, 0.14, -1.07, -4.19, -1.17, -0.10, 0.50, 1.68]
    ])


def test_dct_zeros_block_all_zeros():
    dct = pyjpeg.dct(np.zeros((8, 8)))
    np.testing.assert_array_equal(dct, 0)


def test_idct_of_dct_is_identitcal_to_input():
    idct = pyjpeg.idct(pyjpeg.dct(np.zeros((8, 8))))
    np.testing.assert_array_equal(idct, np.zeros((8, 8)))


def test_dct_raises_value_error_wrong_patch_size():
    with pytest.raises(ValueError):
        pyjpeg.dct(np.zeros((3, 3)))


def test_idct_raises_value_error_wrong_patch_size():
    with pytest.raises(ValueError):
        pyjpeg.idct(np.zeros((3, 3)))


def test_dct_wikipedia_example(g, G):
    assert (pyjpeg.dct(g) - G < 1e-2).all()


def test_idct_dct_wikipedia_example(g):
    np.testing.assert_array_almost_equal(pyjpeg.idct(pyjpeg.dct(g)), g)


def test_scipy_dct_same_as_pyjpeg_dct_wikipedia_example(g):
    np.testing.assert_array_almost_equal(
        pyjpeg.dct(g),
        fftpack.dctn(g, norm='ortho')
    )


def test_scipy_idct_same_as_pyjpeg_dct_wikipedia_example(G):
    np.testing.assert_array_almost_equal(
        pyjpeg.idct(G),
        fftpack.idctn(G, norm='ortho')
    )


def test_scipy_idct_dct_same_as_pyjpeg_idct_dct_wikipedia_example(g):
    np.testing.assert_array_almost_equal(
        pyjpeg.idct(pyjpeg.dct(g)),
        fftpack.idctn(fftpack.dctn(g, norm='ortho'), norm='ortho')
    )


@pytest.mark.parametrize(
    "bits,expected",
    [('0', 0),
     ('1', 1),
     ('10', 2),
     ('11', 3),
     ('100', 4),
     ('101', 5),
     ('110', 6),
     ('111', 7),
     ('1000', 8),
     ('1001', 9),
     ('1010', 10),
     ('1011', 11),
     ('1100', 12),
     ('1101', 13),
     ('1110', 14),
     ('1111', 15)]
)
def test_bits_to_int_uptill_fifteen(bits, expected):
    assert pyjpeg.bits_to_int(bits) == expected


@pytest.mark.parametrize(
    "bits,expected",
    [('11101001', 233),
     ('1010110101', 693),
     ('1111000100', 964),
     ('1001111001', 633),
     ('1101101101', 877)]
)
def test_bits_to_int_large_numbers(bits, expected):
    assert pyjpeg.bits_to_int(bits) == expected

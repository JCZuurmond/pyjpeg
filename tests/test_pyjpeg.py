import numpy as np
import pytest

from pyjpeg import pyjpeg


def test_pyjpeg():
    assert pyjpeg


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

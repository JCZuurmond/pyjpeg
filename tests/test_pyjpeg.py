import numpy as np
import pytest

from pyjpeg import pyjpeg


@pytest.fixture
def zeros_block():
    return np.zeros((8, 8))


def test_pyjpeg():
    assert pyjpeg


def test_dct_zeros_block_all_zeros(zeros_block):
    dct = pyjpeg.dct(zeros_block)
    assert (dct == 0).all()


def test_idct_of_dct_is_identitcal_to_input(zeros_block):
    idct = pyjpeg.idct(pyjpeg.dct(zeros_block))
    assert np.array_equal(idct, zeros_block)


def test_dct_raises_value_error_wrong_patch_size():
    with pytest.raises(ValueError):
        pyjpeg.dct(np.zeros((3, 3)))


def test_idct_raises_value_error_wrong_patch_size():
    with pytest.raises(ValueError):
        pyjpeg.idct(np.zeros((3, 3)))

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

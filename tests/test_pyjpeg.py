import numpy as np
import pytest

import pyjpeg


@pytest.fixture
def zeros_block():
    return np.zeros((8, 8))


def test_pyjpeg():
    assert pyjpeg

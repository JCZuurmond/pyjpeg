import numpy as np
from scipy import fftpack


def dct(array: np.array) -> np.array:
    """
    Get the discrete cosine transform of the array.

    Parameters
    ----------
    array : np.array
        The array of which the discrete cosine transform is taken.

    Returns
    -------
    np.array : The discrete cosine transform of the array.
    """
    return fftpack.dct(array)

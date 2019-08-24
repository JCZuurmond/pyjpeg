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


def idct(array: np.array) -> np.array:
    """
    Get the inverse discrete cosine transform of the array.

    Parameters
    ----------
    array : np.array
        The array of which the inverse discrete cosine transform is taken.

    Returns
    -------
    np.array : The inverse discrete cosine transform of the array.
    """
    return fftpack.idct(array)

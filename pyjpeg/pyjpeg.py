import numpy as np
from scipy import fftpack


def dct(patch: np.ndarray) -> np.ndarray:
    """
    Get the discrete cosine transform of the patch.

    Parameters
    ----------
    patch : np.ndarray
        The 8 by 8 patch of which the discrete cosine transform is taken.

    Returns
    -------
    np.ndarray : The discrete cosine transform of the patch.

    Raises
    ------
    ValueError : If the patch is not 8 by 8
    """
    if not patch.shape == (8, 8):
        raise ValueError(f'Patch should have shape (8, 8): patch.shape')
    return fftpack.dct(patch)


def idct(patch: np.ndarray) -> np.ndarray:
    """
    Get the inverse discrete cosine transform of the patch.

    Parameters
    ----------
    patch : np.ndarray
        The patch of which the inverse discrete cosine transform is taken.

    Returns
    -------
    np.array : The inverse discrete cosine transform of the patch.

    Raises
    ------
    ValueError : If the patch is not 8 by 8
    """
    if not patch.shape == (8, 8):
        raise ValueError(f'Patch should have shape (8, 8): patch.shape')
    return fftpack.idct(patch)

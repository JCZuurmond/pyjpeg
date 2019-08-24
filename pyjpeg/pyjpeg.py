import numpy as np
from scipy import fftpack
from typing import Union


ONE_OVER_SQRT_TWO = 2 ** (-0.5)


def _cosine_1d(
        pixels: Union[int, np.array],
        spatial_frequency: Union[int, np.array]) -> np.array:
    """
    Get the 1D cosines needed for (i)DCT.

    Parameters
    ----------
    pixels : Union[int, np.array]
        The pixels locations.
    spatial_frequency : Union[int, np.array]
        The spatial frequency.

    Returns
    -------
    np.array : The 1D cosine.
    """
    assert type(pixels) != type(spatial_frequency), \
        'pixels and spatial_frequency should have different types.'
    return np.cos(((2 * pixels + 1) * spatial_frequency * np.pi) / 16)


def _dct_cosine_2d(
        vertical_spatial_frequency: int,
        horizontal_spatial_frequency: int) -> np.array:
    """
    Get the 2D cosine for DCT, given the vertical and horizontal spatial
    frequencies.

    Parameters
    ----------
    vertical_spatial_frequency : int
        Vertical spatial frequency.
    horizontal_spatial_frequency : int
        Horizontal spatial frequency.

    Returns
    -------
    np.array : 2D cosine, used in the DCT.
    """
    ver_cosine_1d = _cosine_1d(np.arange(8), vertical_spatial_frequency)
    hor_cosine_1d = _cosine_1d(np.arange(8), horizontal_spatial_frequency)
    return ver_cosine_1d.reshape(8, 1) @ hor_cosine_1d.reshape(1, 8)


def _dct_cosines() -> np.ndarray:
    """
    Get the 2D cosines used for the DCT.

    Returns
    -------
    np.ndarray : 2D cosines, used in the DCT.
    """
    return np.array([
        _dct_cosine_2d(ver_sfreq, hor_sfreq)
        for ver_sfreq in range(8)
        for hor_sfreq in range(8)
    ])


def _alpha_1d() -> np.array:
    """
    Normalization constant `alpha`, one dimensional.

    Returns
    ------
    np.array : Normalization constants.
    """
    alpha_arr = np.ones(8)
    alpha_arr[0] = ONE_OVER_SQRT_TWO
    return alpha_arr


def _alpha_2d() -> np.ndarray:
    """
    Normalization constant `alpha`, two dimensional.

    Returns
    ------
    np.array : Normalization constants.
    """
    alpha_arr = _alpha_1d()
    return alpha_arr.reshape(8, 1) @ alpha_arr.reshape(1, 8)


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

    cosines = _dct_cosines()
    alphas = _alpha_2d().flatten()

    return (
        np.array([0.25 * alphas[idx] * (patch * cosine).sum()
                  for idx, cosine in enumerate(cosines)])
        .reshape(8, 8)
    )


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

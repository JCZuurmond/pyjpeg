from typing import (
    Tuple,
    Callable,
    Union,
)

import numpy as np


ONE_OVER_SQRT_TWO = 2 ** (-0.5)


def discrete_cosine(freq: int, *, patch_size: int = 8) -> float:
    """
    Discrete cosine value for a certain frequency

    Parameters
    ----------
    freq : int
        The frequency
    patch_size : int, optional (default : 8)
        The patch size.

    Returns
    -------
    float : The discrete cosine value.
    """
    return np.cos(freq * (np.arange(patch_size) + .5) * np.pi / 8)


def discrete_cosine_filter(
    freq_ver: int,
    freq_hor: int
) -> np.ndarray:
    """
    Create a discrete cosine filter.

    Parameters
    ----------
    freq_ver : int
        The vertical frequency.
    freq_hor : int
        The horizontal frequency.

    Returns
    -------
    np.ndarray : The discrete cosine filter.
    """
    dc_ver = discrete_cosine(freq_ver).reshape((-1, 1))
    dc_hor = discrete_cosine(freq_hor).reshape((-1, 1))
    c = normalization_constant(freq_ver) * normalization_constant(freq_hor)
    return .25 * c * (dc_ver @ dc_hor)


def apply_filter(
    patch: np.ndarray,
    filter_: Union[Callable, np.ndarray]
) -> Union[float, np.ndarray]:
    """
    Apply a filter to a patch.

    Parameters
    ----------
    patch : np.ndarray
        The patch.
    filter_ : Union[Callable, np.ndarray]
        The filter to be applied to the patch

    Returns
    -------
    Union[float, np.ndarray] : The output of the filter.
    """
    if callable(filter_):
        return filter_(patch)
    else:
        return (patch * filter_).sum()


def apply_filters(
    patch: np.ndarray,
    *filters: Tuple[Union[Callable, np.ndarra]],
) -> np.array:
    """
    Apply multiple filters to a patch.

    Parameters
    ----------
    patch : np.ndarray
        The patch to which the filter is applied.
    *filters : Tuple[Union[Callable, np.ndarray]
        The filters to be applied.

    Returns
    -------
    np.array : The results of the filters.
    """
    if not any(filters):
        raise ValueError('Expecting at least one filter.')
    return np.array([apply_filter(patch, filter_) for filter_ in filters])


def normalization_constant(value: int) -> float:
    """
    Normalization constant.

    Parameters
    ----------
    value : int
        Given the value get the normalization constant.

    Returns
    -------
    float : The normalization constant.
    """
    return ONE_OVER_SQRT_TWO if value == 0 else 1.


def _dct_spatial_frequency(
        patch: np.ndarray,
        v: int,
        u: int) -> float:
    """
    Get the DCT value for a certain spatial frequency.

    Parameters
    ----------
    patch : np.ndarray
        The 8 by 8 patch of which the discrete cosine transform is taken.
    v : int
        The vertical spatial frequency.
    u : int
        The horizontal spatial frequency.

    Returns
    -------
    float : The DCT value for a certain spatial frequency.
    """
    out = 0
    for y in range(8):
        for x in range(8):
            out += patch[y, x] * _dct_cos(y, v) * _dct_cos(x, u)
    return out * _normalization_constant(v) * _normalization_constant(u) * 0.25


def _idct_pixel(
        patch: np.ndarray,
        y: int,
        x: int) -> float:
    """
    Get the inverse DCT value for a certain pixel.

    Parameters
    ----------
    patch : np.ndarray
        The 8 by 8 patch spatial frequency patch.
    y : int
        The vertical pixel location.
    x : int
        The horizontal pixel location

    Returns
    -------
    float : The inverse DCT value for a certain pixel.
    """
    out = 0
    for v in range(8):
        for u in range(8):
            c = (
                _normalization_constant(v) * _normalization_constant(u)
            )
            out += c * patch[v, u] * _dct_cos(y, v) * _dct_cos(x, u)
    return out * 0.25


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
        raise ValueError(f'Patch should have shape (8, 8): {patch.shape}')

    return (
        np.array([_dct_spatial_frequency(patch, v, u)
                  for v in range(8) for u in range(8)])
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
        raise ValueError(f'Patch should have shape (8, 8): {patch.shape}')
    return (
        np.array([_idct_pixel(patch, y, x)
                  for y in range(8) for x in range(8)])
        .reshape(8, 8)
    )

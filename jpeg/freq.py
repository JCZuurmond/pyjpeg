from typing import (
    Callable,
    List,
    Tuple,
    Union,
)

import numpy as np

from .utils import generate_patches


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


def transform(
    im: np.ndarray,
    filters_: List[Union[Callable, np.ndarray]],
    *,
    patch_size: int = 8
) -> np.ndarray:
    """
    Transform an image using the filters.

    Parameters
    ----------
    im : np.ndarray
        The image to transform.
    filters_ : List[Union[Callable, np.ndarray]]
        The filters to apply to the image.
    patch_size : int, optional (default : 8)
        The patch size.

    Returns
    -------
    np.ndarray : The transformed image.
    """
    if not len(filters_) == patch_size ** 2:
        raise ValueError('Expecting as many filters as the len of a patch.')

    im_transformed = [
        apply_filters(patch, *filters_).reshape(patch_size, patch_size)
        for patch in generate_patches(im, patch_size=patch_size)
    ]

    n_hor_patches = int(im.shape[1] / patch_size)
    return np.vstack([
        np.hstack(im_transformed[y * n_hor_patches: (y + 1) * n_hor_patches])
        for y in range(int(im.shape[0] / patch_size))
    ])


def dct(im: np.ndarray) -> np.ndarray:
    """
    Get the discrete cosine transform of an image.

    Parameters
    ----------
    im : np.ndarray
        The image (to be transformed).

    Returns
    -------
    np.ndarray : The image transformed using the discrete cosine transform
    filters.
    """
    dc_filters = [
        discrete_cosine_filter(x, y)
        for x in range(8)
        for y in range(8)
    ]
    return transform(im - 128, dc_filters)

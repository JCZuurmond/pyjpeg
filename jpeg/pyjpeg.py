import numpy as np


ONE_OVER_SQRT_TWO = 1 / np.sqrt(2)


def _norm_constant(freq: int) -> float:
    """
    Normalization constant

    Parameters
    ----------
    freq : int
        TODO

    Returns
    -------
    float : TODO
    """
    return ONE_OVER_SQRT_TWO if freq == 0 else 1


def discrete_cosine(x: float, freq: float) -> float:
    """
    Discrete cosine

    Parameters
    ----------
    x : float
        TODO
    freq : float
        TODO

    Returns
    -------
    float : TODO
    """
    return np.cos((2 * np.pi * freq * (x + 0.5)) / 16)


def dct_frequency(patch: np.ndarray, v: int, u: int) -> float:
    """
    DCT value

    Parameters
    ----------
    patch : np.ndarray
        TODO
    v : int
        TODO
    u : int
        TODO

    Returns
    -------
    float : TODO
    """
    out = 0
    for y in range(8):
        for x in range(8):
            out += patch[y, x] * discrete_cosine(y, v) * discrete_cosine(x, u)
    return out * _norm_constant(v) * _norm_constant(u) * 0.25


def dct_patch(patch: np.ndarray) -> np.ndarray:
    """
    Apply discrete cosine transform to a patch

    Parameters
    ----------
    patch : np.ndarray
        TODO

    Returns
    -------
    np.ndarray : TODO
    """
    return np.array([
        dct_frequency(patch, v, u)
        for v in range(8)
        for u in range(8)
    ]).reshape(8, 8)


def dct(image: np.ndarray) -> np.ndarray:
    """
    Apply a DCT to an image.

    Parameters
    ----------
    image : np.ndarray
        TODO

    Returns
    -------
    np.ndarray : TODO
    """
    image = image - 128
    out = np.zeros(image.shape)
    for y in range(0, out.shape[0], 8):
        for x in range(0, out.shape[1], 8):
            patch = image[x: x + 8, y: y + 8]
            dct_values = dct_patch(patch)
            out[x: x + 8, y: y + 8] = dct_values
    return out

import numpy as np
import scipy
from scipy.ndimage import generic_filter


def _entropy(values):
    probabilities = np.bincount(values.astype(np.int)) / float(len(values))
    return scipy.stats.entropy(probabilities)


def local_entropy(img, kernel_size=3):
    """
    Compute the local entropy for each pixel in an image or image stack using
    the neighbourhood specified by the kernel.

    Arguments:
    ----------
    img : np.ndarray
        The image.
    kernel_size : int
        Neighbourhood over which to compute the local entropy.

    Returns:
    --------
    np.ndarray : Local entropy.
    """
    return generic_filter(img.astype(np.float), _entropy, size=kernel_size)


def entropy2d(img, kernel_size=3):
    """
    Entropy for a 2D images.

    Arguments:
    ----------
    img : np.ndarray
        The image.
    kernel_size : int
        Neighbourhood over which to compute the local entropy.

    Returns:
    --------
    np.ndarray : Local entropy.
    """
    return np.mean(local_entropy(img, kernel_size=kernel_size))

import numpy as np


def generate_patches(im: np.ndarray, *, patch_size: int = 8) -> np.ndarray:
    """
    Generates patches from a given image.

    Parameters
    ----------
    im : np.ndarray
        Image
    patch_size, optional (default : 8)
        Patch size.

    Returns
    -------
    np.ndarray : A patch.
    """
    if len(im.shape) != 2:
        raise ValueError(f'Expecting 2D image: {im.shape}')
    for y in range(0, im.shape[0], patch_size):
        for x in range(0, im.shape[1], patch_size):
            yield im[y: y + patch_size, x: x + patch_size]

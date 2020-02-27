import numpy as np

from typing import Union

from .freq import (
    discrete_cosine_filter,
    inverse_discrete_cosine_filter,
    transform,
)
from .huffman import (
    decode,
    encode,
)
from .utils import (
    bits_to_int,
    generate_patches,
    int_to_bits,
    izigzag_patch,
    zigzag_patch,
)


def compress(im: np.ndarray, *, Q: Union[float, np.ndarray] = 1.) -> str:
    """
    Compress an image.

    Parameters
    ----------
    im : np.ndarray
        The image to be compressed.
    Q : Union[float, np.ndarray] (default : 1.)
        The quantization matrix or number.

    Returns
    -------
    str : The bit representation of the compressed image.
    """
    im = im - 128

    dc_filters = [
        discrete_cosine_filter(x, y)
        for x in range(8)
        for y in range(8)
    ]

    dct = transform(im, dc_filters)

    bit_string = (
        int_to_bits(im.shape[0]).zfill(32) +
        int_to_bits(im.shape[1]).zfill(32)
    )
    bit_string += ''.join(
        encode(zigzag_patch((patch / Q).astype(int)))
        for patch in generate_patches(dct, patch_size=8)
    )

    return bit_string


def decompress(
    bit_string: str,
    *,
    Q: Union[float, np.ndarray] = 1
) -> np.ndarray:
    """
    Decompress an image.

    Parameters
    ----------
    bit_string : str
        The bit representation of an image.
    Q : Union[float, np.ndarray], optional (default : 1.)
        The quantization matrix.

    Returns
    -------
    np.ndarray : The decompressed image.
    """
    height = bits_to_int(bit_string[:32])
    width = bits_to_int(bit_string[32: 64])
    bit_string = bit_string[64:]

    im_transformed = []
    while len(bit_string) > 0:
        patch, bit_string = decode(bit_string, remainder=True)
        im_transformed.append(izigzag_patch(patch) * Q)

    patch_size = 8
    n_hor_patches = int(width / patch_size)
    im_dc = np.vstack([
        np.hstack(im_transformed[y * n_hor_patches: (y + 1) * n_hor_patches])
        for y in range(int(height / patch_size))
    ])

    idc_filters = [
        inverse_discrete_cosine_filter(u, v)
        for u in range(8)
        for v in range(8)
    ]

    im_back = transform(im_dc, idc_filters) + 128

    return im_back.astype(int)

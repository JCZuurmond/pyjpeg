import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotnine as p9
from PIL import Image


def load_image(path):
    image = Image.open(path)
    im = np.array(image.getdata()).reshape(image.size[::-1] + (-1,))
    # Ignore the alpha channel
    im = im[:, :, :3].mean(axis=2)
    return im


def plot_patch(patch, vmin=None, vmax=None, round_digits=1, threshold=None):
    if len(patch.shape) == 1:
        patch = patch.reshape(1, -1)
    if threshold is None:
        threshold = patch.mean()
    vmin = vmin or patch.min()
    vmax = vmax or patch.max()

    tile_height = tile_width = 0.95

    hshift = 0
    vshift = 0.5 * tile_height

    plotr = pd.DataFrame({
        'x': (
            np.tile(np.arange(patch.shape[1]), patch.shape[0]).flatten()
            + hshift
        ),
        'y': (
            - np.repeat(np.arange(patch.shape[0]), patch.shape[1]).flatten()
            + vshift
        ),
        'value': np.round(patch.flatten(), round_digits),
        'color_text': patch.flatten() < threshold
    })

    return (
        p9.ggplot(p9.aes('x', 'y'))
        + p9.geom_tile(plotr, p9.aes(width=tile_width, height=tile_height))
        + p9.geom_text(plotr, p9.aes(label='value', color='color_text'))
        + p9.aes(fill='value')
        + p9.coord_equal(expand=False)
        + p9.theme_void()
        + p9.scales.scale_fill_gradient(
            high='#f0f0f0', low='#252525', guide=False)
        + p9.scales.scale_color_gray(breaks=[False, True], guide=False)
    )


def plot_pixel_values(im):
    plotr = pd.DataFrame(
        {'values': im.flatten()},
        index=range(len(im.flatten()))
    )
    return (
        p9.ggplot()
        + p9.geom_histogram(data=plotr, mapping=p9.aes('values'))
        + p9.theme_xkcd()
        + p9.labels.xlab('Pixel values')
    )


def plot_compare(im_left, im_right):
    fig, (ax_left, ax_right) = plt.subplots(ncols=2, figsize=(10, 8))
    ax_left.imshow(im_left, vmin=0, cmap='gray')
    ax_right.imshow(im_right, vmin=0, cmap='gray')
    for ax in (ax_left, ax_right):
        ax.axis('off')
    ax_left.set_title(f'Original image')
    ax_right.set_title(f'Transformed image')

    fig.tight_layout()
    return fig, (ax_left, ax_right)


def plot_image(im, figsize=(10, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(im, vmin=0, vmax=255, cmap='gray')
    ax.axis('off')
    fig.tight_layout()
    return fig, ax

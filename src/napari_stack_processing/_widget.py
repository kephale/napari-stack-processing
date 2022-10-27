"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import List

import napari
import numpy as np
from magicgui import magic_factory
from napari.layers.image import Image


@magic_factory
def deinterleave_widget(
    img_layer: "napari.layers.Image", num_channels: int = 2
) -> List[napari.types.LayerDataTuple]:
    """
    The ImageJ deinterleave behavior is equivalent to deinterleaving on
    numpy axis==0.
    """
    img = img_layer.data

    deinterleaved = []

    for channel in range(num_channels):
        # Extract channel
        channel_img = img[channel::num_channels, ...]

        deinterleaved += [
            (channel_img, {"name": f"{img_layer.name} C{channel}"})
        ]

    return deinterleaved


@magic_factory
def interleave_widget(
    layer_a: "napari.layers.Image", layer_b: "napari.layers.Image"
) -> Image:
    img_a = layer_a.data
    img_b = layer_b.data

    if img_a.dtype != img_b.dtype:
        print(
            "Inputs must have the same type, but are ",
            f"{img_a.dtype} and {img_b.dtype}.",
        )
        return

    if len(img_a.shape) != len(img_b.shape):
        print(
            "Inputs must have the same dimensionality, but are ",
            f"{img_a.shape} and {img_b.shape}.",
        )
        return

    # Check that all but the first dimension match
    if np.any(img_a.shape[1:] != img_b.shape[1:]):
        print(
            "Inputs must have the same shape except the first dimension",
            f", but are {img_a.shape} and {img_b.shape}.",
        )
        return

    new_shape = list(img_a.shape)
    new_shape[0] += img_b.shape[0]

    interleaved = np.empty(new_shape, dtype=img_a.dtype)
    interleaved[0::2, ...] = img_a
    interleaved[1::2, ...] = img_b

    return Image(
        interleaved, name=f"Interleaved {layer_a.name} and {layer_b.name}"
    )


@magic_factory
def stack_splitter_widget(
    layer: "napari.layers.Image", num_substacks: int
) -> Image:
    """
    The ImageJ deinterleave behavior is equivalent to deinterleaving on
    numpy axis==0.
    """
    img = layer.data

    stacks = []

    if img.shape[0] % num_substacks != 0:
        print(f"Number of substacks must be a divisor of {img.shape[0]}")
        return

    substack_length = img.shape[0] / num_substacks

    for substack_id in range(num_substacks):
        start_idx = substack_id * substack_length
        stop_idx = (substack_id + 1) * substack_length - 1

        substack = img[start_idx:stop_idx, ...]

        stacks += [(substack, {"name": f"{layer.name} Sub{substack_id}"})]

    return stacks

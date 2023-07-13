import math

import halftone as ht
import numpy as np
from PIL import Image, ImageOps

CANVAS_SIZE = (1000, 1000)


def doit(
    size=CANVAS_SIZE,
    subject_size_factor=0.5,
    background_glow_factor=0.5,
    export_intermediates=True,
):
    img = Image.new("RGBA", size=size)

    background = generate_background_gradient(
        size=size, size_factor=background_glow_factor
    )
    if export_intermediates:
        background.save("background.png")

    img.paste(background)

    source = Image.open("source.png").convert("RGBA")

    # WARNING: currently the source is assumed to be square
    subject_size = (
        int(size[0] * subject_size_factor),
        int(size[1] * subject_size_factor),
    )
    scaled_source = source.resize(subject_size)

    img.paste(
        scaled_source,
        box=(
            int((size[0] - subject_size[0]) / 2),
            int((size[1] - subject_size[1]) / 2),
        ),
        mask=scaled_source,
    )

    if export_intermediates:
        img.save("combined.png")

    img = halftoneit(img)

    img.save("output.png")
    img_inverted = ImageOps.invert(img)
    img_inverted.save("output.inverted.png")


def halftoneit(img):
    img = img.convert("L")
    return ht.halftone(img=img, spot_fn=ht.euclid_dot(spacing=9, angle=30))


def generate_background_gradient(size=CANVAS_SIZE, size_factor=1):

    image = Image.new("RGB", size)

    innerColor = [255, 255, 255]
    outerColor = [0, 0, 0]

    for y in range(size[1]):
        for x in range(size[0]):
            # Find the distance to the center
            distanceToCenter = math.sqrt(
                (x - size[0] / 2) ** 2 + (y - size[1] / 2) ** 2
            )

            # Make it on a scale from 0 to 1
            distanceToCenter = (
                float(distanceToCenter)
                / (math.sqrt(2) * size[0] / 2)
                * (1 / size_factor)
            )

            # Calculate r, g, and b values
            r = outerColor[0] * distanceToCenter + innerColor[0] * (
                1 - distanceToCenter
            )
            g = outerColor[1] * distanceToCenter + innerColor[1] * (
                1 - distanceToCenter
            )
            b = outerColor[2] * distanceToCenter + innerColor[2] * (
                1 - distanceToCenter
            )

            # Place the pixel
            image.putpixel((x, y), (int(r), int(g), int(b)))
    return image.convert("RGBA")


doit()

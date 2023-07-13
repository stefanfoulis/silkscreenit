import math

import halftone as ht
import numpy as np
from PIL import Image, ImageOps

CANVAS_SIZE = (1000, 1000)

TURTLE_SKIN_COLOR = (105, 186, 201)
TURTLE_SHELL_COLOR_1 = (16, 155, 53)
TURTLE_SHELL_COLOR_2 = (32, 94, 105)


def doit(
    size=CANVAS_SIZE,
    subject_size_factor=0.7,
    subject_offset=(20, 0),
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
    source = replace_color(source, TURTLE_SKIN_COLOR, (255, 255, 255))
    source = replace_color(source, TURTLE_SHELL_COLOR_1, (200, 200, 200))
    source = replace_color(source, TURTLE_SHELL_COLOR_2, (120, 120, 120))

    # WARNING: currently the source is assumed to be square
    subject_size = (
        int(size[0] * subject_size_factor),
        int(size[1] * subject_size_factor),
    )
    scaled_source = source.resize(subject_size)

    img.paste(
        scaled_source,
        box=(
            int(
                ((size[0] - subject_size[0]) / 2)
                + (size[0] / subject_offset[0] if subject_offset[0] else 0)
            ),
            int(
                ((size[1] - subject_size[1]) / 2)
                + (size[1] / subject_offset[1] if subject_offset[1] else 0)
            ),
        ),
        mask=scaled_source,
    )

    if export_intermediates:
        img.save("combined.png")

    img = halftoneit(img)

    img.save("output.png")
    img_inverted = ImageOps.invert(img)
    img_inverted.save("output.inverted.png")


def replace_color(img, color1, color2):
    # "data" is a height x width x 4 numpy array
    data = np.array(img)

    # Temporarily unpack the bands for readability
    red, green, blue, alpha = data.T

    # Replace color1 with color2... (leaves alpha values alone...)
    white_areas = (red == color1[0]) & (blue == color1[2]) & (green == color1[1])
    data[..., :-1][white_areas.T] = color2  # Transpose back needed

    im2 = Image.fromarray(data)
    return im2


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

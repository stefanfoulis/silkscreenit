import math

import halftone as ht
import numpy as np
from PIL import Image, ImageOps


def generate_background_gradient():
    imgsize = (1000, 1000)

    image = Image.new("RGB", imgsize)

    innerColor = [80, 80, 255]
    outerColor = [0, 0, 0]

    for y in range(imgsize[1]):
        for x in range(imgsize[0]):
            # Find the distance to the center
            distanceToCenter = math.sqrt(
                (x - imgsize[0] / 2) ** 2 + (y - imgsize[1] / 2) ** 2
            )

            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * imgsize[0] / 2)

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
    return image


background = generate_background_gradient()
background.save("background.png")

img = Image.open("source.png")
img = img.convert("L")
# img = PIL.Image.open("lena.png")

halftoned = ht.halftone(img=img, spot_fn=ht.euclid_dot(spacing=9, angle=30))

halftoned.save("output.png")

inverted = ImageOps.invert(halftoned)
inverted.save("output.inverted.png")

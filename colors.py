# -*- encoding: utf-8 -*-
import colorsys

from settings import LOGFILE

"""
Various functions to deal with colors.

The formats for input and output of colors these functions handle is:

- HSV: a tuple `(H, S, V)`, such that:
    - 0 < `H` < 1
    - 0 < `S` < 1
    - 0 < `V` < 1

- RGB: a string with a hex color like "#ff0000"

But **colorsys** treats these colors differently:

- HSV: a tuple `(H, S, V)`, such that:
    - 0 < `H` < 1
    - 0 < `S` < 1
    - 0 < `V` < 255

- RGB: a tuple `(R, G, B)`, such that:
    - 0 < `R` < 255
    - 0 < `G` < 255
    - 0 < `B` < 255
"""

def debug(msg):
    """
    Debugs a message to a log file.
    """
    with open(LOGFILE, 'a') as logfile:
        logfile.write(msg + '\n')

def rgb_average(color1, color2):
    """
    Returns the 'average color' between two colors.

    The average color is calculated taking average of the two 'red' values,
    two 'green' values and 'two' blue values of `color1` and `color2`.

    Args:
        - color1: string, hex representation of a RGB color (e.g. "#ff0000")
        - color2: string, hex representation of a RGB color (e.g. "#ff0000")
    """

    def rgb_hex_to_decimal(rgb_hex):
        hex_values = rgb_hex[1:3], rgb_hex[3:5], rgb_hex[5:7]
        return tuple(int(v, 16) for v in hex_values)

    def rgb_decimal_to_hex(rgb_decimal):
        hex_values = [hex(int(d))[2:] for d in rgb_decimal]
        padded_hex_values = ['{:0>2}'.format(h) for h in hex_values]
        return '#' + ''.join(padded_hex_values)

    color1_decimals = rgb_hex_to_decimal(color1)
    color2_decimals = rgb_hex_to_decimal(color2)

    avg = lambda a, b: (a+b)/2

    average_color_decimals = tuple(
        avg(c1, c2) for c1, c2 in zip(color1_decimals, color2_decimals)
    )

    return rgb_decimal_to_hex(average_color_decimals)

def hsv_change_brightness(hsv_color, value_offset):
    """
    Receives a HSV color and changes its value according to an offset.

    Arguments:
        - hsv_color: a HSV color (see module documentation)
        - value_offset: a offset to the value of the color
    """
    new_hsv_color = list(hsv_color)

    new_hsv_color[2] += value_offset

    if new_hsv_color[2] < 0:
        new_hsv_color[2] = 0
    elif new_hsv_color[2] > 1:
        new_hsv_color[2] = 1

    return new_hsv_color

def rgb_to_hsv(rgb):
    """
    Returns the HSV representation of the RGB color provided.

    Arguments:
        - rgb: a RGB color (see module documentation)
    """
    assert(len(rgb) == 7), rgb_hex

    hex_colors = [rgb[i:i+2] for i in [1, 3, 5]]
    rgb_decimal = tuple(int(c, 16) for c in hex_colors)
    rgb_fraction = tuple(d / 255.0 for d in rgb_decimal)

    return colorsys.rgb_to_hsv(*rgb_fraction)

def hsv_to_rgb(hsv):
    """
    Returns the RGB representation of the HSV color provided.

    Arguments:
        - hsv: a HSV color (see module documentation)
    """
    rgb_fractions = colorsys.hsv_to_rgb(*hsv)
    rgb_decimal = [int(255 * v) for v in rgb_fractions]
    hex_colors = ['{:0>2}'.format(hex(v)[2:]) for v in rgb_decimal]
    return '#' + ''.join(hex_colors)

# -*- encoding: utf-8 -*-
import colorsys

def hsv_change_brightness(hsv_color, brightness_offset):
    new_hsv_color = list(hsv_color)

    new_hsv_color[2] += brightness_offset

    if new_hsv_color[2] < 0:
        new_hsv_color[2] = 0
    elif new_hsv_color[2] > 255:
        new_hsv_color[2] = 255

    return new_hsv_color


def rgb_to_hsv(rgb):
    assert(len(rgb) == 7), rgb_hex

    hex_colors = [rgb[i:i+2] for i in [1, 3, 5]]
    rgb_decimal = tuple(int(c, 16) for c in hex_colors)

    return colorsys.rgb_to_hsv(*rgb_decimal)

def hsv_to_rgb(hsv):
    rgb_decimal = [int(v) for v in colorsys.hsv_to_rgb(*hsv)]
    hex_colors = ['{:0>2}'.format(hex(v)[2:]) for v in rgb_decimal]
    return '#' + ''.join(hex_colors)

def rgb_hex_to_decimal(rgb_hex):
    hex_values = rgb_hex[1:3], rgb_hex[3:5], rgb_hex[5:7]
    return tuple(int(v, 16) for v in hex_values)

def rgb_decimal_to_hex(rgb_decimal):
    hex_values = [hex(int(d))[2:] for d in rgb_decimal]
    padded_hex_values = ['{:0>2}'.format(h) for h in hex_values]
    return '#' + ''.join(padded_hex_values)

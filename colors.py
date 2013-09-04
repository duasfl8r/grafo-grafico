# -*- encoding: utf-8 -*-

def hsv_change_brightness(hsv_color, brightness_offset):
    new_hsv_color = list(hsv_color)

    new_hsv_color[2] += brightness_offset

    if new_hsv_color[2] < 0:
        new_hsv_color[2] = 0
    elif new_hsv_color[2] > 255:
        new_hsv_color[2] = 255

    return new_hsv_color

def rgb_hex_to_rgb_dec(rgb_hex):
    assert(len(rgb_hex) == 7), rgb_hex

    hex_colors = [rgb_hex[i:i+2] for i in [1, 3, 5]]
    return tuple(int(c, 16) for c in hex_colors)

def rgb_dec_to_rgb_hex(rgb_dec):
    assert(len(rgb_dec) == 3)

    hex_colors = ['{:0>2}'.format(hex(v)[2:]) for v in rgb_dec]
    return '#' + ''.join(hex_colors)

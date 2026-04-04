import numpy as np

FRAME_WIDTH = 32
FRAME_HEIGHT = 8

TNR_THRESHOLD = 60

golden_pixels = []

prev_r = 0
prev_g = 0
prev_b = 0

for y in range(FRAME_HEIGHT):
    for x in range(FRAME_WIDTH):

        if x < 2:
            pixel_in = 0
        elif x < 14:
            pixel_in = 220 if y < 4 else 140
        elif x < 20:
            pixel_in = 100 + (x * 3)
        else:
            pixel_in = 160 + ((x + 1) % 2) * 40

        # Demosaic
        if (y % 2 == 0) and (x % 2 == 0):
            r = pixel_in
            g = pixel_in >> 1
            b = pixel_in >> 2

        elif (y % 2 == 0) and (x % 2 == 1):
            r = pixel_in >> 1
            g = pixel_in
            b = pixel_in >> 1

        elif (y % 2 == 1) and (x % 2 == 0):
            r = pixel_in >> 1
            g = pixel_in
            b = pixel_in >> 1

        else:
            r = pixel_in >> 2
            g = pixel_in >> 1
            b = pixel_in

        # White balance
        r = min(255, (r * 270) >> 8)
        g = min(255, (g * 256) >> 8)
        b = min(255, (b * 280) >> 8)

        # Gamma
        r = min(255, int((r / 255.0) ** 0.90 * 255))
        g = min(255, int((g / 255.0) ** 0.90 * 255))
        b = min(255, int((b / 255.0) ** 0.90 * 255))

        # TNR
        diff_r = abs(r - prev_r)
        diff_g = abs(g - prev_g)
        diff_b = abs(b - prev_b)

        if diff_r > TNR_THRESHOLD or diff_g > TNR_THRESHOLD or diff_b > TNR_THRESHOLD:
            r_out = r
            g_out = g
            b_out = b
        else:
            r_out = (3 * r + prev_r) >> 2
            g_out = (3 * g + prev_g) >> 2
            b_out = (3 * b + prev_b) >> 2

        prev_r = r_out
        prev_g = g_out
        prev_b = b_out

        golden_pixels.append([r_out, g_out, b_out])

with open("golden_frame_1.txt", "w") as f:
    for pixel in golden_pixels:
        f.write(f"{pixel[0]} {pixel[1]} {pixel[2]}\n")

print("golden_frame_1.txt generated successfully")
import os
import numpy as np
import matplotlib.pyplot as plt

FRAME_WIDTH = 32
FRAME_HEIGHT = 8

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RTL_FILE = os.path.join(BASE_DIR, "processed_frame_1.txt")
GOLDEN_FILE = os.path.join(BASE_DIR, "golden_frame_1.txt")

DISPLAY_ERROR_LIMIT = 120
PIXEL_TOLERANCE = 90


def load_rgb_file(filename):
    pixels = []

    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"File not found:\n{filename}\n\n"
            f"Make sure the file exists in the same folder as compare_output.py"
        )

    with open(filename, "r") as f:
        for line in f:
            values = line.strip().split()

            if len(values) == 3:
                r = int(values[0])
                g = int(values[1])
                b = int(values[2])
                pixels.append([r, g, b])

    pixels = np.array(pixels, dtype=np.uint8)

    expected_pixels = FRAME_WIDTH * FRAME_HEIGHT

    if len(pixels) < expected_pixels:
        raise ValueError(
            f"{filename} contains only {len(pixels)} pixels, "
            f"but {expected_pixels} are required"
        )

    pixels = pixels[:expected_pixels]
    pixels = pixels.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

    return pixels


rtl_frame = load_rgb_file(RTL_FILE)
golden_frame = load_rgb_file(GOLDEN_FILE)

error_map = np.abs(
    rtl_frame.astype(np.int32) - golden_frame.astype(np.int32)
)

error_intensity = np.sum(error_map, axis=2)

display_error = np.clip(
    error_intensity,
    0,
    DISPLAY_ERROR_LIMIT
)

match_mask = (error_intensity <= PIXEL_TOLERANCE).astype(np.uint8)

total_pixels = FRAME_WIDTH * FRAME_HEIGHT
matching_pixels = np.sum(match_mask)
mismatched_pixels = total_pixels - matching_pixels
accuracy = (matching_pixels / total_pixels) * 100.0

avg_error = np.mean(error_intensity)
max_error = np.max(display_error)

plt.style.use("dark_background")

fig, axes = plt.subplots(1, 3, figsize=(22, 7))
fig.patch.set_facecolor("#17172f")

axes[0].imshow(rtl_frame, interpolation="nearest")
axes[0].set_title(
    "RTL Output",
    fontsize=18,
    color="white",
    pad=12
)
axes[0].axis("off")

axes[1].imshow(golden_frame, interpolation="nearest")
axes[1].set_title(
    "Golden Reference",
    fontsize=18,
    color="white",
    pad=12
)
axes[1].axis("off")

heatmap = axes[2].imshow(
    display_error,
    cmap="hot",
    vmin=0,
    vmax=DISPLAY_ERROR_LIMIT
)

axes[2].set_title(
    "Error Heatmap",
    fontsize=18,
    color="white",
    pad=12
)
axes[2].axis("off")

cbar = fig.colorbar(
    heatmap,
    ax=axes[2],
    fraction=0.046,
    pad=0.04
)
cbar.set_label(
    "RGB Error Magnitude",
    color="white",
    fontsize=11
)
cbar.ax.yaxis.set_tick_params(color="white")
plt.setp(cbar.ax.get_yticklabels(), color="white")

plt.suptitle(
    "RTL vs Golden Reference Comparison",
    fontsize=24,
    fontweight="bold",
    color="white"
)

plt.figtext(
    0.5,
    0.07,
    f"Accuracy = {accuracy:.2f}%   |   "
    f"Matching Pixels = {matching_pixels}   |   "
    f"Mismatched Pixels = {mismatched_pixels}   |   "
    f"Average Error = {avg_error:.2f}   |   "
    f"Displayed Max Error = {max_error}",
    ha="center",
    fontsize=13,
    color="#d0d0d0"
)

plt.tight_layout(rect=[0, 0.10, 1, 0.92])
plt.show()
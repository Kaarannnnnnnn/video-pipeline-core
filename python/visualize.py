import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.patches import FancyBboxPatch

FRAME_WIDTH = 32
FRAME_HEIGHT = 8

base_dir = os.path.dirname(os.path.abspath(__file__))


def load_rgb_file(filename):
    pixels = []

    full_path = os.path.join(base_dir, filename)

    with open(full_path, "r") as f:
        for line in f:
            values = line.strip().split()

            if len(values) == 3:
                r = int(values[0])
                g = int(values[1])
                b = int(values[2])
                pixels.append([r, g, b])

    pixels = np.array(pixels, dtype=np.uint8)
    pixels = pixels[:FRAME_WIDTH * FRAME_HEIGHT]
    pixels = pixels.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

    return pixels


def create_fake_bayer(rgb_frame):
    bayer = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)

    for y in range(FRAME_HEIGHT):
        for x in range(FRAME_WIDTH):

            r = rgb_frame[y, x, 0]
            g = rgb_frame[y, x, 1]
            b = rgb_frame[y, x, 2]

            # RGGB Bayer pattern
            if (y % 2 == 0) and (x % 2 == 0):
                bayer[y, x] = [r, 0, 0]
            elif (y % 2 == 0) and (x % 2 == 1):
                bayer[y, x] = [0, g, 0]
            elif (y % 2 == 1) and (x % 2 == 0):
                bayer[y, x] = [0, g, 0]
            else:
                bayer[y, x] = [0, 0, b]

    return bayer


# Load frames
frame1 = load_rgb_file("processed_frame_1.txt")
frame2 = load_rgb_file("processed_frame_2.txt")
frame3 = load_rgb_file("processed_frame_3.txt")

raw1 = create_fake_bayer(frame1)
raw2 = create_fake_bayer(frame2)
raw3 = create_fake_bayer(frame3)

plt.style.use("dark_background")

# ==========================================================
# FIGURE 1 - Processed Output Frames
# ==========================================================
fig1 = plt.figure(figsize=(18, 9))
fig1.patch.set_facecolor("#17172f")

plt.suptitle(
    "Video Pipeline Core — Processed Output Frames",
    fontsize=22,
    fontweight="bold",
    color="white",
    y=0.94
)

plt.figtext(
    0.5,
    0.88,
    "DVP Receiver  →  Frame Sync  →  Demosaic  →  White Balance  →  Gamma  →  TNR",
    ha="center",
    fontsize=12,
    color="#A0A0B0"
)

frames = [frame1, frame2, frame3]
titles = ["Frame 1", "Frame 2", "Frame 3"]

for i in range(3):
    ax = plt.subplot(1, 3, i + 1)
    ax.imshow(frames[i], interpolation="nearest")
    ax.set_title(titles[i], fontsize=16, color="white")
    ax.axis("off")

plt.subplots_adjust(left=0.03, right=0.97, top=0.82, bottom=0.12, wspace=0.02)

# ==========================================================
# FIGURE 2 - Raw Bayer vs Processed RGB
# ==========================================================
fig2 = plt.figure(figsize=(20, 10))
fig2.patch.set_facecolor("#17172f")

plt.suptitle(
    "Raw Bayer Sensor Input  vs  Processed RGB Output",
    fontsize=22,
    fontweight="bold",
    color="white",
    y=0.95
)

plt.figtext(
    0.5,
    0.91,
    "Demosaicing reconstructs full RGB from single-channel Bayer pattern",
    ha="center",
    fontsize=12,
    color="#B0B0C0"
)

raw_frames = [raw1, raw2, raw3]
processed_frames = [frame1, frame2, frame3]

for i in range(3):
    ax = plt.subplot(2, 3, i + 1)
    ax.imshow(raw_frames[i], interpolation="nearest")
    ax.set_title(f"Raw Bayer\nFrame {i+1}", color="#ff9999", fontsize=12)
    ax.axis("off")

plt.figtext(
    0.5,
    0.51,
    "▼  Demosaic + White Balance + Gamma + TNR  ▼",
    ha="center",
    fontsize=14,
    color="#ffe082",
    fontweight="bold"
)

for i in range(3):
    ax = plt.subplot(2, 3, i + 4)
    ax.imshow(processed_frames[i], interpolation="nearest")
    ax.set_title(f"Processed RGB\nFrame {i+1}", color="#99ff99", fontsize=12)
    ax.axis("off")

plt.subplots_adjust(left=0.03, right=0.97, top=0.84, bottom=0.08, wspace=0.08, hspace=0.45)

# ==========================================================
# FIGURE 3 - TNR Comparison
# ==========================================================
fig3 = plt.figure(figsize=(18, 8))
fig3.patch.set_facecolor("#17172f")

plt.suptitle(
    "Temporal Noise Reducer (TNR) — Motion-Adaptive Blending",
    fontsize=20,
    fontweight="bold",
    color="white",
    y=0.94
)

plt.figtext(
    0.5,
    0.88,
    "Static regions blend across frames to reduce sensor noise  |  Moving regions use current frame to prevent ghosting",
    ha="center",
    fontsize=11,
    color="#A0A0B0"
)

ax1 = plt.subplot(1, 2, 1)
ax1.imshow(frame1, interpolation="nearest")
ax1.set_title(
    "Frame 1  —  TNR Cold Start\nNo previous frame history",
    fontsize=14,
    color="#ff9999"
)
ax1.axis("off")

ax2 = plt.subplot(1, 2, 2)
ax2.imshow(frame3, interpolation="nearest")
ax2.set_title(
    "Frame 3  —  TNR Stabilized\n2 frames of temporal blending applied",
    fontsize=14,
    color="#99ff99"
)
ax2.axis("off")

plt.subplots_adjust(left=0.03, right=0.97, top=0.80, bottom=0.10, wspace=0.03)

# ==========================================================
# FIGURE 4 - Architecture Diagram
# ==========================================================
fig4, ax = plt.subplots(figsize=(18, 8))
fig4.patch.set_facecolor("#17172f")
ax.set_facecolor("#17172f")

ax.set_xlim(0, 14)
ax.set_ylim(0, 6)
ax.axis("off")

plt.text(
    7,
    5.4,
    "Streaming Video Pipeline — Fully Parameterized  |  Valid/Ready Backpressure  |  AXI-Stream Output",
    ha="center",
    va="center",
    fontsize=16,
    color="#ffe082",
    fontweight="bold"
)

blocks = [
    ("DVP\nReceiver", 1.0, 3.0, "#264653"),
    ("Frame\nSync FSM", 3.0, 3.0, "#2a4d69"),
    ("Demosaic", 5.0, 3.0, "#1f4e5f"),
    ("White\nBalance", 7.0, 3.0, "#1b4965"),
    ("Gamma\nLUT", 9.0, 3.0, "#0f4c5c"),
    ("TNR", 11.0, 3.0, "#073b4c"),
    ("Output\nFIFO", 13.0, 3.0, "#022b3a")
]

for label, x, y, color in blocks:
    rect = FancyBboxPatch(
        (x - 0.8, y - 0.7),
        1.6,
        1.4,
        boxstyle="round,pad=0.2,rounding_size=0.12",
        linewidth=2,
        edgecolor="#5bc0eb",
        facecolor=color
    )
    ax.add_patch(rect)

    plt.text(
        x,
        y,
        label,
        ha="center",
        va="center",
        fontsize=11,
        color="white",
        fontweight="bold"
    )

for i in range(len(blocks) - 1):
    x1 = blocks[i][1] + 0.8
    x2 = blocks[i + 1][1] - 0.8

    ax.annotate(
        "",
        xy=(x2, 3.0),
        xytext=(x1, 3.0),
        arrowprops=dict(arrowstyle="->", lw=2, color="#5bc0eb")
    )

info_text = [
    "Samples PCLK\nVSYNC HSYNC",
    "4-state FSM\nPx coordinates",
    "3×3 Bayer\nLine buffer",
    "Q2.6 fixed\npoint gain",
    "256-entry\nROM lookup",
    "Motion-adaptive\ntemporal blend",
    "AXI-Stream\nbackpressure"
]

for i in range(len(blocks)):
    plt.text(
        blocks[i][1],
        1.1,
        info_text[i],
        ha="center",
        fontsize=9,
        color="#b0bec5"
    )

plt.figtext(
    0.5,
    0.08,
    "Each module: PIXEL_DEPTH / FRAME_WIDTH / FRAME_HEIGHT parameterized  —  VGA → 720p → 1080p without RTL changes",
    ha="center",
    fontsize=11,
    color="#9e9e9e"
)

plt.show()


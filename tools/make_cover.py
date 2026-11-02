"""Draw the cover of 'A Hands-on Guide to Streaming Speech Recognition and Synthesis' as covers/streaming-speech.svg.

A waveform cut into chunks of 8 bars, the way a streaming model receives audio; the first chunk, the one the user
waits for, is the accent colour. Colours are the book's figure palette (ink, muted, focus).
    python3 tools/make_cover.py covers/streaming-speech.svg
"""
import math
import sys

INK, MUTED, FOCUS, PAPER = "#1F1F1F", "#8A8A8A", "#D1495B", "#F4F1E8"
W, H = 600, 800
BARS, CHUNK, BAR_W, GAP = 48, 8, 6.0, 4.0
step = BAR_W + GAP
x0 = (W - (BARS * step - GAP)) / 2
cy = 300

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Cover: A Hands-on Guide to Streaming Speech Recognition and Synthesis">',
         f'<rect width="{W}" height="{H}" fill="{INK}"/>']
for i in range(BARS):
    env = math.sin(math.pi * (i + 0.5) / BARS) ** 0.8
    amp = abs(math.sin(i * 0.9) * 0.6 + math.sin(i * 2.3 + 1) * 0.4)
    h = 18 + 150 * env * (0.25 + 0.75 * amp)
    first = i < CHUNK
    x = x0 + i * step
    parts.append(f'<rect x="{x:.1f}" y="{cy - h / 2:.1f}" width="{BAR_W}" height="{h:.1f}" rx="2" '
                 f'fill="{FOCUS if first else MUTED}"/>')
for k in range(1, BARS // CHUNK):
    x = x0 + k * CHUNK * step - GAP / 2
    parts.append(f'<line x1="{x:.1f}" y1="{cy - 130}" x2="{x:.1f}" y2="{cy + 130}" stroke="{MUTED}" '
                 f'stroke-width="1" stroke-dasharray="3 4" opacity="0.6"/>')
font = 'font-family="Helvetica Neue, Helvetica, Arial, DejaVu Sans, sans-serif" fill="%s"' % PAPER
parts += [
    f'<text x="48" y="510" font-size="26" {font} opacity="0.85">A Hands-on Guide to</text>',
    f'<text x="48" y="568" font-size="46" font-weight="700" {font}>Streaming Speech</text>',
    f'<text x="48" y="616" font-size="30" {font}>Recognition and Synthesis</text>',
    f'<rect x="48" y="650" width="64" height="4" fill="{FOCUS}"/>',
    f'<text x="48" y="720" font-size="22" {font} opacity="0.85">Rocky Shi</text>',
    '</svg>',
]
open(sys.argv[1], "w").write("\n".join(parts) + "\n")

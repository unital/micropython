# Test FrameBuffer.blit method.

import sys

try:
    import framebuf
except ImportError:
    print("SKIP")
    raise SystemExit

if not framebuf.ALPHA:
    print("SKIP")
    raise SystemExit

# This test and its .exp file is based on a little-endian architecture.
if sys.byteorder != "little":
    print("SKIP")
    raise SystemExit


def printbuf(bpp=1):
    print("--8<--")
    for y in range(h):
        for x in range(w * bpp):
            print("%02x" % buf[(x + y * w * bpp)], end="")
        print()
    print("-->8--")


w = 5
h = 4
buf = bytearray(w * h)
fbuf = framebuf.FrameBuffer(buf, w, h, framebuf.GS8)

fbuf2 = framebuf.FrameBuffer(bytearray(4), 2, 2, framebuf.GS8)
fbuf2.fill(0x7F)

# set pixel at various locations with alpha.
for x, y in ((-1, -1), (0, 0), (1, 1), (4, 3)):
    fbuf.fill(0)
    fbuf.pixel(x, y, 0x7F, 0x7F)
    printbuf()

# rect at various locations with alpha.
for x, y in ((-1, -1), (0, 0), (1, 1), (4, 3)):
    fbuf.fill(0)
    fbuf.fill_rect(x, y, 2, 2, 0x7F, 0x7F)
    printbuf()

# hline at various locations with alpha.
for x, y in ((-1, -1), (0, 0), (1, 1), (4, 3)):
    fbuf.fill(0)
    fbuf.hline(x, y, 2, 0x7F, 0x7F)
    printbuf()

# vline at various locations with alpha.
for x, y in ((-1, -1), (0, 0), (1, 1), (4, 3)):
    fbuf.fill(0)
    fbuf.vline(x, y, 2, 0x7F, 0x7F)
    printbuf()

# unfilled rect at various locations with alpha.
for x, y in ((-1, -1), (0, 0), (1, 1), (4, 3)):
    fbuf.fill(0)
    fbuf.rect(x, y, 3, 3, 0x7F, False, 0x7F)
    printbuf()

# Blit another FrameBuffer, at various locations with alpha.
for x, y in ((-1, -1), (0, 0), (1, 1), (4, 3)):
    fbuf.fill(0)
    fbuf.blit(fbuf2, x, y, -1, None, 0x7F)
    printbuf()

# Blit another FrameBuffer, with alpha mask.
alphas = [[0, 0x3F], [0x7F, 0xFF]]
for bpp, format in [
    (8, framebuf.GS8),
    (4, framebuf.GS4_HMSB),
    (2, framebuf.GS2_HMSB),
    (1, framebuf.MONO_HLSB),
]:
    mask = framebuf.FrameBuffer(bytearray(4), 2, 2, format)
    for x in [0, 1]:
        for y in [0, 1]:
            mask.pixel(x, y, alphas[x][y] >> (8 - bpp))

    fbuf.fill(0)
    fbuf.blit(fbuf2, 1, 1, -1, None, mask)
    printbuf()

# Blit another FrameBuffer, with alpha mask, non-black background.
alphas = [[0, 0x3F], [0x7F, 0xFF]]
for bpp, format in [
    (8, framebuf.GS8),
    (4, framebuf.GS4_HMSB),
    (2, framebuf.GS2_HMSB),
    (1, framebuf.MONO_HLSB),
]:
    mask = framebuf.FrameBuffer(bytearray(4), 2, 2, format)
    for x in [0, 1]:
        for y in [0, 1]:
            mask.pixel(x, y, alphas[x][y] >> (8 - bpp))

    fbuf.fill(0xEF)
    fbuf.blit(fbuf2, 1, 1, -1, None, mask)
    printbuf()

# Now in color
buf = bytearray(2 * w * h)
fbuf = framebuf.FrameBuffer(buf, w, h, framebuf.RGB565)

fbuf2 = framebuf.FrameBuffer(bytearray(8), 2, 2, framebuf.RGB565)
fbuf2.fill(0b1111101111100000)

# Blit a color FrameBuffer, at various locations with alpha.
for x, y in ((-1, -1), (0, 0), (1, 1), (4, 3)):
    fbuf.fill(0)
    fbuf.blit(fbuf2, x, y, -1, None, 0x7F)
    printbuf(2)

# Blit a color FrameBuffer, with alpha mask.
alphas = [[0, 0x3F], [0x7F, 0xFF]]
for bpp, format in [
    (8, framebuf.GS8),
    (4, framebuf.GS4_HMSB),
    (2, framebuf.GS2_HMSB),
    (1, framebuf.MONO_HLSB),
]:
    mask = framebuf.FrameBuffer(bytearray(4), 2, 2, format)
    for x in [0, 1]:
        for y in [0, 1]:
            mask.pixel(x, y, alphas[x][y] >> (8 - bpp))

    fbuf.fill(0)
    fbuf.blit(fbuf2, 1, 1, -1, None, mask)
    printbuf(2)

# Blit a color FrameBuffer, with alpha mask, non-black background.
alphas = [[0, 0x3F], [0x7F, 0xFF]]
for bpp, format in [
    (8, framebuf.GS8),
    (4, framebuf.GS4_HMSB),
    (2, framebuf.GS2_HMSB),
    (1, framebuf.MONO_HLSB),
]:
    mask = framebuf.FrameBuffer(bytearray(4), 2, 2, format)
    for x in [0, 1]:
        for y in [0, 1]:
            mask.pixel(x, y, alphas[x][y] >> (8 - bpp))

    fbuf.fill(0b00000_111111_00000)
    fbuf.blit(fbuf2, 1, 1, -1, None, mask)
    printbuf(2)

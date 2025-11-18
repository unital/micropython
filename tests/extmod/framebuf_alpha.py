# Test FrameBuffer.blit method.

try:
    import framebuf
except ImportError:
    print("SKIP")
    raise SystemExit

if not framebuf.ALPHA:
    print("SKIP")
    raise SystemExit


def printbuf():
    print("--8<--")
    for y in range(h):
        for x in range(w):
            print("%02x" % buf[(x + y * w)], end="")
        print()
    print("-->8--")


w = 5
h = 4
buf = bytearray(w * h)
fbuf = framebuf.FrameBuffer(buf, w, h, framebuf.GS8)

fbuf2 = framebuf.FrameBuffer(bytearray(4), 2, 2, framebuf.GS8)
fbuf2.fill(0xFF)

# Blit another FrameBuffer, at various locations with alpha.
for x, y in ((-1, -1), (0, 0), (1, 1), (4, 3)):
    fbuf.fill(0)
    fbuf.blit(fbuf2, x, y, -1, None, 0x7F)
    printbuf()

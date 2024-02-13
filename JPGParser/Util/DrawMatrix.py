def DrawMatrix(x, y, matL, matCb, matCr):
    for yy in range(8):
        for xx in range(8):
            c = "#%02x%02x%02x" % ColorConversion(
                matL[yy][xx], matCb[yy][xx], matCr[yy][xx]
            )
            x1, y1 = (x * 8 + xx) * 2, (y * 8 + yy) * 2
            x2, y2 = (x * 8 + (xx + 1)) * 2, (y * 8 + (yy + 1)) * 2
            w.create_rectangle(x1, y1, x2, y2, fill=c, outline=c)

def DrawMatrix(x, y, matL, matCb, matCr, canvas):
    for yy in range(8):
        for xx in range(8):
            c = "#%02x%02x%02x" % ColorConversion(
                matL[yy][xx], matCb[yy][xx], matCr[yy][xx]
            )
            x1, y1 = (x * 8 + xx) * 2, (y * 8 + yy) * 2
            x2, y2 = (x * 8 + (xx + 1)) * 2, (y * 8 + (yy + 1)) * 2
            canvas.create_rectangle(x1, y1, x2, y2, fill=c, outline=c)
            
    return

def ColorConversion(Y, Cr, Cb):
    R = Cr*(2-2*.299) + Y
    B = Cb*(2-2*.114) + Y
    G = (Y - .114*B - .299*R)/.587
    return (Clamp(R+128),Clamp(G+128),Clamp(B+128) )

def Clamp(col):
    col = 255 if col>255 else col
    col = 0 if col<0 else col
    return  int(col)
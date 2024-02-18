import math


class IDCT:
    """
    An inverse Discrete Cosine Transformation Class
    """

    def __init__(self):
        self.base = [0] * 64
        self.zigzag = [
            [0, 1, 5, 6, 14, 15, 27, 28],
            [2, 4, 7, 13, 16, 26, 29, 42],
            [3, 8, 12, 17, 25, 30, 41, 43],
            [9, 11, 18, 24, 31, 40, 44, 53],
            [10, 19, 23, 32, 39, 45, 52, 54],
            [20, 22, 33, 38, 46, 51, 55, 60],
            [21, 34, 37, 47, 50, 56, 59, 61],
            [35, 36, 48, 49, 57, 58, 62, 63],
        ]
        self.idct_precision = 8
        # Contain in a function and make this more reasonable to look at. Add comments if necessary
        self.idct_table = [
            [
                (self.NormCoeff(u) * math.cos(((2.0 * x + 1.0) * u * math.pi) / 16.0))
                for x in range(self.idct_precision)
            ]
            for u in range(self.idct_precision)
        ]
        
    # Test this after testing unchanged IDCT.py
    def construct_idct_table(self, precision):
        idct_table = []
        
        for u in range(precision):
            row = []
            
            for x in range(precision):
                row.append(self.NormCoeff(u) * math.cos(((2.0 * x + 1.0) * u * math.pi) / 16.0))
            
            idct_table.append(row)
        
        return idct_table

    # Why is this the only function capitalized? Fix it
    def NormCoeff(self, n):
        if n == 0:
            return 1.0 / math.sqrt(2.0)
        else:
            return 1.0

    # What does 'rearrange' mean? Find a better descriptor
    def rearrange_using_zigzag(self):
        for x in range(8):
            for y in range(8):
                self.zigzag[x][y] = self.base[self.zigzag[x][y]]
        return self.zigzag

    # "perform" is ambiguous and not used elsewhere in this codebase. Chose a better word.
    # looks like there could be a few functions extracted here. At most keep the outer double loop and contain the rest in a method
    def perform_IDCT(self):
        out = [list(range(8)) for i in range(8)]

        for x in range(8):
            for y in range(8):
                local_sum = 0
                for u in range(self.idct_precision):
                    for v in range(self.idct_precision):
                        # This formatting is awful
                        local_sum += (
                            self.zigzag[v][u]
                            * self.idct_table[u][x]
                            * self.idct_table[v][y]
                        )
                out[y][x] = local_sum // 4
        self.base = out

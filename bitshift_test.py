import math

for i in range(100):
    b = i >> 3
    s = 7-(i & 0x7)
    
    print('-----------------------------------------')
    print(f'i = {i}')
    print(f'{math.floor(i/8) == b}')
    print(f'Bitshift i: {b}')
    print(f's: {s}')
    print(f'{7 - (i % 8) == s}')
    print(f'b shifted by s: {(b >> s) & 1}')
    print('-----------------------------------------')

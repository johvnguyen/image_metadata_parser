'''
Converts a character stream into ASCII code, then convert the ASCII code into a bitstream.
'''

class Stream:
    def __init__(self, data):
        self.data= data
        self.pos = 0

    # GetBit will parse the next bit in the stream (SoS)
    # What is the point of the b and s variables?
    def GetBit(self):
        # interesting that we shift the index by 3 bits
        # We then obtain s by using 7 in the manipulation -- b'111' = 7 so... there is someting here
        b = self.data[self.pos >> 3]
        s = 7-(self.pos & 0x7)
        
        '''
        print((b >> s) & 1)
        if self.pos % 8 == 0:
            print('\n')
        '''
        self.pos+=1
        
        #print((b >> s) & 1)
        #print(f'NGUYEN: GetBit called!')
        return (b >> s) & 1

    # Reads an l-length binary and converts it to int (quantized value)
    def GetBitN(self, l):
        #print(f'NGUYEN: {l}')
        val = 0
        for i in range(l):
            val = val*2 + self.GetBit()
            
        print(f'val : {val}')
        return val

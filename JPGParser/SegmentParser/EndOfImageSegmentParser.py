from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class EndOfImageSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffd9)
        assert(length == None)
        
        self.seg_name = 'End of Image'
        self.sig = sig
        
    
    def parse(self, image_fp):
        # EoI segment only contains the signature, which is already read
        return
    
    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        print(f'----------------------------------------\n\n')
        
        return

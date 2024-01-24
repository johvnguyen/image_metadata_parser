from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class StartOfScanSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffda)
        
        self.seg_name = 'Start of Scan'
        self.sig = sig
        self.len = length
        
        self.img_data = None
        
    def parse(self, image_fp):
        self.skip_byte_stuffing(image_fp)
        self.img_data = image_fp.read(self.len)
        
        return
    
    def skip_byte_stuffing(self, image_fp):
        start = image_fp.tell()
        n_stuffed_bytes = 0
        
        while self.has_stuffing(image_fp):
            n_stuffed_bytes += 1
            
        image_fp.seek(start)
        stuffed_bytes = image_fp.read(n_stuffed_bytes)
        
        return
    
    def has_stuffing(self, image_fp):
        next_byte = image_fp.read(1)
        next_byte = struct.unpack(">B", next_byte)[0]
        
        if next_byte == 0:
            return True
        else:
            return False

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        print(f'----------------------------------------\n\n')
        return

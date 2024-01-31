from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class APP0HeaderExtensionSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffe0)
        
        self.seg_name = 'APP0 Header Extension Segment'
        self.sig = sig
        self.length = length
        
        self.thumbnail_fmt = None
        self.thumbnail_data = None
        
    
    def parse(self, image_fp):
        thumbnail_fmt_metadta_bytes = image_fp.read(1)
        thumbnail_fmt_metadata = struct.unpack('>B', thumbnail_fmt_metadta_bytes)[0]

        self.thumbnail_fmt = thumbnail_fmt_metadata

        self.thumbnail_data = self.parse_thumbnail_data(image_fp)
        
        return
    
    def parse_thumbnail_data(self, image_fp):
        # Remaining bytes is length, minus the already parsed length, identifier and thumbnail format data
        thumbnail_size = self.length - 2 - 5 - 1
        
        return image_fp.read(thumbnail_size)
    
    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        self.print_thumbnail_fmt()
        print(f'----------------------------------------\n\n')
        
        return

    def print_thumbnail_fmt(self):
        print(f'Thumbnail Format: {self.thumbnail_fmt}')
        
        if self.thumbnail_fmt == 10:
            print(f'\tJPEG Format')
        elif self.thumbnail_fmt == 11:
            print(f'\t1 byte per pixel palletized format')
        elif self.thumbnail_fmt == 13:
            print(f'\t 3 byte per pixel RGB format')

        return
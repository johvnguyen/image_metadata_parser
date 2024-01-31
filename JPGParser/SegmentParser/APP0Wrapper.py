from JPGParser.SegmentParser.SegmentParser import SegmentParser
from JPGParser.SegmentParser.APP0HeaderSegmentParser import APP0HeaderSegmentParser
from JPGParser.SegmentParser.APP0HeaderExtensionSegmentParser import APP0HeaderExtensionSegmentParser

import struct
import logging

class APP0Wrapper(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffe0)
        
        self.seg_name = None
        self.sig = sig
        self.len = length
        
        self.identifier = None
        self.segment = None
        
    
    def parse(self, image_fp):
        self.identifier = self.parse_identifier(image_fp)
        
        if self.is_header(self.identifier):
            self.seg_name = 'JFIF APP0 Segment'
            self.segment = APP0HeaderSegmentParser(self.sig, self.len)
            
        elif self.is_header_extension(self.identifier):
            self.seg_name = 'JFIF APP0 Segment Extension'
            self.segment = APP0HeaderExtensionSegmentParser(self.sig, self.len)
            
        self.segment.parse(image_fp)
        
        return

    def parse_identifier(self, image_fp):
        identifier_fmt_str = '>5s'
        
        identifier_size = struct.calcsize(identifier_fmt_str)
        identifier_bytes = image_fp.read(identifier_size)
        identifier_string = struct.unpack(identifier_fmt_str, identifier_bytes)[0]
        
        identifier = self.extract_identifier_hexstring(identifier_string)
        
        return identifier
    
    def extract_identifier_hexstring(self, identifier_string):
        identifier_arr = bytearray(identifier_string)
        identifier_chars = [format(c, '02x') for c in identifier_arr]
        hexstring = ''.join(identifier_chars)
        
        return hexstring
        
    # I should handle identifier parsing by converting the identifier to a string and checking for 'JFIF' and 'JFXX'
    def is_header(self, identifier):
        return identifier == '4a46494600'
    
    def is_header_extension(self, identifier):
        return identifier == '4a46585800'
            

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        print(f'Identifier: {self.identifier}')
        self.segment.print_metadata()
        print(f'----------------------------------------\n\n')
        
        return

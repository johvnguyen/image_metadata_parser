from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class StartOfFrameSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffc0)
        
        self.seg_name = 'Start of Scan'
        self.sig = sig
        self.len = length
        
        self.precision = None
        self.img_height = None
        self.img_width = None
        self.n_components = None
        self.components = {}
        
    def parse(self, image_fp):
        self.parse_precision(image_fp)
        self.parse_img_dim(image_fp)
        self.parse_n_components(image_fp)
        
        self.parse_components(image_fp)
        
        return
    
    def parse_precision(self, image_fp):
        precision_fmt_str = '>B'
        precision_size = struct.calcsize(precision_fmt_str)
        precision_bytes = image_fp.read(precision_size)
        precision = struct.unpack(precision_fmt_str, precision_bytes)[0]
        
        self.precision = precision
        
        return
    
    def parse_img_dim(self, image_fp):
        dim_fmt_str = '>HH'
        dim_size = struct.calcsize(dim_fmt_str)
        dim_bytes = image_fp.read(dim_size)
        
        (height, width) = struct.unpack(dim_fmt_str, dim_bytes)
        
        self.img_height = height
        self.img_width = width

        return
    
    def parse_n_components(self, image_fp):
        # Parsing the number of components
        noc_fmt_str = '>B'
        noc_size = struct.calcsize(noc_fmt_str)
        noc_bytes = image_fp.read(noc_size)
        number_of_components = struct.unpack(noc_fmt_str, noc_bytes)[0]
        
        self.n_components = number_of_components

        return
    
    def parse_components(self, image_fp):
        # TODO
        return

    def print_metadata(self):
        # TODO
        return
        

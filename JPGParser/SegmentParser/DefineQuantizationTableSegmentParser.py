from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class DefineQuantizationTableSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffdb)
        
        self.seg_name = 'Define Quantization Table'
        self.sig = sig
        self.len = length
        
        self.qt_info = None
        self.qt_vals = None
        
    def parse(self, image_fp):
        self.parse_qt_info(image_fp)
        self.parse_quantization_table(image_fp)
        
        return
    
    def parse_qt_info(self, image_fp):
        qt_info_fmt_str = '>B'
        qt_info_size = struct.calcsize(qt_info_fmt_str)
        qt_info_bytes = image_fp.read(qt_info_size)
        
        self.qt_info = struct.unpack(qt_info_fmt_str, qt_info_bytes)
        
        return
    
    def parse_quantization_table(self, image_fp):
        # JFIF format uses 8x8 quantization tables, so 64 values per table
        qt_fmt_str = 64 * 'B'
        qt_size = struct.calcsize(qt_fmt_str)
        qt_bytes = image_fp.read(qt_size)
        
        self.qt_vals = struct.unpack(qt_fmt_str, qt_bytes)
        
        return

    
    
    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        print(f'Quantization Table Info: {self.qt_info}')
        
        self.print_qt_table()
        
        print(f'----------------------------------------\n\n')
        
        return
    
    def print_qt_table(self):
        assert(self.qt_vals != None)
        assert(len(self.qt_vals) == 64)
        
        for i in range(64):
            if i % 8 == 0:
                print('\n')
            print(self.qt_vals[i], end = ' ')
        
        return
        
        
from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class APP0HeaderSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffe0)
        
        self.seg_name = 'APP0 Header Segment'
        self.sig = sig
        self.length = length
        
        self.data = {}
        self.thumbnail_data = None
        
    
    def parse(self, image_fp):
        data_fmt_str = '>HBHHBB'
        data_size = struct.calcsize(data_fmt_str)
        data_bytes = image_fp.read(data_size)
        data_arr = struct.unpack(data_fmt_str, data_bytes)
        
        self.data['JFIF Version'] = data_arr[0]
        self.data['Density Units'] = data_arr[1]
        self.data['X Density'] = data_arr[2]
        self.data['Y Density'] = data_arr[3]
        self.data['X Thumbnail'] = data_arr[4]
        self.data['Y Thumbnail'] = data_arr[5]
        
        self.parse_thumbnail_data(image_fp)
        return
    
    def parse_thumbnail_data(self, image_fp):
        # Calculate remaining bytes in APP0Header, subtracting out already parsed data, length bytes and identifier bytes
        remaining_data = self.length - struct.calcsize('>HBHHBB') - 2 - 5
        assert(remaining_data % 3 == 0)
        
        # Figure out how to parse this into an image
        self.thumbnail_data = image_fp.read(remaining_data)
        
        return
    
    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        for key in self.data.keys():
            print(f'{key}: {self.data[key]}')
        print(f'----------------------------------------\n\n')
        
        return

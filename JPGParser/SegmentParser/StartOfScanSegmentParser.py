from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class StartOfScanSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffda)
        
        self.seg_name = 'Start of Scan'
        self.sig = sig
        self.len = length
        
        self.raw_img_data = None
        self.img_data = None
        
    def parse(self, image_fp):
        start = image_fp.tell()
        self.raw_img_data = image_fp.read()

        scan_data_len, self.img_data = self.remove_byte_stuffing(self.raw_img_data)
        
        # Setting file reader to just after SoS Segment
        image_fp.seek(start + scan_data_len)
        
        return
    
    def remove_byte_stuffing(self, data):
        img_data = []
        i = 0
        while(True):
            byte,next_byte = struct.unpack("BB",data[i:i+2])        
            if (byte == 0xff):
                if (next_byte != 0):
                    break
                else:
                    img_data.append(data[i])
                    i+=2
                
            else:
                img_data.append(data[i])
                i+=1
        return i, img_data
       
    
    def get_scan_data(self):
        return self.img_data           

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        #print(f'Segment Length: {self.len}')
        print(f'----------------------------------------\n\n')
        return

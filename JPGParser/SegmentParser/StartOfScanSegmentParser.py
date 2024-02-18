from JPGParser.SegmentParser.SegmentParser import SegmentParser
import struct
import logging

class StartOfScanSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffda)
        
        self.seg_name = 'Start of Scan'
        self.sig = sig
        self.len = length
        
        # Parse these bytes out later
        self.raw_img_data = None
        self.img_data = None
        
    def parse(self, image_fp):
        start = image_fp.tell()
        self.raw_img_data = image_fp.read()
        #self.raw_img_data = self.raw_img_data[start:]
        
        #self.img_data = self.parse_img_data(image_fp)
        lenchunk, self.img_data = self.remove_byte_stuffing(self.raw_img_data)
        image_fp.seek(start + lenchunk)
        
        return
    
    def parse_img_data(self, image_fp):
        img_data = self.remove_byte_stuffing(image_fp)
        
        return img_data
    
    def remove_byte_stuffing(self, data):
        datapro = []
        i = 0
        while(True):
            b,bnext = struct.unpack("BB",data[i:i+2])        
            if (b == 0xff):
                if (bnext != 0):
                    break
                datapro.append(data[i])
                i+=2
            else:
                datapro.append(data[i])
                i+=1
        return i, datapro
    
    '''
    
    def remove_byte_stuffing(self, image_fp):
        img_data = []
        i = 0
        start = image_fp.tell()
        while(True):
            image_fp.seek(start + i)
            curr_byte = image_fp.read(1)
            next_byte = image_fp.read(1)
            
            byte = struct.unpack('>B', curr_byte)[0]
            nbyte = struct.unpack('>B', next_byte)[0]
            
            
            if byte == 0xff:
                if nbyte != 0x00:
                    break
                i += 2
                img_data.append(curr_byte)
            else:
                # Don't count the 0 in calculations. Hence the term 'stuffing'
                i += 1
                img_data.append(curr_byte)
        
        image_fp.seek(start + i)
        return img_data
    '''    
    
    def get_scan_data(self):
        return self.img_data
    
                

    '''
    def skip_byte_stuffing(self, image_fp):
        start = image_fp.tell()
        
        n_stuffed_bytes = self.remove_stuffing(image_fp)
        print(n_stuffed_bytes)
        
        image_fp.seek(start)
        stuffed_bytes = image_fp.read(n_stuffed_bytes)
        return
   
    # TODO: Refactor this function to have more expressive names
    def remove_stuffing(self, image_fp):
        i = 0
        last_byte = 0x00
        while(True):
            next_byte = image_fp.read(1)
            #print(len(next_byte))
            next_byte = struct.unpack('>B', next_byte)[0]
            print(hex(next_byte))
            
            if last_byte == 0xff:
                if next_byte == 0x00:
                    i += 1
                    last_byte = next_byte
                else:
                    return i
            elif last_byte == 0x00:
                if next_byte == 0xff:
                    i += 1
                    last_byte = next_byte
                else:
                    return i
            else:
                raise Exception(f'I should not get here. last_byte = {last_byte}, next_byte = {hex(next_byte)}')
    '''
                    

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        #print(f'Segment Length: {self.len}')
        print(f'----------------------------------------\n\n')
        return

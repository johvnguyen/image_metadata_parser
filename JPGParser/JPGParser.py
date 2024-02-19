from ImageParser import ImageParser
from JPGParser.SegmentParser.SegmentParserFactory import SegmentParserFactory
from JPGParser.Util.IDCT import IDCT
from JPGParser.Util.Stream import Stream
from JPGParser.Util.DrawMatrix import Clamp, ColorConversion, DrawMatrix
from JPGParser.Util.HuffmanTable import HuffmanTable
from tkinter import Canvas, Tk
import logging
import struct
import os

class JPGParser(ImageParser):
    def __init__(self):
        self.image_fp = None
        self.segment_parsers = []
        self.segment_parser_factory = SegmentParserFactory()
        self.master = Tk()      # Is there a better name for this?
        self.canvas = Canvas(self.master, width = 1600, height = 600)   # Can I initialize size dynamically?
        self.ht_map = {}
        
        return
        
    def parse(self, filename):
        try:
            self.validate_input(filename)
            self.image_fp = open(filename, 'rb')
            #self.validate_header()
            
        except (ValueError, FileNotFoundError) as err:
            logging.warning(err)
            print(err)
            exit()
            
        
        self.parse_segments()
        
        return
        
        

    def validate_input(self, filename):
        extension = os.path.splitext(filename)[-1]
        extension_lc = extension.lower()
        
        if self.valid_extension(extension_lc):
            return
        else:
            raise ValueError(f'Expected file extension jpg or jpeg but received {extension} from {filename}')

    def valid_extension(self, file_extension):
        if file_extension == '.jpg' or file_extension == '.jpeg':
            return True
        
        return False
    
    def validate_header(self):
        section_header = self.parse_segment_header()
        
        if section_header == 0xffd8:
            return
        else:
            raise ValueError('Header of input file is not 0xffd8 which is not JPG compliant.')
        
    def parse_segment_header(self):
        header_fmt_str = ">H"
        header_size = struct.calcsize(header_fmt_str)
        header_bytes = self.image_fp.read(header_size)
        header = struct.unpack(header_fmt_str, header_bytes)[0]
        
        return header
    
    def parse_segments(self):
        signature = ''
        
        #offset = 0

        while signature != 0xffd9:
            signature = self.parse_segment_signature()
            
            if signature in self.get_segments_with_length():
                length = self.parse_length()
            
            else:
                length = None
            

            print(hex(signature))
            segment_parser = self.segment_parser_factory.generate(signature, length)
            segment_parser.parse(self.image_fp)
            
            self.segment_parsers.append(segment_parser)
            segment_parser.print_metadata()
            
        return
            
            
            
    def parse_segment_signature(self):
        sig_fmt_str = '>H'
        sig_size = struct.calcsize(sig_fmt_str)
        sig_bytes = self.image_fp.read(sig_size)
        signature = struct.unpack(sig_fmt_str, sig_bytes)[0]
        
        return signature
        
    def get_segments_with_length(self):
        return [0xffe0, 0xffdb, 0xffc0, 0xffc4, 0xffda]
    
    def parse_length(self):
        length_fmt_str = '>H'
        length_size = struct.calcsize(length_fmt_str)
        length_bytes = self.image_fp.read(length_size)
        length = struct.unpack(length_fmt_str, length_bytes)[0]
        
        return length
    
    def decode_scan_data(self, display = False):
        assert(len(self.segment_parsers) != 0)
        start_of_frame_parser = self.get_parser(0xffc0)
        (img_height, img_width) = start_of_frame_parser.get_img_dimensions()
        
        quant_mappings = start_of_frame_parser.get_quant_mappings()
        dqt_parsers = self.get_parsers(0xffdb)
        assert(len(dqt_parsers) == 2)
        
        dqt_map = self.make_dqt_map(dqt_parsers)

        sos_parser = self.get_parsers(0xffda)
        assert(len(sos_parser) == 1)
        sos_parser = sos_parser[0]
        img_data = sos_parser.get_scan_data()
        print(f'Length of image data: {len(img_data)}')
        #img_data = bytearray(img_data)
        st = Stream(img_data)
        
        # Sets self.ht_map
        self.build_ht_map()
        
        oldlumdccoeff, oldCbdccoeff, oldCrdccoeff = 0, 0, 0
        
        for y in range(img_height // 8):
            for x in range(img_width // 8):
                matL, oldlumdccoeff = self.BuildMatrix(st,0, dqt_map[quant_mappings[0]], oldlumdccoeff)
                matCr, oldCrdccoeff = self.BuildMatrix(st,1, dqt_map[quant_mappings[1]], oldCrdccoeff)
                matCb, oldCbdccoeff = self.BuildMatrix(st,1, dqt_map[quant_mappings[2]], oldCbdccoeff)
                DrawMatrix(x, y, matL.base, matCb.base, matCr.base, self.canvas )
        
        
        self.display_jpg()
        
        return 
    
    def build_ht_map(self):
        dht_parsers = self.get_parsers(0xffc4)
        
        for parser in dht_parsers:
            # idx = 0 -> DC table values
            # idx = 1 -> AC table values
            (idx, ht) = parser.get_ht_data()
            
            self.ht_map[idx] = ht
            
        return
    
    def make_dqt_map(self, dqt_parsers):
        dqt_map = {}
        
        for parser in dqt_parsers:
            dqt_map[parser.qt_info[0]] = parser.qt_vals
            
        return dqt_map
        
        

    def BuildMatrix(self, st, idx, quant, olddccoeff):
        i = IDCT()

        # TODO: Replace this with my code
        code = self.ht_map[0 + idx].GetCode(st)
        bits = st.GetBitN(code)
        dccoeff = self.decode_number(code, bits) + olddccoeff

        i.base[0] = (dccoeff) * quant[0]
        l = 1
        while l < 64:
            code = self.ht_map[16 + idx].GetCode(st)
            if code == 0:
                break

            # The first part of the AC quantization table
            # is the number of leading zeros
            if code > 15:
                l += code >> 4
                code = code & 0x0F

            bits = st.GetBitN(code)

            if l < 64:
                coeff = self.decode_number(code, bits)
                i.base[l] = coeff * quant[l]
                l += 1

        i.rearrange_using_zigzag()
        i.perform_IDCT()

        return i, dccoeff
        
    def decode_number(self, code, bits):
        l = 2 ** (code - 1)
        
        if bits >= l:
            return bits
        else:
            return bits - (2 * l - 1)
        
        
    def get_parser(self, sig):
        for parser in self.segment_parsers:
            if parser.sig == sig:
                return parser
        
        raise Exception(f'No parser for segment {sig} found.')
    
    def get_parsers(self, sig):
        matching_parsers = []
        
        for parser in self.segment_parsers:
            if parser.sig == sig:
                matching_parsers.append(parser)
            
        return matching_parsers
    
    def display_jpg(self):
        self.canvas.pack()
        self.master.mainloop()
    
    def print_metadata(self):
        pass
        return
#from stat import FILE_ATTRIBUTE_ENCRYPTED
from ImageParser import ImageParser
from JPGParser.SegmentParser.SegmentParserFactory import SegmentParserFactory
import logging
import struct
import os

class JPGParser(ImageParser):
    def __init__(self):
        self.image_fp = None
        self.segment_parsers = []
        self.segment_parser_factory = SegmentParserFactory()
        
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
            
        # TODO: Begin parsing the file. I've already "read" the header signature, so the file pointer is moved up 2 bytes
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
    
    def print_metadata(self):
        pass
        return
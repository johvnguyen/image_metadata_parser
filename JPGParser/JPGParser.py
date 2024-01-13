from stat import FILE_ATTRIBUTE_ENCRYPTED
from ImageParser import ImageParser
from SegmentParserFactory import SegmentParserFactory   # TODO
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
            self.validate_header()
            
        except (ValueError, FileNotFoundError) as err:
            logging.warning(err)
            print(err)
            
        # TODO: Begin parsing the file. I've already "read" the header signature, so the file pointer is moved up 2 bytes
        self.parse_segments()
        
        
        

    def validate_input(self, filename):
        extension = os.path.splitext(filename)[-1]
        extension_lc = extension.lower()
        
        if self.valid_extension(extension_lc):
            return
        else:
            raise ValueError(f'Expected file extension jpg or jpeg but received {extension} from {filename}')

    def valid_extension(self, file_extension):
        if file_extension == 'jpg' or file_extension == 'jpeg':
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
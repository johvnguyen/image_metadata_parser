from ImageParser import ImageParser
from PNGParser.ChunkParser.ChunkParserFactory import ChunkParserFactory
import logging
import struct
import os

class PNGParser(ImageParser):
    def __init__(self):
        self.image_fp = None
        self.chunk_parsers = []
        self.chunk_parser_factory = ChunkParserFactory()

        return

    def parse(self, filename):
        try:
            self.image_fp = open(filename, 'rb')
        except FileNotFoundError as err:
            logging.warning(f"No such file {filename} found. Returning without parsing!")
            print(err)
            return

        self.validate_header()

        # TODO: Iterate through chunks, parsing 
        while not self.end_of_file():
            self.parse_chunk()

        return
        

    def validate_header(self):
        try:
            header_signature = ['0x89', '0x50', '0x4e', '0x47', '0xd', '0xa', '0x1a', '0xa']

            header_format_string = '>BBBBBBBB'
            header_size = struct.calcsize(header_format_string)

            header_bytes = self.image_fp.read(header_size)
            header_values = struct.Struct(header_format_string).unpack_from(header_bytes)

            header_values = [hex(x) for x in header_values]

            for (val, sig) in zip(header_values, header_signature):
                if val != sig:
                    raise ValueError

        except ValueError as err:            # TODO: Move this exception into parse() function
            logging.warning(f"File does not have header signature. File is potentiall corrupted! Terminating parse() call")
            print(err)
            return

        return
    
    def end_of_file(self):
        return self.image_fp.tell() == os.fstat(self.image_fp.fileno()).st_size

    def parse_chunk(self):
        # Parse chunk length and type
        lentype_format_string = '>I4s'
        lentype_size = struct.calcsize(lentype_format_string)

        lentype_bytes = self.image_fp.read(lentype_size)
        chunk_len, chunk_type = struct.Struct(lentype_format_string).unpack_from(lentype_bytes)
        chunk_type = chunk_type.decode('utf-8')

        logging.debug(f"Parsed chunk type {chunk_type} with data length {chunk_len}")

        # Create a parser for this type of chunk and parse
        parser = self.chunk_parser_factory.generate(chunk_len, chunk_type)

        if chunk_type == 'tRNS':
            color_type = self.get_color_type()
            bit_depth = self.get_bit_depth()

            parser.parse(self.image_fp, color_type, bit_depth)
        elif chunk_type == 'bKGD':
            color_type = self.get_color_type()

            parser.parse(self.image_fp, color_type)
        else:
            parser.parse(self.image_fp)

        # Add to chunk parser list
        self.chunk_parsers.append(parser)

        return

    def get_color_type(self):
        assert(len(self.chunk_parsers) > 0)
        assert(self.chunk_parsers[0].type == 'IHDR')

        return self.chunk_parsers[0].data['Color Type']

    def get_bit_depth(self):
        assert(len(self.chunk_parsers) > 0)
        assert(self.chunk_parsers[0].type == 'IHDR')

        return self.chunk_parsers[0].data['Bit Depth']


    def print_metadata(self):
        for parser in self.chunk_parsers:
            parser.print_metadata()
        return

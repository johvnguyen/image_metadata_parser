from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class tRNSChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = '', color_type = None, bit_depth = None):
        assert(color_type != None)
        assert(bit_depth != None)
        assert(chunk_type == 'tRNS')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        self.color_type = color_type
        self.bit_depth = bit_depth

        return

    def parse(self, image_fp):
        if self.color_type == 0:
            self.parse_grayscale(image_fp)
            self.parse_crc(image_fp)
        elif self.color_type == 2:
            self.parse_truecolor(image_fp)
            self.parse_crc(image_fp)
        elif self.color_type == 3:
            self.parse_indexed_color(image_fp)
            self.parse_crc(image_fp)
        else:
            logging.warning(f'tRNS Chunk found when Color Type is {self.color_type}. Color Type must be 0, 2, or 3.')
            raise Exception(f'tRNS Chunk found with color type {self.color_type}')
        return

    def parse_grayscale(self, image_fp):
        trns_gray_format_string = '>H'
        trns_gray_size = struct.calcsize(trns_gray_format_string)
        trns_gray_bytes = image_fp.read(trns_gray_size)
        trns_gray_data = struct.Struct(trns_gray_format_string).unpack_from(trns_gray_bytes)

        self.validate_grayscale_data(trns_gray_data)

        self.data['Grayscale Transparency'] = trns_gray_data[0]

        return

    def validate_grayscale_data(self, data):
        assert(0 <= data[0])
        assert(data[0] <= (2 ** self.bit_depth) - 1)
        return

    def parse_truecolor(self, image_fp):
        trns_tc_format_string = '>HHH'
        trns_tc_size = struct.calcsize(trns_tc_format_string)
        trns_tc_bytes = image_fp.read(trns_tc_size)
        trns_tc_data = struct.Struct(trns_tc_format_string).unpack_from(trns_tc_bytes)

        self.validate_truecolor_data(trns_tc_data)

        self.data['Red Transparency'] = trns_tc_data[0]
        self.data['Green Transparency'] = trns_tc_data[1]
        self.data['Blue Transparency'] = trns_tc_data[2]

        return

    def validate_truecolor_data(self, data):
        assert(len(data) == 3)

        for trns in data:
            assert(0 <= trns)
            assert(trns <= (2 ** self.bit_depth) - 1)

        return

    def parse_indexed_color(self, image_fp):
        trns_ic_format_string = ''.join('>', self.data_len * 'B')
        trns_ic_size = struct.calcsize(trns_ic_format_string)
        trns_ic_bytes = image_fp.read(trns_ic_size)
        trns_ic_data = struct.Struct(trns_ic_format_string).unpack_from(trns_ic_bytes)

        # Not storing transparency data values because for n pixels, we have n data values
        # For the sake of not printing thousands/millions of lines, we will not save/print anything for the indexed color case

        return
    
    def parse_crc(self, image_fp):
        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        for key in self.data.keys():
            print(f'{key} = {self.data[key]}')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

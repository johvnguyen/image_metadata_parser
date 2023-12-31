from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class sBITChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(chunk_type == 'sBIT')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp, color_type):
        self.parse_significant_bits(image_fp, color_type)

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def parse_significant_bits(self, image_fp, color_type):
        sig_bits_format_string = self.get_format_string(color_type)
        sig_bits_size = struct.calcsize(sig_bits_format_string)
        sig_bits_bytes = image_fp.read(sig_bits_size)

        sig_bits_data = struct.Struct(sig_bits_format_string).unpack_from(sig_bits_bytes)

        self.set_sig_bits(color_type, sig_bits_data)

        return

    def get_format_string(self, color_type):
        if color_type == 0:         # Grayscale
            return '>B'
        elif color_type in [2, 3]:  # Truecolor, Indexed color
            return '>BBB'
        elif color_type == 4:       # Grayscale with alpha channel
            return '>BB'
        elif color_type == 6:       # Truecolor with alpha channel
            return '>BBBB'
        else:
            raise Exception("Invalid color type")

    def set_sig_bits(self, color_type, sig_bits_data):
        if color_type == 0:
            self.data['Significant Bits - Source Grayscale Channel'] = sig_bits_data[0]

        elif color_type == 2:
            self.data['Significant Bits - Source Red Channel'] = sig_bits_data[0]
            self.data['Significant Bits - Source Green Channel'] = sig_bits_data[1]
            self.data['Significant Bits - Source Blue Channel'] = sig_bits_data[2]

        elif color_type == 3:
            self.data['Significant Bits - Source Red Palette'] = sig_bits_data[0]
            self.data['Significant Bits - Source Green Palette'] = sig_bits_data[1]
            self.data['Significant Bits - Source Blue Palette'] = sig_bits_data[2]

        elif color_type == 4:
            self.data['Significant Bits - Source Grayscale Channel'] = sig_bits_data[0]
            self.data['Significant Bits - Source Alpha Channel'] = sig_bits_data[1]

        elif color_type == 6:
            self.data['Significant Bits - Source Red Channel'] = sig_bits_data[0]
            self.data['Significant Bits - Source Green Channel'] = sig_bits_data[1]
            self.data['Significant Bits - Source Blue Channel'] = sig_bits_data[2]
            self.data['Significant Bits - Source Alpha Channel'] = sig_bits_data[4]

        else:
            raise Exception("Invalid color type")

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        for key in self.data.keys():
            print(f'{key} = {self.data[key]}')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

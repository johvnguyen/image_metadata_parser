from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class bKGDChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len in [1, 2, 6])
        assert(chunk_type == 'bKGD')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp, color_type):
        if color_type == 3:
            bkgd_format_string = '>B'
        elif color_type in [0, 4]:
            bkgd_format_string = '>H'
        elif color_type in [2, 6]:
            bkgd_format_string = '>HHH'
        else:
            raise Exception(f'Invalid color type: {color_type}')

        bkgd_size = struct.calcsize(bkgd_format_string)
        bkgd_bytes = image_fp.read(bkgd_size)
        bkgd_data = struct.Struct(bkgd_format_string).unpack_from(bkgd_bytes)

        if color_type == 3:
            self.data['Palette Index'] = bkgd_data[0]
        elif color_type in [0, 4]:
            self.data['Gray'] = bkgd_data[0]
        elif color_type in [2, 6]:
            self.data['Red'] = bkgd_data[0]
            self.data['Green'] = bkgd_data[1]
            self.data['Blue'] = bkgd_data[2]

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

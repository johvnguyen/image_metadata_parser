from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class pHYsChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == 9)
        assert(chunk_type == 'pHYs')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        # Parse data bytes
        phys_format_string = '>II?'
        phys_size = struct.calcsize(phys_format_string)

        phys_bytes = image_fp.read(phys_size)
        phys_data = struct.Struct(phys_format_string).unpack_from(phys_bytes)
        self.data['Pixels per unit - X'] = phys_data[0]
        self.data['Pixels per unit - Y'] = phys_data[1]
        self.data['In meters'] = phys_data[2]

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
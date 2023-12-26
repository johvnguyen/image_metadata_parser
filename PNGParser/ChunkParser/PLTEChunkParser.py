from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class PLTEChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == 3)
        assert(chunk_type == 'PLTE')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        plte_format_string = '>BBB'
        plte_size = struct.calcsize(plte_format_string)
        plte_bytes = image_fp.read(plte_size)

        plte_data = struct.Struct(plte_format_string).unpack_from(plte_bytes)

        self.data['Red'] = plte_data[0]
        self.data['Green'] = plte_data[1]
        self.data['Blue'] = plte_data[2]

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

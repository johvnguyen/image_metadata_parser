from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class ___ChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == -1)
        assert(chunk_type == '___')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        # TODO
        return

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        # TODO

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return
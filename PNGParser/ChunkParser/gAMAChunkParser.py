from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class gAMAChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == 4)
        assert(chunk_type == 'gAMA')

        self.data_len = data_len
        self.type = chunk_type

        self.data = None
        self.crc = None

        return

    def parse(self, image_fp):
        # Parse data byte
        gama_format_string = '>I'
        gama_size = struct.calcsize(gama_format_string)

        gama_bytes = image_fp.read(gama_size)
        self.data = struct.Struct(gama_format_string).unpack_from(gama_bytes)[0]

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)

        return

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        print(f'10000 * gAMA = {self.data}')
        print(f'(gAMA = {self.data/10000})')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')
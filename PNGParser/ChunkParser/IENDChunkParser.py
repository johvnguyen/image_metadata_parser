from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class IENDChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == 0)
        assert(chunk_type == 'IEND')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        # Data part of IEND Chunk is empty, i.e. size 0 so only read crc byte

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)

        return

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        print(f'Data = N/A')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

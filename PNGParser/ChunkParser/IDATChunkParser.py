from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class IDATChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(chunk_type == 'IDAT')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        idat_bytes = image_fp.read(self.data_len)
        self.data = self.decompress_to_image_data(idat_bytes)

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        print(f'IDAT Data = N/A')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

    def decompress_to_image_data(self, idat_bytes):
        # TODO
        return idat_bytes
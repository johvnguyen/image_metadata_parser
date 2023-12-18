from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct

class GenericChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        self.data_length = data_len
        self.type = chunk_type
        self.data = None
        self.crc = None

        return

    def parse(self, image_fp):
        if self.data_length == -1 or self.type == '':
            raise Exception("Failed to initialize GenericChunkParser with chunk_len or chunk_type values.")

        self.data = image_fp.read(self.data_length)

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_length}')
        print(f'Chunk Type = {self.type}')
        print(f'Chunk Data = N/A')
        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

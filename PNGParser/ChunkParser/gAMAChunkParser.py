from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class gAMAChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == 1)
        assert(chunk_type == 'gAMA')

        self.len = data_len
        self.type = chunk_type

        self.data = None
        self.crc = None

        return

    def parse(self, image_fp):
        # TODO
        return

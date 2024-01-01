from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class hISTChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == 6)
        assert(chunk_type == 'hIST')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        hist_format_string = ">HHH"
        hist_size = struct.calcsize(hist_format_string)
        hist_bytes = image_fp.read(hist_size)
        hist_data = struct.Struct(hist_format_string).unpack_from(hist_bytes)

        self.data['Red'] = hist_data[0]
        self.data['Green'] = hist_data[1]
        self.data['Blue'] = hist_data[2]

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

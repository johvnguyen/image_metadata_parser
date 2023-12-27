from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class cHRMChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == 32)
        assert(chunk_type == 'cHRM')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        chrm_format_string = ''.join('>', 8 * 'I')
        chrm_size = struct.calcsize(chrm_format_string)

        assert(chrm_size == self.data_len)

        chrm_bytes = image_fp.read(chrm_size)
        chrm_data = struct.Struct(chrm_format_string).unpack_from(chrm_bytes)

        self.data['White Point x'] = chrm_data[0]
        self.data['White Point y'] = chrm_data[1]
        self.data['Red Point x'] = chrm_data[2]
        self.data['Red Point y'] = chrm_data[3]
        self.data['Green Point x'] = chrm_data[4]
        self.data['Green Point y'] = chrm_data[5]
        self.data['Blue Point x'] = chrm_data[6]
        self.data['Blue Point y'] = chrm_data[7]

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Strct('>I').unpack_from(crc_bytes)[0]

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

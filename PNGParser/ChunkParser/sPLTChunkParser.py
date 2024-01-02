from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class sPLTChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(chunk_type == 'sPLT')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        palette_name_bytes = self.parse_palette_name(image_fp)
        palette_name_len = len(palette_name_bytes)
        palette_name_format_string = ''.join(['>', palette_name_len * 's'])
        palette_name = struct.Struct(palette_name_format_string).unpack_from(palette_name_bytes)[0]

        # Null seperator is parsed in parse_palette_name()

        # -5 because there is 1 byte for the null seperator and 4 bytes for crc that is later parsed
        palette_data_len = self.data_len - palette_name_len - 5
        palette_data_bytes = image_fp.read(palette_data_len)

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        logging.debug(f'Not parsing sPLT Chunk palette data because different palettes must be parsed differently.')

        return

    def parse_palette_name(self, image_fp):
        palette_name = b''


        for i in range(self.data_len):
            char_byte = image_fp.read(1)

            if char_byte == bytes([0]):
                return palette_name
            else:
                palette_name = b''.join([palette_name, char_byte])

        raise Exception('Parsed entire data segment of iCCP Chunk and failed to find null seperator')

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        for key in self.data.keys():
            print(f'{key} = {self.data[key]}')
        print("NOT printing palette data because parsing different palette types is not yet supoprted!")

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

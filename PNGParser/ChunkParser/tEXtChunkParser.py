from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class tEXtChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(chunk_type == 'tEXt')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        keyword_bytes = self.parse_keyword(image_fp)
        keyword_len = len(keyword_bytes)
        keyword_format_string = ''.join(['>', keyword_len * 's'])
        keyword = struct.Struct(keyword_format_string).unpack_from(keyword_bytes)[0].decode('utf-8')

        # Null seperator is parsed in parse_keyword()

        # size of text is size of chunk minus size of keyword minus 1 for the null seperator and minus 4 for the crc
        text_size = self.data_len - keyword_len - 1 - 4
        text_bytes = image_fp.read(text_size)
        text_format_string = ''.join(['>', text_size * 's'])
        text = struct.Struct(text_format_string).unpack_from(text_bytes)[0].decode('utf-8')

        self.data[keyword] = text

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def parse_keyword(self, image_fp):
        keyword = b''


        for i in range(self.data_len):
            char_byte = image_fp.read(1)

            if char_byte == bytes([0]):
                return keyword
            else:
                keyword = b''.join([keyword, char_byte])

        raise Exception('Parsed entire keyword segment of tEXt Chunk and failed to find null seperator')

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        # TODO

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

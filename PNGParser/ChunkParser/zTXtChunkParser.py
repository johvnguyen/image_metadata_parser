from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class zTXtChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(data_len == -1)
        assert(chunk_type == 'zTXt')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        keyword_bytes = self.parse_keyword(image_fp)
        keyword_len = len(keyword_bytes)
        keyford_format_string = ''.join(['>', keyword_len * 's'])
        keyword = struct.Struct(keyford_format_string).unpack_from(keyword_bytes)[0]

        # Null seperator is parsed in parse_keyword()

        compression_method = self.parse_compression_method(image_fp)

        # -2 because there is 1 byte for the null seperator, 1 byte for the compression method and 4 bytes for crc that is later parsed
        compressed_text_size = self.data_len - keyword_len - 2 - 4
        compressed_text_bytes = image_fp.read(compressed_text_size)
        compressed_text_format_string = ''.join(['>', 's' * compressed_text_size])
        compressed_text = struct.Struct(compressed_text_format_string).unpack_from(compressed_text_bytes)[0].decode('utf-8')

        self.data['Keywords'] = keyword
        self.data[keyword] = compressed_text

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

        raise Exception('Parsed entire data segment of zTXt Chunk and failed to find null seperator')

    def parse_compression_method(self, image_fp):
        compression_method_format_string = '>B'
        compression_method_size = struct.calcsize(compression_method_format_string)
        compression_method_bytes = image_fp.read(compression_method_size)

        return struct.Struct(compression_method_format_string).unpack_from(compression_method_bytes)[0]

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        # TODO

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

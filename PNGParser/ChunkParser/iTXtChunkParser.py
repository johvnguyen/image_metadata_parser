from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class iTXtChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(chunk_type == 'iTXt')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        self.parse_keyword(image_fp)
        self.parse_compression_data(image_fp)
        self.parse_language_tag(image_fp)
        self.parse_translated_keyword(image_fp)
        self.parse_text(image_fp)

        self.parse_crc(image_fp)
        
        return

    def parse_keyword(self, image_fp):
        keyword_bytes = self.parse_to_null(image_fp)
        keyword_size = len(keyword_bytes)
        keyword_format_string = ''.join(['>', 's' * keyword_size])
        keyword = struct.Struct(keyword_format_string).unpack_from(keyword_bytes)[0]

        self.data['Keyword'] = keyword

        return

    def parse_compression_data(self, image_fp):
        compression_format_string = '>BB'
        compression_size = struct.calcsize(compression_format_string)
        compression_bytes = image_fp.read(compression_size)
        compression_data = struct.Struct(compression_format_string).unpack_from(compression_bytes)

        self.data['Compression Flag'] = compression_data[0]
        self.data['Compression Method'] = compression_data[1]

        return

    def parse_language_tag(self, image_fp):
        language_bytes = self.parse_to_null(image_fp)
        language_size = len(language_bytes)

        if language_size == 0:
            return

        language_format_string = ''.join(['>', 's' * language_size])
        language_tag = struct.Struct(language_format_string).unpack_from(language_bytes)[0]

        self.data['Language Tag'] = language_tag

        return

    def parse_translated_keyword(self, image_fp):
        translated_key_bytes = self.parse_to_null(image_fp)
        translated_key_size = len(translated_key_bytes)

        if translated_key_size == 0:
            return

        translated_key_fstring = ''.join(['>', 's' * translated_key_size])
        translated_keyword = struct.Struct(translated_key_fstring).unpack_from(translated_key_bytes)[0]

        self.data['Translated Keyword'] = translated_keyword

        return

    def parse_text(self, image_fp):
        text_bytes = self.parse_to_null(image_fp)
        text_size = len(text_bytes)

        if text_size == 0:
            return

        text_fstring = ''.join(['>', 's' * text_size])
        text = struct.Struct(text_fstring).unpack_from(text_bytes)[0]

        self.data['Text'] = text

        return

    def parse_crc(self, image_fp):
        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def parse_to_null(self, image_fp):
        parsed_string = b''

        for i in range(self.data_len):
            char_byte = image_fp.read(1)

            if char_byte == bytes([0]):
                return parsed_string
            else:
                parsed_string = b''.join([parsed_string, char_byte])

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        for key in self.data.keys():
            print(f'{key} = {self.data[key]}')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

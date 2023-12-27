from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class iCCPChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(chunk_type == 'iCCP')

        self.data_len = data_len
        self.type = chunk_type

        self.data = {}
        self.crc = None

        return

    def parse(self, image_fp):
        profile_name_bytes = self.parse_profile_name(image_fp)
        profile_name_len = len(profile_name_bytes)
        profile_name_format_string = ''.join(['>', profile_name_len * 's'])
        profile_name = struct.Struct(profile_name_format_string).unpack_from(profile_name_bytes)[0]

        # Null seperator is parsed in parse_profile_name()

        compression_method = self.parse_compression_method(image_fp)

        # -2 because there is 1 byte for the null seperator and 1 byte for the compression method
        compressed_profile_size = self.data_len - profile_name_len - 2
        compressed_profile_bytes = image_fp.read(compressed_profile_size)
        compressed_profile_format_string = ''.join(['>', 's' * compressed_profile_size])
        compressed_profile = struct.Struct(compressed_profile_format_string).unpack_from(compressed_profile_bytes)[0]

        self.data['Profile Name'] = profile_name
        self.data['Compression Method'] = compression_method
        # Is this even a string? Do not print until I have a testing sample
        #self.data['Compressed Profile'] = compressed_profile

        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def parse_profile_name(self, image_fp):
        profile_name = b''


        for i in range(self.data_len):
            char_byte = image_fp.read(1)

            if char_byte == bytes([0]):
                return profile_name
            else:
                profile_name = b''.join([profile_name, char_byte])

        raise Exception('Parsed entire data segment of iCCP Chunk and failed to find null seperator')

    def parse_compression_method(self, image_fp):
        compression_method_format_string = '>B'
        compression_method_size = struct.calcsize(compression_method_format_string)
        compression_method_bytes = image_fp.read(compression_method_size)

        return struct.Struct(compression_method_format_string).unpack_from(compression_method_bytes)[0]



    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        for key in self.data.keys():
            print(f'{key} = {self.data[key]}')
        print("NOT printing Compression Profile because I am not sure if it can even be printed as a string. Test this!")

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

        return

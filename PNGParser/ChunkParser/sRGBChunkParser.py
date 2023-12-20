from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class sRGBChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(chunk_type == 'sRGB')
        assert(data_len == 1)

        self.data_len = 1
        self.type = chunk_type

        self.data = None
        self.crc = None

        return

    def parse(self, image_fp):
        # Parse data byte
        srgb_format_string = ">B"
        srgb_size = struct.calcsize(srgb_format_string)

        assert(self.data_len == srgb_size)

        srgb_bytes = image_fp.read(srgb_size)
        rendering_intent = struct.Struct(srgb_format_string).unpack_from(srgb_bytes)[0]
        
        try:
            self.validate_rendering_intent(rendering_intent)
        except ValueError as err:
            logging.debug(f"Error found in sRGB rendering intent value: {rendering_intent}")
            print(err)
            exit()

        self.data = rendering_intent

        # Parse crc
        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def validate_rendering_intent(self, rendering_intent):
        if rendering_intent not in [0, 1, 2]:
            logging.warning(f'Rendering intent is {rendering_intent}. Valid values: {[0, 1, 2]}')
            raise ValueError
        return

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        if self.data == 0:
            print(f'Rendering Intent = {self.data}, Perceptual')
        elif self.data == 1:
            print(f'Rendering Intent = {self.data}, Relative colormetric')
        elif self.data == 2:
            print(f'Rendering Intent = {self.data}, Saturation')
        else:
            print(f'Rendering Intent = {self.data}, Absolute colormetric')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')

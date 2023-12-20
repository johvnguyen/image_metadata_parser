from PNGParser.ChunkParser.ChunkParser import ChunkParser
import struct
import logging

class IHDRChunkParser(ChunkParser):
    def __init__(self, data_len = -1, chunk_type = ''):
        assert(chunk_type == 'IHDR')

        self.data_len = data_len
        self.type = chunk_type
        
        # Store IHDR data values with label as keys and values as dictionary entires
        self.data = {}

        self.crc = None

        return

    def parse(self, image_fp):
        ihdr_format_string = '>IIBBBBB'
        ihdr_size = struct.calcsize(ihdr_format_string)

        assert(ihdr_size == self.data_len)

        ihdr_bytes = image_fp.read(ihdr_size)
        ihdr_vals = struct.Struct(ihdr_format_string).unpack_from(ihdr_bytes)

        try:
            self.validate_ihdr_data(ihdr_vals)
        except ValueError as err:
            logging.debug(f"Error found in IHDR data values: {ihdr_vals}")
            print(err)
            exit()

        self.data['Width'] = ihdr_vals[0]
        self.data['Hieght'] = ihdr_vals[1]
        self.data['Bit Depth'] = ihdr_vals[2]
        self.data['Color Type'] = ihdr_vals[3]
        self.data['Compresion Method'] = ihdr_vals[4]
        self.data['Filter Method'] = ihdr_vals[5]
        self.data['Interface Values'] = ihdr_vals[6]

        # Parse crc
        crc_bytes = image_fp.read(struct.calcsize('>I'))
        self.crc = struct.Struct('>I').unpack_from(crc_bytes)[0]

        return

    def validate_ihdr_data(self, ihdr_vals):
        assert(len(ihdr_vals) == 7)

        # Should these validate functions also set the values in self.data? We have redundant processing
        # No, it might fail for one of the later values, in which case we do not want self.data to be filled out
        self.validate_bit_depth(ihdr_vals[2])
        self.validate_color_type(ihdr_vals[3])
        self.validate_compression_method(ihdr_vals[4])
        self.validate_filter_method(ihdr_vals[5])
        self.validate_interface_method(ihdr_vals[6])

        return

    def validate_bit_depth(self, bit_depth):
        if bit_depth not in [1, 2, 4, 8, 16]:
            logging.warning(f'Bit depth is {bit_depth}. Valid values: {[1, 2, 4, 8, 16]}')
            raise ValueError
        return

    def validate_color_type(self, color_type):
        if color_type not in [0, 2, 3, 4, 16]:
            logging.warning(f'Color type is {color_type}. Valid values: {[0, 2, 3, 4, 16]}')
            raise ValueError
        return

    def validate_compression_method(self, compression_method):
        if compression_method != 0:
            logging.warning(f'Compression method is {compression_method}. Must be 0')
            raise ValueError
        return

    def validate_filter_method(self, filter_method):
        if filter_method != 0:
            logging.warning(f'Filter method is {filter_method}. Must be 0')
            raise ValueError
        return

    def validate_interface_method(self, interface_method):
        if interface_method not in [0, 1]:
            logging.warning(f'Interface Method is {interface_method}. Valid values: {[0, 1]}')
            raise ValueError
        return


    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Chunk Data Length = {self.data_len}')
        print(f'Chunk Type = {self.type}')
        
        for key in self.data.keys():
            print(f'{key} = {self.data[key]}')

        print(f'Chunk CRC32 Checksum = {self.crc}')
        print(f'----------------------------------------\n\n')
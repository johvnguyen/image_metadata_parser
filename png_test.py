import struct
import sys

def parseIHDR(ihdr_bytes):
    # All ihdr chunks are 13 bytes long
    assert(len(ihdr_bytes) == 13)
    
    ihdr_format_string = '>IIBBBBB'

    ihdr_values = struct.Struct(ihdr_format_string).unpack_from(ihdr_bytes)

    width = ihdr_values[0]
    height = ihdr_values[1]

    ihdr_bit_depths = [1, 2, 4, 8, 16]
    bit_depth = ihdr_values[2]
    assert(bit_depth in ihdr_bit_depths)

    ihdr_color_types = [0, 2, 3, 4, 16]
    color_type = ihdr_values[3]
    assert(color_type in ihdr_color_types)

    compression_method = ihdr_values[4]
    assert(compression_method == 0)

    filter_method = ihdr_values[5]
    assert(filter_method == 0)

    interface_values = [0, 1]
    interface_value = ihdr_values[6]

    print(f'Width = {width}\nHeight = {height}\nBit depth = {bit_depth}\nColor Type = {color_type}')
    print(f'Compression Method = {compression_method}\nFilter Method = {filter_method}\nInterface Value = {interface_value}')



    return

### Parsing header
format_string = '>BBBBBBBB'
header_size = struct.calcsize(format_string)

img_file = open('images/duck.png', 'rb')
png_header_bytes = img_file.read(header_size)
header_values = struct.Struct(format_string).unpack_from(png_header_bytes)

# convert to hex
header_values = [hex(x) for x in header_values]

print(header_values)

### Parsing Chunks
# Parsing the Chunk Length and Chunk Type
lentype_format_string = '>I4s'
lentype_size = struct.calcsize(lentype_format_string)
lentype_bytes = img_file.read(lentype_size)
lentype_values = struct.Struct(lentype_format_string).unpack_from(lentype_bytes)

chunk_length = lentype_values[0]
chunk_type = lentype_values[1].decode('utf-8')

print(f'Chunk Length: {chunk_length}\nChunk Type: {chunk_type}')

crc_format_string = 'I'
crc_size = struct.calcsize(crc_format_string)

chunk_bytes = img_file.read(chunk_length)

crc_bytes = img_file.read(crc_size)

if chunk_type == "IHDR":
    parseIHDR(chunk_bytes)

crc_values = struct.Struct(crc_format_string).unpack_from(crc_bytes)[0]

# The crc32 value (remainder after dividing by standard polynomial), used for data error detection. See CRC32 algorithm for more information
print(f'{crc_values:08x}')


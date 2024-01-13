import struct

filename = 'profile.jpg'

filepath = ''.join(['./images/jpg/', filename])

image_fp = open(filepath, 'rb')
image_data = image_fp.read()

# Print the first two bytes
#print(image_data[0:2])

# Parse the "Start of File" segment signature
segment_signature = struct.unpack('>H', image_data[0:2])[0]

# Note that 0xffd8 is an int in hex form, but '0xffd8' is a string of the hex form
assert(segment_signature == 0xffd8)
print(segment_signature)
print(hex(segment_signature))
#print(type(hex(segment_signature)))

# Each segment except for 0xffd8 (start of file), 0xffd0 (???) and 0xffd9 (end of file) and 0xffd1 (???) have length data proceeding
no_length_data = [0xffd8, 0xffd0, 0xffd9, 0xffd1]

def parseSignature(image_data, i):
    segment_signature = struct.unpack('>H', image_data[i:i+2])[0]

    if segment_signature in no_length_data:
        print(f'Segment Signature: {hex(segment_signature)}\n\n')

        

        return i + 2

    else:
        segment_length = struct.unpack('>H', image_data[ i+2 : i+4 ])[0]
        print(f'Segment Signature: {hex(segment_signature)}')
        print(f'Segment Length: {segment_length}\n\n')

        if segment_signature == 0xffda:
            print(f'Start of Scan found! Skipping Scan to the end of the file!')
            return len(image_data) - 2
        elif segment_signature == 0xffc4:    # Huffman Table sections
            extract_huffman_coding(image_data, i, segment_length)
        elif segment_signature == 0xffdb:   # Define Quantization Table sections
            extract_dqt(image_data, i, segment_length)


        # segment_length includes the bytes storing itself (2 bytes)
        return i + 2 + segment_length

# TODO: Refactor this parsing so it looks reasonable
def extract_huffman_coding(image_data, i, segment_length):

    #print(4 + segment_length)
    huffman_segment_bytes = image_data[i:i+ 4 + 17]
    huffman_segment_fmt_string = '>HHB16B'
    huffman_segment_data = struct.unpack(huffman_segment_fmt_string, huffman_segment_bytes)

    segment_marker = huffman_segment_data[0]
    segment_length = huffman_segment_data[1]
    ht_information = huffman_segment_data[2]
    # This is a list of the number of codewords of that length by index. So if codewords_by_length[4] = 2, there are 2 codewords of lenght 5(=4 + 1)
    codewords_lengths_by_index = huffman_segment_data[3:]

    symbol_bytes = image_data[i + 4 + 17 : i + 4 + segment_length]
    codeword_list = []
    
    offset = 0

    # For all codeword lengths, extract all codewords
    for codeword_length in codewords_lengths_by_index:
        # Get the bytes associated with these codewords
        codeword_bytes = symbol_bytes[offset : offset + codeword_length]
        # Parse the codewords of this length
        codewords = struct.unpack('B' * codeword_length, codeword_bytes)
        # Store these codewords in the list of codewords
        codeword_list += codewords

        # Uncomment this out to see codewords in increasing length (mostly... we need to 0-pad some values)
        #for codeword in codewords:
        #    print(bin(codeword))

        # Maintain the offset for byte slicing
        offset += codeword_length





    print(f'\tSegment Marker: {hex(segment_marker)}')
    print(f'\tSegment Length: {segment_length}')
    print(f'\tHuffman Table Information: {ht_information}')
    print(f'\tNumber of Symbols: {codewords_lengths_by_index}')
    print(f'\tLength of Symbols: {len(codeword_list)}\n')
    return

def extract_dqt(image_data, i, segment_length):
    
    static_field_fmt_string = '>HHB'
    static_field_size = struct.calcsize(static_field_fmt_string)
    static_field_bytes = image_data[i : i + static_field_size]
    
    static_field_data = struct.unpack(static_field_fmt_string, static_field_bytes)
    
    signature = hex(static_field_data[0])
    length = static_field_data[1]
    qt_info = static_field_data[2]
    
    precision = 0xb11110000 & qt_info
    number_of_qt = 0b00001111 & qt_info
    
    # TODO: Parse QT Table values and store them
    
    print(f'\tSignature: {signature}')
    print(f'\tLength: {length}')
    print(f'\tQT Info: {"{:08b}".format(qt_info)}\n')
    #print(f'\t\tPrecision: {precision}')
    #print(f'\t\tNumber of QT: {number_of_qt}')
    
    return

i = 0
    
while i < len(image_data):
    i = parseSignature(image_data, i)






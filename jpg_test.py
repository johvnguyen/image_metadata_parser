import struct

filename = 'pexels-samphan-korwong-6949272.jpg'

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

        # segment_length includes the bytes storing itself (2 bytes)
        return i + 2 + segment_length

i = 0
    
while i < len(image_data):
    i = parseSignature(image_data, i)






from JPGParser.JPGParser import JPGParser

filename = 'profile.jpg'
filepath = ''.join(['./images/jpg/', filename])

parser = JPGParser()
parser.parse(filepath)
#print(f'Exitting early until I finish testing Huffman Table parsing')
parser.decode_scan_data(display = True)

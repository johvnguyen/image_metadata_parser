from JPGParser.SegmentParser.StartOfImageSegmentParser import StartOfImageSegmentParser
from JPGParser.SegmentParser.DefineHuffmanTableSegmentParser import DefineHuffmanTableSegmentParser
from JPGParser.SegmentParser.StartOfFrameSegmentParser import StartOfFrameSegmentParser

class SegmentParserFactory():
    def __init__(self):
        # TODO
        return
    
    def generate(self, signature, length = None):
        if signature == 0xffd8:
            return StartOfImageSegmentParser(signature, length)
        elif signature == 0xffd9:
            # TODO
            pass
        elif signature == 0xffe0:
            # TODO
            pass
        elif signature == 0xffdb:
            # TODO
            pass
        elif signature == 0xffc0:
            return StartOfFrameSegmentParser(signature, length)
            pass
        elif signature == 0xffc4:
            return DefineHuffmanTableSegmentParser(signature, length)
        elif signature == 0xffda:
            # TODO
            pass
        else:
            raise ValueError(f'Found section signature {signature} which is not supported.')
        
        return
    

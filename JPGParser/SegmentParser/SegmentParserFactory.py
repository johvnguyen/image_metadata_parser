from JPGParser.SegmentParser.StartOfImageSegmentParser import StartOfImageSegmentParser
from JPGParser.SegmentParser.DefineHuffmanTableSegmentParser import DefineHuffmanTableSegmentParser
from JPGParser.SegmentParser.StartOfFrameSegmentParser import StartOfFrameSegmentParser
from JPGParser.SegmentParser.StartOfScanSegmentParser import StartOfScanSegmentParser
from JPGParser.SegmentParser.DefineQuantizationTableSegmentParser import DefineQuantizationTableSegmentParser
from JPGParser.SegmentParser.APP0Wrapper import APP0Wrapper
from JPGParser.SegmentParser.EndOfImageSegmentParser import EndOfImageSegmentParser

class SegmentParserFactory():
    def __init__(self):
        # TODO
        return
    
    def generate(self, signature, length = None):
        if signature == 0xffd8:
            return StartOfImageSegmentParser(signature, length)
        elif signature == 0xffd9:
            return EndOfImageSegmentParser(signature, length)
        elif signature == 0xffe0:
            return APP0Wrapper(signature, length)
        elif signature == 0xffdb:
            return DefineQuantizationTableSegmentParser(signature, length)
        elif signature == 0xffc0:
            return StartOfFrameSegmentParser(signature, length)
        elif signature == 0xffc4:
            return DefineHuffmanTableSegmentParser(signature, length)
        elif signature == 0xffda:
            return StartOfScanSegmentParser(signature, length)
        else:
            raise ValueError(f'Found section signature {signature} which is not supported.')
        


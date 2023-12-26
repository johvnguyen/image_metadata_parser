from PNGParser.ChunkParser.GenericChunkParser import GenericChunkParser
from PNGParser.ChunkParser.IHDRChunkParser import IHDRChunkParser
from PNGParser.ChunkParser.sRGBChunkParser import sRGBChunkParser
from PNGParser.ChunkParser.gAMAChunkParser import gAMAChunkParser
from PNGParser.ChunkParser.pHYsChunkParser import pHYsChunkParser
from PNGParser.ChunkParser.PLTEChunkParser import PLTEChunkParser


class ChunkParserFactory():
    def __init__(self):
        # TODO
        return

    def generate(self, chunk_len, chunk_type):
        if chunk_type == 'IHDR':    # TODO: Fill this out later
            return IHDRChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'sRGB':
            return sRGBChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'gAMA':
            return gAMAChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'pHYs':
            return pHYsChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'PLTE':
            return PLTEChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'FILL IN LATER':  # TODO
            pass
        else:
            return GenericChunkParser(chunk_len, chunk_type)
        
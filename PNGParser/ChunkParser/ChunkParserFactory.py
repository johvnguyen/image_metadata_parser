from PNGParser.ChunkParser.GenericChunkParser import GenericChunkParser
from PNGParser.ChunkParser.IHDRChunkParser import IHDRChunkParser
from PNGParser.ChunkParser.sBITChunkParser import sBITChunkParser
from PNGParser.ChunkParser.sRGBChunkParser import sRGBChunkParser
from PNGParser.ChunkParser.gAMAChunkParser import gAMAChunkParser
from PNGParser.ChunkParser.pHYsChunkParser import pHYsChunkParser
from PNGParser.ChunkParser.PLTEChunkParser import PLTEChunkParser
from PNGParser.ChunkParser.IDATChunkParser import IDATChunkParser
from PNGParser.ChunkParser.IENDChunkParser import IENDChunkParser
from PNGParser.ChunkParser.tIMEChunkParser import tIMEChunkParser
from PNGParser.ChunkParser.tRNSChunkParser import tRNSChunkParser
from PNGParser.ChunkParser.cHRMChunkParser import cHRMChunkParser
from PNGParser.ChunkParser.iCCPChunkParser import iCCPChunkParser
from PNGParser.ChunkParser.tEXtChunkParser import tEXtChunkParser
from PNGParser.ChunkParser.zTXtChunkParser import zTXtChunkParser
from PNGParser.ChunkParser.bKGDChunkParser import bKGDChunkParser
from PNGParser.ChunkParser.sBITChunkParser import sBITChunkParser
from PNGParser.ChunkParser.hISTChunkParser import hISTChunkParser
from PNGParser.ChunkParser.sPLTChunkParser import sPLTChunkParser
from PNGParser.ChunkParser.tIMEChunkParser import tIMEChunkParser





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
        elif chunk_type == 'IDAT':
            return IDATChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'IEND':
            return IENDChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'tRNS':
            return tRNSChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'cHRM':
            return cHRMChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'iCCP':
            return iCCPChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'tEXt':
            return tEXtChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'zTXt':
            return zTXtChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'bKGD':
            return bKGDChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'sBIT':
            return sBITChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'hIST':
            return hISTChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'sPLT':
            return sPLTChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'tIME':
            return tIMEChunkParser(chunk_len, chunk_type)
        elif chunk_type == 'FILL IN LATER':  # TODO
            pass
        else:
            return GenericChunkParser(chunk_len, chunk_type)
        
from JPGParser.SegmentParser.SegmentParser import SegmentParser
from JPGParser.Util.HuffmanTable import HuffmanTable
import struct
import logging

class DefineHuffmanTableSegmentParser(SegmentParser):
    def __init__(self, sig, length):
        assert(sig == 0xffc4)
        
        self.seg_name = 'Define Huffman Table'
        self.sig = sig
        self.len = length
        
        self.ht_info = None
        self.huffman_tables = {}
        
        self.lengths = None
        self.codewords = []
        self.ht = None
        
    
    def parse(self, image_fp):
        # Signature and Length already parsed
        
        self.parse_huffman_table_info(image_fp)
        self.parse_codewords(image_fp)
        
        self.construct_huffman_table()
        
        #self.set_huffman_table()
        
        return
    
    def parse_huffman_table_info(self, image_fp):
        info_fmt_str = '>B'
        info_size = struct.calcsize(info_fmt_str)
        info_bytes = image_fp.read(info_size)
        ht_info = struct.unpack_from(info_fmt_str, info_bytes)[0]
        
        self.ht_info = ht_info
        
        return

    def parse_codewords(self, image_fp):
        codeword_lengths = self.parse_codeword_lengths(image_fp)
        self.lengths = codeword_lengths
        
        for length in codeword_lengths:
            codewords_fmt_str = 'B' * length
            codewords_size = struct.calcsize(codewords_fmt_str)
            codewords_bytes = image_fp.read(codewords_size)
            codeword = struct.unpack_from(codewords_fmt_str, codewords_bytes)
            
            self.codewords += codeword

        return
    
    def parse_codeword_lengths(self, image_fp):
        lengths_fmt_str = '16B'
        lengths_size = struct.calcsize(lengths_fmt_str)
        lengths_bytes = image_fp.read(lengths_size)
        
        return struct.unpack_from(lengths_fmt_str, lengths_bytes)
    
    def construct_huffman_table(self):
        # JPGParser calls this to obtain the HuffmanTable object which it
        # uses to construct the huffman table map.
        # self.ht_info is used toindex the huffman table map
        print(f'Lengths: {self.lengths}')
        print(f'Elements {self.codewords}')
            
        self.ht = HuffmanTable()
        self.ht.GetHuffmanBits(self.lengths, self.codewords)
        
        return
    
    def get_ht_data(self):
        return (self.ht_info, self.ht)
        

    def print_metadata(self):
        print(f'----------------------------------------')
        print(f'Segment Name: {self.seg_name}')
        print(f'Segment Signature: {self.sig}')
        self.print_ht_info()
        
        
        print(f'----------------------------------------\n\n')
        
        return

    def print_ht_info(self):
        # TODO: extract the bits
        print("{:08b}".format(self.ht_info))
        print(f'\t({self.ht_info})')
        return
    
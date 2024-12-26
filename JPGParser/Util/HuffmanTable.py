class HuffmanTable:
    def __init__(self):
        self.root = []
        
        self.count = 0
        
    def DecodeHuffmanBits(self,  lengths, elements):
        '''
        DecodeHuffmanBits - This function builds the nested list data structure which maps Huffman encodings to the corresponding element by list index. Effectively, makes self.root become a Huffman tree.
            lengths:    counts number of encodings at a particular length
            elements:   values which the bitstrings map to (are actually delta encoding values). Ordered from shortest to longest encodings
        '''
        assert(sum(lengths) == len(elements))
        
        elem_iter = 0
        
        for encoding_length in self.getEncodingLength(lengths):
            # Last bit is assigned by placing the element in the tree. So we only need to account for the remaining bits prefix bits
            prefix_len = encoding_length - 1
            for char_encoding in self.getNumOfEncodingsWithLengthN(lengths, prefix_len):
                self.BitsFromLengths(self.root, elements[elem_iter], prefix_len)
                elem_iter += 1
                
        #print(f'Huffman Tree: {self.root}')
                
        return
    
    def getEncodingLength(self, lengths):
        encoding_lengths = range(1, len(lengths) + 1)
        
        return encoding_lengths
    
    def getNumOfEncodingsWithLengthN(self, lengths, prefix_len):
        return range(lengths[prefix_len])
    
    def BitsFromLengths(self, root, element, suffix):
        if isinstance(root,list):
            if self.remainingSuffixIsEmpty(suffix):
                if self.availableEncodingInRoot(root):
                    root.append(element)
                    return True
                return False
            for bit in self.nextBitValues():  # [0, 1]
                if self.needMoreEncodingBits(root, bit):
                    # Extend the nested list to represent another bit
                    root.append([])
                if self.testBitInEncoding(root, element, suffix, bit):
                    return True
        return False
    
    def remainingSuffixIsEmpty(self, suffix):
        return suffix == 0
    
    def availableEncodingInRoot(self, root):
        return len(root) < 2
    
    def nextBitValues(self):
        return [0, 1]
    
    def needMoreEncodingBits(self, root, i):
        return len(root) == i
    
    def testBitInEncoding(self, root, element, suffix, i):
        return self.BitsFromLengths(root[i], element, suffix - 1)


    # Is this function necessary?
    def Find(self,st):
        char = self.decodeCharacter(st)
            
        return char 
    
    def decodeQuantizedValue(self, st):
        child_node = self.root

        while self.isSubTree(child_node):
            child_node = self.traverseTree(child_node, st)
            

        # In Yasoob's code, it checks for -1 and refuses to return in this case
        # Not clear why but it is possible for -1 to be a delta encoding
        # So I'm leaving this comment hear for now.
        # if huffman_tree != -1:
        #   return huffman_tree            
        return child_node
    
    def isSubTree(self, tree):
        return isinstance(tree, list)
    
    def traverseTree(self, tree, st):
        #print(f'NGUYEN: Calling GetBit()')
        return tree[st.GetBit()]

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
        elem_iter = 0
        
        assert(sum(lengths) == len(elements))
        
        for encoding_length in self.getEncodingLength(lengths):
            # Last bit is assigned by placing the element in the tree. So we only need to account for the remaining bits
            # prefix bits
            n = encoding_length - 1
            for encoding in self.getNumOfEncodingsWithLengthN(lengths, n):
                self.BitsFromLengths(self.root, elements[elem_iter], n)
                elem_iter += 1
                
        return
    
    def getEncodingLength(self, lengths):
        encoding_lengths = range(1, len(lengths) + 1)
        
        return encoding_lengths
    
    def getNumOfEncodingsWithLengthN(self, lengths, prefix_len):
        return range(lengths[prefix_len])
    
    def BitsFromLengths(self, root, element, pos):
        # Consider the inputs as:
        # root: The current sub-list we are traversing. The index to get to this sub-list is the prefix for the bitstring encoding we are considering
        # element: The value we are trying to place in our Huffman Tree
        # pos: The length of the remaining suffix of the encoded value (that we are trying to determine)
        # if root input is not a list (i.e. a list value) then return False
        if isinstance(root,list):
            # if pos == 0, then we are trying to place the element in this list
            if pos==0:
                # if there is room, append the element to the list
                if len(root)<2:
                    root.append(element)
                    return True
                # If there is no room in (i.e. all encodings at this length with this prefix has been assigned), then return False
                return False
            # this for-loop executes as the recursive step
            for i in [0,1]:
                # if the root is empty or already has 1 element (and we are still trying to place another element), add a new list to represent considering a new bit
                # NOTE: If there is no room in any previous sublist and all lengths available in self.root has already been assigned, this case will always make room for a new element by creating a new sub-list
                if len(root) == i:
                    root.append([])
                # Recursive call to try to place an element in this new sublist. If this fails, return False
                if self.BitsFromLengths(root[i], element, pos-1) == True:
                    return True
        return False
    


    def Find(self,st):
        r = self.root
        while isinstance(r, list):
            #print(self.count)
            #self.count += 1
            #print(type(r))
            #print(len(r))
            r=r[st.GetBit()]
        return  r 

    def GetCode(self, st):
        while(True):
            res = self.Find(st)
            if res == 0:
                return 0
            elif ( res != -1):
                return res
